
from django.urls import path
from . import views

# make sure have app name to avoid reverse match error
app_name = 'mystats'

# and patters need a name
urlpatterns = [
    path('run_streak', views.run_streak, name='record run streak'),

]