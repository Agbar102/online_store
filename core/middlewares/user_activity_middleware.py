from users.models import UserActivity

class UserActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if ( request.user.is_authenticated and
             request.method in ['POST', 'PUT', 'PATCH', 'DELETE', 'GET'] and
             not request.path.startswith('/admin/') ):


            UserActivity.objects.create(
                user=request.user,
                method=request.method,
                path=request.path,
                data=request.body.decode('utf-8') if request.body else ''
            )

        return response