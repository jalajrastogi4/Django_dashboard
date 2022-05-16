from django.urls import path
from . import views

urlpatterns = [
    path('', views.workflows, name='workflows'),
    path('daily-workflow/', views.dailyworkflow, name='daily-workflow'),
    path('daily-workflow/all-trusts', views.alltrusts, name='all-trusts'),
    path('daily-workflow/all-iterations', views.alliterations, name='all-iterations'),
    path('ajax/iteration_chart/', views.iteration_chart, name='iteration_chart'),
    path('ajax/trust_chart/', views.trust_chart, name='trust_chart'),
]