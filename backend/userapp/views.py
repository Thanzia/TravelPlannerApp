from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from userapp.serializers import *
from userapp.models import *

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken


# Create your views here.

# userview (EmailSignupView and CompleteSignupView)
class EmailSignupView(APIView):

	def post(self,request):

		serializer = EmailOnlySignupSerializer(data=request.data)

		if serializer.is_valid():

			serializer.save()

			return Response("Verification link send to email.",status=status.HTTP_201_CREATED)
		
		return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
	
# UID: MQ
# Token: ctpmlh-43b5290bdc2cc6113b54d98bac4a029c
# Link: http://localhost:8000/api/users/complete-signup/?uid=MQ&token=ctpmlh-43b5290bdc2cc6113b54d98bac4a029c

class CompleteSignupView(APIView):

	def post(self,request):

		serializer = CompleteSignupSerializer(data=request.data)

		if serializer.is_valid():

			try:

				user = serializer.save()

				refresh = RefreshToken.for_user(user)

				return Response({"refresh": str(refresh), "access": str(refresh.access_token)}, status=status.HTTP_201_CREATED)

			except serializers.ValidationError as e:

				return Response(str(e),status=status.HTTP_400_BAD_REQUEST)
		
		return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
	
# {"refresh":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc1Mzg4NTU0NywiaWF0IjoxNzUzNzk5MTQ3LCJqdGkiOiJiZTFlYjAxNTNmYTA0YzFmODIyM2ZlYTRiNjdhNzk1MSIsInVzZXJfaWQiOiIxIn0.tKxnzIHNxK7Icow29nvUJI7w65SjzYAnxdISm_80M70",
# "access":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzUzNzk5NDQ3LCJpYXQiOjE3NTM3OTkxNDcsImp0aSI6IjU4ZTE0ZTgwYTRmMjQ3MTQ4NTViMTA2YmZkZmZmYjBmIiwidXNlcl9pZCI6IjEifQ.I_BH1YW-ppDUiE6kKMDqssaJ--0YSPWpSbvHJ3nnYi4"}

#  Login View
class LoginView(APIView):

	
	def post(self,request):

		serializer = LoginSerializer(data=request.data)

		if serializer.is_valid():

			user = serializer.validated_data['user']

			refresh = RefreshToken.for_user(user)

			return Response({"refresh": str(refresh), "access": str(refresh.access_token)}, status=status.HTTP_200_OK)
		
		return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
	
# logout view
class LogoutView(APIView):

	authentication_classes = [JWTAuthentication]

	permission_classes = [IsAuthenticated]

	def post(self,request):

		try:

			refresh_token = request.data.get('refresh')

			token = RefreshToken(refresh_token)

			token.blacklist()

			return Response("Logged out successfully.",status=status.HTTP_205_RESET_CONTENT)
		
		except Exception as e:

			return Response(str(e),status=status.HTTP_400_BAD_REQUEST)	

# User Profile View
class UserProfileView(APIView):

	authentication_classes = [JWTAuthentication]

	permission_classes = [IsAuthenticated]

	def get(self,request):

		user = request.user

		serializer = UserProfileSerializer(user)

		return Response(serializer.data,status=status.HTTP_200_OK)
	
	def put(self,request):

		user = request.user

		serializer = UserProfileSerializer(user,data=request.data,partial=True)

		if serializer.is_valid():

			serializer.save()

			return Response(serializer.data,status=status.HTTP_200_OK)
		
		return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
	
#  Forgot Password  View
class ForgotPasswordView(APIView):

	def post(self, request):

		serializer = ForgotPasswordSerializer(data=request.data)

		if serializer.is_valid():

			serializer.save()

			return Response("OTP sent to email.", status=status.HTTP_200_OK)

		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	
# Passwordreset view
class PasswordResetView(APIView):

	def post(self, request):

		serializer = PasswordResetSerializer(data=request.data)

		if serializer.is_valid():

			try:

				user = serializer.save()

				return Response("Password reset successfully.", status=status.HTTP_200_OK)

			except serializers.ValidationError as e:

				return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
		
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
