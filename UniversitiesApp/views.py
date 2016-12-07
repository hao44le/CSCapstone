"""
UniversitiesApp Views

Created by Jacob Dunbar on 11/5/2016.
"""
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from . import models
from . import forms

def getUniversities(request):
    if request.user.is_authenticated():
        universities_list = models.University.objects.all()
        context = {
            'universities' : universities_list,
        }
        return render(request, 'universities.html', context)
    # render error page if user is not logged in
    return render(request, 'autherror.html')

def getUniversity(request):
    if request.user.is_authenticated():
        in_name = request.GET.get('name', 'None')
        in_university = models.University.objects.get(name__exact=in_name)
        is_member = in_university.members.filter(email__exact=request.user.email)
        is_professor = request.user.is_professor
        is_student = request.user.is_student
        context = {
            'university' : in_university,
            'userIsMember': is_member,
            'is_professor' : is_professor,
            'is_student' : is_student
        }
        return render(request, 'university.html', context)
    # render error page if user is not logged in
    return render(request, 'autherror.html')

def getUniversityForm(request):
    if request.user.is_authenticated():
        form = forms.UniversityForm()
        if request.method == 'POST':
            form = forms.UniversityForm(request.POST, request.FILES)
            if form.is_valid():
                if models.University.objects.filter(name__exact=form.cleaned_data['name']).exists():
                    messages.error(request, 'That university name already exists!')
                    return render(request, 'universityform.html')
                new_university = models.University(name=form.cleaned_data['name'],
                                             photo=request.FILES['photo'],
                                             description=form.cleaned_data['description'],
                                             website=form.cleaned_data['website'])
                new_university.save()
                context = {
                    'name' : form.cleaned_data['name'],
                }
                return render(request, 'universityformsuccess.html', context)
        # else:
        #     return render(request, 'universityform.html', {'error' : 'Error: Photo upload failed!'})
        context = {
            "form": form,
            "page_name" : "Create University",
            "button_value" : "Create"
        }
        return render(request, 'universityform.html',context)
    # render error page if user is not logged in
    return render(request, 'autherror.html')

@login_required
def editUniversity(request):
    in_name = request.GET.get('name', 'None')
    in_university = models.University.objects.get(name__exact=in_name)
    form = forms.UpdateUniversityForm(request.POST,request.FILES, instance=in_university)
    if request.method != 'POST':
        form = forms.UpdateUniversityForm(None,instance=in_university)
    if form.is_valid():
        form.save()
        messages.success(request, 'Success, this University is updated!')

    context = {
        "form" : form,
        "page_name" : "Update University",
        "button_value" : "Update"
    }
    return render(request, 'universityform.html', context)

def joinUniversity(request):
    if request.user.is_authenticated():
        in_name = request.GET.get('name', 'None')
        in_university = models.University.objects.get(name__exact=in_name)
        is_professor = request.user.is_professor
        is_student = request.user.is_student
        in_university.members.add(request.user)
        in_university.save();
        request.user.university_set.add(in_university)
        request.user.save()
        context = {
            'university' : in_university,
            'userIsMember': True,
            'is_professor' : is_professor,
            'is_student' : is_student
        }
        return render(request, 'university.html', context)
    return render(request, 'autherror.html')

def unjoinUniversity(request):
    if request.user.is_authenticated():
        in_name = request.GET.get('name', 'None')
        in_university = models.University.objects.get(name__exact=in_name)
        is_professor = request.user.is_professor
        is_student = request.user.is_student
        in_university.members.remove(request.user)
        in_university.save();
        request.user.university_set.remove(in_university)
        request.user.save()
        context = {
            'university' : in_university,
            'userIsMember': False,
            'is_professor' : is_professor,
            'is_student' : is_student
        }
        return render(request, 'university.html', context)
    return render(request, 'autherror.html')

def deleteUniversity(request):
    if request.user.is_authenticated():
        in_university_name = request.GET.get('name', 'None')
        in_university = models.University.objects.get(name__exact=in_university_name)
        in_university.delete()
        universities_list = models.University.objects.all()
        context = {
            'universities' : universities_list,
        }
        return render(request, 'universities.html', context)
    # render error page if user is not logged in
    return render(request, 'autherror.html')

def getCourse(request):
    if request.user.is_authenticated():
        in_university_name = request.GET.get('name', 'None')
        in_university = models.University.objects.get(name__exact=in_university_name)
        in_course_tag = request.GET.get('course', 'None')
        in_course = in_university.course_set.get(tag__exact=in_course_tag)
        is_member = in_course.members.filter(email__exact=request.user.email)
        is_student = request.user.is_student
        is_professor = request.user.is_professor
        context = {
            'university' : in_university,
            'course' : in_course,
            'userInCourse' : is_member,
            'is_professor' : is_professor,
            'is_student' : is_student
        }
        return render(request, 'course.html', context)
    return render(request, 'autherror.html')

