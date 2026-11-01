from django.contrib import messages
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .models import Bouquet, Consultation, Occasions, Order, PromoCode

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


def save_consultation(request, template, context, redirect_url):
    item = Consultation(
        first_name=request.POST.get("fname", ""),
        phone_number=request.POST.get("tel", ""),
        confirmation=True,
    )
    try:
        item.full_clean()
    except ValidationError as error:
        return render(request, template, {**context, "errors": error.message_dict})
    item.save()
    messages.success(request, "Заявка на консультацию успешно отправлена")
    return redirect(redirect_url)


def index(request):
    context = {"bouquets": Bouquet.objects.all()[:3]}
    if request.method == "POST":
        return save_consultation(request, "index.html", context, reverse("flower:index") + "#consultation")
    return render(request, "index.html", context)


def card(request, pk):
    context = {"bouquet": get_object_or_404(Bouquet, pk=pk)}
    if request.method == "POST":
        return save_consultation(request, "card.html", context, reverse("flower:card", args=[pk]) + "#consultation")
    return render(request, "card.html", context)


def catalog(request):
    context = {"bouquets": Bouquet.objects.all()}
    if request.method == "POST":
        return save_consultation(request, "catalog.html", context, reverse("flower:catalog") + "#consultation")
    return render(request, "catalog.html", context)


def consultation(request):
    if request.method == "POST":
        return save_consultation(request, "consultation.html", {}, reverse("flower:consultation"))
    return render(request, "consultation.html")


def order(request, pk):
    bouquet = get_object_or_404(Bouquet, pk=pk)

    if request.method == "POST":
        item = Order(
            bouquet=bouquet,
            first_name=request.POST.get("fname", ""),
            phone_number=request.POST.get("tel", ""),
            address=request.POST.get("adres", ""),
            date_deliver=SLOTS.get(request.POST.get("orderTime"), ""),
            total_price=bouquet.price,
        )
        try:
            item.full_clean()
        except ValidationError as error:
            return render(
                request,
                "order.html",
                {"bouquet": bouquet, "errors": error.message_dict},
            )

        item.save()
        return redirect(reverse("flower:order_step") + f"?order_id={item.pk}")

    return render(request, "order.html", {"bouquet": bouquet})


def order_step(request):
    order_id = request.POST.get("order_id") or request.GET.get("order_id", "")
    order = Order.objects.filter(pk=order_id).first() if order_id.isdigit() else None

    if request.method == "POST":
        if not order:
            return render(request, "order-step.html", {"errors": {"order_id": ["Заказ не найден"]}})
        order.status = "WD"
        order.save()
        messages.success(request, "Оплата прошла успешно. Заказ принят в работу")
        return redirect(reverse("flower:order_step") + f"?order_id={order.pk}")

    if not order:
        return render(request, "order-step.html", {"order_id": order_id})

    context = {"order_id": order_id, "bouquet": order.bouquet, "price": order.total_price}
    promocode = request.GET.get("promocode", "")
    if promocode:
        promo = PromoCode.objects.filter(promo_code__iexact=promocode, is_active=True).first()
        if promo:
            order.total_price = round(order.bouquet.price * (100 - promo.procent_promo) / 100)
            order.save(update_fields=["total_price"])
            context["price"] = order.total_price
        else:
            context["errors"] = {"promocode": ["Промокод не найден"]}
    return render(request, "order-step.html", context)


def quiz(request):
    return render(request, "quiz.html", {"occasions": Occasions.objects.all()})


def quiz_step(request):
    return render(request, "quiz-step.html", {"occasion": request.GET.get("occasion", "")})


def result(request):
    bouquets = Bouquet.objects.all()
    occasion = request.GET.get("occasion", "")
    if occasion.isdigit():
        bouquets = bouquets.filter(occasions__id=occasion)
    if request.GET.get("budget") in BUDGETS:
        low, high = BUDGETS[request.GET["budget"]]
        bouquets = bouquets.filter(price__gte=low, price__lt=high)
    context = {"bouquet": bouquets.order_by("?").first() or Bouquet.objects.order_by("?").first()}
    if request.method == "POST":
        return save_consultation(request, "result.html", context, reverse("flower:result") + "#consultation")
    return render(request, "result.html", context)
