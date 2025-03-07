from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model

# make email or username all work when logging in

class EmailOrUsernameBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            # try to find user by email
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            try:
                # try to find user by username if by email fails
                user = UserModel.objects.get(username=username)
            except UserModel.DoesNotExist:
                return None

        if user.check_password(password):
            return user
        return None

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
