from django.urls import path
from . import views

app_name = 'website'

urlpatterns = [
    path('', views.IndexView.as_view(), name='home'),
    path('contact/', views.ContactUsView.as_view(), name='contact'),
    path('about/', views.AboutView.as_view(), name='about'),
    path("newletters/", views.NewsletterView.as_view(), name="newsletter"),
]

