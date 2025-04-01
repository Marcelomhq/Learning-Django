from django.shortcuts import redirect,HttpResponse
from django.urls import reverse

# class RequireLoginMiddleware:
#     """
#     Middleware that redirects users to the login page if they are not authenticated,
#     except for certain allowed paths.
#     """
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         # allowed_paths = [reverse("tasks:login"), reverse("tasks:register")] 
#         allowed_paths = [reverse("tasks:authenticate"),reverse("tasks:authenticate")] # URLs that don't require login

#         if not request.user.is_authenticated and request.path not in allowed_paths:
#             return redirect("tasks:authenticate")  # Redirect to login if user is not authenticated

#         return self.get_response(request)
    
class RequireLoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        allowed_paths = [reverse("tasks:authenticate")]  # URLs that don't require login
        
        print(f"🚨 Checking request path: {request.path}")  # 🔍 Debug print
        
        if not request.user.is_authenticated and request.path not in allowed_paths and not request.path.startswith('/admin/'):
            print("⚠️ User is NOT authenticated. Redirecting to /authenticate/")
            return redirect("tasks:authenticate")  # Redirect to correct login page

        return self.get_response(request)
    
class RedirectOldLoginMiddleware:
    """
    Redirects any requests specifically for the old '/login/' path
    to the new '/authenticate/' path. Acts as a safety net.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the path is exactly '/login/'
        if request.path == '/login/':
            # Log that we caught it (optional)
            print(f"ℹ️ Intercepted request to old path '{request.path}', redirecting to 'tasks:authenticate'")
            # Redirect to the named URL for '/authenticate/'
            return redirect('tasks:authenticate')

        # If the path is not '/login/', pass the request to the next middleware
        return self.get_response(request)

# class DebugRedirectMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         if request.path == "/login/":
#             return HttpResponse(f"Redirect detected!<br>Referer: {request.META.get('HTTP_REFERER', 'N/A')}", status=200)
#         return self.get_response(request)