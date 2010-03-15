from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext
from django.utils.translation import ugettext_lazy as _


class TaskManager(models.Manager):
    use_for_related_fields = True

    def open(self):
        return self.get_query_set().exclude(status=4)


def get_team_or_create():
    team, created = Team.objects.get_or_create(name=ugettext('Main'))
    return team


def get_context_or_create():
    context, created =  Context.objects.get_or_create(name=ugettext('Inbox'))
    return context


class Team(models.Model):
    name = models.CharField(_('Name'), max_length=128)

    def url_dashboard_team(self):
        return ('helpdesk_dashboard_team', [str(self.id)])
    url_dashboard_team = models.permalink(url_dashboard_team)

    def url_team_edit(self):
        return ('helpdesk_team_edit', [str(self.id)])
    url_team_edit = models.permalink(url_team_edit)

    def __unicode__(self):
        return self.name


class Task(models.Model):

    STATUS_CHOICES = (
        (1, _('Open')),
        (2, _('Reopened')),
        (4, _('Closed')),
    )

    PRIORITY_CHOICES = (
        (1, _('Critical')),
        (2, _('High')),
        (3, _('Normal')),
        (4, _('Low')),
    )

    description = models.TextField(_('Description'), blank=True, null=True,)
    context = models.ForeignKey('Context', verbose_name=_('Context'), default=get_context_or_create, related_name='tasks')
    created = models.DateTimeField(_('Created'), auto_now_add=True)
    created_by = models.ForeignKey(User, verbose_name=_('Created by'), related_name='tasks_created')
    closed = models.DateTimeField(_('Closed'), blank=True, null=True)
    closed_by = models.ForeignKey(User, verbose_name=_('Closed by'), related_name='tasks_closed', blank=True, null=True)
    due = models.DateTimeField(_('Due date'), blank=True, null=True)
    show_from = models.DateTimeField(_('Show from'), blank=True, null=True)
    team = models.ForeignKey('Team', verbose_name=_('Team'), related_name='tasks', default=get_team_or_create)
    attachments = models.ManyToManyField('Attachment', verbose_name=_('Attachments'), blank=True, null=True)
    status = models.IntegerField(_('Status'), choices=STATUS_CHOICES, default=1)
    priority = models.IntegerField(_('Priority'), choices=PRIORITY_CHOICES, default=3, blank=3)
    assigned_to = models.ForeignKey(User, verbose_name=_('Assigned to'), related_name='tasks_assigned', blank=True, null=True)

    objects = TaskManager()

    def __unicode__(self):
        return self.description


class Context(models.Model):
    name = models.CharField(_('Name'), max_length=64)
    team = models.ForeignKey('Team', verbose_name=_('Team'), default=get_team_or_create, related_name='contexts')

    def url_context_edit(self):
        return ('helpdesk_context_edit', [str(self.id)])
    url_context_edit = models.permalink(url_context_edit)

    def __unicode__(self):
        return self.name


class Note(models.Model):
    created_by = models.ForeignKey(User, verbose_name=_('Created by'), related_name='notes_created')
    created_date = models.DateTimeField(_('Open date'), auto_now_add=True)
    description = models.TextField(_('Description'))
    task = models.ForeignKey('Task', verbose_name=_('Task'), related_name='notes')

    def __unicode__(self):
        return self.description


class Attachment(models.Model):
    file = models.FileField(_('File'), upload_to='attachment')
    filename = models.CharField(_('Filename'), max_length=128)
    mime_type = models.CharField(_('MIME Type'), max_length=32)
    size = models.IntegerField(_('Size'))

    def __unicode__(self):
        return self.filename
