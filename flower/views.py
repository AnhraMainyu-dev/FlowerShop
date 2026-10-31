import phonenumbers
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .models import Bouquet, Consultation, Occasions, Order

BUDGETS = {
    "low": (0, 1000),
    "mid": (1000, 5000),
    "high": (5000, 999999),
}

SLOTS = {
    "Как можно скорее": "FA",
    "с 10:00 до 12:00": "MO",
    "с 12:00 до 14:00": "PO",
    "с 14:00 до 16:00": "BR",
    "с 16:00 до 18:00": "PB",
    "с 18:00 до 20:00": "PM",
}


def index(request):
    if request.method == "POST":
        item = Consultation(
            first_name=request.POST.get("fname", ""),
            phone_number=request.POST.get("tel", ""),
            confirmation=True,
        )
        try:
            item.full_clean()
        except ValidationError as error:
            return render(request, "index.html", {"bouquets": Bouquet.objects.all()[:3], "errors": error.message_dict})
        item.save()
        messages.success(request, "Заявка на консультацию успешно отправлена")
        return redirect(reverse("flower:index") + "#consultation")

    return render(request, "index.html", {"bouquets": Bouquet.objects.all()[:3]})


def card(request, pk):
    bouquet = get_object_or_404(Bouquet, pk=pk)

    if request.method == "POST":
        item = Consultation(
            first_name=request.POST.get("fname", ""),
            phone_number=request.POST.get("tel", ""),
            confirmation=True,
        )
        try:
            item.full_clean()
        except ValidationError as error:
            return render(request, "card.html", {"bouquet": bouquet, "errors": error.message_dict})
        item.save()
        messages.success(request, "Заявка на консультацию успешно отправлена")
        return redirect(reverse("flower:card", args=[pk]) + "#consultation")

    return render(request, "card.html", {"bouquet": bouquet})


def catalog(request):
    if request.method == "POST":
        item = Consultation(
            first_name=request.POST.get("fname", ""),
            phone_number=request.POST.get("tel", ""),
            confirmation=True,
        )
        try:
            item.full_clean()
        except ValidationError as error:
            return render(request, "catalog.html", {"bouquets": Bouquet.objects.all(), "errors": error.message_dict})
        item.save()
        messages.success(request, "Заявка на консультацию успешно отправлена")
        return redirect(reverse("flower:catalog") + "#consultation")

    return render(request, "catalog.html", {"bouquets": Bouquet.objects.all()})


def consultation(request):
    if request.method == "POST":
        item = Consultation(
            first_name=request.POST.get("fname", ""),
            phone_number=request.POST.get("tel", ""),
            confirmation=True,
        )
        try:
            item.full_clean()
        except ValidationError as error:
            return render(request, "consultation.html", {"errors": error.message_dict})
        item.save()
        messages.success(request, "Заявка на консультацию успешно отправлена")
        return redirect(reverse("flower:consultation"))

    return render(request, "consultation.html")


def order(request, pk):
    bouquet = get_object_or_404(Bouquet, pk=pk)

    if request.method == "POST":
        try:
            parsed = phonenumbers.parse(request.POST["tel"], "RU")
        except phonenumbers.NumberParseException:
            return render(
                request,
                "order.html",
                {"bouquet": bouquet, "errors": {"phone_number": ["Введите корректный номер телефона"]}},
            )

        if not phonenumbers.is_valid_number(parsed):
            return render(request, "order.html", {"bouquet": bouquet, "errors": {"phone_number": ["Неверный номер"]}})

        item = Order(
            bouquet=bouquet,
            first_name=request.POST.get("fname", ""),
            phone_number=request.POST.get("tel", ""),
            address=request.POST.get("adres", ""),
            date_deliver=SLOTS.get(request.POST.get("orderTime"), ""),
        )

        try:
            item.full_clean()
        except ValidationError as error:
            return render(request, "order.html", {"bouquet": bouquet, "errors": error.message_dict})

        item.save()
        return redirect(f"/order-step/?order_id={item.id}")

    return render(request, "order.html", {"bouquet": bouquet})


def order_step(request):
    if request.method == "POST":
        order_id = request.POST.get("order_id")

        if order_id:
            try:
                order = Order.objects.get(id=order_id)
                order.status = "WD"
                order.save()
            except Order.DoesNotExist:
                pass

        messages.success(request, "Оплата прошла успешно. Заказ принят в работу")
        return redirect(reverse("flower:order_step"))

    order_id = request.GET.get("order_id", "")
    return render(request, "order-step.html", {"order_id": order_id})


def quiz(request):
    return render(request, "quiz.html", {"occasions": Occasions.objects.all()})


def quiz_step(request):
    return render(request, "quiz-step.html", {"occasion": request.GET.get("occasion", "")})


def result(request):
    if request.method == "POST":
        item = Consultation(
            first_name=request.POST.get("fname", ""),
            phone_number=request.POST.get("tel", ""),
            confirmation=True,
        )
        try:
            item.full_clean()
        except ValidationError as error:
            bouquets = Bouquet.objects.all()
            occasion = request.GET.get("occasion", "")
            if occasion.isdigit():
                bouquets = bouquets.filter(occasions=occasion)
            if request.GET.get("budget") in BUDGETS:
                low, high = BUDGETS[request.GET["budget"]]
                bouquets = bouquets.filter(price__gte=low, price__lt=high)
            bouquet = bouquets.order_by("?").first() or Bouquet.objects.order_by("?").first()
            return render(request, "result.html", {"bouquet": bouquet, "errors": error.message_dict})
        item.save()
        messages.success(request, "Заявка на консультацию успешно отправлена")
        return redirect(reverse("flower:result") + "#consultation")

    bouquets = Bouquet.objects.all()
    occasion = request.GET.get("occasion", "")
    if occasion.isdigit():
        bouquets = bouquets.filter(occasions__id=occasion)
    if request.GET.get("budget") in BUDGETS:
        low, high = BUDGETS[request.GET["budget"]]
        bouquets = bouquets.filter(price__gte=low, price__lt=high)
    bouquet = bouquets.order_by("?").first() or Bouquet.objects.order_by("?").first()
    return render(request, "result.html", {"bouquet": bouquet})
