from django.contrib import admin
from models import CinemaClub, CinemaClubEvent

class CinemaClubAdmin(admin.ModelAdmin):
    pass
admin.site.register(CinemaClub, CinemaClubAdmin)

class CinemaClubEventAdmin(admin.ModelAdmin):
    pass
admin.site.register(CinemaClubEvent, CinemaClubEventAdmin)

