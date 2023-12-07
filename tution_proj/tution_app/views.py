
from datetime import datetime
from django.shortcuts import render
from datetime import date
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
import re
from .models import TeacherAttendance
from django.shortcuts import render, redirect, get_object_or_404

from .models import *
from django.contrib.auth.models import User, auth
from django.http import HttpResponse
from django.contrib import messages
from django.core.mail import send_mail
import random
from django.contrib.auth.models import Group
import string
from django.contrib.auth import authenticate, login
from .models import Notification
# Create your views here.


def home(requet):
    return render(requet, 'home.html')


def signup_page(request):
    course = CourseModel.objects.all()
    department = DepartmentModel.objects.all()
    context = {
        'course': course,
        'department': department

    }
    return render(request, 'signup_form.html', context)

# this is used for temperory for sign up its working
# def signup(request):

#     if request.method == 'POST':
#         user_type = request.POST.get('user_type')  # Fetch the selected user type
#         #Common fields for both Teacher and Student
#         first_name = request.POST['first_name']
#         last_name = request.POST['last_name']
#         username = request.POST['email']
#         email = request.POST['email']
#         add = request.POST['address']
#         gender = request.POST['gender']
#         age = request.POST['age']
#         number = request.POST['phone']
#         select = request.POST['select']
#         department=DepartmentModel.objects.get(id=select)
#         photo = request.FILES.get('file')
#         password = request.POST['password']
#         cpassword = request.POST['cpassword']

#         if password == cpassword:
#             if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
#                 messages.info(request, 'Username or email already exists!')
#                 return redirect('signup_page')

#             user = User.objects.create_user(
#                 first_name=first_name,
#                 last_name=last_name,
#                 email=email,
#                 username=username,
#                 password=password
#             )

#             if user_type == 'teacher':
#                 # Create a teacher and associated notification
#                 teacher_data = TeacherModel(
#                     tr_address=add,
#                     tr_gender=gender,
#                     tr_age=age,
#                     tr_phone=number,
#                     tr_image=photo,
#                     department=department,
#                     # course=course,
#                     teacher=user,
#                     status=False,
#                 )
#                 teacher_data.save()

#                 # Create a notification for the admin about the new teacher
#                 Notification.objects.create(user=user, notification_type='New Teacher',notification_for='admin')

#             elif user_type == 'student':
#                 # Create a student and associated notification
#                 student_data = StudntModel(
#                     Std_address=add,
#                     std_gender=gender,
#                     Std_age=age,
#                     std_phone=number,
#                     std_image=photo,
#                     department=department,
#                     # course=course,
#                     student=user,
#                     status=False,
#                 )
#                 student_data.save()

#                 # Create a notification for the admin about the new student
#                 Notification.objects.create(user=user, notification_type='New Student',notification_for='admin')

#             messages.success(request, f'Welcome {user.first_name}!')
#             return redirect('signinpage')
#         else:
#             messages.info(request, 'Passwords do not match!')
#             return redirect('signup_page')
#     else:
#         return render(request, 'signup_form.html')


def generate_random_password():
    return ''.join(random.choices(string.digits, k=6))


def signup(request):
    if request.method == 'POST':
        user_type = request.POST.get('user_type')
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['email']
        email = request.POST['email']
        add = request.POST['address']
        gender = request.POST['gender']
        age = request.POST['age']
        number = request.POST['phone']
        select = request.POST['select']
        department = DepartmentModel.objects.get(id=select)
        photo = request.FILES.get('file')

        if User.objects.filter(username=username, email=email).exists():
            messages.info(request, 'Username or email already exists!')
            return render(request, 'signup_form.html')

        # Generate a random 6-digit password
        confirmation_password = generate_random_password()

        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            username=username,
            password=confirmation_password  # Temporary password for confirmation
        )

        if user_type == 'teacher':
            teacher_data = TeacherModel(
                tr_address=add,
                tr_gender=gender,
                tr_age=age,
                tr_phone=number,
                tr_image=photo,
                department=department,
                teacher=user,
                status=False,
            )
            teacher_data.save()
            Notification.objects.create(
                user=user, notification_type='New Teacher', notification_for='admin')

        elif user_type == 'student':
            student_data = StudntModel(
                Std_address=add,
                std_gender=gender,
                Std_age=age,
                std_phone=number,
                std_image=photo,
                department=department,
                student=user,
                status=False,
            )
            student_data.save()
            Notification.objects.create(
                user=user, notification_type='New Student', notification_for='admin')

        # Sending confirmation email
        send_mail(
            'Confirmation Email',
            f'Your confirmation code: {confirmation_password}',
            'dheerajks.2610@gmail.com',
            [email],
            fail_silently=False,
        )

       # messages.success(request, f'Welcome {user.first_name}!')
        return redirect('signinpage')

    else:
        return render(request, 'signup_form.html')


