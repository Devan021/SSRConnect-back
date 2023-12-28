from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("user.urls")),
    path("", include("project.urls")),
]

urlpatterns = [path("api/", include(urlpatterns))]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# login
# register
# logout

# get profile - me query

# reset password
# forgot password
# update profile - name, password, profile pic
# get all students - admin and mentor only
# get all teams - admin and mentor only
# get all mentors - admin only
# get all projects
# get all projects by year
# get all projects by category
# get project by id
# get all teams by mentor - admin and mentor only
