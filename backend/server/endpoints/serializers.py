from rest_framework import serializers
from .models import *


class EndpointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Endpoint
        read_only_fields = ('id', 'owner', 'name', 'created_at')
        fields = read_only_fields


class MLAlgorithmSerializer(serializers.ModelSerializer):

    current_status = serializers.SerializerMethodField()

    class Meta:
        model = MLAlgorithm
        read_only_fields = ('code', 'description', 'owner', 'version', 'parent_endpoint', 'created_at')
        fields = ['id', 'code', 'description', 'owner', 'version', 'parent_endpoint', 'created_at', 'current_status']

    def get_current_status(self, mlalgorithm):
        return MLAlgorithmStatus.objects.filter(parent_mlalgorithm=mlalgorithm).latest('created_at').status


class MLAlgorithmStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = MLAlgorithmStatus
        read_only_fields = ('active', 'id')
        fields = ['status', 'id', 'active', 'parent_mlalgorithm', 'created_at', 'created_by']


class MLRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = MLRequest
        read_only_fields = ('input_data', 'response', 'full_response', 'parent_mlalgorithm', 'created_at')
        fields = ['id', 'input_data', 'response', 'full_response', 'created_at', 'feedback', 'parent_mlalgorithm']


class ABTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ABTest
        read_only_fields = ('id', 'created_at', 'ended_at', 'summary')
        fields = ['id', 'title', 'created_at', 'ended_at', 'summary', 'created_by', 'parent_mlalgorithm_1', 'parent_mlalgorithm_2']