def check_email(request):
    if request.method == 'POST' and 'email' in request.POST:
        email = request.POST['email']
        email_exists = User.objects.filter(email=email).exists()
        return JsonResponse({'emailExists': email_exists})
    return JsonResponse({'emailExists': False})  # Default response


def signinpage(request):
    return render(request, 'signin.html')

# def signin(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')

#         user = authenticate(request, username=username, password=password)

#         if user is not None:
#             if user.is_superuser:
#                 messages.info(request, f'Welcome {username}')
#                 login(request, user)
#                 return redirect('admin_page')

#             is_teacher_pending = TeacherModel.objects.filter(teacher=user, status=False).exists()
#             is_student_pending = StudntModel.objects.filter(student=user, status=False).exists()

#             if not (is_teacher_pending or is_student_pending):
#                 login(request, user)

#                 if TeacherModel.objects.filter(teacher=user).exists():
#                     messages.info(request, f'Welcome {username}')
#                     return redirect('teacher_page')
#                 elif StudntModel.objects.filter(student=user).exists():
#                     messages.info(request, f'Welcome {username}')
#                     return redirect('student_page')
#                 else:
#                     messages.error(request, 'Your profile is not approved by the admin yet. You can access only after approval.')

#     return render(request, 'signin.html')


def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_superuser:
                # messages.info(request, f'Welcome {username}')
                login(request, user)
                return redirect('admin_page')

            is_teacher_pending = TeacherModel.objects.filter(
                teacher=user, status=False).exists()
            is_student_pending = StudntModel.objects.filter(
                student=user, status=False).exists()

            if not (is_teacher_pending or is_student_pending):
                login(request, user)

                if TeacherModel.objects.filter(teacher=user).exists():
                    # messages.info(request, f'Welcome {username}')
                    return redirect('teacher_page')
                elif StudntModel.objects.filter(student=user).exists():
                    # messages.info(request, f'Welcome {username}')
                    return redirect('student_page')
                else:
                    messages.error(
                        request, 'Your profile is not approved by the admin yet. You can access only after approval.')
            else:
                return render(request, 'signin.html', {'pending_user': True})
        else:
            # If the user is not found or authentication fails, display an error message.
            messages.error(
                request, 'Invalid username or password. Please try again.')
            return render(request, 'signin.html')

    return render(request, 'signin.html')


def show_course(request):
    course = CourseModel.objects.all()
    return render(request, 'course_details.html', {'course': course})


def CoursePage(request):
    return render(request, 'add_course.html')


def AddCourse(request):
    if request.method == 'POST':
        coursename = request.POST['coursename']
        duration = request.POST['duration']
        coursefees = request.POST['coursefees']
        syllabus = request.POST['syllabus']

        data = CourseModel(cs_name=coursename, cs_duration=duration,
                           cs_fee=coursefees, cs_syllabus=syllabus)
        data.save()
        return redirect('CoursePage')
    return render(request, 'add_course.html',)


def edit_course_page(request, pk):
    course = get_object_or_404(CourseModel, id=pk)
    return render(request, 'edit_course.html', {'course': course})


def edit_course(request, pk):
    if request.method == 'POST':
        course = get_object_or_404(CourseModel, id=pk)
        course.cs_name = request.POST['coursename']
        course.cs_duration = request.POST['duration']
        course.cs_fee = request.POST['coursefees']
        course.cs_syllabus = request.POST['syllabus']
        course.save()

        messages.success(request, 'Course updated successfully!')
        return redirect('show_course')

    return redirect('edit_course_page', pk=pk)


def course_delete(requset, pk):
    course = CourseModel.objects.filter(id=pk)
    course.delete()
    return redirect('show_course')


def deptpage(request):
    return render(request, 'add_dept.html')


def Add_dept(request):
    if request.method == 'POST':
        deptname = request.POST['deptname']
        data = DepartmentModel(dept_name=deptname,)
        data.save()

        return redirect('deptpage')
    return render(request, 'add_dept.html')


