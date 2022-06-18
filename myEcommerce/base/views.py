# from crawl.crawl.spiders.tipy import TipySpider
import this
from rest_framework.decorators import action
from rest_framework.decorators import api_view
from .serializers import TodoSerializer
from rest_framework import viewsets, status
from rest_framework.pagination import PageNumberPagination
from rest_framework import pagination
from rest_framework.response import Response

from django.views.generic import ListView
from django.http import HttpResponse
from django.core.serializers import serialize
from uuid import uuid4
from urllib.parse import urlparse
from http import HTTPStatus
from django.forms.models import model_to_dict
from django.shortcuts import redirect, render
from itertools import product
from urllib import response
from django.shortcuts import render
from django.views.generic import View
from requests import request
from django.core import serializers
# from .models import Friend
from django.http import JsonResponse, request, response
from .models import *
from django.db.models import Sum
from django.core.paginator import Paginator
from scrapy.crawler import CrawlerProcess
from twisted.internet import reactor
# from crawl.crawl.spiders.tipy import *

from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging
from scrapy.crawler import CrawlerRunner
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from scrapyd_api import ScrapydAPI


scrapyd = ScrapydAPI('http://localhost:6800')


def is_valid_url(url):
    validate = URLValidator()
    try:
        validate(url)
    except ValidationError:
        return False

    return True


class SchedulingError(Exception):
    def __str__(self):
        return 'scheduling error'


class Ecommerce(View):

    paginate_by = 20
    model = Product

    def get(self, request):
        obj = {
            'page_obj': Product.objects.all(),
            'total':  Product.objects.all().count(),
            'total_price': Product.objects.aggregate(Sum('product_price')),
            'rating_5_star': Product.objects.aggregate(Sum('rating_5_star')),
            'rating_4_star': Product.objects.aggregate(Sum('rating_4_star')),
            'rating_3_star': Product.objects.aggregate(Sum('rating_3_star')),
            'rating_2_star': Product.objects.aggregate(Sum('rating_2_star')),
            'rating_1_star': Product.objects.aggregate(Sum('rating_1_star')),
        }

        return render(request, 'main.html', obj)


def listing(request, page):
    keywords = Product.objects.all()
    paginator = Paginator(keywords, per_page=20)
    page_object = paginator.get_page(page)
    page_object.adjusted_elided_pages = paginator.get_elided_page_range(page)
    context = {"page_obj": page_object}
    return render(request, 'main.html', context)


class CustomPagination(pagination.PageNumberPagination):
    page_size = 40
    page_size_query_param = 'page_size'
    max_page_size = 1000
    page_query_param = 'p'

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'results': data
        })

    # def get_page_size(self, request):
    #     # if self.page_size_query_param:
    #     # print(request)
    #     # data = serializers.serialize(self.page_size)
    #     return self.page_size


class TodoView(viewsets.ModelViewSet):

    queryset = Product.objects.all().order_by('product_name')

    pagination_class = CustomPagination

    serializer_class = TodoSerializer

    @action(detail=False, methods=['post'])
    def set_query(self, request, pk=None):
        fromPrice = request.data.get('price').get('fromPrice')

        toPrice = request.data.get('price').get('toPrice', 1200000)

        recent_users = Product.objects.filter(
            product_price__gte=fromPrice, product_price__lte=toPrice).order_by('product_name')

        print(recent_users.count())
        self.queryset = recent_users

        # serializer = self.get_serializer(recent_users, many=True)

        # self.queryset.save()
        page = self.paginate_queryset(recent_users)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(recent_users, many=True)

        print(self.queryset.count())
        return Response(serializer.data, status=status.HTTP_200_OK)


class TodoView2(viewsets.ModelViewSet):

    serializer_class = TodoSerializer
    product = Product.objects.all().order_by('product_name')
    # pagination_class = CustomPagination
    queryset = product


@api_view(['POST'])
# @require_http_methods(['POST'])
def crawl(request):

    if request.method == 'POST':
        # print(request.data)
        tikiUrl = request.data

        return JsonResponse({'url': tikiUrl})

        # shopeeUrl = request.POST.get('shopeeUrl', None)
        # lazadaUrl = request.POST.get('lazadaUrl', None)
        # configure_logging()

        # settings = get_project_settings()
        # runner = CrawlerRunner(settings)
        # runner.crawl(EcommerceSpiderSpider)
        # runner.crawl(TipySpider)
        # d = runner.join()
        # d.addBoth(lambda _: reactor.stop())

        # reactor.run()

        # print(request.data)


# @csrf_exempt
@api_view(['POST'])
# @require_http_methods(['POST'])
def filterProduct(request):

    if request.method == 'POST':

        fromPrice = request.data.get('price').get('fromPrice')

        toPrice = request.data.get('price').get('toPrice', 1200000)

        product2 = Product.objects.filter(
            product_price__gte=fromPrice, product_price__lte=toPrice).order_by('product_name')
        TodoView.queryset = product2

        return JsonResponse({'fromPrice': fromPrice, 'toPrice': toPrice})
