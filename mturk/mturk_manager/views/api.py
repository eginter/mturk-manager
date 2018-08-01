import urllib.parse
from django.http import JsonResponse
from mturk_manager.models import *
from viewer.models import *
from mturk_manager.views import code_shared
import json, time
from django.db.models import F, Value, Count, Q, Sum, IntegerField, ExpressionWrapper


def balance(request, slug_project):
    try:
        use_sandbox = False if urllib.parse.parse_qs(request.META['QUERY_STRING'])['use_sandbox'][0] == 'false' else True
    except KeyError:
        use_sandbox = True

    db_obj_project = m_Project.objects.get(
        slug=slug_project
    )
    return JsonResponse({
        'balance': float(code_shared.get_client(db_obj_project, use_sandbox=use_sandbox).get_account_balance()['AvailableBalance'])
    })

def api(request, name):
    name_quoted = name
    name_project = urllib.parse.unquote(name_quoted)
    db_obj_project = m_Project.objects.get(
        name=name_project
    )

    if request.method == 'POST':
        if request.POST['task'] == 'unblock_workers':
            unblock_workers(request, db_obj_project)
        elif request.POST['task'] == 'block_workers':
            block_workers(request, db_obj_project)
        elif request.POST['task'] == 'approve_assignments_selected':
            approve_assignments_selected(request, db_obj_project)
            block_workers(request, db_obj_project)
        elif request.POST['task'] == 'reject_assignments_selected':
            reject_assignments_selected(request, db_obj_project)

    return JsonResponse({})

def api_assignments_real_approved_for_batch(request, name, name_batch):
    dict_result = {}

    queryset = m_Assignment.objects.filter(
        fk_hit__fk_batch__fk_project__name=name,
        fk_hit__fk_batch__use_sandbox=False,
        corpus_viewer_tags__name='approved',
        fk_hit__fk_batch__name=name_batch,
    )

    list_assignments = [assignment.id_assignment for assignment in queryset]

    dict_result['success'] = True
    dict_result['assignments'] = list_assignments
    dict_result['count_assignments'] = len(list_assignments)
    return JsonResponse(dict_result)

def api_assignments_real_approved(request, name):
    dict_result = {}
 
    queryset = m_Assignment.objects.filter(
        fk_hit__fk_batch__fk_project__name=name,
        fk_hit__fk_batch__use_sandbox=False,
        corpus_viewer_tags__name='approved'
    )

    list_assignments = [assignment.id_assignment for assignment in queryset]

    dict_result['success'] = True
    dict_result['assignments'] = list_assignments
    dict_result['count_assignments'] = len(list_assignments)
    return JsonResponse(dict_result)

def api_assignments_real_approved_tmp(request, slug_project):
    try:
        use_sandbox = False if urllib.parse.parse_qs(request.META['QUERY_STRING'])['use_sandbox'][0] == 'false' else True
    except KeyError:
        use_sandbox = True
    
    dict_batches = {}
    list_hits = []

    queryset = m_Hit.objects.filter(
        fk_batch__fk_project__slug=slug_project,
        fk_batch__use_sandbox=use_sandbox,
        # fk_batch__use_sandbox=False,
    ).select_related(
        'fk_batch'
    ).annotate(
        count_assignments_approved=Count('assignments', filter=Q(
            # fk_batch__use_sandbox=False,
            assignments__corpus_viewer_tags__name='approved',
        ), distinct=True),
        count_assignments_rejected=Count('assignments', filter=Q(
            # fk_batch__use_sandbox=False,
            assignments__corpus_viewer_tags__name='rejected',
        ), distinct=True),

    ).order_by('-datetime_creation')
    
    for obj_db_hit in queryset:
        if not obj_db_hit.fk_batch.name in dict_batches:
            dict_batches[obj_db_hit.fk_batch.name] = {
                'id': obj_db_hit.fk_batch.name,
                'reward': float(obj_db_hit.fk_batch.reward),
                'count_assignments_per_hit': obj_db_hit.fk_batch.count_assignments,
            }

        list_hits.append({
            'id_batch': obj_db_hit.fk_batch.name,    
            'id_hit': obj_db_hit.id_hit,
            'count_assignments_approved': obj_db_hit.count_assignments_approved,
            'count_assignments_rejected': obj_db_hit.count_assignments_rejected,
            'datetime_creation': obj_db_hit.datetime_creation,
        })   
    # time.sleep(3)
    
    # queryset = m_Assignment.objects.filter(
    #     fk_hit__fk_batch__fk_project__name=name,
    #     fk_hit__fk_batch__use_sandbox=False,
    #     corpus_viewer_tags__name='approved'
    # ).select_related(
    #     'fk_hit__fk_batch'
    # ).order_by('fk_hit__datetime_creation')




    # for assignment in queryset:
    #     list_result.append({
    #         'id_assigment': assignment.id_assignment,
    #         'datetime_creation': assignment.fk_hit.datetime_creation,
    #         'id_hit': assignment.fk_hit.id_hit,
    #         'id_batch': assignment.fk_hit.fk_batch.name,
    #     })

    return JsonResponse({
        'dict_batches': dict_batches, 
        'list_hits': list_hits, 
    }, safe=False)

