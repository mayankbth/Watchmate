# Generating Tokens
# By using signals
# If you want every user to have an automatically generated Token, you can simply catch the User's post_save signal.

# Note:
# If you are storing these type of signal code not just for authentication token but in future also, make sure to
# import or make sure to add this code in file where you are going to call that file.


from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


# as we register a new user, this will be called. So, that means we are auto generating token for each single user.
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


# NOTE:
# Note that you'll want to ensure you place this code snippet in an installed models.py module, or some other location
# that will be imported by Django on startup.