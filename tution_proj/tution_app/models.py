from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

# Create your models here.

class DepartmentModel(models.Model):
    dept_name=models.CharField(max_length=200)

class CourseModel(models.Model):
    cs_name = models.CharField(max_length=100)
    cs_duration = models.CharField(max_length=50)
    cs_fee = models.DecimalField(max_digits=10, decimal_places=2)
    cs_syllabus = models.TextField()
    teachers = models.ManyToManyField('tution_app.TeacherModel', blank=True)
    students = models.ManyToManyField('tution_app.StudntModel', blank=True)
    

class TeacherModel(models.Model):
    department=models.ForeignKey(DepartmentModel,on_delete=models.CASCADE,null=True)
    course=models.ForeignKey(CourseModel,on_delete=models.CASCADE,null=True)
    teacher=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    tr_address=models.CharField(max_length=200)
    tr_gender=models.CharField(max_length=200)
    tr_age=models.IntegerField()
    tr_phone=models.CharField(max_length=50)
    tr_image=models.ImageField(upload_to="image/",null=True)
    status = models.BooleanField(default=False)  # Add a status field for teacher approval
    
    

class StudntModel(models.Model):
    department=models.ForeignKey(DepartmentModel,on_delete=models.CASCADE,null=True)
    student=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    Std_address=models.CharField(max_length=200)
    std_gender=models.CharField(max_length=200)
    Std_age=models.IntegerField()
    std_phone=models.IntegerField()
    std_image = models.ImageField(upload_to="image/", null=True)
    status = models.BooleanField(default=False)  # Add a status field for student approval
    assignment_file = models.FileField(upload_to='assignments/', null=True)
    course = models.ForeignKey(CourseModel, on_delete=models.CASCADE, related_name='students_assigned', null=True)
    assign_tchr = models.ForeignKey(TeacherModel, on_delete=models.CASCADE, related_name='students_assigned', null=True)
    
    #department = models.CharField(max_length=50)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    teacher = models.OneToOneField(TeacherModel, on_delete=models.CASCADE, blank=True, null=True)
    student = models.OneToOneField(StudntModel, on_delete=models.CASCADE, blank=True, null=True)


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=50)  # For example, 'New Teacher' or 'New Student'
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    notification_for = models.CharField(max_length=50, default='admin')



class TeacherAttendance(models.Model):
    teacher = models.ForeignKey(TeacherModel, on_delete=models.CASCADE)
    date = models.DateField()
    is_present = models.BooleanField(default=False)

class StudentAttendance(models.Model):
    student = models.ForeignKey(StudntModel, on_delete=models.CASCADE)
    date = models.DateField()
    is_present = models.BooleanField(default=False)


class Assignment(models.Model):
    course = models.ForeignKey(CourseModel, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    due_date = models.DateField()
    created_by = models.ForeignKey(TeacherModel, on_delete=models.CASCADE)
     # New field to store the submitted file
    submitted_file = models.FileField(upload_to='submitted_files/', blank=True, null=True)
    submitted_by = models.ForeignKey(StudntModel, on_delete=models.CASCADE, blank=True, null=True)
    submission_date = models.DateTimeField(blank=True, null=True)




# class Assignment(models.Model):
#     course = models.ForeignKey(CourseModel, on_delete=models.CASCADE)
#     title = models.CharField(max_length=100)
#     description = models.TextField()
#     due_date = models.DateField()

# class AssignmentSubmission(models.Model):
#     assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
#     student = models.ForeignKey(StudntModel, on_delete=models.CASCADE)
#     submission_file = models.FileField(upload_to="assignments/")
#     submitted_at = models.DateTimeField(auto_now_add=True)
