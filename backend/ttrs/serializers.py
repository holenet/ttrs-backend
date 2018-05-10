from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.core.exceptions import ValidationError as DjangoValidationError, ObjectDoesNotExist

from .models import Student, College, Department, Major, Course, Lecture, Evaluation, TimeTable, MyTimeTable, \
    BookmarkedTimeTable, ReceivedTimeTable, TimeSlot, Classroom


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('id', 'username', 'password', 'email', 'grade', 'college', 'department', 'major', 'not_recommends',
                  'my_time_tables', 'bookmarked_time_tables', 'received_time_tables')
        read_only_fields = ('not_recommends', 'my_time_tables', 'bookmarked_time_tables', 'received_time_tables')
        extra_kwargs = {
            'email': {'required': True, 'allow_null': False, 'allow_blank': False}
        }

    def get_field_value(self, data, key):
        if key in data:
            return data[key]
        if self.instance:
            return getattr(self.instance, key)
        return None

    def validate_email(self, email):
        if email.split('@')[1] != 'snu.ac.kr':
            raise ValidationError("The host must be 'snu.ac.kr'.")
        if Student.objects.filter(email=email).exists():
            raise ValidationError("A Student with that email already exists.")
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


class ClassroomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classroom
        fields = '__all__'


class TimeSlotSerializer(serializers.ModelSerializer):
    classroom = ClassroomSerializer()

    class Meta:
        model = TimeSlot
        fields = '__all__'


class LectureSerializer(serializers.ModelSerializer):
    course = CourseSerializer()
    time_slots = TimeSlotSerializer(many=True)

    class Meta:
        model = Lecture
        fields = '__all__'


class EvaluationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evaluation
        fields = '__all__'
        read_only_fields = ('author', 'like_it')

    def validate_rate(self, rate):
        if not (1 <= rate <= 10):
            raise ValidationError("The rate should be an integer between 1 and 10 inclusive.")
        return rate


class EvaluationDetailSerializer(EvaluationSerializer):
    lecture = serializers.ReadOnlyField(source='lecture.id')


class TimeTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeTable
        fields = '__all__'
        read_only_fields = ('owner', 'year', 'semester')

    @staticmethod
    def time_to_minute(time):
        hour, minute = map(int, time.split(':'))
        return hour * 60 + minute

    def validate_lectures(self, lectures):
        codes = set()
        for lecture in lectures:
            if lecture.course.code in codes:
                raise ValidationError("All lectures should have distinct courses.")
            codes.add(lecture.course.code)
        days = {}
        for lecture in lectures:
            for time_slot in lecture.time_slots.all():
                start_minute = self.time_to_minute(time_slot.start_time)
                end_minute = self.time_to_minute(time_slot.end_time)
                if time_slot.day_of_week not in days:
                    days[time_slot.day_of_week] = []
                days[time_slot.day_of_week].append((start_minute, end_minute))
        for times in days.values():
            times.sort()
            for i in range(len(times)-1):
                if times[i][1] > times[i+1][0]:
                    raise ValidationError("Time slots of lectures should not overlap.")
        return lectures

    def validate(self, data):
        error_lectures = []
        for lecture in data['lectures']:
            if lecture.year != data['year'] or lecture.semester != data['semester']:
                error_lectures.append(lecture.id)
        if error_lectures:
            raise ValidationError({"Lectures should belong to the year and semester.": error_lectures})
        return data


class MyTimeTableSerializer(TimeTableSerializer):
    class Meta(TimeTableSerializer.Meta):
        model = MyTimeTable


class BookmarkedTimeTableSerializer(TimeTableSerializer):
    class Meta(TimeTableSerializer.Meta):
        model = BookmarkedTimeTable
        read_only_fields = TimeTableSerializer.Meta.read_only_fields+('bookmarked_at',)


class ReceivedTimeTableSerializer(TimeTableSerializer):
    class Meta(TimeTableSerializer.Meta):
        model = ReceivedTimeTable
        read_only_fields = TimeTableSerializer.Meta.read_only_fields+('sender', 'received_at')


class CopyTimeTableSerializer(serializers.Serializer):
    time_table_id = serializers.IntegerField()

    def __init__(self, *args, **kwargs):
        self.owner = kwargs.pop('owner')
        super().__init__(*args, **kwargs)

    def validate_time_table_id(self, time_table_id):
        try:
            TimeTable.objects.get(pk=time_table_id)
        except ObjectDoesNotExist:
            raise ValidationError("There is no time table with this id.")
        table_models = (MyTimeTable, BookmarkedTimeTable, ReceivedTimeTable)
        if not any([model.objects.filter(owner=self.owner, pk=time_table_id) for model in table_models]):
            raise ValidationError("You can send only your tables.")
        return time_table_id


class SendTimeTableSerializer(CopyTimeTableSerializer):
    receiver_name = serializers.CharField(max_length=150)

    def validate_receiver_name(self, receiver_name):
        try:
            Student.objects.get_by_natural_key(receiver_name)
        except ObjectDoesNotExist:
            raise ValidationError("The receiver with this name does not exist or is not a student.")
        return receiver_name


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
