from django.db import models


class Home(models.Model):
    headline = models.CharField(max_length=200)
    subheadline = models.TextField()
    hero_image = models.ImageField(upload_to="home/", blank=True, null=True)

    def __str__(self):
        return "Home Section"


class About(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    profile_image = models.ImageField(upload_to="about/", blank=True, null=True)

    def __str__(self):
        return self.title


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name}"

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to="projects/")
    github_link = models.URLField(blank=True, null=True)
    live_link = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title