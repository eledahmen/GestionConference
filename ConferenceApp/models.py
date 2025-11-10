# ConferenceApp/models.py

from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.utils import timezone


class Conference(models.Model):
    conference_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    THEME_CHOICES = [
        ("cs_ai", "Computer Science & Artificial Intelligence"),
        ("sci_eng", "Science & Engineering"),
        ("social_edu", "Social Sciences & Education"),
        ("interdisciplinary", "Interdisciplinary Themes"),
    ]
    theme = models.CharField(max_length=50, choices=THEME_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.start_date and self.end_date and self.start_date > self.end_date:
            raise ValidationError("La date de début doit être antérieure à la date de fin.")

    def __str__(self):
        return self.name


class submission(models.Model):
    submission_id = models.AutoField(primary_key=True)  # ← ENTIER, AUTO-INCRÉMENTÉ

    def validate_keywords(value):
        keywords = [k.strip() for k in value.split(',') if k.strip()]
        if len(keywords) > 10:
            raise ValidationError("Maximum 10 mots-clés autorisés")

    user = models.ForeignKey(
        "UserApp.User",
        on_delete=models.CASCADE,
        related_name="conference_submissions"
    )
    conference = models.ForeignKey(
        Conference,
        on_delete=models.CASCADE,
        related_name="submissions_list"
    )
    title = models.CharField(max_length=255)
    abstract = models.TextField()
    keywords = models.CharField(
        max_length=500,
        validators=[validate_keywords],
        help_text="Séparez par des virgules (max 10)"
    )
    STATUS_CHOICES = [
        ("submitted", "Submitted"),
        ("under review", "Under Review"),
        ("accepted", "Accepted"),
        ("rejected", "Rejected"),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="submitted")
    paper = models.FileField(
        upload_to='submissions/',
        validators=[FileExtensionValidator(['pdf'])],
        null=True, blank=True
    )
    submission_date = models.DateField(auto_now_add=True)
    payed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    

    def can_be_modified(self):
        return self.status in ['submitted', 'under review']

    def __str__(self):
        return f"{self.title} - {self.user.username}"