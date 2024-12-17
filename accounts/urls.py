from django.urls import path
from . import views

from .views import  (ManageFeesAPIView ,FeesHistoryView,EditFeesAPIView,student_add_fee,
                     ManageLibraryAPIView, EditLibraryAPIView, LibraryHistoryView,student_add_library,
                     AddStudentAPIView, EditStudentAPIView, StudentListAPIView,
                    AddLibrarianAPIView,EditLibrarianAPIView,DeleteLibrarianAPIView,LibrarianListAPIView,
                    AddOfficeStaffAPIView, EditOfficeStaffAPIView, DeleteOfficeStaffAPIView,OfficeStaffListAPIView,
                    AdminDashboardAPIView,OfficeStaffDashboardAPIView, LibrarianDashboardAPIView,
                    LoginAPIView, LogoutAPIView
)
urlpatterns = [
    
   
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    
    # Dashboards
    path('admin_dashboard/', AdminDashboardAPIView.as_view(), name='admin_dashboard'),
    path('api/dashboard/office_staff/', OfficeStaffDashboardAPIView.as_view(), name='office_staff_dashboard'),
    path('dashboard/librarian/', LibrarianDashboardAPIView.as_view(), name='librarian_dashboard'),

    # Office Staff Crud
    path('add_office_staff/', AddOfficeStaffAPIView.as_view(), name='add_office_staff'),
    path('edit_office_staff/', EditOfficeStaffAPIView.as_view(), name='edit_office_staff'),
    path('delete_office_staff/', DeleteOfficeStaffAPIView.as_view(), name='delete_office_staff'),
    path('office_staff_list/', OfficeStaffListAPIView.as_view(), name='office_staff_list'),
    
    # Librarian Crud
    path('add_librarian/', AddLibrarianAPIView.as_view(), name='add_librarian'),
    path('edit_librarian/', EditLibrarianAPIView.as_view(), name='edit_librarian'),
    path('delete_librarian/', DeleteLibrarianAPIView.as_view(), name='delete_librarian'),
    path('librarian_list/', LibrarianListAPIView.as_view(), name='librarian_list'),
    
    # Student Crud
    path('students/', StudentListAPIView.as_view(), name='student_list'),
    path('students/add/', AddStudentAPIView.as_view(), name='add_student'),
    path('students/edit/', EditStudentAPIView.as_view(), name='edit_student'),
       
    # Library History CRUD
    path('manage_library/', ManageLibraryAPIView.as_view(), name='manage_library'),
    path('view_library_history/', LibraryHistoryView.as_view(), name='view_library_history'),
    path('edit_library/', EditLibraryAPIView.as_view(), name='edit_library'),
    path('student_add_library/', student_add_library.as_view(), name='student_add_library'),

    
    # Fee History CRUD
    path('view_fees_history/', FeesHistoryView.as_view(), name='view_fees_history'),
    path('api/add_fees/', ManageFeesAPIView.as_view(), name='add_fees_api'),
    path('api/edit_fees/', EditFeesAPIView.as_view(), name='edit_fees'),
    path('student_add_fee/', student_add_fee.as_view(), name='student_add_fee'),
    
    
    
    
    

]