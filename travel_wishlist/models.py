from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import default_storage

class Place(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE) #specific when user delete and casacade delete all the associate places
    name = models.CharField(max_length=200)
    visited = models.BooleanField(default=False)
    notes = models.TextField(blank=True, null=True)
    date_visited = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='user_images/', blank=True, null=True) # photo upload

    def save(self, *args, **kwargs):# Get the old version of this Place from the database
        old_place = Place.objects.filter(pk=self.pk).first()
        if old_place and old_place.photo: # If there is an existing photo and it is being replaced
            if old_place.photo != self.photo:
                self.delete_photo(old_place.photo)
        
        super().save(*args, **kwargs)  # Run the normal Django save()

    def delete_photo(self, photo):
        if default_storage.exists(photo.name):
            default_storage.delete(photo.name)

    def delete(self, *args, **kwargs):# Delete method override to remove photo file upon object delete
        if self.photo:
            self.delete_photo(self.photo)
        
        super().delete(*args, **kwargs)

    def __str__(self):#for admin, shell, and debugging
        photo_str = self.photo.url if self.photo else 'no photo'
        notes_str = (self.notes[:100] + "...") if self.notes else "no notes" #include notes
        return f'{self.name} visited? {self.visited} on {self.date_visited}. Photo {photo_str}'
