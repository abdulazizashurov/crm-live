from django.urls import path
from .views import *


urlpatterns = [
    path('', index, name='listings'),
    path('<int:listing_id>', listing, name='listing'),
    path('search', search, name='search'),
]