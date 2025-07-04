from users.models import UserActivity

class UserActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            body = request.body.decode('utf-8') if request.body else ''
        except Exception:
            body = '[Не удалось декодировать тело запроса]'

        response = self.get_response(request)

        if ( request.user.is_authenticated and
             request.method in ['POST', 'PUT', 'PATCH', 'DELETE'] and
             not request.path.startswith('/admin/') ):


            UserActivity.objects.create(
                user=request.user,
                method=request.method,
                path=request.path,
                data=body
            )

        return response