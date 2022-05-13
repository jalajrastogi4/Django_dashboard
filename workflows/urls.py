from django.urls import path
from . import views

urlpatterns = [
    path('', views.workflows, name='workflows'),
    path('examples', views.examples, name='examples'),
    path('ajax/iteration_chart/', views.iteration_chart, name='iteration_chart'),
    path('ajax/trust_chart/', views.trust_chart, name='trust_chart'),
]