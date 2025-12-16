from django.contrib import admin

from communities.models import Communities, CommunityAdmin

admin.site.register(Communities)
admin.site.register(CommunityAdmin)
