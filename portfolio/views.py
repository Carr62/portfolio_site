from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from rest_framework import generics
from .models import Home, About, ContactMessage, Project
from .serializers import HomeSerializer, AboutSerializer, ContactMessageSerializer, ProjectSerializer

# --- HOME API ---
class HomeView(generics.RetrieveAPIView):
    queryset = Home.objects.all()
    serializer_class = HomeSerializer

    def get_object(self):
        return Home.objects.first()


# --- ABOUT API ---
class AboutView(generics.RetrieveAPIView):
    queryset = About.objects.all()
    serializer_class = AboutSerializer

    def get_object(self):
        return About.objects.first()


# --- CONTACT API (With Email Sending) ---
class ContactCreateView(generics.CreateAPIView):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer

    def perform_create(self, serializer):
        # 1. Save the message to the database
        instance = serializer.save()

        # 2. Prepare the email content
        subject = f"New Portfolio Message from {instance.name}"
        message_body = (
            f"You have received a new message via your portfolio website.\n\n"
            f"Name: {instance.name}\n"
            f"Email: {instance.email}\n\n"
            f"Message:\n{instance.message}"
        )
        
        # 3. Send the email
        try:
            send_mail(
                subject,
                message_body,
                settings.EMAIL_HOST_USER,
                ['dominicquainoo62@gmail.com'],  # Your email
                fail_silently=False,
            )
        except Exception as e:
            print(f"Error sending email: {e}")


# --- FRONTEND VIEW (This was missing) ---
def index(request):
    return render(request, 'home.html')

# --- PROJECT API ---
class ProjectListView(generics.ListAPIView):
    queryset = Project.objects.all().order_by('-created_at')
    serializer_class = ProjectSerializer

# --- FRONTEND VIEW FOR PROJECTS PAGE ---
def projects_page(request):
    return render(request, 'projects.html')