from django.contrib import admin

from users.models import VerificationCodes, CustomUser

admin.site.register(VerificationCodes)
admin.site.register(CustomUser)
