from django.urls import path
from . import views

urlpatterns = [
    path('available-slots/', views.get_available_slots, name='available_slots'),
    path('book-appointment/', views.book_appointment, name='book_appointment'),
]