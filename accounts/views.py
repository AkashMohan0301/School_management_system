from django.contrib.auth import authenticate, login, logout,get_user_model
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Classes, Student,LibraryHistory,FeesHistory,Student
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .permissions import AdminLibrarianMixin, AdminOfficeStaffMixin, AdminRequiredMixin,AdminOfficeStaffLibrarianMixin, LibrarianRequiredMixin, OfficeStaffRequiredMixin
#   DRF
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from .serializers import FeesHistorySerializer,LibraryHistorySerializer,StudentSerializer,LibrarianSerializer,OfficeStaffSerializer

# Login view
class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    # Handling GET requests (e.g., rendering a login page)
    def get(self, request, *args, **kwargs):
        return render(request, 'login/login.html')  # The login page template

    # Handling POST requests for authentication
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({"error": "Email and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        # Authenticate the user
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)  # Log the user in and create a session

            # Based on the user role, set the appropriate redirect URL
            if user.is_admin:
                return redirect('admin_dashboard')
            elif user.is_office_staff:
                return redirect('office_staff_dashboard')
            elif user.is_librarian:
                return redirect('librarian_dashboard')
            else:
                return Response({"error": "Unauthorized access."}, status=status.HTTP_403_FORBIDDEN)
        return HttpResponse("""<script>alert('Login Failed.');window.location.href = '/accounts/login/';</script>""")


# Logout view
class LogoutAPIView(APIView):
    def post(self, request, *args, **kwargs):
        logout(request)  # Log the user out
        return HttpResponse("""<script>alert('You Have Been Logged Out');window.location.href = '/accounts/login/';</script>""")

# Dashboard 
class AdminDashboardAPIView(AdminRequiredMixin,APIView):
    def get(self, request, *args, **kwargs):
        return render(request, 'admin/admin_dashboard.html')

class OfficeStaffDashboardAPIView(OfficeStaffRequiredMixin,APIView):
    def get(self, request, *args, **kwargs):
        return render(request, 'office_staff/office_staff_dashboard.html')

class LibrarianDashboardAPIView(LibrarianRequiredMixin,APIView):
    def get(self, request, *args, **kwargs):
        return render(request, 'librarian/librarian_dashboard.html')

# 
# Office Staff CRUD /////////////////////////////////////////////////////////////////////////////////////////
User = get_user_model()
class AddOfficeStaffAPIView(AdminRequiredMixin, APIView):

    def get(self, request, *args, **kwargs):
        return render(request, 'admin/add_office_staff_view.html')

    def post(self, request, *args, **kwargs):
        serializer = OfficeStaffSerializer(data=request.POST)
        if serializer.is_valid():
            serializer.save()
            return HttpResponse(
                """<script>alert('Office Staff Added successfully.');window.location.href = '/accounts/office_staff_list/';</script>"""
            )

        # Pass serializer errors to the template
        return render(
            request,
            'admin/add_office_staff_view.html',
            {'errors': serializer.errors, 'form_data': request.POST}
        )

class EditOfficeStaffAPIView(AdminRequiredMixin, APIView):

    def post(self, request, *args, **kwargs):
        method = request.POST.get('method')
        id = request.POST.get('id')
        if method == 'get':
            return self.get(request, id)
        elif method == 'put':
            return self.put(request, id)
        else:
            return redirect('admin_dashboard')

    def get(self, request, id, *args, **kwargs):
        try:
            office_staff = User.objects.get(id=id, is_office_staff=True)
            serializer = OfficeStaffSerializer(office_staff)
            return render(request, 'admin/edit_office_staff_view.html', {'data': serializer.data})
        except User.DoesNotExist:
            return Response({"message": "Office staff not found."}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, id, *args, **kwargs):
        try:
            office_staff = User.objects.get(id=id, is_office_staff=True)
            serializer = OfficeStaffSerializer(office_staff, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return HttpResponse("""<script>alert('Office Staff updated successfully.');window.location.href = '/accounts/office_staff_list/';</script>""")
            # If the serializer is not valid, return with validation errors
            return render(request, 'admin/edit_office_staff_view.html', {'data': request.data, 'errors': serializer.errors})
        except User.DoesNotExist:
            return Response({"message": "Office staff not found."}, status=status.HTTP_404_NOT_FOUND)
        
        
class DeleteOfficeStaffAPIView(AdminRequiredMixin,APIView):
    def post(self, request, *args, **kwargs):
        method = request.POST.get('method')
        id= request.POST.get('id')
        if method == 'delete':
            return self.delete(request, id)
        return Response({"detail": f"Method {method} not allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    def delete(self, request, id, *args, **kwargs):
        try:
            office_staff = User.objects.get(id=id, is_office_staff=True)
            office_staff.delete()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        except User.DoesNotExist:
            return HttpResponse("""<script>alert('Office Staff Not Found.');window.location.href = '/accounts/office_staff_list/';</scripts>""")
        
class OfficeStaffListAPIView(AdminRequiredMixin,APIView):

    def get(self, request, *args, **kwargs):
        office_staffs = User.objects.filter(is_office_staff=True)
        serializer = OfficeStaffSerializer(office_staffs, many=True)
        return render(request, 'admin/office_staff_list.html', {'datas': serializer.data})




# Librarian CRUD /////////////////////////////////////////////////////////////////////////////////////////

class AddLibrarianAPIView(AdminRequiredMixin,APIView):

    def get(self, request, *args, **kwargs):
        return render(request, 'admin/add_librarian_view.html')

    def post(self, request, *args, **kwargs):
        serializer = LibrarianSerializer(data=request.POST)
        if serializer.is_valid():
            serializer.save()
            return HttpResponse(
                """<script>alert('Librarian Added successfully.');window.location.href = '/accounts/add_librarian/';</script>"""
            )

        # Pass serializer errors to the template
        return render(
            request,
            'admin/add_librarian_view.html',
            {'errors': serializer.errors, 'form_data': request.POST}
        )
        

class EditLibrarianAPIView(AdminRequiredMixin,APIView):

    def post(self, request, *args, **kwargs):
        method = request.POST.get('method')
        id = request.POST.get('id')
        if method == 'get':
            return self.get(request, id)
        elif method == 'put':
            return self.put(request, id)
        else:
            return redirect('admin_dashboard')
    def get(self, request, id, *args, **kwargs):
        try:
            librarian = User.objects.get(id=id, is_librarian=True)
            serializer = LibrarianSerializer(librarian)
            return render(request, 'admin/edit_librarian_view.html', {'data': serializer.data})
        except User.DoesNotExist:
            return HttpResponse("""<script>alert('Librarian Not Found.');window.location.href = '/accounts/librarian_list/';</script>""")

    def put(self, request, id, *args, **kwargs):
        try:
            librarian = User.objects.get(id=id, is_librarian=True)
            serializer = LibrarianSerializer(librarian, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return HttpResponse("""<script>alert('Librarian updated successfully.');window.location.href = '/accounts/librarian_list/';</script>""")
            return render(request, 'admin/edit_librarian_view.html', {'data': request.data, 'errors': serializer.errors})
        except User.DoesNotExist:
            return HttpResponse("""<script>alert('Librarian Not Found.');window.location.href = '/accounts/librarian_list/';</script>""")
        
        
class DeleteLibrarianAPIView(AdminRequiredMixin,APIView):
    def post(self, request, *args, **kwargs):
        method = request.POST.get('method')
        id= request.POST.get('id')
        if method == 'delete':
            return self.delete(request, id)
        return Response({"detail": f"Method {method} not allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    def delete(self, request, id, *args, **kwargs):
        try:
            librarian = User.objects.get(id=id, is_librarian=True)
            librarian.delete()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        except User.DoesNotExist:
            return HttpResponse("""<script>alert('Office Staff Not Found');window.location.href = '/accounts/librarian_list/';</script>""")
        

class LibrarianListAPIView(AdminRequiredMixin,APIView):
    def get(self, request, *args, **kwargs):
        librarians = User.objects.filter(is_librarian=True)
        serializer = LibrarianSerializer(librarians, many=True)
        return render(request, 'admin/librarian_list.html', {'datas': serializer.data})

# Student CRUD /////////////////////////////////////////////////////////////////////////////////////////
class AddStudentAPIView(AdminRequiredMixin,APIView):

    def get(self, request, *args, **kwargs):
        classes = Classes.objects.all()  # Get all available classes
        return render(request, 'admin/add_student.html', {'classes': classes})

    def post(self, request, *args, **kwargs):
        data = {
            "name": request.POST.get("name"),
            "age": request.POST.get("age"),
            "dob": request.POST.get("dob"),
            "address": request.POST.get("address"),
            "gender": request.POST.get("gender"),
            "phone_number": request.POST.get("phone_number"),
            "class_name": request.POST.get("class_name"),  # Get class_id from form
        }

        # Check if a profile picture is included in the request files
        if 'profile_picture' in request.FILES:
            data['profile_picture'] = request.FILES['profile_picture']

        # Create and validate the serializer with the provided data
        serializer = StudentSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return HttpResponse("""<script>alert('Added successfully.');window.location.href = '/accounts/admin_dashboard/';</script>""")
        else:
            # Pass the errors back to the template
            classes = Classes.objects.all()  # Get all available classes
            return render(request, 'admin/add_student.html', {
                'classes': classes,
                'errors': serializer.errors,  # Pass errors to the template
                'data': data  # Pass the entered data back to the form
            })

class EditStudentAPIView(AdminRequiredMixin,APIView):

    def post(self, request, *args, **kwargs):
        method = request.POST.get('method')
        id = request.POST.get('student_id')

        if method == 'get':
            return self.get(request, id)
        elif method == 'put':
            return self.put(request, id)
        elif method == 'delete':
            return self.delete(request, id)
        else:
            return redirect('admin_dashboard')

    def get(self, request, id, *args, **kwargs):
        try:
            student = Student.objects.get(id=id)
            serializer = StudentSerializer(student)
            return render(request, 'admin/edit_student.html', {'student': serializer.data, 'classes': Classes.objects.all()})
        except Student.DoesNotExist:
            return Response({"message": "Student not found."}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, id, *args, **kwargs):
        data = {
            "id": request.POST.get("student_id"),
            "name": request.POST.get("name"),
            "age": request.POST.get("age"),
            "class_name": request.POST.get("class_name"),
            "dob": request.POST.get("dob"),
            "address": request.POST.get("address"),
            "gender": request.POST.get("gender"),
            "phone_number": request.POST.get("phone_number"),
        }

        if 'profile_picture' in request.FILES:
            data['profile_picture'] = request.FILES['profile_picture']

        try:
            student = Student.objects.get(id=data['id'])

            update_data = data.copy()
            if 'profile_picture' in update_data and not update_data['profile_picture']:
                update_data.pop('profile_picture')

            serializer = StudentSerializer(student, data=update_data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return HttpResponse("""<script>alert('Edited Successfully');window.location.href = '/accounts/students/';</script>""")
            else:
                # Pass the errors to the template
                return render(request, 'admin/edit_student.html', {
                    'student': data,  # pass the current data back to the form
                    'classes': Classes.objects.all(),
                    'errors': serializer.errors  # Pass the errors here
                })
        except Student.DoesNotExist:
            return HttpResponse("""<script>alert('Student Not Found');window.location.href = '/accounts/students/';</script>""")

    def delete(self, request, id, *args, **kwargs):
        try:
            student = Student.objects.get(id=id)
            student.delete()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        except Student.DoesNotExist:
            return HttpResponse("""<script>alert('Student Not Found');window.location.href = '/accounts/admin_dashboard/';</script>""")

class StudentListAPIView(AdminOfficeStaffLibrarianMixin,APIView):
    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_admin or request.user.is_office_staff or request.user.is_librarian):
            messages.error(request, "You do not have permission to view this page.")
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        if request.user.is_admin:
            role='admin'
        else:
            role=""
        return render(request, 'admin/student_list.html',{'students':serializer.data ,'role':role })

# Library History CRUD /////////////////////////////////////////////////////////////////////////////////////////
class ManageLibraryAPIView(AdminLibrarianMixin,APIView):

    def get(self, request, *args, **kwargs):
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return render(request, 'admin/student_list_library.html', {'students': serializer.data})
        
class student_add_library(AdminLibrarianMixin,APIView):
    def post(self, request, *args, **kwargs):
        # Handle Create/Update/Delete actions
        method = request.POST.get('method')
        id = request.POST.get('student')
        
        if method == 'get':
            return self.get(request, id)
        elif method == 'post':
            return self.posts(request)
        else:
            return redirect('manage_library')
        
    def get(self, request, id, *args, **kwargs):
        # Fetch record for editing
        student = Student.objects.get(id=id)
        return render(request, 'admin/add_library_history.html', {
            'student': student
        })
        
    def posts(self, request, *args, **kwargs):
        print(request.data)
        serializer = LibraryHistorySerializer(data=request.data)
        student_id = request.data.get('student')
        try:
            student = Student.objects.get(id=student_id)
        except Student.DoesNotExist:
            return HttpResponse("Student not found", status=404)

        if serializer.is_valid():
            serializer.save()
            return HttpResponse("""<script>alert('Added successfully.');window.location.href = '/accounts/api/add_fees/';</script>""")
        print("Validation Errors:", serializer.errors)
        # Render the form with errors and student details
        return render(request, 'admin/add_library_history.html', {
            'student': student,
            'data': request.data,
            'errors': serializer.errors
        })          
        
class EditLibraryAPIView(AdminLibrarianMixin,APIView):

    def post(self, request, *args, **kwargs):
        method = request.POST.get('method')
        id = request.POST.get('lib_id')

        if method == 'get':
            return self.get(request, id)
        elif method == 'put':
            return self.put(request, id)
        elif method == 'delete':
            return self.delete(request, id)
        else:
            return redirect('admin_dashboard')

    def get(self, request, id, *args, **kwargs):
        record = LibraryHistory.objects.get(id=id)
        students = Student.objects.all()
        serializer = LibraryHistorySerializer(record)
        return render(request, 'admin/view_edit_library_history.html', {
            'data': serializer.data,
            'students': students
        })

    def put(self, request, id, *args, **kwargs):
        record = LibraryHistory.objects.get(id=id)
        data = {
            "student": request.POST.get("student_id"),
            "book_name": request.POST.get("book_name"),
            "borrow_date": request.POST.get("borrow_date"),
            "return_date": request.POST.get("return_date"),
            "status": request.POST.get("status"),
        }
        serializer = LibraryHistorySerializer(record, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return HttpResponse("""<script>alert('Updated successfully.');window.location.href = '/accounts/view_library_history/';</script>""")
        return HttpResponse("""<script>alert('Failed. Validation error occurred.');window.location.href = '/accounts/view_library_history/';</script>""")

    def delete(self, request, id, *args, **kwargs):
        try:
            record = LibraryHistory.objects.get(id=id)
            record.delete()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        except Student.DoesNotExist:
            return HttpResponse("""<script>alert('Student Not Found');window.location.href = '/accounts/admin_dashboard/';</script>""")


class LibraryHistoryView(AdminOfficeStaffLibrarianMixin,APIView):

    def get(self, request):
        library_histories = LibraryHistory.objects.all()
        serializer = LibraryHistorySerializer(library_histories, many=True)
        if request.user.is_admin:
            role='admin'
        elif request.user.is_librarian:
            role="librarian"
        else :
            role=""
        return render(request, 'admin/view_library_history.html', {'datas': serializer.data,'role':role})


 # Fee History CRUD /////////////////////////////////////////////////////////////////////////////////////////
       
class ManageFeesAPIView(AdminOfficeStaffMixin,APIView):

    def get(self, request, *args, **kwargs):
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return render(request, 'admin/student_list_fee.html', {'students': serializer.data})

class student_add_fee(AdminOfficeStaffMixin,APIView):
    def post(self, request, *args, **kwargs):
        # Handle Create/Update/Delete actions
        method = request.POST.get('method')
        id = request.POST.get('student')
        
        if method == 'get':
            return self.get(request, id)
        elif method == 'post':
            return self.posts(request)
        else:
            return redirect('add_fees_api')
        
    def get(self, request, id, *args, **kwargs):
        # Fetch record for editing
        student = Student.objects.get(id=id)
        return render(request, 'admin/add_fees.html', {
            'student': student
        })
        
    def posts(self, request, *args, **kwargs):
        serializer = FeesHistorySerializer(data=request.data)
        student_id = request.data.get('student')
        try:
            student = Student.objects.get(id=student_id)
        except Student.DoesNotExist:
            return HttpResponse("Student not found", status=404)

        if serializer.is_valid():
            serializer.save()
            return HttpResponse("""<script>alert('Added successfully.');window.location.href = '/accounts/api/add_fees/';</script>""")
        
        # Render the form with errors and student details
        return render(request, 'admin/add_fees.html', {
            'student': student,
            'data': request.data,
            'errors': serializer.errors
        })
        
class EditFeesAPIView(AdminOfficeStaffMixin,APIView):

    def post(self, request, *args, **kwargs):
        # Handle Create/Update/Delete actions
        method = request.POST.get('method')
        id = request.POST.get('id')

        if method == 'get':  # Fetch record for editing
            return self.get(request, id)
        elif method == 'put':  # Update record
            return self.put(request, id)
        elif method == 'delete':  # Delete record
            return self.delete(request, id)
        else:
            return redirect('admin_dashboard')  # Redirect to a default page on error

    def get(self, request, id, *args, **kwargs):
        # Fetch record for editing
        fee = FeesHistory.objects.get(id=id)
        students = Student.objects.all()
        serializer = FeesHistorySerializer(fee)
        return render(request, 'admin/edit_fees_history.html', {
            'data': serializer.data,
            'students': students
        })

    def put(self, request, id, *args, **kwargs):
        fee = FeesHistory.objects.get(id=id)
        serializer = FeesHistorySerializer(fee, data=request.data, partial=True)  # Use partial=True for partial updates
        if serializer.is_valid():
            serializer.save()
            return HttpResponse("""<script>alert('Updated successfully.');window.location.href = '/accounts/view_fees_history/';</script>""")
        else:
            # Pass errors to the template
            students = Student.objects.all()
            return render(request, 'admin/edit_fees_history.html', {
                'data': request.data,
                'students': students,
                'errors': serializer.errors  # Pass the errors to the template
            })

    def delete(self, request, id, *args, **kwargs):
        # Delete the record
        fee = FeesHistory.objects.get(id=id)
        fee.delete()
        return HttpResponse("""<script>alert('Deleted successfully.');window.location.href = '/accounts/view_fees_history/';</script>""")


class FeesHistoryView(AdminOfficeStaffMixin,APIView):
    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_admin or request.user.is_office_staff):
            messages.error(request, "You do not have permission to view this page.")
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        # Serialize the data
        fees_histories = FeesHistory.objects.all()
        serializer = FeesHistorySerializer(fees_histories, many=True)
        
        # Render the template with serialized data
        return render(request, 'admin/view_fees_history.html', {'datas': serializer.data})
    
    
