from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.core.exceptions import ValidationError as DjangoValidationError

from .models import Student, College, Department


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('id', 'username', 'password', 'email', 'grade', 'college', 'department', 'major', 'not_recommends')
        extra_kwargs = {
            'email': {'required': True, 'allow_null': False, 'allow_blank': False}
        }

    def validate_email(self, email):
        if email.split('@')[1] != 'snu.ac.kr':
            raise ValidationError("The host must be 'snu.ac.kr'.")
        return email

    def validate_grade(self, grade):
        if grade not in range(1, 5):
            raise ValidationError("The grade must be a integer of 1~4")
        return grade

    def get_field_value(self, data, key):
        if key in data:
            return data[key]
        if self.instance:
            return getattr(self.instance, key)
        return None

    def validate(self, data):
        # belonging validations of college-department, department-major
        errors = []
        college = self.get_field_value(data, 'college')
        department = self.get_field_value(data, 'department')
        major = self.get_field_value(data, 'major')
        if department:
            if not college or college.id != department.college_id:
                errors.append('The department must belong to the college')
        if major is not None:
            if not department or department.id != major.department_id:
                errors.append('The major must belong to the department')
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


class CollegeSerializer(serializers.ModelSerializer):
    class Meta:
        model = College
        fields = '__all__'


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'
