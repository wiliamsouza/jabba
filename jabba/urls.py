import settings
from django.conf.urls.defaults import *
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required


from helpdesk.views import dashboard_user, dashboard_staff, task_user_add, task_detail, team, note_add, attachment_add


from django.contrib import admin
admin.autodiscover()


@login_required
def index(request):
    if request.user.is_staff:
        return HttpResponseRedirect(reverse('helpdesk_dashboard_staff'))
    else:
        return HttpResponseRedirect(reverse('helpdesk_dashboard_user'))


urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^accounts/', include('registration.backends.default.urls')),
#    (r'^helpdesk/', include('helpdesk.urls')),
    url(r'^$', index, name='home'),
    url(r'^dashboard/user/$', dashboard_user, name='helpdesk_dashboard_user'),
    url(r'^dashboard/staff/$', dashboard_staff, name='helpdesk_dashboard_staff'),
    url(r'^task/add/user/$', task_user_add, name='helpdesk_task_user_add'),
    url(r'^task/(?P<task_id>\d+)/$', task_detail, name='helpdesk_task_detail'),
    url(r'^team/$', team, name='helpdesk_team'),
    url(r'^team/(?P<team_id>\d+)/$', team, name='helpdesk_team_edit'),
    url(r'^note/add/$', note_add, name='helpdesk_note_add'),
    url(r'^attachment/add/$', attachment_add, name='helpdesk_attachment_add'),
)


if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$',
         'django.views.static.serve',
         {'document_root': '/home/waa/dev/jabba/jabba/static'}),
    )
