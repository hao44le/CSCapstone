"""CSCapstone Views

Created by Harris Christiansen on 9/18/16.
"""

from __future__ import print_function
import re
from django.shortcuts import render
from ProjectsApp.models import Project
from ProjectsApp.models import Bookmarks
from GroupsApp.models import Group
from UniversitiesApp.models import University
from UniversitiesApp.models import Course
from CompaniesApp.models import Company
from django.db.models import Q

def getIndex(request):
    projects_list = Project.objects.all()
    bookmarks_list = Bookmarks.objects.all()
    groups_list = Group.objects.all()
    universities_list = University.objects.all()
    companies_list = Company.objects.all()
    bookmarks = []
    for bookmark in bookmarks_list:
        if request.user == bookmark.user:
            bookmarks.append(bookmark.project)

    context = {
        'projects' : projects_list,
        'groups' : groups_list,
        'universities' : universities_list,
        'companies' : companies_list,
        'bookmarks' : bookmarks
    }
    return render(request, 'index.html', context)

def getTable(request):
    return render(request, 'table.html')

def getForm(request):
    return render(request, 'form.html')

def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    ''' Splits the query string in invidual keywords, getting rid of unecessary spaces
        and grouping quoted words together.
        Example:

        >>> normalize_query('  some random  words "with   quotes  " and   spaces')
        ['some', 'random', 'words', 'with quotes', 'and', 'spaces']

    '''
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]

def get_query(query_string, search_fields):
    ''' Returns a query, that is a combination of Q objects. That combination
        aims to search keywords within a model by testing the given search fields.

    '''
    query = None # Query to search for every search term
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query | or_query
    return query

def search(request):
    query_string = ''
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']

        company_entry_query = get_query(query_string, ['name', 'description','website'])
        company_found_entries = Company.objects.filter(company_entry_query).order_by('-id')

        group_entry_query = get_query(query_string, ['name', 'description'])
        group_found_entries = Group.objects.filter(group_entry_query).order_by('-id')

        project_entry_query = get_query(query_string, ['name', 'description','programmingLanguage','yearsOfExperience','speciality'])
        project_found_entries = Project.objects.filter(project_entry_query).order_by('-updated_at')

        university_found_entries = University.objects.filter(company_entry_query).order_by('-id')

        course_entry_query = get_query(query_string, ['name', 'description','tag'])
        course_found_entries = Course.objects.filter(course_entry_query).order_by('-id')

    context = {
        'query_string' : query_string,
        'company_found_entries' : company_found_entries,
        'group_found_entries' : group_found_entries,
        'project_found_entries' : project_found_entries,
        'university_found_entries' : university_found_entries,
        'course_found_entries' : course_found_entries
    }
    return render(request,'searchresults.html',context)
