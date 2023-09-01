import uuid
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
from django.views.generic import DetailView, ListView
from django.views.generic.edit import UpdateView
from .forms import UserForm
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.views import PasswordResetView
from .models import User, Order, Review
from django.core.mail import send_mail
from django.views import View
from django.shortcuts import redirect
from .igdbAPi import IGDBAPI
from .forms import AddGameForm
from .models import Game, Cart
from django.shortcuts import render
from django.urls import reverse_lazy


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
        amount = int(request.POST.get("amount", 0))
        if amount > 0:
            user = request.user
            user.balance += amount
            user.save()
        return redirect("profile")


class ProductDetailView(DetailView):
    model = Game
    template_name = "source/product-details.html"
    context_object_name = "game"
    pk_url_kwarg = "id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Получите отзывы для текущей игры
        reviews = Review.objects.filter(game=self.object)

        context["reviews"] = reviews
        return context


class AddToCartView(View):
    def post(self, request, *args, **kwargs):
        game_id = self.kwargs["game_id"]
        print(game_id)
        game = Game.objects.get(pk=game_id)
        cart, created = Cart.objects.get_or_create(user=request.user, game=game)
        if not created:
            cart.quantity += 1
            cart.save()
        return redirect("cart")


class RemoveFromCartView(View):
    def post(self, request, *args, **kwargs):
        cart_id = self.kwargs["cart_id"]
        cart = Cart.objects.get(pk=cart_id)
        if cart.quantity > 1:
            cart.quantity -= 1
            cart.save()
        else:
            cart.save()
        return redirect("cart")


class CartListView(ListView):
    template_name = "source/cart.html"
    model = Cart
    context_object_name = "carts"

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total_price = sum(cart.game.price * cart.quantity for cart in context["carts"])
        context["total_price"] = total_price
        return context


class RemoveCartItemView(View):
    def get(self, request, *args, **kwargs):
        cart_item = Cart.objects.get(pk=kwargs["pk"])
        cart_item.delete()
        return redirect("cart")


def send_game_key_email(user, game, game_key):
    subject = "Your Game Key"
    message = f"Here is your game key for {game.title}: {game_key}"
    from_email = "slappyyya@gmail.com"
    recipient_list = [user.email]
    send_mail(subject, message, from_email, recipient_list)


class CheckoutView(View):
    def post(self, request, *args, **kwargs):
        user = request.user
        cart_items = Cart.objects.filter(user=user)

        total_price = sum(item.game.price * item.quantity for item in cart_items)

        if user.balance >= total_price:
            for item in cart_items:
                game_key = str(uuid.uuid4())
                send_game_key_email(user, item.game, game_key)
                user.balance -= item.game.price
                user.save()

                order = Order.objects.create(
                    user=user,
                    game=item.game,
                    sum_order=item.game.price * item.quantity,
                    quantity=item.quantity,
                )
                item.delete()

            return redirect(
                "SuccessPay"
            )  # Перенаправьте на страницу успешного завершения покупки
        else:
            return redirect("NoBalance")


class SuccessPay(View):
    def get(self, request):
        return render(request, "source/successpay.html")


class NoBalance(View):
    def get(self, request):
        return render(request, "source/NoBalance.html")


class DashBoard(View):
    def get(self, request):
        return render(request, "source/dashboard.html")


class SubmitReviewView(View):
    def post(self, request, game_id, *args, **kwargs):
        user = request.user
        game = Game.objects.get(id=game_id)
        rating = int(request.POST.get("rating"))
        comment = request.POST.get("comment")

        review = Review.objects.create(
            user=user, game=game, rating=rating, comment=comment
        )

        return redirect("game_list")


class CustomPasswordResetView(PasswordResetView):
    email_template_name = "source/password_reset_email.html"
    success_url = reverse_lazy("password_reset_done")
    form_class = PasswordResetForm
