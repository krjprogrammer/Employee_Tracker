from rest_framework import serializers
from .models import user_data,employee_details
class user_serializer(serializers.ModelSerializer):
    class Meta:
        model = user_data
        fields = '__all__'

class employee_data_serializer(serializers.ModelSerializer):
    class Meta:
        model = employee_details
        fields = '__all__'