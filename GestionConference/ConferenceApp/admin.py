from django.contrib import admin ,messages
from .models import *
from django.utils.html import format_html
from django.utils.text import Truncator
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
class SubmissionAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "status",
        "user",
        "conference",
        "submission_date",
        "payed",
        "short_abstract",  # c) afficher la méthode
    )
    list_display_links = ("title",)

    list_filter = (
        "status",
        "payed",
        "conference",
        ("submission_date", admin.DateFieldListFilter),
    )

    search_fields = ("title", "keywords", "user__username")

    list_editable = ("status", "payed")

    ordering = ("-submission_date",)
    date_hierarchy = "submission_date"
    list_per_page = 25
    list_select_related = ("user", "conference")  # perf

    fieldsets = (
        ("Infos générales", {
            "fields": ("submission_id", "title", "abstract", "keywords")
        }),
        ("Fichier et conférence", {
            "fields": ("paper", "conference")
        }),
        ("Suivi", {
            "fields": ("status", "payed", "submission_date", "user")
        }),
    )

    readonly_fields = ("submission_id", "submission_date")

    def short_abstract(self, obj):
        if not obj.abstract:
            return "—"
        return Truncator(obj.abstract).chars(50)
    short_abstract.short_description = "Abstract (50)"
    short_abstract.admin_order_field = "abstract"

    actions = ["mark_as_payed", "accept_submissions"]

    def mark_as_payed(self, request, queryset):
        updated = queryset.update(payed=True)
        self.message_user(
            request,
            f"{updated} soumission(s) marquée(s) comme payée(s).",
            messages.SUCCESS,
        )
    mark_as_payed.short_description = "Marquer comme payées"

    def accept_submissions(self, request, queryset):
       
        new_status = getattr(Submission, "STATUS_ACCEPTED", "accepted")
        updated = queryset.update(status=new_status)
        self.message_user(
            request,
            f"{updated} soumission(s) acceptée(s).",
            messages.SUCCESS,
        )
    accept_submissions.short_description = "Accepter les soumissions sélectionnées"