def api_assignment(request, name, id_assignment):
    dict_result = {}
 
    obj_db_assignment = m_Assignment.objects.get(
        id_assignment=id_assignment
    )


    dict_result['success'] = True
    dict_result['answer'] = obj_db_assignment.answer
    return JsonResponse(dict_result)

def api_assignments_real(request, name):
    dict_result = {}
 
    queryset = m_Assignment.objects.filter(
        fk_hit__fk_batch__fk_project__name=name,
        fk_hit__fk_batch__use_sandbox=False,
    )

    list_assignments = [assignment.id_assignment for assignment in queryset]

    dict_result['success'] = True
    dict_result['assignments'] = list_assignments
    dict_result['count_assignments'] = len(list_assignments)
    return JsonResponse(dict_result)

def api_assignments_fake(request, name):
    dict_result = {}
 
    queryset = m_Assignment.objects.filter(
        fk_hit__fk_batch__fk_project__name=name,
        fk_hit__fk_batch__use_sandbox=True,
    )

    list_assignments = [assignment.id_assignment for assignment in queryset]

    dict_result['success'] = True
    dict_result['assignments'] = list_assignments
    dict_result['count_assignments'] = len(list_assignments)
    return JsonResponse(dict_result)

def api_status_worker(request, name, id_worker):
    dict_result = {} 

    try:
        db_obj_worker = m_Worker.objects.get(name=id_worker, fk_project__name=name)
    except m_Worker.DoesNotExist:
        dict_result['success'] = False
    else:
        dict_result['success'] = True
        dict_result['blocked'] = db_obj_worker.is_blocked
    finally:
        response_json = JsonResponse(dict_result)
        response_json['Access-Control-Allow-Origin'] = '*'
        return response_json

def approve_assignments_selected(request, db_obj_project):
    list_ids = request.POST.getlist('list_ids[]')
    
    db_obj_tag_submitted = m_Tag.objects.get(key_corpus=db_obj_project.name, name='submitted')
    db_obj_tag_approved = m_Tag.objects.get(key_corpus=db_obj_project.name, name='approved')
    db_obj_tag_rejected = m_Tag.objects.get(key_corpus=db_obj_project.name, name='rejected')
    
    for assignment in m_Assignment.objects.filter(id__in=list_ids):
        db_obj_tag_submitted.corpus_viewer_items.remove(assignment)
        db_obj_tag_rejected.corpus_viewer_items.remove(assignment)
        db_obj_tag_approved.corpus_viewer_items.add(assignment)

def reject_assignments_selected(request, db_obj_project):
    list_ids = request.POST.getlist('list_ids[]')
    
    db_obj_tag_submitted = m_Tag.objects.get(key_corpus=db_obj_project.name, name='submitted')
    db_obj_tag_approved = m_Tag.objects.get(key_corpus=db_obj_project.name, name='approved')
    db_obj_tag_rejected = m_Tag.objects.get(key_corpus=db_obj_project.name, name='rejected')
    
    for assignment in m_Assignment.objects.filter(id__in=list_ids):
        db_obj_tag_submitted.corpus_viewer_items.remove(assignment)
        db_obj_tag_approved.corpus_viewer_items.remove(assignment)
        db_obj_tag_rejected.corpus_viewer_items.add(assignment)

def unblock_workers(request, db_obj_project):
    list_ids = request.POST.getlist('list_ids[]')

    m_Worker.objects.filter(
        fk_project=db_obj_project,
        id__in=list_ids
    ).update(is_blocked=False)

def block_workers(request, db_obj_project):
    list_ids = request.POST.getlist('list_ids[]')

    m_Worker.objects.filter(
        fk_project=db_obj_project,
        id__in=list_ids
    ).update(is_blocked=True)
# WORKERS #################################


