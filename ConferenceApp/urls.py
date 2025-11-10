# ConferenceApp/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.ConferenceList.as_view(), name='conference_liste'),
    path('details/<int:pk>/', views.ConferenceDetail.as_view(), name='conference_detail'),
    path('add/', views.ConferenceCreate.as_view(), name='conference_add'),
    path('<int:pk>/edit/', views.ConferenceUpdate.as_view(), name='conference_edit'),
    path('<int:pk>/delete/', views.ConferenceDelete.as_view(), name='conference_delete'),

    path('my-submissions/', views.SubmissionListView.as_view(), name='submission_list'),
    path('submission/<int:pk>/', views.SubmissionDetailView.as_view(), name='submission_detail'),
    path('submission/add/', views.SubmissionCreateView.as_view(), name='submission_add'),
    path('submission/<int:pk>/edit/', views.SubmissionUpdateView.as_view(), name='submission_edit'),
]