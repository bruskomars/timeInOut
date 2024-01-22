from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.loginUser, name='login'),
    path('logout/', views.logoutUser, name='logout'),

    path('profile/<int:pk>/', views.dashboardProfile, name='profile'),

    path('generate-report/', views.generateReport, name='generate-report'),

    path('create-record/', views.create_record, name='create-record'),
    path('update-record/<int:pk>/', views.update_record, name='update-record'),
    path('record/<int:pk>/', views.view_record, name='view-record'),
    path('delete-record/<int:pk>/', views.delete_record, name='delete-record'),

    path('export-timereport-csv/', views.export_csv_timeReport, name='export-timereport-csv'),

    path('timeInOut/', views.timeInOut, name='timeInOut'),
    path('timeIn/', views.timeIn, name='timeIn'),
    path('timeOut/', views.timeOut, name='timeOut'),
    # path('export-task-csv/', views.export_csv_task, name='export-task-csv'),
    #
    # path('status-report/<int:pk>/', views.taskStatus, name='status-report'),
    # path('create-status/', views.createTaskStatus, name='create-status'),
    # path('view-status/<int:pk>', views.view_status, name='view-status'),
    # path('edit-status/<int:pk>', views.editStatus, name='edit-status'),
    # path('delete-status/<int:pk>', views.deleteStatus, name='delete-status'),
    # path('view-all-status/', views.viewAllStatus, name='view-all-status'),
]
