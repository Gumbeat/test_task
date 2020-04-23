import jwt
from django.contrib.auth.models import User, update_last_login
from django.utils.timezone import now
from test_task.settings import SECRET_KEY

from .models import AppUser


class AnalyticsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        response = self.get_response(request)
        if 'access' in response.data:
            token = response.data['access']
            user_id = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])['user_id']
            user = User.objects.get(id=user_id)
            update_last_login(None, user)
        if request.user.is_authenticated:
            AppUser.objects.filter(user_id=request.user.id).update(last_activity=now())
        return response
