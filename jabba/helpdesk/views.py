from datetime import datetime

from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.http import Http404, HttpResponseRedirect, HttpResponse, \
                        HttpResponseForbidden


from helpdesk.models import get_team_or_create,  get_context_or_create, Team, \
                            Task, Context
from helpdesk.forms import TeamForm, UserTaskForm, NoteForm, AttachmentForm, \
                           TeamTaskForm, ContextForm, PriorityForm, \
                           TeamChangeForm, ContextChangeForm



@login_required
def index(request):
    if request.user.is_staff:
        return HttpResponseRedirect(reverse('helpdesk_dashboard_staff'))
    else:
        return HttpResponseRedirect(reverse('helpdesk_dashboard_user'))


@login_required
def dashboard_user(request):
    tasks = Task.objects.filter(created_by=request.user)
    open_tasks = tasks.filter(status=1).order_by('-created')
    closed_tasks = tasks.filter(status=4)
    return render_to_response(
        'helpdesk/dashboard_user.html',
        context_instance=RequestContext(
            request,
            {'user_task_form': UserTaskForm(),
             'open_tasks': open_tasks,
             'closed_tasks': closed_tasks,}
            )
        )


@login_required
def dashboard_staff(request):
    if not request.user.is_staff:
        return HttpResponseForbidden()
    teams = Team.objects.exclude(name=get_team_or_create())
    new_tasks = Task.objects.filter(team=get_team_or_create())
    return render_to_response(
        'helpdesk/dashboard_staff.html',
        context_instance=RequestContext(
            request,
            {'new_tasks': new_tasks,
             'teams': teams,}
            )
        )


@login_required
def dashboard_team(request, team_id=0):
    if not request.user.is_staff:
        return HttpResponseForbidden()
    team = get_object_or_404(Team, id=team_id)
    tasks_open = team.tasks.filter(status=1).filter(
        context=get_context_or_create()).order_by('-created')
    tasks_closed = team.tasks.filter(status=4)
    teamtaskform = TeamTaskForm(
        team, initial={'current_team':team.id, 'team':team.id})
    return render_to_response(
        'helpdesk/dashboard_team.html',
        context_instance=RequestContext(
            request,
            {'team': team,
             'tasks_open': tasks_open,
             'tasks_closed': tasks_closed,
             'teamtaskform': teamtaskform,}
            )
        )


@login_required
def task_detail(request, task_id=0):
    if task_id:
        task = get_object_or_404(Task, id=task_id)
        noteform = NoteForm(initial={'task':task_id})
        attachmentform = AttachmentForm(initial={'task':task_id})
        priorityform = PriorityForm(initial={'priority': task.priority, 'task': task_id})
        teamchangeform = TeamChangeForm(initial={'task':task_id, 'team': task.team.id})
        contextchangeform = ContextChangeForm(team=task.team, initial={'task':task_id, 'context': task.context.id})
    return render_to_response(
        'helpdesk/task_detail.html',
        {'task': task,
         'noteform': noteform,
         'attachmentform': attachmentform,
         'priorityform': priorityform,
         'teamchangeform': teamchangeform,
         'contextchangeform': contextchangeform,
        },
        context_instance=RequestContext(request)
        )


@login_required
def task_team_add(request):
    team = get_object_or_404(Team, id=request.POST['team'])
    form = TeamTaskForm(team)
    if not request.user.is_staff:
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = TeamTaskForm(team, request.POST)
        if form.is_valid():
            task = form.save(request.user)
            return HttpResponseRedirect(
                reverse('helpdesk_dashboard_team',
                args=[request.POST['current_team']]))
    return render_to_response(
        'helpdesk/new.html',
        {'form': form,},
        context_instance=RequestContext(request)
        )