def show_teachers(request):
    course = CourseModel.objects.all()
    teacher = TeacherModel.objects.all()

    context = {
        'course': course,
        'teacher': teacher,

    }
    return render(request, 'teacher_details.html', context)


def edit_teacher_page(request, pk):
    course = CourseModel.objects.all()
    teacher = TeacherModel.objects.get(id=pk)
    context = {
        'course': course,
        'teacher': teacher
    }
    return render(request, 'edit_teacher.html', context)


def edit_teacher(request, pk):
    teacher = TeacherModel.objects.get(id=pk)
    user = teacher.teacher

    if request.method == 'POST':
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        # Update other fields in the TeacherModel
        teacher.tr_address = request.POST.get('address')
        teacher.tr_gender = request.POST.get('gender')
        teacher.tr_age = request.POST.get('age')
        teacher.tr_phone = request.POST.get('phone')
        select_course_id = request.POST['select']
        teacher.course = CourseModel.objects.get(id=select_course_id)

        if request.FILES.get('file'):
            teacher.tr_image = request.FILES['file']

        user.save()  # Save the updated user details
        teacher.save()  # Save the updated teacher details
        return redirect('show_teachers')  # Redirect to the teachers list page

    courses = CourseModel.objects.all()
    return render(request, 'edit_teacher.html', {'teacher': teacher, 'courses': courses})


def delete_teacher(request, pk):
    teacher = get_object_or_404(TeacherModel, id=pk)
    teacher.delete()
    return redirect('show_teachers')


def show_students(request):
    stds = StudntModel.objects.all()
    return render(request, 'student_details.html', {'stds': stds})


def edit_student_page(request, pk):
    department = DepartmentModel.objects.all()
    stds = StudntModel.objects.get(id=pk)  # Retrieve the specific student

    context = {
        'department': department,
        'stds': stds
    }
    return render(request, 'edit_student.html', context)


def edit_student(request, pk):
    stds = StudntModel.objects.get(id=pk)
    if request.method == 'POST':
        user = stds.student  # Access the related User object
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        stds.Std_address = request.POST.get('address')
        stds.std_gender = request.POST.get('gender')
        stds.Std_age = request.POST.get('age')
        stds.std_phone = request.POST.get('phone')
        select_department_id = request.POST['select']
        stds.department = DepartmentModel.objects.get(id=select_department_id)

        if request.FILES.get('file'):
            stds.std_image = request.FILES['file']

        user.save()  # Save the updated user details
        stds.save()  # Save the updated student details
        return redirect('show_students')  # Redirect to the students list page
    courses = CourseModel.objects.all()
    department = DepartmentModel.objects.all()
    context = {
        'courses': courses,
        'department': department
    }
    return render(request, 'edit_student.html', context)


def delete_student(request, pk):
    student = StudntModel.objects.filter(id=pk)
    student.delete()
    return redirect('show_students')


def admin_notifications(request):
    notifications = Notification.objects.filter(notification_for='admin')
    return render(request, 'admin_notification.html', {'notifications': notifications})


def delete_selected_notifications(request):
    if request.method == 'POST':
        selected_notifications = request.POST.getlist('selected_notifications')
        Notification.objects.filter(id__in=selected_notifications).delete()
    return redirect('admin_notifications')


def manage_registrations(request):
    pending_teachers = TeacherModel.objects.filter(status=False)
    pending_students = StudntModel.objects.filter(status=False)
    return render(request, 'manage_regestrations.html', {
        'pending_teachers': pending_teachers,
        'pending_students': pending_students,
    })


def approve_teacher(request, teacher_id):
    teacher = get_object_or_404(TeacherModel, pk=teacher_id)
    teacher.status = True  # Update the status to approved
    teacher.save()
    # Grant access to the teacher dashboard upon approval
    user = teacher.teacher
    return redirect('manage_registrations')


def approve_student(request, student_id):
    student = get_object_or_404(StudntModel, pk=student_id)
    student.status = True  # Update the status to approved
    student.save()
    # Grant access to the student dashboard upon approval
    user = student.student
    return redirect('manage_registrations')


def delete_teacher_approve(request, teacher_id):
    teacher = TeacherModel.objects.get(pk=teacher_id)

    if teacher:
        user = teacher.teacher  # Fetch associated user

        if user:
            teacher.delete()  # Delete the TeacherModel instance
            user.delete()  # Delete the associated User

            return redirect('manage_registrations')
    return redirect('show_teachers')


