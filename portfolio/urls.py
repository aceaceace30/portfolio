from django.urls import path
from . import views

app_name = 'portfolio'

urlpatterns = [
    path('project/<slug:slug>/', views.ProjectDetailView.as_view(), name='project_details'),
    path('form/send-message/', views.send_message, name='send_message'),
]
