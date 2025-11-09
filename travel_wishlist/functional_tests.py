# Import Firefox WebDriver from Selenium
from selenium.webdriver.firefox.webdriver import webdriver

from django.test import LiveServerTestCase 
from .models import Place

class TitleTest(LiveServerTestCase):

    fixtures = ['test_place'] # Load sample data before running the tests

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = webdriver()
        cls.selenium.implicitly_wait(10) # wait up to 10s for elements to load

    
    @classmethod
    def tearDownClass(cls):
        # Close the browser after tests finish
        cls.selenium.quit()
        super.tearDownClass()

     # Checks that the homepage title contains 'Travel Wishlist'
    def test_title_on_home_page(self):
        self.selenium.get(self.live_server_url)
        self.assertIn('Travel Wishlist', self.selenium.title)

     # Tests adding a new place through the form
    def test_add_new_place(self):

        self.selenium.get(self.live_server_url)
        input_name = self.selenium.find_element_by_id('id_name') # Find the input field a enter denver
        input_name.send_keys('Denver')

        add_button = self.selenium.find_element_by_id('add-new-place')
        add_button.click()

        denver = self.selenium.find_element_by_id('palce-name-5')
        self.assertEqual('Denver', denver.text)

         # Verify that expected places appear on the page
        self.assertIn('Denver', self.selenium.page_source)
        self.assertIn('New York', self.selenium.page_source)
        self.assertIn('Tokyo', self.selenium.page_source)

        # Confirm the new place exists in the database
        denver_db = Place.objects.get(pk=5)
        self.assertEqual('Denver', denver_db.name)
        self.assertTrue(denver_db.visited)