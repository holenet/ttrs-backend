from django.urls import path

from . import views

urlpatterns = [
    path('students/', views.StudentList.as_view()),
    path('students/<int:pk>/', views.StudentDetail.as_view()),
    path('colleges/', views.CollegeList.as_view()),
    path('departments/', views.DepartmentList.as_view()),
    path('majors/', views.MajorList.as_view()),
]
