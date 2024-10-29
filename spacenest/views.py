from django.shortcuts import render, redirect
from django.db.models import Q
from .models import *
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
import requests
import os
from dotenv import load_dotenv
from django.http import HttpResponse

load_dotenv()


def index(request):
    properties = Property.objects.all()[:3]
    context = {"properties": properties}
    return render(request, "spacenest/index.html", context)


def property_list(request):
    properties = Property.objects.values_list(
        "id",
        "name",
        "listing_type",
        "price",
        "property_image",
        "parking",
        "bathroom",
        "bedroom",
    )

    if request.method == "GET":
        location = request.GET.get("location")
        min_price = request.GET.get("min-price")
        max_price = request.GET.get("max-price")
        listing_type = request.GET.get("listing-type")
        province = request.GET.get("province")

        filters = Q()

        if location:
            filters &= Q(location__icontains=location)
        if min_price:
            filters &= Q(price__gte=min_price)
        if max_price:
            filters &= Q(price__lte=max_price)
        if listing_type and listing_type != "all":
            filters &= Q(listing_type=listing_type)
        if province and province != "all":
            filters &= Q(province=province)
        properties = Property.objects.filter(filters)
    context = {"properties": properties}
    return render(request, "spacenest/properties.html", context)


def property(request, pk):
    property = Property.objects.get(id=pk)
    images = Image.objects.filter(property=property)
    is_favourite = False
    favourite = Favourite.objects.filter(property=property, user=request.user)
    if favourite:
        is_favourite = True
    else:
        is_favourite = False
    agent = property.owner
    properties = Property.objects.filter(
        Q(owner=agent) | Q(location=property.location)
    )[:3]
    if request.method == "POST":
        sender = request.user
        receiver = agent
        phone = request.POST.get("phone")
        date = request.POST.get("date")
        message = request.POST.get("message")
        if sender and receiver and phone and date and message:
            Mailbox.objects.create(
                sender=sender,
                receiver=receiver,
                phone=phone,
                date=date,
                message=message,
            )
        id = request.POST.get("property_id")
        if id:
            if not is_favourite:
                property = Property.objects.get(id=id)
                Favourite.objects.create(user=request.user, property=property)
                return redirect(f"/property/{id}")
            else:
                property = Property.objects.get(id=id)
                favourite = Favourite.objects.get(user=request.user, property=property)
                favourite.delete()
                return redirect(f"/property/{id}")
    context = {
        "properties": properties,
        "property": property,
        "agent": agent,
        "is_favourite": is_favourite,
        "images": images,
    }
    return render(request, "spacenest/property.html", context)


@login_required(login_url="login")
def add_property(request):
    agent = request.user
    user_membership = UserMembership.objects.select_related("user", "membership").get(
        user=agent
    )
    current_date = timezone.now()
    if current_date > user_membership.expiry:
        agent.is_agent = False
        agent.save()
        user_membership.delete()
        return redirect("pricing")
    else:
        allowed_listing = user_membership.membership.listing_count
        user_listed = (
            Property.objects.filter(owner=agent).select_related("owner").count()
        )
        print(allowed_listing, user_listed)
        if user_listed > allowed_listing:
            return HttpResponse("Count Exceeded")

    if request.method == "POST":
        name = request.POST["name"]
        location = request.POST["location"]
        province = request.POST["province"]
        listing_type = request.POST["listing_type"]
        price = request.POST["price"]
        image = request.FILES["image"]
        description = request.POST["description"]
        parking = request.POST["parking"]
        bathroom = request.POST["bathroom"]
        bedroom = request.POST["bedroom"]
        Property.objects.create(
            name=name,
            location=location,
            province=province,
            listing_type=listing_type,
            description=description,
            price=price,
            property_image=image,
            parking=parking,
            owner=request.user,
            bathroom=bathroom,
            bedroom=bedroom,
        )
        return redirect("properties")
    return render(request, "spacenest/add_property.html")


def add_images(request, pk):
    property = Property.objects.get(id=pk)
    images = Image.objects.filter(property=property)
    if request.method == "POST":
        image = request.FILES["image"]
        Image.objects.create(property=property, image=image)
        return redirect(f"/add-images/{pk}")
    context = {'images':images}
    return render(request, "spacenest/add_images.html", context)


