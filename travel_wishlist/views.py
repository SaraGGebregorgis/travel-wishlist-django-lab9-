from django.shortcuts import render, redirect, get_object_or_404
from .models import Place
from .forms import NewPlaceForm

def place_list(request):
    if request.method == 'POST': # Create a form instance from the submitted POST data
        form = NewPlaceForm(request.POST) ##creating a form from data thsts in the req
        place = form.save() ##create a model object form form
        if form.is_valid(): ##validation againtst DB constraints
            place.save() ## saves place to db
            return redirect('place_list') ##reload homepage
        
        # Retrieve all places that have not been visited
    places = Place.objects.filter(visited=False).order_by('name')
    new_place_form = NewPlaceForm() ##used to creat hmtl
    return render(request, 'travel_wishlist/wishlist.html', {'places': places, 'new_place_form': new_place_form}) 
    ##take template list of place and form all together to make a web page

def place_visited(request):
     # Query all visited places
    visited = Place.objects.filter(visited=True)
    return render(request, 'travel_wishlist/visited.html', { 'visited': visited})

def place_was_visited(request, place_pk):
    if request.method == 'POST':
        # Retrieve the Place object by its primary key or return 404 if not found
        #place = Place.objects.get(pk=place_pk)
        place= get_object_or_404(Place, pk=place_pk)
        # Mark the place as visited and save the change
        place.visited = True
        place.save()

    return redirect('place_list')##you can put the place visited as well

def about (request):
     # info and description to the template
    author = "Sara"
    about = "A websiter to create a list  of places to visit"
    return render(request, 'travel_wishlist/about.html', {'author': author, 'about': about})
