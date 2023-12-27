from rest_framework import serializers
from .models import Project, Proposal


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'


class ProposalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proposal
        read_only_fields = ['created_at', 'updated_at']
        fields = '__all__'
