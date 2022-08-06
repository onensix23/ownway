from django.urls import path
from django.views.generic import TemplateView


from . import views

urlpatterns = [
    path('',views.index),
    # path('', TemplateView.as_view(template_name='index.html')),
    # path('howtoresign', views.index, name='index2'),
]