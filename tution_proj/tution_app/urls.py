from django.urls import path
from .import views

urlpatterns = [
    path('', views.home, name='home'),

    path('signup_page', views.signup_page, name='signup_page'),
    path('signup', views.signup, name='signup'),
    path('check_email/', views.check_email, name='check_email'),
    path('signinpage', views.signinpage, name='signinpage'),
    path('signin', views.signin, name='signin'),
    # path('validate-email/', views.validate_email, name='validate_email'),

    path('admin_page', views.admin_page, name='admin_page'),
    path('teacher_page', views.teacher_page, name='teacher_page'),
    path('student_page', views.student_page, name='student_page'),


    path('CoursePage', views.CoursePage, name='CoursePage'),
    path('AddCourse', views.AddCourse, name='AddCourse'),
    path('show_course', views.show_course, name='show_course'),
    path('edit_course_page/<int:pk>/',
         views.edit_course_page, name='edit_course_page'),
    path('edit_course/<int:pk>', views.edit_course, name='edit_course'),
    path('course_delete/<int:pk>', views.course_delete, name='course_delete'),

    path('deptpage', views.deptpage, name='deptpage'),
    path('Add_dept', views.Add_dept, name='Add_dept'),


    path('show_teachers', views.show_teachers, name='show_teachers'),
    path('edit_teacher_page/<int:pk>/',
         views.edit_teacher_page, name='edit_teacher_page'),
    path('edit_teacher/<int:pk>/', views.edit_teacher, name='edit_teacher'),
    path('delete_teacher/<int:pk>/', views.delete_teacher, name='delete_teacher'),

    path('show_students', views.show_students, name='show_students'),
    path('edit_student_page/<int:pk>/',
         views.edit_student_page, name='edit_student_page'),
    path('edit_student/<int:pk>/', views.edit_student, name='edit_student'),
    path('delete_student/<int:pk>/', views.delete_student, name='delete_student'),

    path('admin_notifications', views.admin_notifications,
         name='admin_notifications'),
    path('delete_selected_notifications', views.delete_selected_notifications,
         name='delete_selected_notifications'),

    path('manage_registrations', views.manage_registrations,
         name='manage_registrations'),
    path('approve_teacher/<int:teacher_id>',
         views.approve_teacher, name='approve_teacher'),
    path('approve_student/<int:student_id>',
         views.approve_student, name='approve_student'),
    path('delete_teacher_approve/<int:teacher_id>',
         views.delete_teacher_approve, name='delete_teacher_approve'),
    path('delete_student_approve/<int:student_id>',
         views.delete_student_approve, name='delete_student_approve'),

    path('assign_page_tchr', views.assign_page_tchr, name='assign_page_tchr'),
    path('assign-course/teacher/', views.assign_course_teacher,
         name='assign_course_teacher'),

    path('assign_page_stu', views.assign_page_stu, name='assign_page_stu'),
    path('assign-course/student/', views.assign_course_student,
         name='assign_course_student'),  # temporory stopped for assign teacher

    path('teacher_notifications', views.teacher_notifications,
         name='teacher_notifications'),
    path('delete_teacher_notifications', views.delete_teacher_notifications,
         name='delete_teacher_notifications'),


    # path('all-courses-details/', views.all_courses_details, name='all_courses_details'),
    path('select_course_page', views.select_course_page, name='select_course_page'),
    path('select_course_details_page', views.select_course_details_page,
         name='select_course_details_page'),
    path('assign_course/', views.assign_course, name='assign_course'),
    # path('course-details/', views.assign_course_details, name='assign_course_details'),


    path('mark_teacher_attendance', views.mark_teacher_attendance,
         name='mark_teacher_attendance'),
    path('view_attendance_by_date', views.view_attendance_by_date,
         name='view_attendance_by_date'),

    path('password_reset/', views.password_reset_form, name='password_reset_form'),
    # path('student_course_details',views.teacher_student_course_details, name='teacher_student_course_details'),
    path('syllabus', views.syllabus, name='syllabus'),

    path('mark_student_attendance', views.mark_student_attendance,
         name='mark_student_attendance'),
    path('view_student_attendance_by_date', views.view_student_attendance_by_date,
         name='view_student_attendance_by_date'),

    path('create_assignment_student', views.create_assignment_student,
         name='create_assignment_student'),
    path('view_stu_assignments', views.view_stu_assignments,
         name='view_stu_assignments'),

    # path('view_student_assignments', views.view_student_assignments, name='view_student_assignments'),
    path('view-assignments/', views.view_assignments_student,
         name='view_assignments_student'),
    path('submit-assignment/<int:assignment_id>/',
         views.submit_assignment, name='submit_assignment'),
    # path('teacher/view-submitted-assignments/<int:assignment_id>/', views.view_submitted_assignments, name='view_submitted_assignments'),
    path('teacher/view-student-assignments/',
         views.student_assignment_details, name='student_assignment_details'),

    path('password_reset_stu/', views.password_reset_stu,
         name='password_reset_stu'),
    path('syllabus_student', views.syllabus_student, name='syllabus_student'),

    path('view_student_attendance_student',
         views.view_attendance_student, name='view_attendance_student'),
    # path('edit_user_stu_page', views.edit_user_stu_page, name='edit_user_stu_page'),

    path('user_details_stu', views.user_details_stu, name='user_details_stu'),
    path('edit_user_stu', views.edit_user_stu_page, name='edit_user_stu_page'),
    path('edit_user/<int:pk>/', views.edit_user_stu, name='edit_user_stu'),

    path('view_stu_attendance_admin', views.view_stu_attendance_admin,
         name='view_stu_attendance_admin'),


    # path('assign_teacher_course render', views.render_assign_teacher_page, name='render_assign_teacher_page'),
    # path('assign_teacher_course/<int:student_id>/', views.assign_teacher_course, name='assign_teacher_course'),
    path('teacher_student_details', views.teacher_student_deta,
         name='teacher_student_deta'),
    # path('student/<int:student_id>/', views.student_detail_assign, name='student_detail_assign'),

    path('assign_course_teacher_to_student/', views.assign_course_teacher_to_student,
         name='assign_course_teacher_to_student'),
    path('get_teachers/<int:pk>', views.get_teachers, name='get_teachers'),
    path('logout', views.logout, name='logout'),

]
