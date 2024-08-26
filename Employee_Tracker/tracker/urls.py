from django.urls import path
from .views import User_Registration,User_Login,Upload_employee_details,Mark_attendance,Declare_Geofenced_area,get_user_data
urlpatterns = [
    path('register',User_Registration.as_view()),
    path('login',User_Login.as_view()),
    path('upload_employee_data',Upload_employee_details),
    path('mark_attendance',Mark_attendance.as_view()),
    path('Declare_area',Declare_Geofenced_area.as_view()),
    path('get_user_data',get_user_data.as_view())
]