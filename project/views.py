from django.http import JsonResponse
# from project.models.project import Project,teamDetails
# from .serializers import projectSerializer,teamDetailsSerializer
from rest_framework.decorators import api_view

from rest_framework import viewsets, parsers
from rest_framework.permissions import AllowAny

from .models import Proposal
from .serializers import ProposalSerializer


class ProposalViewset(viewsets.ModelViewSet):

    queryset = Proposal.objects.all()
    serializer_class = ProposalSerializer
    permission_classes = [AllowAny]
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]
    http_method_names = ['get', 'post', 'patch', 'delete']


# Create your views here.

# class ssrApiView(APIView):
#     # add permission to check if user is authenticated
#     permission_classes = [permissions.IsAuthenticated]
@api_view(['GET'])
def ssrApiView(request):
    if request.method == 'GET':
        projects = Project.objects.all()
        serializer = projectSerializer(projects, many=True)
        # covert categories to list
        # print(serializer.data[0]['category'].split(','))
        for i in range(len(serializer.data)):
            serializer.data[i]['category'] = serializer.data[i]['category'].split(',')
        pages = [serializer.data[i:i + 20] for i in range(0, len(serializer.data), 20)]
        

        return JsonResponse({"Projects":pages})
    elif request.method == 'POST':
        serializer = projectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"Message":"Project posted successfully"})
        return JsonResponse({"Error":serializer.errors})

def ssrYear(request, year):
    projects = Project.objects.filter(year=year)
    serializer = projectSerializer(projects, many=True)
    return JsonResponse({"Projects":serializer.data})

def ssrCategory(request, category):
    projects = Project.objects.filter(category=category)
    serializer = projectSerializer(projects, many=True)
    return JsonResponse({"Projects":serializer.data})

def getCatories(request):
    try:
        categories = Project.objects.values_list('category', flat=True).distinct()
        return JsonResponse({"Categories":list(categories)})
    except:
        return JsonResponse({"Error":"No projects found"})

def getYears(request):
    try:
        years = Project.objects.values_list('year', flat=True).distinct()
        return JsonResponse({"Years":list(years)})
    except:
        return JsonResponse({"Error":"No projects found"})


def ssrProjectId(request, projectId):
    try :
        project = Project.objects.get(projectId=projectId)
        print(project)
    except Project.DoesNotExist:
        return JsonResponse({"Error":"Project not found"})
    serializer = projectSerializer(project)
    return JsonResponse({"Project":serializer.data})

def teamDetailsapi(request, teamId):
    try :
        project = teamDetails.objects.filter(projectId=teamId)
        projectDetails = Project.objects.get(projectId=teamId)
    except teamDetails.DoesNotExist:
        return JsonResponse({"Error":"Team details not found"})
    try:
        serializer = teamDetailsSerializer(project,many=True)
        serializer2 = projectSerializer(projectDetails)
        return JsonResponse({"Team Details":serializer.data,"Project Details":serializer2.data})
        # return JsonResponse({"Team Details":serializer.data})
    except:
        return JsonResponse({"Error":"Team details not found"})

def teams(request):
    try :
        project = teamDetails.objects.all()
        # print teamDetails columns in console
    except teamDetails.DoesNotExist:
        return JsonResponse({"Error":"Team details not found"})
    try:
        serializer = teamDetailsSerializer(project,many=True)
        return JsonResponse({"Team Details":serializer.data})
    except: 
        return JsonResponse({"Error":"Team details not found"})






