from django.contrib.auth.models import User
from rest_framework import serializers


class RegistrationSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    # Here, i am also setting the style regarding input field as password.

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
        # here, "username", "email", "password" are defined in "django.contrib.auth.models" and that is why I have
        # defined "password2"

        extra_kwargs = {
            'password': {'write_only': True}
        }
        # Here, I am also setting my "password" field as "write_only"

    def save(self):
        # here we are checking that password == password2 or not and email is unique or not.

        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        # i am accessing the "password" through "validated_data" because this is going to have all the information about
        # password

        if password != password2:
            raise serializers.ValidationError({'error': 'P1 and P2 should be same'})

        if User.objects.filter(email=self.validated_data['email']).exists():
        # here I am checking the email exist or not.
            raise serializers.ValidationError({'error': 'Email already exists!'})


        # here, we are creating the user manually
        account = User(email=self.validated_data['email'], username=self.validated_data['username'])
        # here we are creating the instance for user registration through the user model
        account.set_password(password)
        # "set_password()" Sets the user's password to the given raw string, taking care of the password
        # hashing. Doesn't save the User object.

        account.save()
        return account