def courseForm(request):
    if request.user.is_authenticated():
        in_university_name = request.GET.get('name', 'None')
        in_university = models.University.objects.get(name__exact=in_university_name)
        form = forms.CourseForm(request.POST or None)
        context = {
            'form' : form,
            'university': in_university,
            'page_name' : 'Create new Course',
            "button_value" : "Create"
        }
        if form.is_valid():
            if in_university.course_set.filter(tag__exact=form.cleaned_data['tag']).exists():
                messages.error(request, 'Error: That course tag already exists at this university!')
                return render(request, 'courseform.html', context)
            new_course = models.Course(tag=form.cleaned_data['tag'],
                                       name=form.cleaned_data['name'],
                                       description=form.cleaned_data['description'],
                                       university=in_university)
            new_course.save()
            in_university.course_set.add(new_course)
            is_member = in_university.members.filter(email__exact=request.user.email)
            is_student = request.user.is_student
            is_professor = request.user.is_professor
            context = {
                'university' : in_university,
                'userIsMember': is_member,
                'is_professor' : is_professor,
                'is_student' : is_student
            }
            return render(request, 'university.html', context)
        # else:
        #     return render(request, 'courseform.html', {'error' : 'Undefined Error!'})
        return render(request, 'courseform.html', context)
    # render error page if user is not logged in
    return render(request, 'autherror.html')

@login_required
def editCourse(request):
    in_university_name = request.GET.get('name', 'None')
    in_university = models.University.objects.get(name__exact=in_university_name)
    in_course_tag = request.GET.get('course', 'None')
    in_course = in_university.course_set.get(tag__exact=in_course_tag)
    form = forms.UpdateCourseForm(request.POST or None, instance=in_course)
    if form.is_valid():
        form.save()
        messages.success(request, 'Success, this Course is updated!')

    context = {
        "form" : form,
        "page_name" : "Update Course",
        "button_value" : "Update"
    }
    return render(request, 'courseform.html', context)

def removeCourse(request):
    if request.user.is_authenticated():
        in_university_name = request.GET.get('name', 'None')
        in_university = models.University.objects.get(name__exact=in_university_name)
        in_course_tag = request.GET.get('course', 'None')
        in_course = in_university.course_set.get(tag__exact=in_course_tag)
        in_course.delete()
        is_member = in_university.members.filter(email__exact=request.user.email)
        is_student = request.user.is_student
        is_professor = request.user.is_professor
        context = {
            'university' : in_university,
            'userIsMember' : is_member,
            'is_professor' : is_professor,
            'is_student' : is_student
        }
        return render(request, 'university.html', context)
    # render error page if user is not logged in
    return render(request, 'autherror.html')

def joinCourse(request):
    if request.user.is_authenticated():
        in_university_name = request.GET.get('name', 'None')
        in_university = models.University.objects.get(name__exact=in_university_name)
        in_course_tag = request.GET.get('course', 'None')
        in_course = in_university.course_set.get(tag__exact=in_course_tag)
        is_student = request.user.is_student
        is_professor = request.user.is_professor
        in_course.members.add(request.user)
        in_course.save();
        request.user.course_set.add(in_course)
        request.user.save()
        context = {
            'university' : in_university,
            'course' : in_course,
            'userInCourse': True,
            'is_professor' : is_professor,
            'is_student' : is_student
        }
        return render(request, 'course.html', context)
    return render(request, 'autherror.html')

def unjoinCourse(request):
    if request.user.is_authenticated():
        test = request.GET.get('email', 'None')        
        in_university_name = request.GET.get('name', 'None')
        user_to_delete = request.GET.get('user', 'None')
        in_university = models.University.objects.get(name__exact=in_university_name)
        in_course_tag = request.GET.get('course', 'None')
        in_course = in_university.course_set.get(tag__exact=in_course_tag)
        is_student = request.user.is_student
        is_professor = request.user.is_professor
        if user_to_delete != 'None':
            to_delete = models.MyUser.objects.get(email__exact=user_to_delete)
            in_course.members.remove(to_delete)
            in_course.save()
            to_delete.course_set.remove(in_course)
            to_delete.save()
            context = {
            'university' : in_university,
            'course' : in_course,
            'userInCourse': True,
            'is_professor' : is_professor,
            'is_student' : is_student
            }
            return render(request, 'course.html', context)
        in_course.members.remove(request.user)
        in_course.save()
        request.user.course_set.remove(in_course)
        request.user.save()
        context = {
            'university' : in_university,
            'course' : in_course,
            'userInCourse': False,
            'is_professor' : is_professor,
            'is_student' : is_student
        }
        return render(request, 'course.html', context)
    return render(request, 'autherror.html')

def addByEmail(request):
    print('hi')
    if request.user.is_authenticated():
        in_university_name = request.GET.get('name', 'None')
        in_university = models.University.objects.get(name__exact=in_university_name)
        in_course_tag = request.GET.get('course', 'None')
        in_course = in_university.course_set.get(tag__exact=in_course_tag)
        is_student = request.user.is_student
        is_professor = request.user.is_professor
        student_email = request.POST.get('email', 'None')
        if student_email != 'None':
            student = models.MyUser.objects.filter(email__exact=student_email)
            if student:
                in_course.members.add(student[0])
                in_course.save();
                student[0].course_set.add(in_course)
                student[0].save()
            else:
                messages.warning(request, 'Invalid email.')
        context = {
            'university' : in_university,
            'course' : in_course,
            'userInCourse': True,
            'is_professor' : is_professor,
            'is_student' : is_student
        }
        return render(request, 'course.html', context)
    return render(request, 'autherror.html')
