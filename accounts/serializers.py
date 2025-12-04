from rest_framework import serializers
from .models import User
import re
import phonenumbers

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name', 'phone', 'username']

    def validate_email(self, value):
        value = value.lower().strip()
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email is already in use.")
        return value

    def validate_username(self, value):
        value = value.strip()
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists.")
        return value

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        if not re.search(r'[A-Z]', value):
            raise serializers.ValidationError("Password must contain at least one uppercase letter.")
        if not re.search(r'[a-z]', value):
            raise serializers.ValidationError("Password must contain at least one lowercase letter.")
        if not re.search(r'[0-9]', value):
            raise serializers.ValidationError("Password must contain at least one digit.")
        if not re.search(r'[@$!%*?&]', value):
            raise serializers.ValidationError("Password must contain at least one special character (@, $, !, %, *, ?, &).")
        return value

    def validate_first_name(self, value):
        if not re.match(r"^[A-Za-z]{2,50}$", value):
            raise serializers.ValidationError("First name should contain only alphabetic characters (2–50 chars).")
        return value.strip()

    def validate_last_name(self, value):
        if not re.match(r"^[A-Za-z]{2,50}$", value):
            raise serializers.ValidationError("Last name should contain only alphabetic characters (2–50 chars).")
        return value.strip()

    def validate_phone(self, value):
        try:
            # Accept Indian numbers without +91
            if len(value) == 10 and value.isdigit():
                value = "+91" + value

            phone_obj = phonenumbers.parse(value, None)

            if not phonenumbers.is_valid_number(phone_obj):
                raise serializers.ValidationError("Invalid phone number format.")

            normalized_phone = phonenumbers.format_number(phone_obj, phonenumbers.PhoneNumberFormat.E164)

        except phonenumbers.NumberParseException:
            raise serializers.ValidationError("Invalid phone number format.")

        if User.objects.filter(phone=normalized_phone).exists():
            raise serializers.ValidationError("Phone number already in use.")

        return normalized_phone

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
