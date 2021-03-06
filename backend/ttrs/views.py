from django.core.exceptions import FieldError
from rest_framework import generics
from rest_framework.exceptions import ParseError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny

from .serializers import StudentSerializer, CollegeSerializer, DepartmentSerializer, MajorSerializer, \
    CollegeDetailSerializer, DepartmentDetailSerializer, CourseSerializer, LectureSerializer
from .models import Student, College, Department, Major, Course, Lecture


class FilterAPIView(generics.GenericAPIView):
    """
    Custom supporting APIView for filtering queryset based on query_params.

    By extend this class, the APIView will automatically filter queryset if the request
    has query_params.
    Keys of the query_params MUST be a valid key of the function 'QuerySet.filter', or
    raises ParseError with status 400.
    """

    def filter_queryset(self, queryset):
        errors = {}
        for key, value in self.request.query_params.items():
            try:
                queryset.filter(**{key: value})
            except (FieldError, ValueError) as e:
                error_key = '{}={}'.format(key, value)
                error_value = list(e.args)
                errors[error_key] = error_value
        if errors:
            raise ParseError(errors)
        return queryset.filter(**self.request.query_params.dict())


class StudentList(generics.ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = (IsAuthenticated,)


class StudentCreate(generics.CreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = (AllowAny,)


class StudentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        username = self.request.user.username
        return get_object_or_404(self.get_queryset(), username=username)


class CourseList(FilterAPIView, generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = (IsAuthenticated,)


class CourseDetail(generics.RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = (IsAuthenticated,)


class LectureList(FilterAPIView, generics.ListAPIView):
    queryset = Lecture.objects.all()
    serializer_class = LectureSerializer
    permission_classes = (IsAuthenticated,)


class LectureDetail(generics.RetrieveAPIView):
    queryset = Lecture.objects.all()
    serializer_class = LectureSerializer
    permission_classes = (IsAuthenticated,)


class CollegeList(generics.ListAPIView):
    queryset = College.objects.all()
    serializer_class = CollegeSerializer
    permission_classes = (IsAuthenticated,)


class CollegeDetail(generics.RetrieveAPIView):
    queryset = College.objects.all()
    serializer_class = CollegeDetailSerializer
    permission_classes = (IsAuthenticated,)


class DepartmentList(FilterAPIView, generics.ListAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = (IsAuthenticated,)


class DepartmentDetail(generics.RetrieveAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentDetailSerializer
    permission_classes = (IsAuthenticated,)


class MajorList(FilterAPIView, generics.ListAPIView):
    queryset = Major.objects.all()
    serializer_class = MajorSerializer
    permission_classes = (IsAuthenticated,)


class MajorDetail(generics.RetrieveAPIView):
    queryset = Major.objects.all()
    serializer_class = MajorSerializer
    permission_classes = (IsAuthenticated,)
