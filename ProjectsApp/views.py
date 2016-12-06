"""ProjectsApp Views

Created by Harris Christiansen on 10/02/16.
"""
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from . import models
from . import forms
import datetime
from CommentsApp.models import Comment
from GroupsApp.models import Group

def getProjects(request):
    projects_list = models.Project.objects.all()
    return render(request, 'projects.html', {
        'projects': projects_list,
    })
@login_required
def getProject(request):
    in_name = request.GET.get('name', 'None')
    in_project = models.Project.objects.get(name__exact=in_name)
    is_member = in_project.createdBy.filter(email__exact=request.user.email)
    is_engineer = request.user.is_engineer
    has_bookmarked = models.Bookmarks.objects.filter(project__exact=in_project,user__exact=request.user)
    comments_list = Comment.objects.all()
    groups_list = Group.objects.all()
    assigned_groups = in_project.project_groups.all()
    context = {
        'project' : in_project,
        'userIsMember': is_member,
        'is_engineer' : is_engineer,
        'comments' : comments_list,
        'has_bookmarked' : has_bookmarked,
        'groups_list' : groups_list,
        'assigned_groups' : assigned_groups
    }
    if request.method == 'POST':
        group_names = request.POST.getlist('dropdownl','None')
        if group_names != 'None':
            for group_name in group_names:
                group = Group.objects.get(name__exact=group_name)
                group.project.add(in_project)
                print group.project
                group.save()
        else:
            messages.error(request, 'Please select at lease one group!')

    return render(request, 'project.html',context)

@login_required
def bookmarkProject(request):
    in_name = request.GET.get('name', 'None')
    in_project = models.Project.objects.get(name__exact=in_name)
    has_bookmarked = models.Bookmarks.objects.filter(project__exact=in_project,user__exact=request.user)
    is_member = in_project.createdBy.filter(email__exact=request.user.email)
    is_engineer = request.user.is_engineer
    comments_list = Comment.objects.all()
    groups_list = Group.objects.all()
    assigned_groups = in_project.project_groups.all()
    context = {
        'project' : in_project,
        'userIsMember': is_member,
        'is_engineer' : is_engineer,
        'comments' : comments_list,
        'groups_list' : groups_list,
        'assigned_groups' : assigned_groups
    }
    if has_bookmarked:
        bookmark = models.Bookmarks.objects.get(user__exact=request.user,project__exact=in_project)
        bookmark.delete()
        messages.success(request, 'Unbookmarked! you have successfully unbookmarked this project!')
        context['has_bookmarked'] = False
    else:
        bookmark = models.Bookmarks(user=request.user,project=in_project)
        bookmark.save()
        messages.success(request, 'Bookmarked! you have successfully bookmarked this project!')
        context['has_bookmarked'] = True

    return render(request, 'project.html',context)


def deleteProject(request):
    in_name = request.GET.get('name', 'None')
    in_project = models.Project.objects.get(name__exact=in_name)
    in_project.delete()
    projects_list = models.Project.objects.all()
    return render(request, 'projects.html', {
        'projects': projects_list,
    })

def getProjectForm(request):
    if request.user.is_authenticated():
            form = forms.ProjectForm(request.POST or None)
            if form.is_valid():
                if models.Project.objects.filter(name__exact=form.cleaned_data['name']).exists():
                    return render(request, 'projectform.html', {'error' : 'Error: That Project name already exists!'})
                new_project = models.Project(name=form.cleaned_data['name'], description=form.cleaned_data['description'],programmingLanguage=form.cleaned_data['programmingLanguage'],yearsOfExperience=form.cleaned_data['yearsOfExperience'],speciality=form.cleaned_data['speciality'])
                new_project.created_at = datetime.datetime.now()
                new_project.updated_at = datetime.datetime.now()

                new_project.save()
                new_project.createdBy.add(request.user)
                # request.user.projects_set.add(new_project)
                new_project.save()
                request.user.save()
                context = {
                    'name' : form.cleaned_data['name'],
                }
                return render(request, 'projectformsuccess.html', context)
            context = {
                "form": form,
                "page_name" : "Create Project",
                "button_value" : "Create"
            }
            return render(request,'projectform.html',context)
    return render(request,'autherror.html')

@login_required
def editProject(request):
    in_name = request.GET.get('name', 'None')
    in_project = models.Project.objects.get(name__exact=in_name)
    form = forms.UpdateForm(request.POST or None, instance=in_project)
    if form.is_valid():
        form.save()
        messages.success(request, 'Success, this project is updated!')

    context = {
        "form" : form,
        "page_name" : "Update Project",
        "button_value" : "Update"
    }
    return render(request, 'projectform.html', context)
