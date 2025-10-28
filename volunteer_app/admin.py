from django.contrib import admin
from .models import Opportunity, Application,Skill
# Register your models here.

admin.site.register(Opportunity)
admin.site.register(Application)
admin.site.register(Skill)