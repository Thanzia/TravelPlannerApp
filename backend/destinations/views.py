from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication

from destinations.models import *
from destinations.serializers import *

from django.db.models import Q
from django.shortcuts import get_object_or_404

# Create your views here.

# view for listing destinations
class DestinationListView(APIView):
    
    authentication_classes = [JWTAuthentication]
    
    permission_classes = [AllowAny]

    def get(self, request):
        
        destinations = DestinationModel.objects.all()
        
        serializer = DestinationSerializer(destinations, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
# detail view for a specific destination
class DestinationDetailView(APIView):
	
	authentication_classes = [JWTAuthentication]
	
	permission_classes = [IsAuthenticated]

	def get(self, request, **kwargs):

		id = kwargs.get("pk")

		try:

			destination = DestinationModel.objects.get(id=id)

			serializer = DestinationSerializer(destination)

			return Response(serializer.data, status=status.HTTP_200_OK)
		
		except DestinationModel.DoesNotExist:
			
			return Response({"error": "Destination not found"}, status=status.HTTP_404_NOT_FOUND)

# view for listing and creating trips
class TripListCreateView(APIView):

	authentication_classes = [JWTAuthentication]
	
	permission_classes = [IsAuthenticated]

	def get(self, request):

		trips = TripModel.objects.filter(Q(user=request.user)| Q(invited_users=request.user)).distinct()

		serializer = TripSerializer(trips, many=True)
		
		return Response(serializer.data, status=status.HTTP_200_OK)
	
	def post(self, request):

		serializer = TripSerializer(data=request.data, context={'request': request})

		if serializer.is_valid():

			serializer.save()

			return Response(serializer.data, status=status.HTTP_201_CREATED)
		
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	
# detail view for a specific trip
class TripDetailView(APIView):

	authentication_classes = [JWTAuthentication]
	
	permission_classes = [IsAuthenticated]

	def get(self, request, **kwargs):

		id = kwargs.get("pk")

		try:

			trip = TripModel.objects.get(id=id)

			if trip.user != request.user and request.user not in trip.invited_users.all():
				# If the user is not the owner and not invited, return a forbidden response

				return Response({"error": "You do not have permission to view this trip"}, status=status.HTTP_403_FORBIDDEN)

			serializer = TripSerializer(trip)

			return Response(serializer.data, status=status.HTTP_200_OK)
		
		except TripModel.DoesNotExist:
			
			return Response({"error": "Trip not found"}, status=status.HTTP_404_NOT_FOUND)
		
	def put(self, request, **kwargs):

		id = kwargs.get("pk")

		try:

			trip = TripModel.objects.get(id=id)

			if trip.user != request.user:

				return Response({"error": "You do not have permission to edit this trip"}, status=status.HTTP_403_FORBIDDEN)

			serializer = TripSerializer(trip, data=request.data, partial=True)

			if serializer.is_valid():

				serializer.save()

				return Response(serializer.data, status=status.HTTP_200_OK)
			
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
		
		except TripModel.DoesNotExist:
			
			return Response({"error": "Trip not found"}, status=status.HTTP_404_NOT_FOUND)
		
	def delete(self, request, **kwargs):

		id = kwargs.get("pk")

		try:

			trip = TripModel.objects.get(id=id)

			if trip.user != request.user:

				return Response({"error": "You do not have permission to delete this trip"}, status=status.HTTP_403_FORBIDDEN)

			trip.delete()

			return Response({"message": "Trip deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
		
		except TripModel.DoesNotExist:
			
			return Response({"error": "Trip not found"}, status=status.HTTP_404_NOT_FOUND)
		
# itinerary create and list
class ItineraryListCreateView(APIView):

    authentication_classes = [JWTAuthentication]

    permission_classes = [IsAuthenticated]

    def get(self, request, **kwargs):

        """
        List all itineraries for a given trip.
        Both the owner and invited users can view.
        """
        trip_id = kwargs.get("pk")   # pk from URL

        trip = get_object_or_404(TripModel, id=trip_id)

        if trip.user != request.user and request.user not in trip.invited_users.all():

            return Response(
                {"error": "You do not have permission to view itineraries for this trip"},
                status=status.HTTP_403_FORBIDDEN
            )

        itineraries = ItineraryModel.objects.filter(trip=trip)

        serializer = ItinerarySerializer(itineraries, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, **kwargs):

        """
        Create an itinerary under a trip.
        Only the trip owner can create.
        """
        trip_id = kwargs.get("pk")   # pk from URL

        trip = get_object_or_404(TripModel, id=trip_id)

        if trip.user != request.user:

            return Response(
                {"error": "You do not have permission to add itineraries to this trip"},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = ItinerarySerializer(data=request.data)

        if serializer.is_valid():

            serializer.save(trip=trip)
			
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# detailview, delete, update
class ItineraryDetailView(APIView):

	permission_classes = [IsAuthenticated]

	authentication_classes = [JWTAuthentication]
	
	def get_object(self, id):
		
		try:
			
			return ItineraryModel.objects.get(id=id)
		
		except ItineraryModel.DoesNotExist:
			
			return None
		
	def get(self, request, **kwargs):
		
		id = kwargs.get("pk")
		
		itinerary = self.get_object(id)
		
		if not itinerary:
			
			return Response({"error": "Itinerary not found"}, status=status.HTTP_404_NOT_FOUND)
		
		trip = itinerary.trip
		
		if trip.user != request.user and request.user not in trip.invited_users.all():
			
			return Response({"error": "You do not have permission to view this itinerary"}, 
                            status=status.HTTP_403_FORBIDDEN)
			
		serializer = ItinerarySerializer(itinerary)
		
		return Response(serializer.data, status=status.HTTP_200_OK)
	
	def put(self, request, **kwargs):
		
		id = kwargs.get("pk")
		
		itinerary = self.get_object(id)
		
		if not itinerary:
			
			return Response({"error": "Itinerary not found"}, status=status.HTTP_404_NOT_FOUND)
		
		trip = itinerary.trip
		
		if trip.user != request.user:
			
			return Response({"error": "You do not have permission to edit this itinerary"}, 
                            status=status.HTTP_403_FORBIDDEN)
			
		serializer = ItinerarySerializer(itinerary, data=request.data, partial=True)
		
		if serializer.is_valid():
			
			serializer.save()
			
			return Response(serializer.data, status=status.HTTP_200_OK)
		
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	
	def delete(self, request, **kwargs):
		
		id = kwargs.get("pk")
		
		itinerary = self.get_object(id)
		
		if not itinerary:
			
			return Response({"error": "Itinerary not found"}, status=status.HTTP_404_NOT_FOUND)
		
		trip = itinerary.trip
		
		if trip.user != request.user:
			
			return Response({"error": "You do not have permission to delete this itinerary"}, 
                            status=status.HTTP_403_FORBIDDEN)
			
		itinerary.delete()
		
		return Response({"message": "Itinerary deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

# expense create and list
class ExpenseListCreateView(APIView):

    authentication_classes = [JWTAuthentication]

    permission_classes = [IsAuthenticated]

    def get(self, request, **kwargs):

        trip_id = kwargs.get("pk")

        trip = get_object_or_404(TripModel, id=trip_id)

        # Check permission
        if trip.user != request.user and request.user not in trip.invited_users.all():

            return Response({"error": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)

        expenses = ExpenseModel.objects.filter(trip=trip)

        serializer = ExpenseSerializer(expenses, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, **kwargs):

        trip_id = kwargs.get("pk")

        trip = get_object_or_404(TripModel, id=trip_id)

        # Only trip owner or invited members can add expense
        if trip.user != request.user and request.user not in trip.invited_users.all():

            return Response({"error": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)

        serializer = ExpenseSerializer(data=request.data)

        if serializer.is_valid():

            serializer.save(trip=trip, paid_by=request.user)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
		
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	
class ExpenseSummaryView(APIView):

    authentication_classes = [JWTAuthentication]

    permission_classes = [IsAuthenticated]
	
    def get(self, request, **kwargs):

        trip_id = kwargs.get("pk")

        trip = get_object_or_404(TripModel, id=trip_id)

        if trip.user != request.user and request.user not in trip.invited_users.all():

            return Response({"error": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)

        expenses = ExpenseModel.objects.filter(trip=trip)

        paid_summary = {}

        share_summary = {}

        balances = {}

        total_expenses = 0

        participants = set()

        # Collect expense info
        for exp in expenses:

            total_expenses += exp.amount

            paid_summary[exp.paid_by.username] = paid_summary.get(exp.paid_by.username, 0) + exp.amount

            participants.add(exp.paid_by.username)

            for user in exp.shared_with.all():

                participants.add(user.username)

        # Equal share
        equal_share = total_expenses / len(participants) if participants else 0

        for user in participants:

            share_summary[user] = equal_share

            balances[user] = paid_summary.get(user, 0) - equal_share

        # Settlement transactions
        transactions = settle_expenses(balances)

        return Response(
            {
                "paid_summary": paid_summary,
                "share_summary": share_summary,
                "balances": balances,
                "transactions": transactions,
            },
            status=status.HTTP_200_OK,
        )
	
def settle_expenses(balances):
		
		creditors = [(p, amt) for p, amt in balances.items() if amt > 0]
		
		debtors = [(p, -amt) for p, amt in balances.items() if amt < 0]
		
		creditors.sort(key=lambda x: x[1], reverse=True)
		
		debtors.sort(key=lambda x: x[1], reverse=True)
		
		transactions = []
		
		i, j = 0, 0
		
		while i < len(creditors) and j < len(debtors):
			
			creditor, credit_amt = creditors[i]
			
			debtor, debt_amt = debtors[j]
			
			settle_amt = min(credit_amt, debt_amt)
			
			transactions.append(f"{debtor} → {creditor}: {settle_amt}")
			
			creditors[i] = (creditor, credit_amt - settle_amt)
			
			debtors[j] = (debtor, debt_amt - settle_amt)
			
			if creditors[i][1] == 0:
				
				i += 1
				
			if debtors[j][1] == 0:
				
				j += 1
				
		return transactions

# checklist create view
class ChecklistListCreateView(APIView):

    authentication_classes = [JWTAuthentication]

    permission_classes = [IsAuthenticated]

    def get(self, request, **kwargs):

        trip_id = kwargs.get("pk")

        trip = get_object_or_404(TripModel, id=trip_id)

        if trip.user != request.user and request.user not in trip.invited_users.all():

            return Response({"error": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)

        items = ChecklistModel.objects.filter(trip=trip)

        serializer = ChecklistSerializer(items, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, **kwargs):

        trip_id = kwargs.get("pk")

        trip = get_object_or_404(TripModel, id=trip_id)

        if trip.user != request.user and request.user not in trip.invited_users.all():

            return Response({"error": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)

        serializer = ChecklistSerializer(data=request.data)

        if serializer.is_valid():

            serializer.save(trip=trip, user=request.user)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# checklist update is_done
class ChecklistDetailView(APIView):

    authentication_classes = [JWTAuthentication]

    permission_classes = [IsAuthenticated]

    def put(self, request, **kwargs):

        checklist_id = kwargs.get("pk")

        checklist_item = get_object_or_404(ChecklistModel, id=checklist_id)

        if checklist_item.trip.user != request.user and request.user not in checklist_item.trip.invited_users.all():

            return Response({"error": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)

        serializer = ChecklistSerializer(checklist_item, data=request.data, partial=True)

        if serializer.is_valid():

            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)
		
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


 
