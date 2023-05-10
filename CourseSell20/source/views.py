from django.shortcuts import render
from django.views import View


def main(request):
    return render(request, "source/shop.html")

def profile(request):
    return render(request, "source/profile.html")