def delete_student_approve(request, student_id):
    student = StudntModel.objects.get(pk=student_id)

    if student:
        user = student.student  # Fetch associated user

        if user:
            student.delete()  # Delete the TeacherModel instance
            user.delete()  # Delete the associated User

            return redirect('manage_registrations')
    return redirect('show_students')


# for asign course to teacher and student
def assign_page_tchr(request):
    students = StudntModel.objects.all()
    teachers = TeacherModel.objects.all()
    courses = CourseModel.objects.all()
    context = {
        'courses': courses,
        'teachers': teachers,
        'students': students
    }
    return render(request, 'assign_course_teacher.html', context)


def assign_course_teacher(request):
    if request.method == 'POST':
        course_id = request.POST.get('course_id')
        teacher_id = request.POST.get('teacher_id')

        course = get_object_or_404(CourseModel, id=course_id)
        teacher = get_object_or_404(TeacherModel, id=teacher_id)

        teacher.course = course
        teacher.save()

        # Create a notification for the teacher
        Notification.objects.create(
            # Assuming 'teacher' is the foreign key to the User model in TeacherModel
            user=teacher.teacher,
            notification_type=f'You have been assigned to the course {course.cs_name}',
            notification_for='teacher'
        )

        # Redirect to a success page after assigning the course
        return redirect('admin_page')

    courses = CourseModel.objects.all()
    teachers = TeacherModel.objects.all()
    return render(request, 'assign_course_teacher.html', {'courses': courses, 'teachers': teachers})


# teacher page
def teacher_notifications(request):
    notifications = Notification.objects.filter(notification_for='teacher')
    return render(request, 'teacher/teacher_notification.html', {'notifications': notifications})


def delete_teacher_notifications(request):
    if request.method == 'POST':
        selected_notifications = request.POST.getlist('selected_notifications')
        Notification.objects.filter(id__in=selected_notifications).delete()
    return redirect('teacher_notifications')


def assign_page_stu(request):
    students = StudntModel.objects.all()
    courses = CourseModel.objects.all()
    context = {
        'courses': courses,
        'students': students
    }
    return render(request, 'assign_course_student.html', context)


def assign_course_student(request):
    if request.method == 'POST':
        course_id = request.POST.get('course_id')
        student_id = request.POST.get('student_id')

        course = get_object_or_404(CourseModel, id=course_id)
        student = get_object_or_404(StudntModel, id=student_id)

        student.course = course
        student.save()

        # Redirect to a success page after assigning the course
        return redirect('admin_page')

    courses = CourseModel.objects.all()
    students = StudntModel.objects.all()
    return render(request, 'assign_course_student.html', {'courses': courses, 'students': students})


# step 1
# def select_course_page(request):
#     course=CourseModel.objects.all()
#     return render(request,'select_course.html',{'courses':course})
def select_course_page(request):
    courses = CourseModel.objects.all()
    return render(request, 'select_course.html', {'courses': courses})


# def select_course_details_page(request):
#     if request.method == 'POST':
#         course_id = request.POST.get('course_id')

#         selected_course = CourseModel.objects.get(pk=course_id)

#         teachers = TeacherModel.objects.filter(course=selected_course)
#         students = StudntModel.objects.filter(course=selected_course)


#         context = {
#             'course': selected_course,
#             'teachers': teachers,
#             'students': students
#         }
#         return render(request, 'select_course_detail.html', context)

#     courses = CourseModel.objects.all()
#     return render(request, 'select_course_detail.html', {'courses': courses})

def select_course_details_page(request):
    if request.method == 'POST':
        course_id = request.POST.get('course_id')

        selected_course = get_object_or_404(CourseModel, pk=course_id)

        teachers = TeacherModel.objects.filter(course=selected_course)
        students = StudntModel.objects.filter(course=selected_course)

        context = {
            'course': selected_course,
            'teachers': teachers,
            'students': students
        }
        return render(request, 'assign_course.html', context)

    courses = CourseModel.objects.all()
    return render(request, 'select_course_detail.html', {'courses': courses})


