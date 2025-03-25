from django.shortcuts import redirect
from django.urls import reverse

class RequireLoginMiddleware:
    """
    Middleware that redirects users to the login page if they are not authenticated,
    except for certain allowed paths.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        allowed_paths = [reverse("tasks:login"), reverse("tasks:register")]  # URLs that don't require login

        if not request.user.is_authenticated and request.path not in allowed_paths:
            return redirect("tasks:login")  # Redirect to login if user is not authenticated

        return self.get_response(request)
