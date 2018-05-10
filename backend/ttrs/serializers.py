from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.core.exceptions import ValidationError as DjangoValidationError

from .models import Student, College, Department, Major, Course, Lecture, Evaluation, TimeTable


class StudentSerializer(serializers.ModelSerializer):
    my_time_table = serializers.SerializerMethodField()
    bookmarked_time_tables = serializers.SerializerMethodField()
    received_time_tables = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = ('id', 'username', 'password', 'email', 'grade', 'college', 'department', 'major', 'not_recommends',
                  'my_time_table', 'bookmarked_time_tables', 'received_time_tables')
        extra_kwargs = {
            'email': {'required': True, 'allow_null': False, 'allow_blank': False}
        }

    def get_my_time_table(self, student):
        my_table = []
        tts = TimeTable.objects.all().filter(owner=student, type='selected')
        for tt in tts:
            my_table.append(tt.id)

        return my_table

    def get_bookmarked_time_tables(self, student):
        bookmarked = []
        tts = TimeTable.objects.all().filter(owner=student, type='bookmarked')
        for tt in tts:
            bookmarked.append(tt.id)

        return bookmarked

    def get_received_time_tables(self, student):
        received = []
        tts = TimeTable.objects.all().filter(owner=student, type='received')
        for tt in tts:
            received.append(tt.id)

        return received

    def get_field_value(self, data, key):
        if key in data:
            return data[key]
        if self.instance:
            return getattr(self.instance, key)
        return None

    def validate_email(self, email):
        if email.split('@')[1] != 'snu.ac.kr':
            raise ValidationError("The host must be 'snu.ac.kr'.")
        return email

    def validate(self, data):
        # belonging validations of college-department, department-major
        errors = []
        college = self.get_field_value(data, 'college')
        department = self.get_field_value(data, 'department')
        major = self.get_field_value(data, 'major')
        if department:
            if not college or college.id != department.college_id:
                errors.append('The department must belong to the college.')
        if major is not None:
            if not department or department.id != major.department_id:
                errors.append('The major must belong to the department.')
        if errors:
            raise ValidationError({'belonging': errors})

        # password hashing
        if 'password' not in data:
            # password not changed
            return data
        tmp_user = User(username=data['username'], email=data['email'])
        try:
            validate_password(data['password'], user=tmp_user)
        except DjangoValidationError as ve:
            raise ValidationError({'password': ve.messages})
        data['password'] = make_password(data['password'])
        return data


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class LectureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecture
        fields = '__all__'


class EvaluationSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.id')
    rate = serializers.IntegerField()
    like_it = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Evaluation
        fields = '__all__'

    def validate_rate(self, rate):
        if not (1 <= rate <= 10):
            raise ValidationError("The rate should be an integer between 1 and 10 inclusive.")
        return rate


class EvaluationDetailSerializer(EvaluationSerializer):
    lecture = serializers.ReadOnlyField(source='lecture.id')


class MajorSerializer(serializers.ModelSerializer):
    college = serializers.SerializerMethodField()

    class Meta:
        model = Major
        fields = '__all__'

    def get_college(self, major):
        return major.department.college_id


class DepartmentSerializer(serializers.ModelSerializer):
    majors = MajorSerializer(many=True, read_only=True)

    class Meta:
        model = Department
        fields = '__all__'


class CollegeSerializer(serializers.ModelSerializer):
    departments = DepartmentSerializer(many=True, read_only=True)

    class Meta:
        model = College
        fields = '__all__'


class RecommendSerializer(serializers.Serializer):
    lectures = serializers.ListField(child=serializers.IntegerField())
    score = serializers.IntegerField()