def assign_course(request):
    if request.method == 'POST':
        course_id = request.POST.get('course_id')
        teacher_id = request.POST.get('teacher_id')
        student_id = request.POST.get('student_id')

        course = get_object_or_404(CourseModel, id=course_id)
        teacher = get_object_or_404(TeacherModel, id=teacher_id)
        student = get_object_or_404(StudntModel, id=student_id)

        teacher.course = course
        teacher.save()

        student.assign_tchr = teacher
        student.save()
        messages.success(request, 'Assign teacher Sucessfully')

        # Redirect to a success page after assigning the course
        return render(request, 'assign_course.html')

    # Redirect back to select_course_page if not a POST request
    return redirect('select_course_page')

# final code  to assign course and teacher and student


def assign_course_teacher_to_student(request):
    if request.method == 'POST':
        course_id = request.POST.get('course_id')
        teacher_id = request.POST.get('teacher_id')
        student_id = request.POST.get('student_id')

        course = get_object_or_404(CourseModel, id=course_id)
        teacher = get_object_or_404(TeacherModel, id=teacher_id)
        student = get_object_or_404(StudntModel, id=student_id)

        teacher.course = course
        teacher.save()

        student.assign_tchr = teacher
        student.course = course  # Assigning the course to the student
        student.save()

        messages.success(request, 'Assign course and teacher successfully')

        # Redirect to a success page after assigning the course and teacher
        return redirect('assign_course_teacher_to_student')

    courses = CourseModel.objects.all()
    teachers = TeacherModel.objects.all()
    students = StudntModel.objects.all()

    context = {
        'courses': courses,
        'teachers': teachers,
        'students': students
    }

    return render(request, 'assign_course_teacher_to_student.html', context)


def get_teachers(request):
    course_id = request.GET.get('course_id')

    # Fetch teachers with their details for the selected course
    teachers = TeacherModel.objects.filter(course_id=course_id)

    # Prepare a list of dictionaries with required details
    teachers_list = [
        {'id': teacher.id, 'username': teacher.teacher.username} for teacher in teachers]

    return JsonResponse({'teachers': teachers_list})


def mark_teacher_attendance(request):
    teachers = TeacherModel.objects.all()

    if request.method == 'POST':
        selected_date_str = request.POST.get('attendance_date')
        selected_date = datetime.strptime(
            selected_date_str, '%Y-%m-%d').date() if selected_date_str else date.today()

        for teacher in teachers:
            present_status = request.POST.get(f"attendance_{teacher.id}")

            if present_status in ['present', 'absent']:
                is_present = present_status == 'present'

                # Update or create attendance for each teacher
                TeacherAttendance.objects.update_or_create(
                    teacher=teacher,
                    date=selected_date,
                    defaults={'is_present': is_present}
                )

    # Get attendance for the selected date
    selected_date_str = request.GET.get('attendance_date')
    selected_date = datetime.strptime(
        selected_date_str, '%Y-%m-%d').date() if selected_date_str else date.today()

    attendance = TeacherAttendance.objects.filter(date=selected_date)
    attendance_dict = {
        attend.teacher_id: attend.is_present for attend in attendance}

    context = {
        'teachers': teachers,
        'attendance_dict': attendance_dict,
        'selected_date': selected_date,
    }
    return render(request, 'mark_teacher_attendance.html', context)


def view_attendance_by_date(request):
    if request.method == 'POST':
        selected_date = request.POST.get('selected_date')

        attendance = TeacherAttendance.objects.filter(date=selected_date)

        context = {
            'selected_date': selected_date,
            'attendance': attendance,
        }

        return render(request, 'view_attendance_by_date.html', context)

    return render(request, 'attendance_date_form.html')


def password_reset_form(request):
    if request.method == 'GET':
        return render(request, 'teacher/password_reset_form.html')

    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        # Check if passwords match
        if new_password == confirm_password:
            # Perform password complexity validation
            if not is_valid_password(new_password):
                messages.error(
                    request, 'Password must contain 8 characters, number, special chracter,uppercase.')
                return redirect('password_reset_form')

            user = request.user
            user.set_password(new_password)
            user.save()
            messages.success(request, 'Password changed successfully.')
            print('password changed')
            return redirect('password_reset_form')
        else:
            messages.error(request, 'Passwords do not match.')
            return redirect('password_reset_form')


def is_valid_password(password):
    # Define password complexity requirements (e.g., minimum length, special characters, numbers)
    # Example: Minimum length of 8 characters, at least one digit, one special character, and one uppercase letter
    if len(password) < 8 or not re.search(r"[A-Z]", password) or not re.search(r"\d", password) or not re.search(r"[!@#$%^&*]", password):
        return False
    return True


