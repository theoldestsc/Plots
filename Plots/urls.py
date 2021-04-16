from django.urls import path
from . import views

app_name = 'Plots'
urlpatterns = [
    path('',views.mainV,name = 'main'),
    path('calc/',views.calculate, name = 'calculate'),
    path('save/',views.save, name = 'save'),
    path('plots',views.usersPlots,name = 'myplots'),
    path('admin/Plots/plot/add/', views.add_plots_admin, name='admin_add_plots'),
]