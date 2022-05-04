from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.core.cache import cache


UserModel = get_user_model()


class EmailBackend(ModelBackend):
    def authenticate(self, request, email=None, code=None, **kwargs):
        try:
            user = UserModel.objects.get(email=email)
            if cache.get(email):
                if int(cache.get(email)) == int(code):
                    cache.delete(email)
                    return user
                return "Code is Invalid"
            return "Code has been expired"
        except UserModel.DoesNotExist:
            return "Your account is not completely created.please try again."
        except UserModel.MultipleObjectsReturned:
            return UserModel.objects.filter(email__iexact=email).first()

            