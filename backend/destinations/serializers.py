from rest_framework import serializers
from destinations.models import *

# Destination serializer
class DestinationSerializer(serializers.ModelSerializer):
    
    class Meta:
        
        model = DestinationModel
        
        fields = '__all__'

# Trip serializer
class TripSerializer(serializers.ModelSerializer):
    
    class Meta:
        
        model = TripModel
        
        fields = '__all__'

        read_only_fields = ['user','created_at']
        
    def create(self, validated_data):

        # Automatically set the user to the currently authenticated user
        request = self.context.get('request')

        validated_data['user'] = request.user

        # overrides the create method by calling parent class ModelSerializer's create method
        # to ensure the user is set correctly
        return super().create(validated_data)

# itinerary serializer
class ItinerarySerializer(serializers.ModelSerializer):

    class Meta:

        model = ItineraryModel

        fields = '__all__'

        read_only_fields = ['id','created_at','updated_at','trip']


# expense serializer
class ExpenseSerializer(serializers.ModelSerializer):

    class Meta:

        model = ExpenseModel

        fields = "__all__"

        read_only_fields = ["id", "trip", "paid_by", "created_at", "updated_at"]

# checklist serializer
class ChecklistSerializer(serializers.ModelSerializer):

    class Meta:

        model = ChecklistModel

        fields = "__all__"
        
        read_only_fields = ["id", "user", "trip", "created_at", "updated_at"]

