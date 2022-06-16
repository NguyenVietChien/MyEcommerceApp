# from crawl.crawl.spiders.tipy import TipySpider
from .serializers import TodoSerializer
from rest_framework import viewsets
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
from django.http import JsonResponse, request
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

# configure_logging()
# settings = get_project_settings()
# runner = CrawlerRunner(settings)
# # runner.crawl(EcommerceSpiderSpider)
# runner.crawl(TipySpider)
# d = runner.join()
# d.addBoth(lambda _: reactor.stop())

# reactor.run()

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


class TodoView(viewsets.ModelViewSet):

    serializer_class = TodoSerializer
    product = Product.objects.filter(
        product_price__gte=20000, product_price__lte=200000)
    queryset = product


@csrf_exempt
@require_http_methods(['POST'])
def crawl(request):

    if request.method == 'POST':

        tikiUrl = request.POST.get('tikiUrl', None)
        shopeeUrl = request.POST.get('shopeeUrl', None)
        lazadaUrl = request.POST.get('lazadaUrl', None)
        configure_logging()

        settings = get_project_settings()
        runner = CrawlerRunner(settings)
        # runner.crawl(EcommerceSpiderSpider)
        # runner.crawl(TipySpider)
        d = runner.join()
        d.addBoth(lambda _: reactor.stop())

        reactor.run()

        return JsonResponse({'task_id': tikiUrl, 'status': 'started'})


@csrf_exempt
@require_http_methods(['POST'])
def filterProduct(request):

    if request.method == 'POST':

        fromPrice = request.POST.get('fromPrice', None)
        toPrice = request.POST.get('toPrice', None)
        product = Product.objects.filter(
            product_price__gte=fromPrice, product_price__lte=toPrice)
        data = serialize('json', product)
        obj = {'page_obj': product}
        return render(request, 'main.html', obj)

        # return HttpResponse(data, content_type="application/json")
