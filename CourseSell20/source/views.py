from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic.edit import UpdateView
from .forms import UserForm
from .models import User
from django.views import View
from django.shortcuts import render, redirect
from .igdbAPi import IGDBAPI
from .forms import AddGameForm
from .models import Game


class GameListView(View):
    def get(self, request):
        games = Game.objects.all()
        return render(request, "source/shop.html", {"games": games})


class ProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name = "source/profile.html"
    success_url = reverse_lazy("profile")

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["balance"] = self.request.user.balance
        context["first_name"] = self.request.user.first_name
        context["last_name"] = self.request.user.last_name
        return context

    def form_valid(self, form):
        user = form.save(commit=False)
        new_password = form.cleaned_data.get("password")
        if new_password:
            user.password = make_password(new_password)
        user.save()
        messages.success(self.request, "Your profile has been updated successfully.")
        return super().form_valid(form)


class AddGameView(View):
    template_name = "source/add_game.html"

    def get(self, request):
        form = AddGameForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = AddGameForm(request.POST)
        if form.is_valid():
            igdb_api = IGDBAPI()
            game_id = form.cleaned_data["game_id"]
            price = form.cleaned_data["price"]
            igdb_api.add_game_to_database(game_id, price)
            return redirect("game_list")

        return render(request, self.template_name, {"form": form})


class BalanceView(LoginRequiredMixin, View):
    template_name = "source/balance.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        amount = int(request.POST.get('amount', 0))
        if amount > 0:
            user = request.user
            user.balance += amount
            user.save()
        return redirect("profile")


class CartListView(View):
    def get(self, request):
        return render(request, "source/cart.html")