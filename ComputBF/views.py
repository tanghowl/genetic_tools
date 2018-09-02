from django.shortcuts import render

# Create your views here.
# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.views.decorators import csrf
from .compute import Compute


def compute_freq(request):
    ctx = {}
    input = request.POST
    print('#######', input)
    if request.POST:
        raw_input = '\t'.join(['Rsid', 'GT', 'freq', 'beta']) + '\r\n'
        raw_input += request.POST['input']
        try:
            tt = Compute(raw_input).cartesian_product()
            ctx['raw'], ctx['rlt'] = tt
        except Exception as e:
            if input:
                ctx['rlt'] = '格式有误'
                ctx['raw'] = raw_input
            else:
                ctx['rlt'] = '亲，你什么都没有输入！'
            print(e)
    return render(request, "compute.html", ctx)