@login_required(login_url="login")
def pricing(request):
    if request.user.is_agent:
        return redirect("index")
    KHALTI_SECRET_KEY = os.getenv("KHALTI_SECRET_KEY")
    URL = "https://a.khalti.com/api/v2/epayment/initiate/"
    if request.method == "POST":
        plan = request.POST["plan"]
        new_membership = Membership.objects.get(name=plan)
        user_membership = UserMembership.objects.create(
            user=request.user, membership=new_membership
        )
        payload = {
            "return_url": "http://localhost:8000/payment-success/",
            "website_url": "http://localhost:8000",
            "amount": int(new_membership.price * 100),
            "purchase_order_id": user_membership.id,
            "purchase_order_name": user_membership.user.full_name,
        }
        headers = {"Authorization": f"Key {KHALTI_SECRET_KEY}"}
        try:
            response = requests.post(URL, data=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
            return redirect(data["payment_url"])
        except requests.RequestException as e:
            print(f"Request to Khalti API failed: {e}")
    return render(request, "spacenest/pricing.html")


@login_required(login_url="login")
def payment_success(request):
    context = {}
    if request.method == "GET":
        try:
            status = request.GET.get("status")
            purchase_order_id = request.GET.get("purchase_order_id")
            if status.lower() == "completed":
                mem = UserMembership.objects.get(id=purchase_order_id)
                mem.payment_status = "completed"
                mem.save()
                Payment.objects.create(
                    pidx=request.GET.get("pidx"),
                    user_membership=mem,
                    txn_id=request.GET.get("transaction_id"),
                    amount=request.GET.get("total_amount"),
                )
                request.user.is_agent = True
                request.user.save()
                context["success"] = True
        except IntegrityError:
            pass

    return render(request, "spacenest/payment_success.html", context)


def agents(request):
    agent_list = User.objects.filter(is_agent=True)
    context = {"agents": agent_list}
    return render(request, "spacenest/agents.html", context)


def agent(request, pk):
    agent = User.objects.get(id=pk)
    if request.method == "POST":
        sender_id = request.POST["sender_id"]
        sender = User.objects.get(id=sender_id)
        title = request.POST["title"]
        content = request.POST["content"]
        Mailbox.objects.create(
            receiver=agent, sender=sender, title=title, content=content
        )
    properties = Property.objects.select_related("owner").filter(owner=agent)
    context = {"agent": agent, "properties": properties}
    return render(request, "spacenest/agent.html", context)


def edit_profile(request):
    user = request.user
    if request.method == "POST":
        name = request.POST["name"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        if request.FILES:
            image = request.FILES["image"]
            user.profile_image = image
        user.full_name = name
        user.email = email
        user.phone = phone
        user.save()
    context = {"user": user}
    return render(request, "spacenest/edit_profile.html", context)


def my_properties(request):
    properties = Property.objects.select_related("owner").filter(owner=request.user)
    context = {"properties": properties}
    return render(request, "spacenest/my_properties.html", context)


def edit_property(request, pk):
    property = Property.objects.get(id=pk)
    if request.method == "POST":
        name = request.POST["name"]
        location = request.POST["location"]
        province = request.POST["province"]
        listing_type = request.POST["listing_type"]
        price = request.POST["price"]
        description = request.POST["description"]
        parking = request.POST["parking"]
        bathroom = request.POST["bathroom"]
        bedroom = request.POST["bedroom"]
        if request.FILES:
            image = request.FILES["image"]
            property.property_image = (image,)
        property.name = name
        property.location = location
        property.province = province
        property.listing_type = listing_type
        property.description = description
        property.price = price
        property.parking = parking
        property.owner = request.user
        property.bathroom = bathroom
        property.bedroom = bedroom
        property.save()
        return redirect("my_properties")
    context = {"property": property}
    return render(request, "spacenest/edit_property.html", context)


def favourites(request):
    properties = Property.objects.select_related("owner").filter(
        favourite__user=request.user
    )
    context = {"properties": properties}
    return render(request, "spacenest/favourites.html", context)


def contact(request):
    if request.method == "POST":
        name = request.POST["name"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        message = request.POST["message"]
        Message.objects.create(name=name, email=email, phone=phone, message=message)
        return redirect("index")
    return render(request, "spacenest/contact.html")


def inbox(request):
    mails = Mailbox.objects.select_related("sender", "receiver").filter(
        receiver=request.user
    )
    context = {"mails": mails}
    return render(request, "spacenest/inbox.html", context)


def inbox_single(request, pk):
    if request.method == "POST":
        id = request.POST["id"]
        mail = Mailbox.objects.get(id=id)
        mail.delete()
        return redirect("inbox")
    mail = Mailbox.objects.select_related("sender", "receiver").get(id=pk)
    context = {"mail": mail}
    return render(request, "spacenest/inbox_single.html", context)
