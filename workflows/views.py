from django.shortcuts import render
from django.http import JsonResponse
from django.urls import resolve
from django.conf import settings
from .models import Workflow
from . import utils
import json
import os
import pandas as pd

# Create your views here.
def workflows(request):

    workflow_objects = Workflow.objects.all()
    workflow_testlist = [w.name.lower().replace(" ", '-') for w in workflow_objects]

    workflow_filepath_list = []
    for dir_name in workflow_testlist:
        workflow_filepath_list.append(utils.read_file(dir_name))

    workflow_filepath_list_dropnone = [i for i in workflow_filepath_list if i]
    chart_list = [None for i in workflow_filepath_list]
    
    count = 0
    for fname in workflow_filepath_list_dropnone:
        raw_list = utils.create_raw_list(fname)
        df_list = utils.create_df_list(raw_list)
        iteration_list = ['Run-' + str(i) for i in range(1, len(df_list)+1)]
        x = utils.max_iteration_time(iteration_list, df_list)
        chart = x.to_json(indent=None)
        chart_list[count] = chart
        count += 1

    # raw_list = utils.read_file()
    # print(raw_list)
    # df_list = utils.create_df_list(raw_list)
    # iteration_list = ['Iteration-' + str(i) for i in range(1, len(df_list)+1)]
    # trust_iteration_list = df_list[0].TrustID.tolist()
    context = {
        'workflow_objects': workflow_objects,
        'chart_list' : chart_list
    }
    # context = {'iteration_list': iteration_list, 'trust_iteration_list': trust_iteration_list}
    # settings.result_df = df_list

    return render(request, 'workflows/workflows.html', context=context)


def dailyworkflow(request):
    workflow_objects = Workflow.objects.all()
    workflow_names = [w.name for w in workflow_objects]
    workflow_url = [ w.slug for w in workflow_objects]
    current_url = resolve(request.path_info).url_name
    workflow_filepath = ""
    for i in workflow_url:
        if i == current_url:
            workflow_filepath = utils.read_file(i)

    fname = os.path.basename(workflow_filepath)
    client = os.path.splitext(fname)[0].split('_')[0]

    raw_list = utils.create_raw_list(workflow_filepath)
    df_list = utils.create_df_list(raw_list)
    settings.result_df = df_list

    # Iteration list df for tables
    iteration_df = utils.max_iteration_df(df_list)
    iteration_list = iteration_df['Iterations'].tolist()
    iteration_time = iteration_df['Time (in sec)'].tolist()

    # Trust List and max time list for tables
    max_trusttime_df = utils.max_trust_df(df_list)
    trust_list = max_trusttime_df.index.tolist()
    max_time_list = max_trusttime_df['Time(in sec)'].tolist()
    trust_time_chart = utils.max_trust_time_chart(max_trusttime_df, "Trust vs Maximum Time")
    trust_time_json = trust_time_chart.to_json(indent=None)

    # Count for Top cards
    iteration_count = len(df_list)
    trust_count = len(df_list[0])
    
    workflow_zip = zip(workflow_names, workflow_url)
    context = {
        'workflow_objects': workflow_zip,
        'client': client,
        'trust_count': trust_count,
        'iteration_count': iteration_count,
        'max_trusttime': zip(trust_list, max_time_list),
        'trust_time_chart': trust_time_json,
        'max_runtime': zip(iteration_list, iteration_time)
    }
    return render(request, 'workflows/daily-workflow.html', context=context)


def alltrusts(request):
    workflow_objects = Workflow.objects.all()
    workflow_names = [w.name for w in workflow_objects]
    workflow_url = [ w.slug for w in workflow_objects]

    result = settings.result_df
    x = utils.all_trust_chart(result)
    chart = x.to_json(indent=None)

    context = {
        'workflow_objects': zip(workflow_names, workflow_url),
        'chart': chart
    }

    return render(request, 'workflows/all-trusts.html', context=context)


def alliterations(request):
    workflow_objects = Workflow.objects.all()
    workflow_names = [w.name for w in workflow_objects]
    workflow_url = [ w.slug for w in workflow_objects]

    result = settings.result_df
    x = utils.all_iteration_chart(result)
    chart = x.to_json(indent=None)

    context = {
        'workflow_objects': zip(workflow_names, workflow_url),
        'chart': chart
    }

    return render(request, 'workflows/all-trusts.html', context=context)


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