def syllabus(request):
    teacher = TeacherModel.objects.get(teacher=request.user)
    # Fetch the first course associated with the teacher, modify if multiple courses are allowed
    course = teacher.course
    context = {
        'teacher': teacher,
        'course': course,
    }

    return render(request, 'teacher/syllabus.html', context)


def mark_student_attendance(request):
    teacher = TeacherModel.objects.get(teacher=request.user)
    students_assigned_to_teacher = StudntModel.objects.filter(
        assign_tchr=teacher)

    if request.method == 'POST':
        selected_date_str = request.POST.get('attendance_date')
        selected_date = datetime.strptime(
            selected_date_str, '%Y-%m-%d').date() if selected_date_str else date.today()

        for student in students_assigned_to_teacher:
            present_status = request.POST.get(f"attendance_{student.id}")

            if present_status in ['present', 'absent']:
                is_present = present_status == 'present'

                # Update or create attendance for each student
                StudentAttendance.objects.update_or_create(
                    student=student,
                    date=selected_date,
                    defaults={'is_present': is_present}
                )

    # Get attendance for the selected date
    selected_date_str = request.GET.get('attendance_date')
    selected_date = datetime.strptime(
        selected_date_str, '%Y-%m-%d').date() if selected_date_str else date.today()

    attendance = StudentAttendance.objects.filter(
        date=selected_date, student__in=students_assigned_to_teacher)
    attendance_dict = {
        attend.student_id: attend.is_present for attend in attendance}

    context = {
        'students': students_assigned_to_teacher,
        'attendance_dict': attendance_dict,
        'selected_date': selected_date,
    }
    return render(request, 'teacher/mark_student_attendance.html', context)


def view_student_attendance_by_date(request):
    if request.method == 'POST':
        selected_date = request.POST.get('selected_date')

        attendance = StudentAttendance.objects.filter(date=selected_date)

        context = {
            'selected_date': selected_date,
            'attendance': attendance,
        }

        return render(request, 'teacher/view_stu_attendance.html', context)

    return render(request, 'teacher/stu_attendance_form.html')


