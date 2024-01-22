from django.shortcuts import render, redirect
from .forms import CreateUserForm, LoginForm, TimeInOutForm

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import GeneratedReport, TimeInOut, User
from django.contrib import messages
import datetime
import calendar
from django.db.models import Q

from django.http import HttpResponse
import csv

# Create your views here.
def home(request):
    return render(request, 'webapp/index.html')


def register(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, "Account successfully created")
            return redirect('login')

        # else:
        #     return HttpResponse('An error occurred during registration')

    context = {'form': form}
    return render(request, 'webapp/register.html', context)


def loginUser(request):
    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request, request.POST)

        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, "Successfully logged in!")

                return redirect('profile', pk=request.user.id)


        else:
            messages.error(request, "Invalid username and password")

    context = {'form':form}
    return render(request, 'webapp/my-login.html', context)


def logoutUser(request):
    logout(request)
    messages.success(request, "Successfully logged out!")
    return redirect('home')

@login_required(login_url='login')
def dashboardProfile(request, pk):
    user = request.user
    date = datetime.date.today().strftime('%B %d, %Y')
    date_number = datetime.date.today()
    my_records = TimeInOut.objects.filter(
        user__username=user.username,
    )

    if request.method == "POST":
        try:
            year = (request.POST.get('date').split("-"))[0]
            month = (request.POST.get('date').split("-"))[1]
            day = (request.POST.get('date').split("-"))[2]

            month_words = calendar.month_name[int(month)]
            date = f"{month_words} {day}, {year}"

            my_records = TimeInOut.objects.filter(
                user__username=user.username,
                date__year=year,
                date__month=month,
                date__day=day,
            )

            context = {'records': my_records, 'date':date}
            return render(request, 'webapp/profile.html', context)

        except:
            messages.error(request, "Please Select a Date")
            return redirect('profile', pk=request.user.id)


    context = {'records': my_records, 'date':date}
    return render(request, 'webapp/profile.html', context)

############################# REPORT ################################
@login_required(login_url='login')
def create_record(request):
    record = 'create'
    form = TimeInOutForm()
    users = User.objects.all()

    if request.method == "POST":

        user = User.objects.get(username=request.POST.get('username'))
        print(user.id)

        TimeInOut.objects.create(
            user=user,
            date=request.POST.get('date'),
            time_start=request.POST.get('time_start'),
            time_end=request.POST.get('time_end'),
            l_hd=request.POST.get('l_hd'),
        )
        if form.is_valid():
            form.save(commit=False)
            form.user = request.user
            form.save()
        messages.success(request, "Record successfully created")

        return redirect('generate-report')

    context = {'form':form, 'record':record, 'users':users}
    return render(request, 'webapp/create-update-record.html', context)


@login_required(login_url='login')
def update_record(request, pk):
    record = TimeInOut.objects.get(id=pk)
    form = TimeInOutForm(instance=record)

    if request.method == "POST":

        strp_time_start = datetime.datetime.strptime(request.POST.get('time_start'), '%H:%M')  # for subtracting time only
        time_start = strp_time_start.strftime('%I:%M %p')

        strp_time_end = datetime.datetime.strptime(request.POST.get('time_end'), '%H:%M')  # for subtracting time only
        time_end = strp_time_end.strftime('%I:%M %p')


        record = form.save(commit=False)
        record.date = request.POST.get('date')
        record.time_start = time_start
        record.time_end = time_end
        record.l_hd = request.POST.get('l_hd')
        record.save()

        messages.success(request, "Record successfully updated")

        return redirect('profile', pk=request.user.id)

        # messages.error(request, "Error")

    context = {'record':record, 'form':form, }
    return render(request, 'webapp/create-update-record.html', context)


@login_required(login_url='login')
def view_record(request, pk):
    record = TimeInOut.objects.get(id=pk)


    context = {'record':record}
    return render(request, 'webapp/view-record.html', context)


@login_required(login_url='login')
def delete_record(request, pk):
    record = TimeInOut.objects.get(id=pk)

    if request.method == "POST":
        record.delete()
        messages.success(request, "Record successfully deleted")
        return redirect('profile', pk=request.user.id)

    return render(request, 'webapp/delete.html', {'obj':record})

#################################### GENERATE CSV ##########################################
#################################### GENERATE CSV ##########################################
#################################### GENERATE CSV ##########################################
@login_required(login_url='login')
def generateReport(request):
    if request.user.is_superuser:
        GeneratedReport.objects.all().delete()
        records = TimeInOut.objects.all().order_by('date')
        context = {'records': records}

        if request.method == "POST":
            GeneratedReport.objects.all().delete()

            q = request.POST.get('q') if request.POST.get('q') != None else ''
            try:
                date_records = TimeInOut.objects.filter(
                    date__range=[request.POST.get('date'), request.POST.get('date2')]
                )
            except:
                date_records = TimeInOut.objects.all().order_by('date')

            records = date_records.filter(Q(user__first_name__icontains=q) |
                                          Q(user__last_name__icontains=q)
                                          )

        for record in records:
            GeneratedReport.objects.create(
                user=record.user,
                date=record.date,
                time_start=record.time_start,
                time_end=record.time_end,
            )

        context = {'records': records}

        return render(request, 'webapp/generate-report.html', context)

    else:
        return HttpResponse("<h1>You are not allowed in this page.</h1>")

def export_csv_timeReport(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="time-report.csv"'

    writer = csv.writer(response)
    writer.writerow(['First Name','Last Name', 'Date', 'Time In', 'Time Out', 'Leave/Halfday'])

    reports = GeneratedReport.objects.all().values_list('user__first_name', 'user__last_name', 'date', 'time_start', 'time_end', 'l_hd')
    for report in reports:
        writer.writerow(report)

    GeneratedReport.objects.all().delete()
    return response

def timeInOut(request):
    date = datetime.date.today().strftime("%A, %B %d, %Y")
    time = datetime.datetime.now()
    context = {
        'date': date,
        'time': time

    }
    return render(request, 'webapp/in_out.html', context)

def timeIn(request):
    user = request.user
    date = datetime.date.today()
    status = TimeInOut.objects.filter(user__username=user.username, date=date)

    if status:
        messages.error(request, "Already Time-In Today")

    else:

        time_In = datetime.datetime.now().strftime('%I:%M %p')
        print(date)

        TimeInOut.objects.create(
            user=request.user,
            time_start=time_In,
            time_end="",
            l_hd="",

        )

        messages.success(request, f"TIME IN at {time_In} ")
    return redirect('profile', pk=request.user.id)


def timeOut(request):
    user = request.user
    date = datetime.date.today()
    try:
        record = TimeInOut.objects.get(user__username=user.username, date=date)

        time_Out = datetime.datetime.now().strftime('%I:%M %p')
        record.time_end = time_Out
        record.save()

        messages.success(request, f"TIME OUT at {time_Out} ")
    except:
        messages.error(request, "You don't have a TIME-IN today")

    return redirect('profile', pk=request.user.id)