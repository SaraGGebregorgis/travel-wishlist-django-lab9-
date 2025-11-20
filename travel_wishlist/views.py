from django.shortcuts import render, redirect, get_object_or_404
from .models import Place
from .forms import NewPlaceForm, TripReviewForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages

@login_required
def place_list(request):
    if request.method == 'POST': # Create a form instance from the submitted POST data
        form = NewPlaceForm(request.POST) ##creating a form from data thsts in the req
        place = form.save(commit=False) ##create a model object form form
        place.user = request.user
        if form.is_valid(): ##validation againtst DB constraints
            place.save() ## saves place to db
            return redirect('place_list') ##reload homepage
        
        # Retrieve all places that have not been visited
    places = Place.objects.filter(user=request.user).filter(visited=False) #filter just places for currently login user
    new_place_form = NewPlaceForm() ##used to creat hmtl
    return render(request, 'travel_wishlist/wishlist.html', {'places': places, 'new_place_form': new_place_form}) 
    ##take template list of place and form all together to make a web page


@login_required
def place_visited(request):
     # Query all visited places
    visited = Place.objects.filter(visited=True)
    return render(request, 'travel_wishlist/visited.html', { 'visited': visited})


@login_required
def place_was_visited(request, place_pk):
    if request.method == 'POST':
        # Retrieve the Place object by its primary key or return 404 if not found
        #place = Place.objects.get(pk=place_pk)
        place= get_object_or_404(Place, pk=place_pk)
        # Mark the place as visited and save the change
        if place.user == request.user:
            place.visited = True
            place.save()
        else:
            return HttpResponseForbidden()

    return redirect('place_list') ##you can put the place visited as well

def about (request):
     # info and description to the template
    author = "Sara"
    about = "A websiter to create a list  of places to visit"
    return render(request, 'travel_wishlist/about.html', {'author': author, 'about': about})

@login_required
def place_details(request, place_pk):
     # Only allow access to a place that belongs to the logged-in user
    place = get_object_or_404(Place, pk=place_pk)
    return render(request, 'travel_wishlist/place_detail.html', {'place' : place})

    if place.user != request.user:
        return HttpResponseForbidden()
    
    if request.method == 'POST':
         # Bind form to POST data and any uploaded files
        form = TripReviewForm(request.POST, request.FILES, instance=place)
        if form.is_valid():
            form.save()
            messages.info(request, 'Trip information updated!')
        else:
            # Show errors in the template
            messages.error(request, form.errors)
        return redirect('place_details', place_pk=place_pk)

    else: 
        # GET request
        if place.visited:
            # If the place has been visited, show a pre-filled review form
            review_form = TripReviewForm(instance=place)
            return render(request, 'travel_wishlist/place_detail.html', {'place': place, 'review_form': review_form})
        else:
            return render(request, 'travel_wishlist/place_detail.html', {'place': place})

@login_required
def delete_place(request, place_pk): # Only get the place if it belongs to the current user
    place = get_object_or_404(Place, pk=place.pk)
    if place.user == request.user:
        place.delete()
        return redirect('place_list')

    else:
        return HttpResponseForbidden # If someone tries to GET this URL, block it