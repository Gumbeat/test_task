from django.utils.timezone import now

from .models import AppUser


class LastActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        response = self.get_response(request)
        if request.user.is_authenticated:
            AppUser.objects.filter(user_id=request.user.id).update(last_activity=now())
        return response
