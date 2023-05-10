from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework import permissions
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import CustomUserCreationForm
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.views import View
from django.http import JsonResponse
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import MyTokenObtainPairSerializer


class MyTokenRefreshView(TokenRefreshView):
    pass


class RegisterView(CreateView):
    """
    View for handling register page.
    """
    form_class = CustomUserCreationForm
    template_name = "source/register.html"
    success_url = reverse_lazy("login")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form_class()
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.is_active = True
        self.object.save()
        return response


class MyTokenObtainPairView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]
    serializer_class = MyTokenObtainPairSerializer


class LoginView(View):
    """
    View for handling login page.
    """

    def get(self, request):
        return render(request, "source/login.html")

    def post(self, request):
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, email=email, password=password)
        if user is not None:
            token_obtain_pair = MyTokenObtainPairView.as_view()(request).data
            login(request, user)
            request.session["refresh_token"] = token_obtain_pair["refresh"]
            return redirect("main")
        else:
            return JsonResponse({"error": "Invalid credentials"})
