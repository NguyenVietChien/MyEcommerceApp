# from crawl.crawl.spiders.tipy import TipySpider
from rest_framework import filters
from rest_framework import generics
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

from rest_framework import generics
import django_filters.rest_framework

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

    @action(detail=False, methods=['get'])
    def set_query(self, request, pk=None):
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

        product = Product.objects.all()

        serializer = self.get_serializer(obj, many=True)

        return JsonResponse({'total':  Product.objects.all().count(),
                             'total_price': Product.objects.aggregate(Sum('product_price')),
                             'total_comments': Product.objects.aggregate(Sum('total_comments')),
                             })


class PurchaseList(generics.ListAPIView):

    serializer_class = TodoSerializer

    pagination_class = CustomPagination

    filter_backends = [filters.SearchFilter]
    search_fields = ['product_name']

    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['product_name', 'product_price',
                       'rating_point', 'total_comments']

    def get_queryset(self):
        queryset = Product.objects.all()
        # fromPrice = self.request
        minPrice = self.request.query_params.get('minPrice')
        maxPrice = self.request.query_params.get('maxPrice')
        ordering = self.request.query_params.get('ordering')
        if ordering is None:
            ordering = 'product_price'
        else:
            ordering = '-' + ordering
        if minPrice is not None and maxPrice is not None:
            queryset = queryset.filter(
                product_price__gte=minPrice, product_price__lte=maxPrice)
        queryset = queryset.order_by(ordering)
        print(ordering)
        return queryset


@api_view(['POST'])
# @require_http_methods(['POST'])
def crawl(request):
    if request.method == 'POST':
        # print(request.data)
        tikiUrl = request.data.get('tikiUrl')
        shopeeUrl = request.data.get('shopeeUrl')
        lazadaUrl = request.data.get('lazadaUrl')

        url = tikiUrl
        if not url:
            return JsonResponse(
                {'error': 'URL 없음'},
                status=HTTPStatus.BAD_REQUEST
            )
        if not is_valid_url(url):
            return JsonResponse(
                {'error': 'URL 유효하지 않음'},
                status=HTTPStatus.BAD_REQUEST
            )
        domain = urlparse(url).netloc
        unique_id = str(uuid4())

        settings = {
            'unique_id': unique_id,
            'USER_AGENT': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
        }
        try:
            task = scrapyd.schedule(
                'default', 'tikipy',
                settings=settings,
                url=url.encode('utf8'),
                domain=domain
            )
        except SchedulingError as e:
            return JsonResponse(
                {'error': e},
                status=HTTPStatus.INTERNAL_SERVER_ERROR
            )
        return JsonResponse({'task_id': task,
                             'unique_id': unique_id,
                             'status': 'started',
                             'url': url})


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
