"""authors URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import url, include
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import include, path
from django.contrib import admin

from rest_framework_swagger.views import get_swagger_view

# Create schema view.
# Responsible for generating and rendering the JSON spec and rendering the UI
schema_view = get_swagger_view(title="Authors Haven API Documentation")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('authors.apps.authentication.urls',
                         namespace='authentication')),
    path('api/articles/', include('authors.apps.articles.urls', namespace='articles')),
    path('', schema_view),
    path('api/', include('authors.apps.profiles.urls', namespace='profiles')),
]