@login_required
def task_user_add(request, task_id=0):
    form = UserTaskForm()
    if request.method == 'POST':
        form = UserTaskForm(request.POST)
        if form.is_valid():
            task = form.save(request.user)
            return HttpResponseRedirect(
                reverse('helpdesk_dashboard_user'))
    return render_to_response(
        'helpdesk/new.html',
        {'form': form,},
        context_instance=RequestContext(request)
        )


@login_required
def task_change_team(request, task_id=0, team_id=0):
    if not request.user.is_staff:
        return HttpResponseForbidden()
    if task_id and team_id:
        task = get_object_or_404(Task, id=task_id)
        team = get_object_or_404(Team, id=team_id)
        task.team = team
        task.save()
        return HttpResponse('OK')
    else:
        return Http404


@login_required
def task_detail_change_team(request):
    if not request.user.is_staff:
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = TeamChangeForm(request.POST)
        if form.is_valid:
            task = get_object_or_404(Task, id=request.POST['task'])
            team = get_object_or_404(Team, id=request.POST['team'])
            task.team = team
            task.save()
    return HttpResponseRedirect(
        reverse('helpdesk_task_detail', args=[request.POST['task']])
        )


@login_required
def task_change_priority(request):
    if not request.user.is_staff:
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = PriorityForm(request.POST)
        if form.is_valid:
            task = get_object_or_404(Task, id=request.POST['task'])
            task.priority = request.POST['priority']
            task.save()
    return HttpResponseRedirect(
        reverse('helpdesk_task_detail', args=[request.POST['task']])
        )


@login_required
def task_assign(request, task_id):
    if not request.user.is_staff:
        return HttpResponseForbidden()
    if task_id:
        task = get_object_or_404(Task, id=task_id)
        task.assigned_to = request.user
        task.save()
        return HttpResponseRedirect(reverse('helpdesk_task_detail', args=[task_id]))



@login_required
def task_change_context(request):
    if not request.user.is_staff:
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = ContextForm(request.POST)
        if form.is_valid:
            task = get_object_or_404(Task, id=request.POST['task'])
            task.context = get_object_or_404(Context, id=request.POST['context'])
            task.save()
    return HttpResponseRedirect(
        reverse('helpdesk_task_detail', args=[request.POST['task']])
        )


@login_required
def task_close(request, task_id):
    if not request.user.is_staff:
        return HttpResponseForbidden()
    if task_id:
        task = get_object_or_404(Task, id=task_id)
        task.closed = datetime.now()
        task.closed_by = request.user
        task.status = 4
        task.save()
        return HttpResponseRedirect(reverse('helpdesk_task_detail', args=[task_id]))


@login_required
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
def context(request, context_id=0):
    if not request.user.is_staff:
        return HttpResponseForbidden()
    contexts = Context.objects.all().exclude(name=get_context_or_create)
    form =  ContextForm()
    form_url = reverse('helpdesk_context')
    context = Context()
    if context_id:
        context = get_object_or_404(Context, id=context_id)
        form_url = context.url_context_edit()
        form = ContextForm(instance=context)
    if request.method == 'POST':
        form = ContextForm(request.POST, instance=context)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('helpdesk_context'))
    return render_to_response(
        'helpdesk/context.html',
        {'contexts': contexts,
         'contextform': form,
         'form_url': form_url,
        },
        context_instance=RequestContext(request)
        )


@login_required
def note_add(request):
    form = NoteForm()
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            form.save(request.user)
            return HttpResponseRedirect(
                reverse('helpdesk_task_detail',
                args=[request.POST['task']]))
    return render_to_response(
        'helpdesk/new.html',
        {'form': form,},
        context_instance=RequestContext(request)
        )


@login_required
def attachment_add(request, task_id):
    form = AttachmentForm(initial={'task':task_id})
    if request.method == 'POST':
        form = AttachmentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(request.user)
            return HttpResponseRedirect(
                reverse('helpdesk_task_detail',
                args=[request.POST['task']]))
    return render_to_response(
        'helpdesk/new.html',
        {'form': form,},
        context_instance=RequestContext(request)
        )
