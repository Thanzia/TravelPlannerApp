from django.db import models
from userapp.models import *


# Create your models here.

# destination model
class DestinationModel(models.Model):

	name = models.CharField(max_length=100)

	country = models.CharField(max_length=100,default="UAE")

	description = models.TextField()

	image = models.ImageField(upload_to = 'store_images',null=True,blank=True)

	latitude = models.DecimalField(max_digits=9,decimal_places=6,null=True,blank=True)

	longitude = models.DecimalField(max_digits=9,decimal_places=6,null=True,blank=True)

	top_attractions = models.TextField(null=True,blank=True)

	travel_type = models.CharField(max_length=50,choices=[
		                                                   ('adventure','Adventure'),
														   ('family','Family'),
														   ('romantic','Romantic'),
														   ('cultural','Cultural'),
														   ('relaxation','Relaxation'),
														   ('beach','Beach'),
														   ('hill_station','Hill Station'),


	])
      
	best_time_to_visit = models.CharField(max_length=100,null=True,blank=True)
	
	created_at = models.DateField(auto_now_add=True)
	
	def __str__(self):

		return self.name
	
# Trip model
class TripModel(models.Model):

	user = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE)

	title = models.CharField(max_length=100)	

	start_date = models.DateField()

	end_date = models.DateField()

	number_of_families = models.PositiveIntegerField(default=1)

	invited_users = models.ManyToManyField(CustomUserModel, related_name='invited_trips', blank=True)

	created_at = models.DateField(auto_now_add=True)

	def __str__(self):

		return f"Trip to {self.title} by {self.user.username}"

# Itinerary model
class ItineraryModel(models.Model):

	trip = models.ForeignKey(TripModel, on_delete=models.CASCADE)

	destination = models.ForeignKey(DestinationModel, on_delete=models.CASCADE)

	title = models.CharField(max_length=100)

	date = models.DateField()

	time = models.TimeField(blank=True, null=True)

	activities = models.TextField()

	created_at = models.DateTimeField(auto_now_add=True)

	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):

		return f"Itinerary for {self.trip.title} at {self.destination.name} on {self.date}"

# expense model

class ExpenseModel(models.Model):

    trip = models.ForeignKey(TripModel, on_delete=models.CASCADE, related_name="expenses")

    title = models.CharField(max_length=100)

    amount = models.DecimalField(max_digits=10, decimal_places=2)

    paid_by = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE, related_name="expenses_paid")

    shared_with = models.ManyToManyField(CustomUserModel, related_name="expenses_shared", blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):

        return f"{self.title} - {self.amount} ({self.trip.title})"

# checklist
class ChecklistModel(models.Model):

    trip = models.ForeignKey(TripModel, on_delete=models.CASCADE, related_name="checklist")

    user = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE, related_name="checklist_items")

    item = models.CharField(max_length=255)

    is_done = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.item} - {'Done' if self.is_done else 'Pending'}"
	


