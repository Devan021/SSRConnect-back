from django.urls import path
from project import views

from rest_framework.routers import SimpleRouter
from .views import ProposalViewset

router = SimpleRouter()
router.register('proposals', ProposalViewset)

urlpatterns = [
    # path('projects/', views.ssrApiView),
    # path('projects/year/<int:year>/', views.ssrYear),
    # path('projects/category/<str:category>/', views.ssrCategory),
    # path('projects/year/', views.getYears),
    # path('projects/category/', views.getCatories),
    # path('projects/team/<str:teamId>/', views.teamDetailsapi),
    # path('projects/teams/', views.teams),
]

urlpatterns += router.urls
