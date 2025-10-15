from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from ConferenceApp.models import Conference
# Create your models here.
room_validator = RegexValidator(r'^[A-Za-z0-9\s]+$', 'Room may contain only letters, numbers and spaces')
def validate_keywords_max10(value: str):
    # découpe sur la virgule et nettoie les espaces
    items = [kw.strip() for kw in value.split(",")]
    # enlève les entrées vides (", , ,")
    items = [kw for kw in items if kw]

    if len(items) > 10:
        raise ValidationError(
            f"Vous ne pouvez pas dépasser 10 mots-clés (actuellement {len(items)})."
        )
class Session(models.Model):
    session_id=models.AutoField(primary_key=True)
    title=models.CharField(max_length=255)
    topic=models.CharField(max_length=255)
    session_day=models.DateField()
    start_time=models.TimeField()
    end_time=models.TimeField()
    room=models.CharField(max_length=255,validators=[room_validator])
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    conference=models.ForeignKey(Conference,
                                 on_delete=models.CASCADE,
                                 related_name="sessions")
  #  conference=models.ForeignKey(Conference)
    def clean(self):
        if self.start_time and self.end_time:
            if self.end_time <= self.start_time:
                raise ValidationError({
                    "end_time": "L'heure de fin doit être supérieure à l'heure de début."
                })
        # Valide l’intervalle de dates
        if self.conference and self.session_day:
            if not (self.conference.start_date <= self.session_day <= self.conference.end_date):
                raise ValidationError({
                    "session_day": (
                        f"La date de la session ({self.session_day}) doit être comprise entre "
                        f"{self.conference.start_date} et {self.conference.end_date}."
                    )
                })
    