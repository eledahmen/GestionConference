from django.contrib import admin
from .models import Session
# Register your models here.

#admin.site.register(Session)
admin.site.site_header="Session Management admin 25/26"
admin.site.site_title="Session dashboard"
admin.site.index_title="Session management"
    
@admin.register(Session)
class Adminses(admin.ModelAdmin):
    list_display=("title","topic","session_day","start_time")
    ordering =("session_day",)
    list_filter=("topic","session_day")
    search_fields =("title",)
    

        
        
    