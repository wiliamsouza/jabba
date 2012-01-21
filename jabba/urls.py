import settings
from django.conf.urls.defaults import *
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required


from helpdesk.views import dashboard_user, dashboard_staff, dashboard_team, \
                           task_user_add, task_detail, team, note_add, \
                           attachment_add, task_team_add, task_change_team, \
                           context, task_change_priority, task_close, \
                           task_detail_change_team, task_assign, \
                           task_change_context, index


from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^accounts/', include('registration.urls')),
    url(r'^$', index, name='home'),
    url(r'^dashboard/user/$', dashboard_user, name='helpdesk_dashboard_user'),
    url(r'^dashboard/staff/$', dashboard_staff, name='helpdesk_dashboard_staff'),
    url(r'^dashboard/team/(?P<team_id>\d+)/$', dashboard_team, name='helpdesk_dashboard_team'),
    url(r'^task/team/add/$', task_team_add, name='helpdesk_task_team_add'),
    url(r'^task/user/add/$', task_user_add, name='helpdesk_task_user_add'),
    url(r'^task/(?P<task_id>\d+)/detail/$', task_detail, name='helpdesk_task_detail'),
    url(r'^task/(?P<task_id>\d+)/change/team/(?P<team_id>\d+)/$', task_change_team, name='helpdesk_task_change_team'),
    url(r'^task/change/team/$', task_detail_change_team, name='helpdesk_task_detail_change_team'),
    url(r'^task/change/priority/$', task_change_priority, name='helpdesk_task_change_priority'),
    url(r'^task/change/context/$', task_change_context, name='helpdesk_task_change_context'),
    url(r'^task/(?P<task_id>\d+)/attachment/add/$', attachment_add, name='helpdesk_task_attachment_add'),
    url(r'^task/(?P<task_id>\d+)/assign/$', task_assign, name='helpdesk_task_assign'),
    url(r'^task/(?P<task_id>\d+)/close/$', task_close, name='helpdesk_task_close'),
    url(r'^team/$', team, name='helpdesk_team'),
    url(r'^team/(?P<team_id>\d+)/edit/$', team, name='helpdesk_team_edit'),
    url(r'^context/$', context, name='helpdesk_context'),
    url(r'^context/(?P<context_id>\d+)/edit/$', context, name='helpdesk_context_edit'),
    url(r'^note/add/$', note_add, name='helpdesk_note_add'),
)


if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$',
         'django.views.static.serve',
         {'document_root': '/home/wiliam/devel/jabba/jabba/static'}),
    )