def create_assignment_student(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        due_date = request.POST.get('due_date')

        if title and description and due_date:  # Basic form validation
            try:
                teacher = TeacherModel.objects.get(teacher=request.user)
            except TeacherModel.DoesNotExist:
                # Handle if the user is not a teacher
                # Maybe redirect or display an error message
                pass
            else:
                # If the user is a teacher, proceed with assignment creation
                course = teacher.course  # Assuming 'course' is a field in TeacherModel

                assignment = Assignment.objects.create(
                    course=course,
                    title=title,
                    description=description,
                    due_date=due_date,
                    # Assign other fields here
                    created_by=teacher  # Assuming 'created_by' is a ForeignKey to TeacherModel
                )
        else:
            # Handle invalid form data, maybe return an error or redirect back to the form
            pass

    return render(request, 'teacher/create_assignment.html')

# view the created assignment by teacher


def view_stu_assignments(request):
    try:
        teacher = TeacherModel.objects.get(teacher=request.user)
        assignments = Assignment.objects.filter(created_by=teacher)
    except TeacherModel.DoesNotExist:
        assignments = []  # Assign an empty list if necessary
    context = {
        'assignments': assignments,
    }
    return render(request, 'teacher/view_assignments.html', context)


def view_assignments_student(request):
    if request.method == 'GET':
        # Get the logged-in student
        student = get_object_or_404(StudntModel, student=request.user)
        assignments = Assignment.objects.filter(
            course=student.course, submitted_by=None)

        context = {
            'assignments': assignments
        }
        return render(request, 'students/view_assignments.html', context)

    # For handling assignment submission
    if request.method == 'POST':
        # Assuming assignment ID is submitted along with the form
        assignment_id = request.POST.get('assignment_id')
        assignment = get_object_or_404(Assignment, pk=assignment_id)
        # Assuming the file input field has name 'submitted_file'
        submitted_file = request.FILES['submitted_file']

        student = get_object_or_404(StudntModel, student=request.user)
        if assignment.course == student.course:
            assignment.submitted_file = submitted_file
            assignment.submitted_by = student
            assignment.save()
        return redirect('view_assignments_student')


def submit_assignment(request, assignment_id):
    if request.method == 'POST':
        assignment = get_object_or_404(Assignment, pk=assignment_id)
        student = get_object_or_404(StudntModel, student=request.user)

        # Check if the assignment belongs to the student's course
        if assignment.course == student.course:
            submitted_file = request.FILES.get(
                'submitted_file_' + str(assignment_id))

            if submitted_file:
                assignment.submitted_file = submitted_file
                assignment.submitted_by = student
                assignment.submission_date = datetime.now()
                assignment.save()
                print(submitted_file)
            else:
                # Handle the case where no file was submitted
                pass
        else:
            # Handle assignment not belonging to the student's course
            pass

    return redirect('view_assignments_student')


# teacher view submitted attendance bt stu in teacher profile
def student_assignment_details(request):
    # Get the logged-in teacher
    teacher = get_object_or_404(TeacherModel, teacher=request.user)
    course = teacher.course  # Assuming a single course for each teacher, modify if necessary
    students_in_course = StudntModel.objects.filter(course=course)
    # Get assignments submitted by students in the same course
    student_assignments = Assignment.objects.filter(
        course=course, submitted_by__in=students_in_course)
    context = {
        'teacher': teacher,
        'course': course,
        'students': students_in_course,
        'student_assignments': student_assignments,  # Add this to the context
    }

    return render(request, 'teacher/view_submitted_assigment.html', context)


def password_reset_stu(request):
    if request.method == 'GET':
        return render(request, 'students/password_reset_student.html')

    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password == confirm_password:
            if not is_valid_password(new_password):
                messages.error(
                    request, 'Password must contain 8 characters, number, special chracter,uppercase.')
                return redirect('password_reset_form')

            user = request.user
            user.set_password(new_password)
            user.save()
            messages.success(request, 'Password changed successfully.')
            print('password changed')
            return redirect('password_reset_stu')

        else:
            messages.error(request, 'Passwords do not match.')
            return redirect('password_reset_form')


def syllabus_student(request):
    student = StudntModel.objects.get(student=request.user)
    # Fetch the first course associated with the teacher, modify if multiple courses are allowed
    course = student.course
    context = {
        'student': student,
        'course': course,
    }
    return render(request, 'students/syllabus_stu.html', context)


def view_attendance_student(request):
    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
        logged_in_student = StudntModel.objects.get(student=request.user)
        attendance_details = StudentAttendance.objects.filter(
            student=logged_in_student, date__range=[start_date, end_date])

        context = {
            'attendance_details': attendance_details,
            'start_date': start_date,
            'end_date': end_date,
        }
        return render(request, 'students/attendance_details_stu.html', context)

    return render(request, 'students/attendance_form_stu.html')

# student details


def user_details_stu(request):
    user = request.user
    student = StudntModel.objects.get(student=request.user)
    context = {
        'user': user,
        'student': student,
    }
    return render(request, 'students/stu_usr_details.html', context)


def edit_user_stu_page(request):
    student = StudntModel.objects.get(student=request.user)
    department = DepartmentModel.objects.all()
    context = {
        'student': student,
        'department': department
    }
    return render(request, 'students/edit_user_stu.html', context)


def edit_user_stu(request, pk):
    student = StudntModel.objects.get(id=pk)

    if request.method == 'POST':
        user = student.student  # Access the related User object
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')

        # Update other fields in the StudntModel
        student.Std_address = request.POST.get('address')
        student.std_gender = request.POST.get('gender')
        student.Std_age = request.POST.get('age')
        student.std_phone = request.POST.get('phone')

        select_department_id = request.POST['select']
        student.department = DepartmentModel.objects.get(
            id=select_department_id)

        if request.FILES.get('file'):
            student.std_image = request.FILES['file']

        user.save()  # Save the updated user details
        student.save()  # Save the updated student details
        # Redirect to the students list page
        return redirect('user_details_stu')

    department = DepartmentModel.objects.all()
    return render(request, 'students/edit_user_stu.html', {'stds': student, 'department': department})


def view_stu_attendance_admin(request):
    if request.method == 'GET':
        return render(request, 'students/select_date_range.html')
    elif request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
        students = StudntModel.objects.all()
        attendance_details = StudentAttendance.objects.filter(
            student__in=students, date__range=[start_date, end_date])

        context = {
            'attendance_details': attendance_details,
            'start_date': start_date,
            'end_date': end_date,
        }
        return render(request, 'students/attendance_stu_admin.html', context)

    return render(request, 'students/select_date_range.html')


def logout(request):
    auth.logout(request)
    return redirect(home)


def admin_page(request):
    teacher = TeacherModel.objects.all()
    student = StudntModel.objects.all()
    department = DepartmentModel.objects.all()
    course = CourseModel.objects.all()
    notification = Notification.objects.filter(notification_for='admin')
    teacher_count = teacher.count()
    pending_teachers = TeacherModel.objects.filter(status=False)
    pending_students = StudntModel.objects.filter(status=False)
    student_count = student.count()
    department_count = department.count()
    course_count = course.count()
    notification_count = notification.count()
    pending_teachers_count = pending_teachers.count()
    pending_students_count = pending_students.count()
    context = {
        'teacher': teacher,
        'teacher_count': teacher_count,
        'student': student,
        'student_count': student_count,
        'department': department,
        'department_count': department_count,
        'course': course,
        'course_count': course_count,
        'notification': notification,
        'notification_count': notification_count,
        'pending_teachers': pending_teachers,
        'pending_students': pending_students,
        'pending_teachers_count': pending_teachers_count,
        'pending_students_count': pending_students_count




    }
    return render(request, 'admin_home.html', context)


def teacher_page(request):
    teacher = request.user
    tchr = TeacherModel.objects.get(teacher=teacher)
    notification_tchr = Notification.objects.filter(notification_for='teacher')
    tchr_count = notification_tchr.count()
    print(teacher)
    context = {
        'notification_tchr': notification_tchr,
        'tchr_count': tchr_count,
        'tchr': tchr
    }
    return render(request, 'teacher/teacher_home.html', context)


def student_page(request):
    student = request.user
    stds = StudntModel.objects.get(student=student)
    return render(request, 'students/student_home.html', {'stds': stds})


def teacher_student_deta(request):
    # Assuming the teacher is logged in and you have the teacher's ID
    logged_in_teacher = request.user  # Get the logged-in teacher

    # Retrieve the teacher's assigned students based on their ID
    assigned_students = StudntModel.objects.filter(
        assign_tchr__teacher=logged_in_teacher)
    course = CourseModel.objects.all()
    context = {
        'assigned_students': assigned_students,
        'course': course
    }
    return render(request, 'teacher/teacher_student_details.html', context)

# def render_assign_teacher_page(request):
#     teachers=TeacherModel.objects.all()
#     students = StudntModel.objects.all()
#     courses=CourseModel.objects.all()
#     context={
#         'student':students,
#         'teachers':teachers,
#         'courses':courses
#     }
#     return render(request, 'assign_teacher_course.html',context)


# def assign_teacher_course(request, student_id):
#     student = StudntModel.objects.get(id=student_id)

#     if request.method == 'POST':
#         teacher_id = request.POST.get('teacher_id')
#         course_id = request.POST.get('course_id')

#         teacher = TeacherModel.objects.get(id=teacher_id)
#         course = CourseModel.objects.get(id=course_id)

#         student.assign_tchr = teacher
#         student.course = course
#         student.save()

#         return redirect('admin_page')
#         # return redirect('student_detail_assign', student_id=student.id)  # Redirect to student detail page

#     teachers = TeacherModel.objects.all()
#     courses = CourseModel.objects.all()

#     return render(request, 'assign_teacher_course.html', {'student': student, 'teachers': teachers, 'courses': courses})

# def assign_teacher_course(request, student_id):
#     students = StudntModel.objects.get(id=student_id)

#     if request.method == 'POST':
#         teacher_id = request.POST.get('teacher_id')
#         course_id = request.POST.get('course_id')
#         selected_student_id = request.POST.get('student_id')

#         teacher = TeacherModel.objects.get(id=teacher_id)
#         course = CourseModel.objects.get(id=course_id)
#         selected_student = StudntModel.objects.get(id=selected_student_id)

#         selected_student.assign_tchr = teacher
#         selected_student.course = course
#         selected_student.save()

#         return redirect('admin_page')  # Redirect to a suitable page after assignment

#     teachers = TeacherModel.objects.all()
#     courses = CourseModel.objects.all()
#     students = StudntModel.objects.all()  # Fetch all students for the selection

#     return render(request, 'assign_teacher_course.html', {'students': students, 'teachers': teachers, 'courses': courses, 'students': students})


# def student_detail_assign(request, student_id):
#     student = StudntModel.objects.get(id=student_id)
#     return render(request, 'student_detail_ass.html', {'student': student})
