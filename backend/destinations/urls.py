from django.urls import path
from .views import *

urlpatterns = [

	path('destinations_list/', DestinationListView.as_view(), name='destination-list'),
	path('destinations_detail/<int:pk>/', DestinationDetailView.as_view(), name='destination-detail'),

	path('trips_list_create/', TripListCreateView.as_view(), name='trip-list'),
	path('trips_detail/<int:pk>/', TripDetailView.as_view(), name='trip-detail'),

	path('itinerary_create_list/<int:pk>/',ItineraryListCreateView.as_view(),name='itinerary-create-list'),
	path('itinerary_detail/<int:pk>/',ItineraryDetailView.as_view(),name='itinerary-detail'),

	path('expense_create_list/<int:pk>/',ExpenseListCreateView.as_view(),name='expense-create'),
	path('expense_summary/<int:pk>/',ExpenseSummaryView.as_view(),name='expense-summary'),

	path('checklist_create_list/<int:pk>/',ChecklistListCreateView.as_view(),name='checklist-create'),
	path('checklist_update/<int:pk>/',ChecklistDetailView.as_view(),name='checklist-update'),

]