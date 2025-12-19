from django.urls import path
from .views import HomeView, AboutView, ContactCreateView
from .views import ProjectListView, projects_page
urlpatterns = [
    path("home/", HomeView.as_view(), name="home"),
    path("about/", AboutView.as_view(), name="about"),
    path("contact/", ContactCreateView.as_view(), name="contact"),
    path("projects-api/", ProjectListView.as_view(), name="project-list-api"), # API
    path("projects/", projects_page, name="projects-page"), # HTML Page
]
