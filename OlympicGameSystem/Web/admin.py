from django.contrib import admin
from models import *
class NationalityAdmin(admin.ModelAdmin):
    list_display = ('Country',)
class AthleteAdmin(admin.ModelAdmin):
    list_display = ('nationality','sex','age')
admin.site.register(Nationality)
admin.site.register(Athlete)
admin.site.register(Event)
admin.site.register(Judge)
admin.site.register(Attend)
admin.site.register(AthleteTeam)
admin.site.register(Leader)
admin.site.register(Team)
admin.site.register(PersonHistory)
admin.site.register(CompetitionEvent)
admin.site.register(Competition)
admin.site.register(Province)
admin.site.register(Person)
# Register your models here.
