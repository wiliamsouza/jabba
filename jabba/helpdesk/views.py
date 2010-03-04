from django.template import RequestContext
from django.core.urlresolvers import reverse
#from django.forms.models import ModelChoiceField
from django.utils.translation import ugettext as _
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.http import Http404, HttpResponseRedirect, HttpResponse, \
                        HttpResponseForbidden


from helpdesk.models import get_team_or_create,  get_context_or_create, Team, Task
from helpdesk.forms import TeamForm, UserTaskForm, NoteForm


@login_required
def dashboard_user(request):
    tasks = Task.objects.filter(created_by=request.user)
    open_tasks = tasks.filter(status=1).order_by('-created')
    closed_tasks = tasks.filter(status=4)
    return render_to_response(
        'helpdesk/dashboard_user.html',
        {'user_task_form': UserTaskForm(),
         'open_tasks': open_tasks,
         'closed_tasks': closed_tasks,
        },
        context_instance=RequestContext(request)
        )


@login_required
def dashboard_staff(request):
    if not request.user.is_staff:
        return HttpResponseForbidden()
    teams = Team.objects.exclude(name=get_team_or_create())
    new_tasks = Task.objects.filter(team=get_team_or_create())
    return render_to_response(
        'helpdesk/dashboard_staff.html',
        {'new_tasks': new_tasks,
         'teams': teams,
        },
        context_instance=RequestContext(request)
        )



@login_required
#@csrf_protect
def task_detail(request, task_id=0):
    if task_id:
        task = get_object_or_404(Task, id=task_id)
        noteform = NoteForm(initial={'task':task_id})
    return render_to_response(
        'helpdesk/task_detail.html',
        {'task': task,
         'noteform': noteform,
        },
        context_instance=RequestContext(request)
        )


@login_required
#@csrf_protect
def task_user_add(request, task_id=0):
    form = UserTaskForm()
    if task_id:
        task = get_object_or_404(Task, id=task_id)
        form = UserTaskForm(instance=task)
    if request.method == 'POST':
        form = UserTaskForm(request.POST, request.FILES)
        if form.is_valid():
            task = form.save(request.user)
            return HttpResponseRedirect(reverse('helpdesk_dashboard_user'))
    return render_to_response(
        'helpdesk/new.html',
        {'form': form,},
        context_instance=RequestContext(request)
        )


@login_required
#@csrf_protect
def team(request, team_id=0):
    if not request.user.is_staff:
        return HttpResponseForbidden()
    teams = Team.objects.all().exclude(name=get_team_or_create)
    form =  TeamForm()
    form_url = reverse('helpdesk_team')
    team = Team()
    if team_id:
        team = get_object_or_404(Team, id=team_id)
        form_url = team.url_team_edit()
        form = TeamForm(instance=team)
    if request.method == 'POST':
        form = TeamForm(request.POST, instance=team)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('helpdesk_team'))
    return render_to_response(
        'helpdesk/team.html',
        {'teams': teams,
         'teamform': form,
         'form_url': form_url,
        },
        context_instance=RequestContext(request)
        )


@login_required
def note_add(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            #print form.cleaned_data['task']
            form.save(request.user)
    return HttpResponseRedirect(
        reverse('helpdesk_task_detail',
        args=[request.POST['task']])
        )

