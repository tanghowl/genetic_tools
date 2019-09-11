from django.shortcuts import render

# Create your views here.
# -*- coding: utf-8 -*-

from .compute_or import ComputeOR
from .querysite import QureyExist
from .compute_beta import ComputeBeta
from .query_ngs import QueryNgsQc


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
            ctx['raw'], ctx['head'], ctx['rlt'] = result
        except Exception as e:
            if raw_post['input'].strip():
                ctx['err'] = '亲，你输入的格式有错误...'
                ctx['raw'] = raw_input
            else:
                ctx['err'] = '亲，你什么都没有输入！'
            print(e)
    return render(request, "compute_beta.html", ctx)


def compute_or(request):
    ctx = {}
    raw_post = request.POST
    print('#######', raw_post)
    if request.POST:
        raw_input = '\t'.join(['Rsid', 'GT', 'freq', 'OR']) + '\r\n'
        raw_input += raw_post['input']
        try:
            result = ComputeOR(raw_input).cartesian_product()
            ctx['raw'], ctx['head'], ctx['rlt'] = result
        except Exception as e:
            if raw_post['input'].strip():
                ctx['err'] = '亲，你输入的格式有错误...'
                ctx['raw'] = raw_input
            else:
                ctx['err'] = '亲，你什么都没有输入！'
            print(e)
    return render(request, "compute_or.html", ctx)


def qurey_exist(request):
    ctx = {}
    raw_post = request.POST
    print('#### query_exist:', raw_post)
    if raw_post:
        chrom = raw_post['chr']
        pos = raw_post['pos']
        ctx['rlt'] = QureyExist(chrom, pos).merge()

    return render(request, 'query_gt.html', ctx)


def qurey_ngs_qc_info(request):
    ctx = {}
    raw_post = request.POST
    print('#######', raw_post)
    if request.POST:
        raw_input = raw_post['input']
        try:
            qnq = QueryNgsQc(raw_input)
            ctx['reads_qc_head'], ctx['reads_qc_info'] = qnq.get_reads_qc_info()
            ctx['interval_head'], ctx['interval_info'] = qnq.get_match_interval_info()
            ctx['unmap_head'], ctx['unmap_info'] = qnq.get_unmap_info()
            ctx['raw'] = raw_input
        except Exception as e:
            print(e)
            ...
    return render(request, "ngs_qc.html", ctx)
