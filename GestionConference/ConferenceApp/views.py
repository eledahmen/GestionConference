from django.shortcuts import render
from django.urls import reverse_lazy
from .models import Conference
from django.views.generic import ListView, DetailView , CreateView ,UpdateView,DeleteView
from .forms import ConferenceModel
# Create your views here.
def all_conferences(req):
    conferences=Conference.objects.all()
    return render(req,'Conference/liste.html',{"liste":conferences})
class ConferenceList(ListView):
    model=Conference
    context_object_name="liste"
    ordering=["start_date"]
    template_name="conference/liste.html"
class ConferenceDetail(DetailView):
    model=Conference
    context_object_name="conference"
    template_name="conference/details.html"
class ConferenceCreate(CreateView):
     model=Conference
     template_name="conference/conference_form.html"
     form_class=ConferenceModel

    #  fields="__all__"
     success_url=reverse_lazy("conference_liste")
class ConferenceUpdate(UpdateView):
     model=Conference
     template_name="conference/conference_form.html"
    #  fields="__all__"
     form_class=ConferenceModel
     success_url=reverse_lazy("conference_liste")

class ConferenceDelete(DeleteView):
     model=Conference
     template_name="conference/conference_confirm_delete.html"
     success_url=reverse_lazy("conference_liste")