from django.urls import path
from . import views

urlpatterns = [
    path('titanic_prediction', views.titanic, name='titanic'),
    path('classify', views.classify, name='classify'),
    path('', views.index, name='index'),
    path('ebay_scraping', views.ebay_scraping, name="ebay_scraping"),
    path('match_image', views.match_image, name="match_image")
]
