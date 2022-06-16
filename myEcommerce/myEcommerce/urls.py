# How to connect your project to your app?

from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
# from myEcommerce.base.views import TodoView

# router = routers.DefaultRouter()
# router.register(r'products', views.TodoView, 'todo')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('base.urls')),
    # path('api/', include(router.urls))
]
