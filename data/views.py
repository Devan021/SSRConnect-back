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


def projectDetails(request, teamId):
    try:
        team = teamDetails.objects.filter(projectId=teamId)  # Use .first() to get a single object or None
        serializer = teamDetailsSerializer(team,many=True)
        return JsonResponse(serializer.data,safe=False)
        # if team is not None:
        # else:
        #     return JsonResponse({"detail": "Team not found"}, status=404)
    except Exception as e:
        print(e)
        return JsonResponse({"detail": "An error occurred"}, status=500)