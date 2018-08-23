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
        input = request.POST['input']
        try:
            tt = Compute(input).main()
            ctx['rlt'] = tt
            ctx['raw'] = input
        except Exception:
            if input:
                ctx['rlt'] = '格式有误'
                ctx['raw'] = input
            else:
                ctx['rlt'] = '亲，你什么都没有输入！'
    return render(request, "compute.html", ctx)
