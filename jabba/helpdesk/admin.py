from django.contrib import admin

from helpdesk.models import Team, Task, Context, Note, Attachment


admin.site.register(Team)
admin.site.register(Task)
admin.site.register(Context)
admin.site.register(Note)
admin.site.register(Attachment)
