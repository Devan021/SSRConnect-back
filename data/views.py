from django.shortcuts import render
from django.http import JsonResponse
from .models import Project,teamDetails
from .serializers import projectSerializer,teamDetailsSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response


# Create your views here.

@api_view(['GET'])
def projects(request):
    projects = Project.objects.all()
    serializer = projectSerializer(projects, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def projectDetails(request, projectId):
    project = Project.objects.get(projectId=projectId)
    teamMembers = teamDetails.objects.get(projectId=projectId)
    serializer = projectSerializer(project, many=False)
    serializer2 = teamDetailsSerializer(teamMembers,many=True)
    return Response(serializer.data + serializer2.data)