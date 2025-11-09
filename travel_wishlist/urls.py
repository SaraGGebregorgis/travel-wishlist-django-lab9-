from django.urls import path
from . import views

# Define URL patterns and map them to view fun
urlpatterns = [
    ##shows a list of all places
    path('', views.place_list, name='place_list'),
     # Page that shows places the user has already visited
    path('visited', views.place_visited, name='place_visited'),
    # Marks a specific place (by primary key) as visited
    path('place/<int:place_pk>/was_visited/', views.place_was_visited, name='place_was_visited'),
    # About page - provides information about the app or developer
    path('about', views.about, name='about')

]
