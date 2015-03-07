from django.contrib import admin
from representME.models import *

# Register your models here.
admin.site.register(Law)
admin.site.register(Topic)
admin.site.register(Party)
admin.site.register(Constituency)
admin.site.register(UserProfile)
admin.site.register(UserVote)
admin.site.register(MSP)
admin.site.register(MSPVote)
admin.site.register(Comment)