"""GroupsApp URL

Created by Naman Patwari on 10/10/2016.
"""
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^group/all$', views.getGroups, name='Groups'),
    url(r'^group/form$', views.getGroupForm, name='GroupForm'),
    url(r'^group/edit$', views.getEditGroup, name='EditProject'),
    url(r'^group/delete$', views.deleteGroup, name='deleteProject'),
    url(r'^group/join$', views.joinGroup, name='GJoin'),
    url(r'^group/unjoin$', views.unjoinGroup, name='GUnjoin'),
    url(r'^group$', views.getGroup, name='Group'),
    url(r'^group/addmember$', views.addMember, name='AddMember'),
]
