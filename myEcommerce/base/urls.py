from re import template
from django import views
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from .views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'tasks', TodoView, 'todo')

urlpatterns = [
    # path("", Ecommerce.as_view(), name='ecommerce_url'),

    path('', TemplateView.as_view(template_name='index.html'), name='ecommerce_url'),
    path('api/', include(router.urls))

    # re_path(r'^api/filter/', filterProduct, name='filter'),
    # re_path(r'^api/crawl/', crawl, name='crawl'),
    # path(
    #     "<int:page>",
    #     listing,
    #     name="terms-by-page"
    # ),
]
