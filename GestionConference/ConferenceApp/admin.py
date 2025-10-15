from django.contrib import admin
from .models import *
# Register your models here.

admin.site.site_header="Conference Management admin 25/26"
admin.site.site_title="Conference dashboard"
admin.site.index_title="Conference management"
#admin.site.register(Conference)
#admin.site.register(Submission)
class SubmissionInline(admin.StackedInline):

    model=Submission
    extra=1
    readonly_fields =("submission_id",)
    
@admin.register(Conference)
class Adminper(admin.ModelAdmin):
    list_display=("name","theme","location","start_date","end_date","duration")
    ordering =("start_date",)
    list_filter=("theme","location","start_date")
    search_fields =("name",)
    fieldsets =(
        ("Info General ",{
            "fields":("conference_id","name","description")
        }),
        ("Logistique",{
            "fields":("location", "start_date","end_date")
        })
        
    )
    readonly_fields =("conference_id",)
    date_hierarchy ="start_date"
    inlines =[SubmissionInline]
    def duration(self,objet):
        if objet.start_date and objet.end_date:
            return (objet.end_date - objet.start_date).days
        return "RAS"
    duration.short_description="Duration (days)"

    
@admin.register(Submission)
class Adminsub(admin.ModelAdmin):
    list_display=("title","status","submission_date")
    ordering =("submission_date",)
    list_filter=("submission_date","status")
    search_fields =("title",)