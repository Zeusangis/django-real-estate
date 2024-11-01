from django.urls import path
from .views import *

urlpatterns = [
    path("", index, name="index"),
    path("properties/", property_list, name="properties"),
    path("property/<str:pk>/", property, name="property"),
    path("my-properties/", my_properties, name="my_properties"),
    path("pricing/", pricing, name="pricing"),
    path("agents/", agents, name="agents"),
    path("edit-property/<str:pk>", edit_property, name="edit_property"),
    path("add-images/<str:pk>", add_images, name="add_images"),
    path("agent/<str:pk>", agent, name="agent"),
    path("contact/", contact, name="contact"),
    path("payment-success/", payment_success, name="payment_success"),
    path("add-property/", add_property, name="add-property"),
    path("edit-profile/", edit_profile, name="edit-profile"),
    path("favourites/", favourites, name="favourites"),
    path("inbox/", inbox, name="inbox"),
    path("inbox-single/<str:pk>", inbox_single, name="inbox_single"),
    path("expired/", expired, name="expired"),
]
