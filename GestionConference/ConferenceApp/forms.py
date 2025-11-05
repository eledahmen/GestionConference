from django  import forms

from .models import Conference

class ConferenceModel(forms.ModelForm):
    class Meta:
        model=Conference
        fields =['name' , 'description' , 'location', 'start_date','end_date']
        labels ={
            "name":"nom de la conference",
            "theme":"thématique"  ,     
             'description' :"description",
             "location" :"location" ,
             "start_date":"date debut de conference",
             "end_date":"date fin de conference"}
        widgets={
                 "start_date":forms.DateInput(
                     attrs={
                         'type':'date',
                         'placeholder':"date de début"
                     }
                 )   ,
                  "end_date":forms.DateInput(
                     attrs={
                         'type':'date',
                         'placeholder':"date de fin" }),
                  "name":forms.TextInput(
                     attrs={
                         
                         'placeholder':"nom"})}