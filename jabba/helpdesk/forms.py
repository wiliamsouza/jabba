from django import forms
from django.utils.translation import ugettext as _

from helpdesk.models import get_team_or_create, get_context_or_create, \
                            Team, Task, Context, Note, Attachment

class LoginForm(forms.Form):
    email = forms.CharField(label=_('Email'))
    password = forms.CharField(label=_('Password'), widget=forms.PasswordInput)


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team


class PriorityForm(forms.Form):
    priority = forms.ChoiceField(label=_('Priority'), choices=Task.PRIORITY_CHOICES)
    task = forms.CharField(widget=forms.HiddenInput())


class TeamChangeForm(forms.Form):
    team = forms.ModelChoiceField(label=_('Team'), queryset=Team.objects.all(), empty_label=None)
    task = forms.CharField(widget=forms.HiddenInput())


class ContextChangeForm(forms.Form):

    def __init__(self, team, *args, **kwargs):
        super(ContextChangeForm, self).__init__(*args, **kwargs)
        self.fields["context"].queryset = team.contexts.all()

    context = forms.ModelChoiceField(label=_('Context'), queryset=Context.objects.none(), empty_label=None)
    task = forms.CharField(widget=forms.HiddenInput())


class ContextForm(forms.ModelForm):
    class Meta:
        model = Context


class TeamTaskForm(forms.ModelForm):

    def __init__(self, team, *args, **kwargs):
        super(TeamTaskForm, self).__init__(*args, **kwargs)
        self.fields["context"].queryset = Context.objects.filter(
            team__in=[team.id, get_context_or_create().id])

    description = forms.CharField(label=_('Description'), widget=forms.Textarea(attrs={'cols':'24', 'rows':'6'}))
    current_team = forms.CharField(widget=forms.HiddenInput())
    assign_to_me = forms.CharField(label=_('Assign to me'), required=False, widget=forms.CheckboxInput())
    context = forms.ModelChoiceField(label=_('Context'), queryset=Context.objects.none(), empty_label=None)

    def save(self, user):
        task = Task()
        task.description = self.cleaned_data['description'].capitalize()
        task.context = Context.objects.get(id=self.cleaned_data['context'].id)
        task.team = Team.objects.get(id=self.cleaned_data['team'].id)
        task.priority = self.cleaned_data['priority']
        task.due_date = self.cleaned_data['due']
        task.show_from = self.cleaned_data['show_from']
        task.created_by = user
        if self.cleaned_data['assign_to_me'] == 'on':
            task.assigned_to = user
        task.save()
        return task

    class Meta:
        model = Task
        fields = ['description', 'context', 'team', 'priority', 'due', 'show_from', 'assign_to_me', 'current_team']
        exclude = ['created_by', 'modified_by', 'closed', 'closed_by', 'status', 'estimated_hours', 'attachments']


class UserTaskForm(forms.Form):
    description = forms.CharField(label=_('Description'), widget=forms.Textarea(attrs={'cols':'24', 'rows':'6'}))

    def save(self, user):
        task = Task()
        task.description = self.cleaned_data['description'].capitalize()
        task.created_by = user
        task.save()
        task.save()
        return task


class NoteForm(forms.Form):
    description = forms.CharField(label=_('Description'), widget=forms.Textarea(attrs={'cols':'24', 'rows':'6'}))
    task = forms.CharField(widget=forms.HiddenInput())

    def save(self, user):
        note = Note()
        note.created_by = user
        note.description = self.cleaned_data['description'].capitalize()
        note.task = Task.objects.get(id=int(self.cleaned_data['task']))
        note.save()
        return note


class AttachmentForm(forms.Form):
    attachment = forms.FileField(label=_('Attachment'))
    task = forms.CharField(widget=forms.HiddenInput())
    
    def save(self, user):
        task = Task.objects.get(id=int(self.cleaned_data['task']))
        if self.cleaned_data['attachment']:
            import mimetypes
            file = self.cleaned_data['attachment']
            filename = file.name.replace(' ', '_')
            a = Attachment(
                filename=filename,
                mime_type=mimetypes.guess_type(filename)[0] or 'application/octet-stream',
                size=file.size,
                )
            a.file.save(file.name, file, save=False)
            a.save()
            task.attachments.add(a)
        task.save()
        return None
