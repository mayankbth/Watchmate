from rest_framework.decorators import api_view
# this is for function based views
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status

# from rest_framework_simplejwt.tokens import RefreshToken
# # this is for JWT authentication system

from user_app.api.serializers import RegistrationSerializer
from user_app import models
# So, every time we load our views.py it is also going to call this model.py


@api_view(['POST',])
def logout_view(request):

    if request.method == 'POST':
        request.user.auth_token.delete()
        # this "request.user" is the current logged in user.
        # here I am deleting the token generated for the current logged in user.
        return Response(status=status.HTTP_200_OK)


@api_view(['POST',])
# with the decorator we also defining the conditions. like, here we have defined "POST" condition.
def registration_view(request):

    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)

        data = {}

        if serializer.is_valid():
            account = serializer.save()
            # when calling the "save()" method we are going to jump to serializer.

            data['response'] = "Registration Successful!"
            data['username'] = account.username
            data['email'] = account.email

            token = Token.objects.get(user=account).key
            # "Token.object.get(user=account)" this is going to return us token like this...
            # {"token":"3a9c382e3c2f48ada48965a4fa513d74e6dae7f0"}
            # and to access the key ".key"
            data['token'] = token

            # refresh = RefreshToken.for_user(account)
            # data['token'] = {
            #                     'refresh': str(refresh),
            #                     'access': str(refresh.access_token),
            #                 }
            # # here we are defining the token as key inside the data dictionary.
            # # either we can call this "data['token']" as refresh and call this "'refresh': str(refresh)," information
            # # and create another variable called "access" and send this information
            # # "'access': str(refresh.access_token),"

        else:
            data = serializer.errors

        return Response(data)
            # here only username and email is returned because password is write_only data
            # REST framework supports HTTP content negotiation by providing a Response class which allows you to return
            # content that can be rendered into multiple content types, depending on the client request.

