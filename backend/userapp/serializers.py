from rest_framework import serializers
from userapp.models import *

from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator

from django.contrib.auth import authenticate
import random


# email only signup serializer
class EmailOnlySignupSerializer(serializers.Serializer):

	email = serializers.EmailField()

	def validate_email(self,data):

		if CustomUserModel.objects.filter(email=data).exists():

			raise serializers.ValidationError("Email already registered.")
		
		return data
	
	def create(self,validated_data):

		user = CustomUserModel.objects.create(email=validated_data['email'],is_active=False,
										      username=validated_data['email'])
		
		uid = urlsafe_base64_encode(force_bytes(user.id))
		
		token = default_token_generator.make_token(user)

		# backend testing link
		verification_link = f"http://localhost:8000/api/users/complete-signup/?uid={uid}&token={token}"

		print(f"UID: {uid}")
		print(f"Token: {token}")
		print(f"Link: {verification_link}\n")

		message = f"Click the link to verify your email: {verification_link}"

		send_mail(subject="Verify your Email",message=message,from_email="thanzia123@gmail.com",
			      recipient_list=[user.email])
		
		return user
		
# Complete signup serializer
class CompleteSignupSerializer(serializers.ModelSerializer):

	uid = serializers.CharField(write_only=True)
	
	token = serializers.CharField(write_only=True)

	password = serializers.CharField(write_only=True)

	class Meta:

		model = CustomUserModel

		fields = ['uid','token','username','password', 'phone_number', 'gender']

	def validate(self, data):

		try:
			uid = urlsafe_base64_decode(data['uid']).decode()

			user = CustomUserModel.objects.get(id=uid)

		except (TypeError, ValueError, OverflowError, CustomUserModel.DoesNotExist):

			raise serializers.ValidationError("Invalid UID.")

		if user is not None and default_token_generator.check_token(user, data['token']):

			self.user = user

			return data

		raise serializers.ValidationError("Invalid token or user ID.")

	def save(self, **kwargs):

		user = self.user

		user.username = self.validated_data['username']

		# Set the password using set_password to hash it
		user.set_password(self.validated_data['password'])

		user.phone_number = self.validated_data['phone_number']
		
		user.gender = self.validated_data['gender']

		user.is_active = True

		user.save()

		return user
	
# Login serializer
class LoginSerializer(serializers.Serializer):

	username = serializers.CharField()

	password = serializers.CharField()

	def validate(self, data):

		try:

			user = authenticate(username=data['username'], password=data['password'])

		except CustomUserModel.DoesNotExist:

			raise serializers.ValidationError("Invalid email or password.")

		if not user.check_password(data['password']):

			raise serializers.ValidationError("Invalid email or password.")

		data['user'] = user

		return data
	
# user serializer
class UserProfileSerializer(serializers.ModelSerializer):	

	class Meta:

		model = CustomUserModel

		fields = ['id', 'email', 'username', 'phone_number', 'gender']

		read_only_fields = ['id','email']

# Forgot pwd serializer
class ForgotPasswordSerializer(serializers.Serializer):

	email = serializers.EmailField()

	def validate_email(self, data):

		if not CustomUserModel.objects.filter(email=data).exists():

			raise serializers.ValidationError("Email not registered.")
		
		return data

	def create(self, validated_data):

		user = CustomUserModel.objects.get(email=validated_data['email'])
		
		otp = random.randint(1000, 9999)
		
		# Save or update OTP in the model
		ForgotPasswordModel.objects.update_or_create(
            email=user.email,
            defaults={"otp": otp}
        )

		message = f"Your OTP for password reset is: {otp}"

		send_mail(subject="Reset your Password", message=message, from_email="thanzia123@gmail.com",
			      recipient_list=[user.email])

		return user
	
# Password reset serializer
class PasswordResetSerializer(serializers.Serializer):

	email = serializers.EmailField()

	otp = serializers.CharField()

	new_password = serializers.CharField(write_only=True)

	def validate(self, data):

		try:

			user = CustomUserModel.objects.get(email=data['email'])

			forgot_password_entry = ForgotPasswordModel.objects.get(email=user.email, otp=data['otp'])

			if forgot_password_entry.is_expired():

				raise serializers.ValidationError("OTP has expired.")

		except CustomUserModel.DoesNotExist:

			raise serializers.ValidationError("Email not registered.")
		
		except ForgotPasswordModel.DoesNotExist:

			raise serializers.ValidationError("Invalid OTP.")

		data['user'] = user

		return data

	def save(self, **kwargs):

		user = self.validated_data['user']
		
		user.set_password(self.validated_data['new_password'])
		
		user.save()
		
		# Remove OTP after use
		ForgotPasswordModel.objects.filter(email=user.email).delete()

		return user