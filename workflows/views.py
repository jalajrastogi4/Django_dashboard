from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from . import utils
import json

# Create your views here.
def workflows(request):
    raw_list = utils.read_file()
    df_list = utils.create_df_list(raw_list)
    iteration_list = ['Iteration-' + str(i) for i in range(1, len(df_list)+1)]
    trust_iteration_list = df_list[0].TrustID.tolist()
    context = {'iteration_list': iteration_list, 'trust_iteration_list': trust_iteration_list}
    settings.result_df = df_list

    return render(request, 'workflows/workflows.html', context=context)


def iteration_chart(request):

    iteration_index = request.GET.get('iteration_index', None)
    iter_index = str(iteration_index).split('-')[1]
    df = settings.result_df[int(iter_index)-1]
    x = utils.make_chart(df)
    chart = x.to_json(indent=None)
    data = {'iteration_index': iteration_index, 'chart': chart}

    return JsonResponse(data)

def trust_chart(request):

    trust_id = request.GET.get('trust_id', None)
    trust_df = utils.trust_frame(settings.result_df, trust_id)
    x = utils.trust_chart(trust_df, trust_id)
    trust_chart = x.to_json(indent=None)
    data = {'trust_id': trust_id, 'trust_chart': trust_chart}
    # print(trust_id)

    return JsonResponse(data)

def examples(request):
    raw_list = utils.read_file()
    df_list = utils.create_df_list(raw_list)
    iteration_list = ['Iteration-' + str(i) for i in range(1, len(df_list)+1)]
    trust_iteration_list = df_list[0].TrustID.tolist()
    df = df_list[0]
    x = utils.make_chart(df)
    chart = x.to_json(indent=None)
    # print(chart)
    # spec = x.to_dict()
    context = {
        'iteration_list': iteration_list,
        'trust_iteration_list': trust_iteration_list,
        'chart': chart
    }

    return render(request, 'workflows/example.html', context=context)