def api_workers(request, name):
    dict_result = {}
 
    queryset = m_Worker.objects.filter(
        assignments__fk_hit__fk_batch__fk_project__name=name,
        assignments__fk_hit__fk_batch__use_sandbox=False,
    )

    list_workers = [{'name': worker.name} for worker in queryset]

    dict_result['success'] = True
    dict_result['workers'] = list_workers
    dict_result['count_workers'] = len(list_workers)
    return JsonResponse(dict_result)

    # name_quoted = name
    # name_project = urllib.parse.unquote(name_quoted)
    # db_obj_project = m_Project.objects.get(
    #     name=name_project
    # )

    # response = {}

    # client = code_shared.get_client(db_obj_project, use_sandbox=True)
    # # client = code_shared.get_client(db_obj_project, use_sandbox=False)

    # if request.method == 'GET':
    #     response = client.list_qualification_types(
    #         MustBeRequestable=False,
    #         MustBeOwnedByCaller=True,
    #     )
    #     response = response['QualificationTypes']

    # elif request.method == 'POST':
    #     print(request.POST)
    #     response = client.create_qualification_type(
    #         Name=request.POST.get('name'),
    #         # Keywords=request.POST['keywords'],
    #         Description=request.POST.get('description'),
    #         QualificationTypeStatus=request.POST.get('status'),
    #         # RetryDelayInSeconds=request.POST['delay_retry_seconds'],
    #         # Test=janek ist doof!,
    #         # AnswerKey=request.POST['answer'],
    #         # TestDurationInSeconds=request.POST['duration_test_seconds'],
    #         # AutoGranted=request.POST['is_auto_granted'],
    #         # AutoGrantedValue=request.POST['value_if_auto_granted'],
    #     )['QualificationType']
    # elif request.method == 'PUT':
    #     print(request.POST)
    #     response = client.update_qualification_type(
    #         QualificationTypeId=request.POST.get('id'),
    #         # Keywords=request.POST['keywords'],
    #         Description=request.POST.get('description'),
    #         QualificationTypeStatus=request.POST.get('status'),
    #         # Keywords=request.POST['keywords'],
    #         # Description=request.POST['description'],
    #         # QualificationTypeStatus=request.POST['status'],
    #         # RetryDelayInSeconds=request.POST['delay_retry_seconds'],
    #         # # Test=janek ist doof!,
    #         # AnswerKey=request.POST['answer'],
    #         # TestDurationInSeconds=request.POST['duration_test_seconds'],
    #         # AutoGranted=request.POST['is_auto_granted'],
    #         # AutoGrantedValue=request.POST['value_if_auto_granted'],
    #     )

    # return JsonResponse(response, safe=False)
# POLICIES #################################
def api_policies(request, name):
    name_quoted = name
    name_project = urllib.parse.unquote(name_quoted)
    db_obj_project = m_Project.objects.get(
        name=name_project
    )

# check if random description for qualification is allowed
# hide messages from workers

    response = {}

    client = code_shared.get_client(db_obj_project, use_sandbox=True)
    # client = code_shared.get_client(db_obj_project, use_sandbox=False)

    if request.method == 'GET':
        response = client.list_qualification_types(
            MustBeRequestable=False,
            MustBeOwnedByCaller=True,
        )
        response = response['QualificationTypes']

    elif request.method == 'POST':
        print(request.POST)
        response = client.create_qualification_type(
            Name=request.POST.get('name'),
            # Keywords=request.POST['keywords'],
            Description=request.POST.get('description'),
            QualificationTypeStatus=request.POST.get('status'),
            # RetryDelayInSeconds=request.POST['delay_retry_seconds'],
            # Test=janek ist doof!,
            # AnswerKey=request.POST['answer'],
            # TestDurationInSeconds=request.POST['duration_test_seconds'],
            # AutoGranted=request.POST['is_auto_granted'],
            # AutoGrantedValue=request.POST['value_if_auto_granted'],
        )['QualificationType']
    elif request.method == 'PUT':
        print(request.POST)
        response = client.update_qualification_type(
            QualificationTypeId=request.POST.get('id'),
            # Keywords=request.POST['keywords'],
            Description=request.POST.get('description'),
            QualificationTypeStatus=request.POST.get('status'),
            # Keywords=request.POST['keywords'],
            # Description=request.POST['description'],
            # QualificationTypeStatus=request.POST['status'],
            # RetryDelayInSeconds=request.POST['delay_retry_seconds'],
            # # Test=janek ist doof!,
            # AnswerKey=request.POST['answer'],
            # TestDurationInSeconds=request.POST['duration_test_seconds'],
            # AutoGranted=request.POST['is_auto_granted'],
            # AutoGrantedValue=request.POST['value_if_auto_granted'],
        )
    elif request.method == 'DELETE':
        response = client.delete_qualification_type(
            QualificationTypeId=request.POST['id']
        )

    return JsonResponse(response, safe=False)
