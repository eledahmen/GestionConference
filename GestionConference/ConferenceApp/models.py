from django.core.validators import FileExtensionValidator
from django.db import models
from django.core.validators import MinLengthValidator 
from django.core.exceptions import ValidationError
import uuid
def generate_submission_id():
    """ Génère un identifiant unique au format SUBABCDEFGH """
    return "SUB-" + uuid.uuid4().hex[:8].upper()
def validate_keywords_max10(value: str):
    # découpe sur la virgule et nettoie les espaces
    items = [kw.strip() for kw in value.split(",")]
    # enlève les entrées vides (", , ,")
    items = [kw for kw in items if kw]

    if len(items) > 10:
        raise ValidationError(
            f"Vous ne pouvez pas dépasser 10 mots-clés (actuellement {len(items)})."
        )
class Conference(models.Model):
    conference_id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=255)
    description=models.TextField(validators=[
        MinLengthValidator(limit_value=30,
                           message="la description doit contenir au minimum 30 caractéres")
    ])
    location=models.CharField(max_length=255)
    THEME= [
        ("CS&IA","Computer science & IA"),
        ("CS","Social science"),
        ("SE","Science and eng")
    
    ]
    theme=models.CharField(max_length=255,
                            choices=THEME)
    start_date = models.DateField()
    end_date =models.DateField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    def clean(self):
        if self.start_date > self.end_date:
            raise ValidationError("la date de début de la conférence doit être antérieur") 
class Submission(models.Model):
    submission_id = models.CharField(
    max_length=12, 
    unique=True, 
    default=generate_submission_id, 
    editable=False
)
    user=models.ForeignKey("UserApp.User",
                           on_delete=models.CASCADE,
                           related_name="submissions")
    conference=models.ForeignKey(Conference,on_delete=models.CASCADE,related_name="submissions")
    title=models.CharField(max_length=255)
    abstract=models.TextField()
    keywords = models.CharField(
        max_length=300,
        validators=[validate_keywords_max10],
        help_text="Mots-clés séparés par des virgules (max 10)."
    )
    paper = models.FileField(upload_to='sub_paper/', validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    CHOICES=[
        ("submitted","submitted"),
        ("under review","under review"),
        ("accepted","accepted"),
        ("rejected","rejected")

    ]
    status=models.CharField(max_length=255,choices=CHOICES)
    payed=models.BooleanField(default=False)
    submission_date=models.DateField(auto_now_add=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    def clean(self):
        errors = {}
        if self.conference and self.submission_date:
            if self.submission_date >= self.conference.start_date:
                errors["submission_date"] = (
                    f"La soumission doit être faite avant le début de la conférence "
                    f"(date de début : {self.conference.start_date})."
                )
        if errors:
            raise ValidationError(errors)
            # 2. Vérifier que l'utilisateur n'a pas dépassé 3 soumissions par jour
        submissions_today = Submission.objects.filter(
            user=self.user,
            submission_date=self.submission_date
        ).exclude(pk=self.pk).count()  # exclude pour ne pas compter soi-même si update

        if submissions_today >= 3:
            errors["submission_date"] = (
                f"Un participant ne peut soumettre que 3 conférences maximum par jour. "
                f"(Vous avez déjà {submissions_today})."
            )

        if errors:
            raise ValidationError(errors)


    def save(self, *args, **kwargs):
        # Si pas d'ID, générer automatiquement
        if not self.submission_id:
            self.submission_id = generate_submission_id()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} - {self.submission_id}"
    