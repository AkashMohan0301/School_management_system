from rest_framework import serializers
from .models import Classes, FeesHistory,LibraryHistory,Student
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
import re
from datetime import date
from django.utils import timezone
from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email


User = get_user_model()



User = get_user_model()

class OfficeStaffSerializer(serializers.ModelSerializer):
    c_password = serializers.CharField(write_only=True, required=False)  # Optional for updates

    class Meta:
        model = User
        fields = [
            'id', 'full_name', 'email', 'phone_number',
            'address', 'password', 'c_password', 'is_office_staff'
        ]
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},  # Optional for updates
        }

    def validate_email(self, value):
        """Ensure email is unique unless unchanged."""
        user_id = self.instance.id if self.instance else None
        if User.objects.filter(email=value).exclude(id=user_id).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value
    
    def validate_full_name(self, value):
        """Ensure the full name has at least 3 characters, contains no numbers, and only alphabetic characters."""
        if len(value) < 3:
            raise serializers.ValidationError("Full name must be at least 3 characters long.")
        
        if not re.match("^[A-Za-z ]*$", value):
            raise serializers.ValidationError("Full name should not contain numbers or special characters.")
        
        return value

    def validate_phone_number(self, value):
        """Ensure phone number contains only digits, is valid, and unique unless unchanged."""
        user_id = self.instance.id if self.instance else None
        if not value.isdigit() or len(value) < 10:
            raise serializers.ValidationError("Enter a valid phone number with at least 10 digits.")
        if User.objects.filter(phone_number=value).exclude(id=user_id).exists():
            raise serializers.ValidationError("This phone number is already in use.")
        return value

    def validate(self, data):
        """Ensure password and confirm_password match if provided."""
        if 'password' in data or 'c_password' in data:
            if data.get('password') != data.get('c_password'):
                raise serializers.ValidationError({"password": "Passwords do not match."})
        return data

    def validate_password(self, value):
        """Use Django's password validation."""
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)
        return value

    def create(self, validated_data):
        """Create a new user with a hashed password."""
        validated_data.pop('c_password', None)  # Remove confirm_password from data
        validated_data['is_office_staff'] = True
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        """Update the user instance."""
        # Handle password updates only if provided
        if 'password' in validated_data:
            instance.set_password(validated_data.pop('password'))
        validated_data.pop('c_password', None)  # Remove confirm_password if present
        return super().update(instance, validated_data)


class LibrarianSerializer(serializers.ModelSerializer):
    c_password = serializers.CharField(write_only=True, required=False)  # Optional for updates

    class Meta:
        model = User
        fields = [
            'id', 'full_name', 'email', 'phone_number',
            'address', 'password', 'c_password', 'is_librarian'
        ]
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},  # Optional for updates
        }

    def validate_email(self, value):
        """Ensure email is unique unless unchanged."""
        user_id = self.instance.id if self.instance else None
        if User.objects.filter(email=value).exclude(id=user_id).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value
    
    def validate_full_name(self, value):
        """Ensure the full name has at least 3 characters, contains no numbers, and only alphabetic characters."""
        if len(value) < 3:
            raise serializers.ValidationError("Full name must be at least 3 characters long.")
        
        if not re.match("^[A-Za-z ]*$", value):
            raise serializers.ValidationError("Full name should not contain numbers or special characters.")
        
        return value    

    def validate_phone_number(self, value):
        """Ensure phone number contains only digits, is valid, and unique unless unchanged."""
        user_id = self.instance.id if self.instance else None
        if not value.isdigit() or len(value) < 10:
            raise serializers.ValidationError("Enter a valid phone number with at least 10 digits.")
        if User.objects.filter(phone_number=value).exclude(id=user_id).exists():
            raise serializers.ValidationError("This phone number is already in use.")
        return value

    def validate(self, data):
        """Ensure password and confirm_password match if provided."""
        if 'password' in data or 'c_password' in data:
            if data.get('password') != data.get('c_password'):
                raise serializers.ValidationError({"password": "Passwords do not match."})
        return data

    def validate_password(self, value):
        """Use Django's password validation."""
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)
        return value

    def create(self, validated_data):
        """Create a new user with a hashed password."""
        validated_data.pop('c_password', None)  # Remove confirm_password from data
        validated_data['is_librarian'] = True
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        """Update the user instance."""
        # Handle password updates only if provided
        if 'password' in validated_data:
            instance.set_password(validated_data.pop('password'))
        validated_data.pop('c_password', None)  # Remove confirm_password if present
        return super().update(instance, validated_data)

class FeesHistorySerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.name', read_only=True)

    class Meta:
        model = FeesHistory
        fields = ['id', 'student', 'fee_type', 'amount', 'payment_date', 'remarks', 'student_name']

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("The amount must be greater than 0.")
        return value

    def validate_payment_date(self, value):
        # Ensure that payment date is not in the future
        if value > timezone.now().date():
            raise serializers.ValidationError("Payment date cannot be in the future.")
        return value
    
    
class LibraryHistorySerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.name', read_only=True)
    status = serializers.CharField(required=False)


    class Meta:
        model = LibraryHistory
        fields = ['id', 'student', 'book_name', 'borrow_date', 'return_date', 'student_name', 'status']

    def validate_borrow_date(self, value):
        """Ensure borrow_date is not in the future."""
        if value > date.today():
            raise serializers.ValidationError("Borrow date cannot be in the future.")
        return value

    def validate(self, data):
        """Validate return_date relative to borrow_date."""
        borrow_date = data.get('borrow_date', getattr(self.instance, 'borrow_date', None))
        return_date = data.get('return_date', getattr(self.instance, 'return_date', None))

        if return_date and borrow_date and return_date < borrow_date:
            raise serializers.ValidationError({"return_date": "Return date cannot be before borrow date."})
        return data


    def update(self, instance, validated_data):
        """Validate status change logic."""
        new_status = validated_data.get('status', instance.status)

        if instance.status == 'returned' and new_status == 'borrowed':
            raise serializers.ValidationError({"status": "Cannot change status from 'returned' to 'borrowed'."})
        if new_status == 'returned' and not validated_data.get('return_date', instance.return_date):
            raise serializers.ValidationError({"return_date": "A return date is required to mark as 'returned'."})

        return super().update(instance, validated_data)

    def create(self, validated_data):
        """Set the status to 'borrowed' when creating a new record."""
        validated_data['status'] = 'borrowed'
        return super().create(validated_data)
        
class StudentSerializer(serializers.ModelSerializer):
    class_name = serializers.PrimaryKeyRelatedField(queryset=Classes.objects.all())  # Handles the ForeignKey to Classes
    class_name_display = serializers.CharField(source='class_name.name', read_only=True)  # Display class name

    # Meta class to specify model and fields
    class Meta:
        model = Student
        fields = ['id', 'name', 'age', 'dob', 'address', 'gender', 'phone_number', 'class_name', 'profile_picture', 'class_name_display']

    # Validate the age field
    def validate_age(self, value):
        if value <= 0:
            raise serializers.ValidationError("Age must be a positive number.")
        if value <= 16 or value >= 30:
            raise serializers.ValidationError("Age must be greater than 16 and less than 30.")
        return value
    
    def validate_name(self, value):
        """Ensure the full name has at least 3 characters, contains no numbers, and only alphabetic characters."""
        if len(value) < 3:
            raise serializers.ValidationError("Full name must be at least 3 characters long.")
        
        if not re.match("^[A-Za-z ]*$", value):
            raise serializers.ValidationError("Full name should not contain numbers or special characters.")
        
        return value
    # Validate the date of birth (dob) to make sure it's not in the future
    def validate_dob(self, value):
        today = date.today()
        if value > today:
            raise serializers.ValidationError("Date of birth cannot be in the future.")
        return value

    # Validate the phone number format using regex (assumes a standard phone number format)
    def validate_phone_number(self, value):
        phone_regex = r'^\+?\d{10,15}$'
        if not re.match(phone_regex, value):
            raise serializers.ValidationError("Phone number must be between 10 and 15 digits and may start with a '+' sign.")
        return value

    # Validate the profile picture (check if the size is under 5 MB)
    def validate_profile_picture(self, value):
        if value:
            max_size = 5 * 1024 * 1024  # 5MB
            if value.size > max_size:
                raise serializers.ValidationError("Profile picture size should not exceed 5MB.")
        return value