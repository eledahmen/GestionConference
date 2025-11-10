# ConferenceApp/views.py

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import Conference, submission
from .forms import ConferenceModel, SubmissionForm


# === Conférences ===
class ConferenceList(ListView):
    model = Conference
    context_object_name = "liste"
    template_name = "conference/liste.html"
    ordering = ["start_date"]


class ConferenceDetail(DetailView):
    model = Conference
    context_object_name = "conference"
    template_name = "conference/details.html"


class ConferenceCreate(LoginRequiredMixin, CreateView):
    model = Conference
    form_class = ConferenceModel
    template_name = "conference/conference_form.html"
    success_url = reverse_lazy("conference_liste")

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_organizer():
            messages.error(request, "Accès refusé.")
            return redirect('conference_liste')
        return super().dispatch(request, *args, **kwargs)


class ConferenceUpdate(LoginRequiredMixin, UpdateView):
    model = Conference
    form_class = ConferenceModel
    template_name = "conference/conference_form.html"
    success_url = reverse_lazy("conference_liste")

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_organizer():
            messages.error(request, "Accès refusé.")
            return redirect('conference_liste')
        return super().dispatch(request, *args, **kwargs)


class ConferenceDelete(LoginRequiredMixin, DeleteView):
    model = Conference
    template_name = "conference/conference_confirm_delete.html"
    success_url = reverse_lazy("conference_liste")
    context_object_name = "objet"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_organizer():
            messages.error(request, "Accès refusé.")
            return redirect('conference_liste')
        return super().dispatch(request, *args, **kwargs)


# === SOUMISSIONS ===
class SubmissionListView(LoginRequiredMixin, ListView):
    model = submission
    template_name = 'submission/list.html'
    context_object_name = 'submissions'

    def get_queryset(self):
        return submission.objects.filter(user=self.request.user).order_by('-submission_date')


class SubmissionDetailView(LoginRequiredMixin, DetailView):
    model = submission
    template_name = 'submission/detail.html'
    context_object_name = 'sub'

    def get_queryset(self):
        return submission.objects.filter(user=self.request.user)


class SubmissionCreateView(LoginRequiredMixin, CreateView):
    model = submission
    form_class = SubmissionForm
    template_name = 'submission/form.html'
    success_url = reverse_lazy('submission_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        # NE TOUCHEZ PAS submission_id → AutoField gère automatiquement
        return super().form_valid(form)


class SubmissionUpdateView(LoginRequiredMixin, UpdateView):
    model = submission
    form_class = SubmissionForm
    template_name = 'submission/form.html'
    success_url = reverse_lazy('submission_list')

    def get_queryset(self):
        return submission.objects.filter(user=self.request.user)

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if not obj.can_be_modified():
            messages.error(request, "Soumission non modifiable.")
            return redirect('submission_list')
        return super().dispatch(request, *args, **kwargs)