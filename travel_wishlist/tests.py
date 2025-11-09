from django.test import TestCase
from django.urls import reverse

from .models import Place

class TestHomePage(TestCase):
    
    def test_home_page_shows_empty_list_message_for_empty_database(self):
         # Checks that the homepage shows the correct message when no places exist
        home_page_url = reverse('place_list')
        response = self.client.get(home_page_url)
        self.assertTemplateUsed(response, 'travel_wishlist/wishlist.html')
        self.assertContains(response, 'You have no places in your wishlist.')

class TestWishList(TestCase):

    fixtures = ['test_places']# Uses sample data from fixtures
    def test_wishlist_contains_not_visited_places(self):
        # Checks that only unvisited places are displayed in the wishlist
        response = self.client.get(reverse('place_list'))
        self.assertTemplateUsed(response, 'travel_wishlist/wishlist.html')
        self.assertContains(response, 'Tokyo')
        self.assertContains(response, 'New York')
        self.assertNotContains(response, 'San Francisco')
        self.assertNotContains(response, 'Moab')


class TestAddNewPlace(TestCase):
  # Tests that a new unvisited place can be added successfully
    def test_add_new_unvisited_place(self):
        add_place_url = reverse('place_list')
        new_place_data = {'name': 'Tokyo', 'visited': False}

        response = self.client.post(add_place_url, new_place_data, follow=True)

        self.assertTemplateUsed(response, 'travel_wishlist/wishlist.html')

        # Get the places from the response and check that one new place was added
        response_places = response.context['places']
        self.assertEqual(1, len(response_places))
        tokyo_from_response = response_places[0]

         # Get the same place from the database to confirm it was saved correctly
        tokyo_from_database = Place.objects.get(name='Tokyo', visited=False)

        self.assertEqual(tokyo_from_database, tokyo_from_response)


class TestVisitPlace(TestCase):

    fixtures = ['test_places']

     # Tests marking a place as visited
    def test_visit_place(self):
        visit_place_url = reverse('place_was_visited', args=(2,))
        response = self.client.post(visit_place_url, follow=True)

        self.assertTemplateUsed(response, 'travel_wishlist/wishlist.html')

        self.assertNotContains(response, 'New York')  # should move to visited list
        self.assertContains(response, 'Tokyo')  # still unvisited

        new_york = Place.objects.get(pk=2)   # Confirm the place is now marked as visited in the database
        self.assertTrue(new_york.visited)

def test_nonexistent_place(self): # Tests what happens if user tries to visit a non-existent place
    visit_nonexistent_place_url = reverse('place_was_visited', args=(123456, ))
    response = self.client.post(visit_nonexistent_place_url, follow=True)
    self.assertEqual(404,response.status_cade)