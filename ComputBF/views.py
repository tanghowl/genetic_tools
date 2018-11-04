from django.shortcuts import render

# Create your views here.
# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.views.decorators import csrf
from .compute_or import ComputeOR
from .querysite import QureyExist
from .compute_beta import ComputeBeta

def get_home(request):
    return render(request, "home.html")


def compute_beta(request):
    ctx = {}
    raw_post = request.POST
    print('#######', raw_post)
    if request.POST:
        raw_input = '\t'.join(['Rsid', 'GT', 'freq', 'beta']) + '\r\n'
        raw_input += raw_post['input']
        try:
            result = ComputeBeta(raw_input).cartesian_product()
            ctx['raw'], ctx['rlt'] = result
        except Exception as e:
            if raw_post['input'].strip():
                ctx['rlt'] = '亲，你输入的格式有错误...'
                ctx['raw'] = raw_input
            else:
                ctx['rlt'] = '亲，你什么都没有输入！'
            print(e)
    return render(request, "compute.html", ctx)

def compute_or(request):
    ctx = {}
    raw_post = request.POST
    print('#######', raw_post)
    if request.POST:
        raw_input = '\t'.join(['Rsid', 'GT', 'freq', 'OR']) + '\r\n'
        raw_input += raw_post['input']
        try:
            result = ComputeOR(raw_input).cartesian_product()
            ctx['raw'], ctx['rlt'] = result
        except Exception as e:
            if raw_post['input'].strip():
                ctx['rlt'] = '亲，你输入的格式有错误...'
                ctx['raw'] = raw_input
            else:
                ctx['rlt'] = '亲，你什么都没有输入！'
            print(e)
    return render(request, "compute.html", ctx)


def qurey_exist(request):
    ctx = {}
    raw_post = request.POST
    print('#### query_exist:', raw_post)
    if raw_post:
        chrom = raw_post['chr']
        pos = raw_post['pos']
        ctx['rlt'] = QureyExist(chrom, pos).merge()

    return render(request, 'query_gt.html', ctx)
