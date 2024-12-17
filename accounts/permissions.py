from django.http import HttpResponse
from django.contrib import messages
from rest_framework.views import APIView

class AdminRequiredMixin(APIView):
    def dispatch(self, request, *args, **kwargs):

        if not (request.user.is_authenticated and request.user.is_admin):
            messages.error(request, "You do not have permission to view this page.")
            return HttpResponse(
                """<script>alert("Please log in to access this page.");window.location.href = "/accounts/login";</script>""",
                content_type="text/html"
            )  
        
        return super().dispatch(request, *args, **kwargs)
    
class OfficeStaffRequiredMixin(APIView):
    def dispatch(self, request, *args, **kwargs):

        if not (request.user.is_authenticated and request.user.is_office_staff):
            messages.error(request, "You do not have permission to view this page.")
            return HttpResponse(
                """<script>alert("Please log in to access this page.");window.location.href = "/accounts/login";</script>""",
                content_type="text/html"
            )  
        
        return super().dispatch(request, *args, **kwargs)
    
    
    
class LibrarianRequiredMixin(APIView):
    def dispatch(self, request, *args, **kwargs):

        if not (request.user.is_authenticated and request.user.is_librarian):
            messages.error(request, "You do not have permission to view this page.")
            return HttpResponse(
                """<script>alert("Please log in to access this page.");window.location.href = "/accounts/login";</script>""",
                content_type="text/html"
            )  
        
        return super().dispatch(request, *args, **kwargs)
    
    
class AdminOfficeStaffLibrarianMixin(APIView):
    def dispatch(self, request, *args, **kwargs):
        # Check if the user has any of the allowed roles (admin, office_staff, librarian)
        if not (request.user.is_authenticated and(request.user.is_admin or request.user.is_office_staff or request.user.is_librarian)):
            messages.error(request, "You do not have permission to view this page.")
            return HttpResponse(
                """<script>alert("Please log in to access this page.");window.location.href = "/accounts/login";</script>""",
                content_type="text/html"
            )  # Redirect to login if the user doesn't have the required role
        
        return super().dispatch(request, *args, **kwargs)
    
class AdminLibrarianMixin(APIView):
    def dispatch(self, request, *args, **kwargs):
        # Check if the user has any of the allowed roles (admin, librarian)
        if not (request.user.is_authenticated and(request.user.is_admin or request.user.is_librarian)):
            messages.error(request, "You do not have permission to view this page.")
            return HttpResponse(
                """<script>alert("Please log in to access this page.");window.location.href = "/accounts/login";</script>""",
                content_type="text/html"
            )  # Redirect to login if the user doesn't have the required role
        
        return super().dispatch(request, *args, **kwargs)

class AdminOfficeStaffMixin(APIView):
    def dispatch(self, request, *args, **kwargs):
        # Check if the user has any of the allowed roles (admin, office_staff)
        if not (request.user.is_authenticated and(request.user.is_admin or request.user.is_office_staff)):
            messages.error(request, "You do not have permission to view this page.")
            return HttpResponse(
                """<script>alert("Please log in to access this page.");window.location.href = "/accounts/login";</script>""",
                content_type="text/html"
            )  # Redirect to login if the user doesn't have the required role
        
        return super().dispatch(request, *args, **kwargs)