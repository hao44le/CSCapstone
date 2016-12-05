"""GroupsApp Views
Created by Naman Patwari on 10/10/2016.
"""
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from . import models
from . import forms

from CommentsApp.models import Comment


def getGroups(request):
    if request.user.is_authenticated():
        groups_list = models.Group.objects.all()
        context = {
            'groups': groups_list,
        }
        return render(request, 'groups.html', context)
    # render error page if user is not logged in
    return render(request, 'autherror.html')


def getGroup(request):
    if request.user.is_authenticated():
        in_name = request.GET.get('name', 'None')
        in_group = models.Group.objects.get(name__exact=in_name)
        is_member = in_group.members.filter(email__exact=request.user.email)
        is_student = request.user.is_student
        comments_list = Comment.objects.all()
        projects = in_group.project.all()
        context = {
            'group': in_group,
            'userIsMember': is_member,
            'comments' : comments_list,
            'is_student': is_student,
            'projects' : projects
        }
        return render(request, 'group.html', context)
    # render error page if user is not logged in
    return render(request, 'autherror.html')


def getGroupForm(request):
    if request.user.is_authenticated():
        form = forms.GroupForm(request.POST or None)
        if form.is_valid():
            if models.Group.objects.filter(name__exact=form.cleaned_data['name']).exists():
                return render(request, 'groupform.html', {'error': 'Error: That Group name already exists!'})
            new_group = models.Group(
            name=form.cleaned_data['name'], description=form.cleaned_data['description'])
            new_group.save()
            context = {
                'name': form.cleaned_data['name'],
            }
            return render(request, 'groupformsuccess.html', context)
        context = {
            "form": form,
            "page_name": "Create Group",
            "button_value": "Create"
        }
        return render(request, 'groupform.html', context)
    # render error page if user is not logged in
    return render(request, 'autherror.html')


@login_required
def getEditGroup(request):
    in_name = request.GET.get('name', 'None')
    in_group = models.Group.objects.get(name__exact=in_name)
    form = forms.UpdateForm(request.POST or None, instance=in_group)
    if form.is_valid():
        form.save()
        messages.success(request, 'Success, this group is updated!')

    context = {
        "form": form,
        "page_name": "Update Group",
        "button_value": "Update"
    }
    return render(request, 'groupform.html', context)


def joinGroup(request):
    if request.user.is_authenticated():
        in_name = request.GET.get('name', 'None')
        in_group = models.Group.objects.get(name__exact=in_name)
        is_student = request.user.is_student
        in_group.members.add(request.user)
        in_group.save()
        request.user.group_set.add(in_group)
        request.user.save()
        projects = in_group.project.all()
        context = {
            'group': in_group,
            'userIsMember': True,
            'is_student': is_student,
            'projects' : projects
        }
        return render(request, 'group.html', context)
    return render(request, 'autherror.html')


def unjoinGroup(request):
    if request.user.is_authenticated():
        in_name = request.GET.get('name', 'None')
        in_group = models.Group.objects.get(name__exact=in_name)
        is_student = request.user.is_student
        in_group.members.remove(request.user)
        in_group.save()
        request.user.group_set.remove(in_group)
        request.user.save()
        projects = in_group.project.all()
        context = {
            'group': in_group,
            'userIsMember': False,
            'is_student': is_student,
            'projects' : projects
        }
        return render(request, 'group.html', context)
    return render(request, 'autherror.html')


def deleteGroup(request):
    if request.user.is_authenticated():
        in_name = request.GET.get('name', 'None')
        in_group = models.Group.objects.get(name__exact=in_name)
        in_group.delete()
        groups_list = models.Group.objects.all()
        context = {
            'groups': groups_list,
        }
        return render(request, 'groups.html', context)
    # render error page if user is not logged in
    return render(request, 'autherror.html')

def addMember(request):
    if request.user.is_authenticated():
        in_name = request.GET.get('name', 'None')
        in_group = models.Group.objects.get(name__exact=in_name)
        is_student = request.user.is_student
        projects = in_group.project.all()
        student_email = request.POST.get('email', 'None')
        if student_email != 'None':
            student = models.MyUser.objects.filter(email__exact=student_email)
            if student:
                in_group.members.add(student[0])
                in_group.save();
                student[0].group_set.add(in_group)
                student[0].save()
        context = {
            'group': in_group,
            'userIsMember': True,
            'is_student': is_student,
            'projects' : projects
        }
        return render(request, 'group.html', context)
    return render(request, 'autherror.html')
