from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .permissions import IsTheStudent
from .serializers import StudentSerializer, CollegeSerializer, DepartmentSerializer, MajorSerializer, \
    CollegeDetailSerializer, DepartmentDetailSerializer, CourseSerializer
from .models import Student, College, Department, Major, Course


class FilterAPIView(generics.GenericAPIView):
    """
    Supporting custom APIView class for filtering queryset based on query_params.

    Extend this class and set 'filter_options', a class variable of 'tuple'
    which defines list of keys you want to filter.
    Each element of 'filter_options' must be valid key for function 'QuerySet.filter'.

    Note: Default 'filter_options' is empty, therefore it filters nothing.
    """

    filter_options = ()

    def get_queryset(self):
        filter_kwargs = {}
        for option in self.filter_options:
            value = self.request.query_params.get(option, None)
            if value is not None:
                filter_kwargs[option] = value
        return self.queryset.filter(**filter_kwargs)


class StudentList(generics.ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = (IsAuthenticated,)


class StudentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = (IsAuthenticated, IsTheStudent)


class CourseList(FilterAPIView, generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = (IsAuthenticated,)
    filter_options = ('code', 'name', 'type', 'field', 'grade', 'credit', 'college_id', 'department_id', 'major_id')


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
    filter_options = ('college_id',)


class DepartmentDetail(generics.RetrieveAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentDetailSerializer
    permission_classes = (IsAuthenticated,)


class MajorList(FilterAPIView, generics.ListAPIView):
    queryset = Major.objects.all()
    serializer_class = MajorSerializer
    permission_classes = (IsAuthenticated,)
    filter_options = ('department__college_id', 'department_id')


class MajorDetail(generics.RetrieveAPIView):
    queryset = Major.objects.all()
    serializer_class = MajorSerializer
    permission_classes = (IsAuthenticated,)
