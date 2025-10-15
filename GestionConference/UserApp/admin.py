from django.contrib import admin
from .models import User,OrganizingCommitee
# Register your models here.
# admin.site.register(User)
#admin.site.register(OrganizingCommitee)
@admin.register(OrganizingCommitee)
class Adminor(admin.ModelAdmin):
    list_display=("commitee_role","date_join","created_at")
    ordering =("date_join",)
    list_filter=("commitee_role",)
    search_fields =("commitee_role",)



@admin.register(User)
class Adminuse(admin.ModelAdmin):
    list_display=("first_name","last_name","created_at")
    ordering =("created_at",)
    list_filter=("role",)
    search_fields =("first_name","last_name",)
