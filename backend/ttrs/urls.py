from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [
    path('students/', views.StudentList.as_view()),
    path('students/signup/', views.StudentCreate.as_view()),
    path('students/my/', views.StudentDetail.as_view()),

    path('courses/', views.CourseList.as_view()),
    path('courses/<int:pk>/', views.CourseDetail.as_view()),
    path('lectures/', views.LectureList.as_view()),
    path('lectures/<int:pk>/', views.LectureDetail.as_view()),

    path('colleges/', views.CollegeList.as_view()),
    path('colleges/<int:pk>/', views.CollegeDetail.as_view()),
    path('departments/', views.DepartmentList.as_view()),
    path('departments/<int:pk>/', views.DepartmentDetail.as_view()),
    path('majors/', views.MajorList.as_view()),
    path('majors/<int:pk>/', views.MajorDetail.as_view()),
]

urlpatterns += format_suffix_patterns(urlpatterns)
