from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CSVUploadForm
from .models import Set, Suite, Test, Question
import pandas as pd
from .masterkey_zeroshot import  MasterKey
import threading
from .hallu_tool import run_single_evaluation, answer_parsing
import concurrent.futures
from django.utils import timezone
import csv
import io
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

models = ["gpt-3.5-turbo"]
evaluators = ["gpt-3.5-turbo"]


def upload_csv(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            # try:
            set_name = csv_file.name
            set_instance = Set.objects.create(name=set_name, cate='jailbreak')
            df = pd.read_csv(csv_file)
            mid = []
            for index, row in df.iterrows():
                question_instance = Question.objects.create(
                    goal=row['goal'],
                    target=row['target'],
                    behavior=row['behavior'],
                    category=row['category']
                )
                mid.append(question_instance.id)
            set_instance.relation.add(*mid)
            messages.success(request, "CSV file uploaded and data added to database.")
            # except Exception as e:
            #     messages.error(request, f"Error processing CSV file: {e}")
        else:
            messages.error(request, "Invalid form submission.")
    else:
        form = CSVUploadForm()
    return render(request, 'upload_csv.html', {'form': form})

import logging
logger = logging.getLogger(__name__)

def upload_json(request):
    if request.method == 'POST':
        logger.info("Received POST request for upload_json")
        logger.info(f"POST data: {request.POST}")
        logger.info(f"FILES: {request.FILES}")
        try:
            file = request.FILES.get('file')
            set_id = request.POST.get('set_id')

            if not file:
                logger.error("No file received")
                return JsonResponse({'ret': 1, 'msg': '缺少文件'})
            if not set_id:
                logger.error("No set_id received")
                return JsonResponse({'ret': 1, 'msg': '缺少数据集id'})

            logger.info(f"File name: {file.name}, size: {file.size}")
            logger.info(f"Set ID: {set_id}")

            set_instance = Set.objects.get(id=set_id)

            file_content = file.read().decode('utf-8')
            try:
                data = json.loads(file_content)
            except json.JSONDecodeError as e:
                logger.error(f"JSON Decode Error: {str(e)}")
                return JsonResponse({'ret': 1, 'msg': f'无效的 JSON 文件: {str(e)}'})

            if not isinstance(data, list):
                logger.error("JSON content is not a list")
                return JsonResponse({'ret': 1, 'msg': 'JSON 内容必须是列表格式'})

            question_count = 0
            for item in data:
                if isinstance(item, str):
                    try:
                        item = json.loads(item)
                    except json.JSONDecodeError:
                        logger.error(f"Invalid JSON string in list: {item}")
                        continue

                if not isinstance(item, dict):
                    logger.error(f"Invalid item in list: {item}")
                    continue

                question = Question.objects.create(
                    goal=item.get('question', ''),
                    target=item.get('answer', ''),
                    behavior='',
                    category=item.get('category', ''),
                    methods='hallucination'
                )
                set_instance.relation.add(question)
                question_count += 1

            set_instance.count = question_count
            set_instance.save()

            return JsonResponse({'ret': 0, 'msg': '数据导入成功', 'question_count': question_count})

        except Set.DoesNotExist:
            logger.error(f"Set with id {set_id} does not exist")
            return JsonResponse({'ret': 1, 'msg': '指定的Set不存在'})
        except Exception as e:
            logger.exception("Error in upload_json")
            return JsonResponse({'ret': 1, 'msg': f'上传失败: {str(e)}'})

    return JsonResponse({'ret': 1, 'msg': '请使用 POST 方法'})

def test(request):
    str = "hello,test."
    return HttpResponse(str)


def run_explain(request):
    ret = {
        'data': [
            {
                'dataset': 'datasetname1',
                'model': 'gpt-3.5-turbo',
                'evaluate': 'gpt-3.5-turbo'
            },

            {
                'dataset': 'datasetname2',
                'model': 'gpt-3.5-turbo',
                'evaluate': 'gpt-3.5-turbo'
            }
        ]
    }
    return JsonResponse(ret)


def get_dataset(dataset_name):
    ds = Question.objects.values()
    ds = list(ds)
    dss = []
    for index in ds:
        dss.append(index['goal'])
    return dss




def run(request):
    if request.method == 'POST':
       # print(request.body)
       jstr = json.loads(request.body)
       datalist = jstr['data']
       ret = {'ret': 0, 'data': []}
       for data in datalist:
           ret['data'].append(exe_eva(data))
       return JsonResponse(ret)
    else:
       return JsonResponse({'ret': 1, 'msg': '请使用POST方法'})


def list_question(request):
    questions = Question.objects.values_list("goal", flat=True)
    questions = list(questions)
    ret = {
        'ret': 0,
        'questions': questions
    }
    return JsonResponse(ret)


def add_question(request):
    """
    传入参数如下
    {
    "data":{
        "goal": "问题",
        "target": "预期回复",
        "behavior": "问题简称",
        "category": "类别描述"
        }
    }
    """
    if request.method == 'POST':
        # print(request.body)
        question = json.loads(request.body)["data"]
        question_instance = Question.objects.create(
            goal=question['goal'],
            target=question['target'],
            behavior=question['behavior'],
            category=question['category']
        )
        ret = {
            'ret': 0,
            'id': question_instance.id
        }
        return JsonResponse(ret)
    else:
        return JsonResponse({'ret': 1, 'msg': '请使用POST方法'})


def modify_question(request):
    example = """
    传入参数如下
    {
        "id": 203,
        "data":{
            "goal": "问题1",
            "target": "预期回复1",
            "behavior": "问题简称1",
            "category": "类别描述1"
        }
    }
    """
    if request.method == 'POST':
        params = json.loads(request.body)
        question_id = params['id']
        data = params['data']
        try:
            question = Question.objects.get(id=question_id)
        except Question.DoesNotExist:
            return JsonResponse({
                'ret': 1,
                'msg': f'id 为`{question_id}`的问题不存在'
            })
        if 'goal' in data:
            question.goal = data['goal']
        if 'target' in data:
            question.target = data['target']
        if 'behavior' in data:
            question.behavior = data['behavior']
        if 'category' in data:
            question.category = data['category']

        question.save()
        return JsonResponse({'ret': 0})
    else:
        return JsonResponse({'ret': 1, 'msg': '请使用POST方法\n' + example})


def del_question(request):
    example = """
    传入参数如下
    {
        "id": 203
    }
    """
    if request.method == 'POST':
        params = json.loads(request.body)
        question_id = params['id']

        try:
            question = Question.objects.get(id=question_id)
        except Question.DoesNotExist:
            return JsonResponse({
                'ret': 1,
                'msg': f'id 为`{question_id}`的问题不存在'
            })

        question.delete()

        return JsonResponse({'ret': 0})
    else:
        return JsonResponse({'ret': 1, 'msg': '请使用POST方法\n' + example})


def list_set(request):
    datasets = Set.objects.values()
    datasets = list(datasets)
    ret = {
        'ret': 0,
        'datasets': datasets
    }
    return JsonResponse(ret)

# 测试类型创建
def test_suit_create(request):
    example = """
    传入参数如下
    {
        "Suite_name" : "testSuite"
    }
    """
    # todo: 添加名称重复时处理
    if request.method == 'POST':
        params = json.loads(request.body)
        suite_name = params['Suite_name']

        # print(request.body)
        suite_instance = Suite.objects.create(
            name=suite_name,
            state="running"
        )
        return HttpResponse()
    else:
        response = HttpResponse()
        response.status_code = 404
        response.content = "请使用post方法"
        return response

# 测试类型展示
def test_suit_show(request):
    example = """
    传入参数如下
    {
        "Suite_name" : "TestSuiteShow"
    }
    """
    if request.method == 'GET':
        # print(request.body)
        test_suit_list = list(Suite.objects.values())
        # print(test_suit_list)
        for item in test_suit_list:
            del item["id"]
        ret = {
            "Suite_list": test_suit_list
        }
        return JsonResponse(ret)
    else:
        response = HttpResponse()
        response.status_code = 404
        response.content = "请使用get方法"
        return response

def set_show(request):
    if request.method == 'GET':
        try:
            page = request.GET.get('page', 1)
            page_size = request.GET.get('pageSize', 10)
            name = request.GET.get('name', '')
            suite = request.GET.get('suite', '')

            queryset = Set.objects.all()
            if name:
                queryset = queryset.filter(name__icontains=name)
            if suite:
                queryset = queryset.filter(suite__name__icontains=suite)

            paginator = Paginator(queryset, page_size)
            try:
                sets = paginator.page(page)
            except PageNotAnInteger:
                sets = paginator.page(1)
            except EmptyPage:
                sets = paginator.page(paginator.num_pages)

            set_list = [{
                'id': set_obj.id,
                'name': set_obj.name,
                'suite_name': set_obj.suite.name,
                'created_at': set_obj.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'question_count': set_obj.relation.count(),
            } for set_obj in sets]

            return JsonResponse({
                'ret': 0,
                'msg': 'Success',
                'data': {
                    'list': set_list,
                    'total': paginator.count,
                    'pageSize': int(page_size),
                    'currentPage': int(page)
                }
            })
        except Exception as e:
            return JsonResponse({'ret': 1, 'msg': f'Error: {str(e)}'})
    else:
        return JsonResponse({'ret': 1, 'msg': 'Please use GET method'})

# 数据集创建 
def set_create(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name')
            suite_name = data.get('suite_name')

            if not name or not suite_name:
                return JsonResponse({'ret': 1, 'msg': '缺少必要参数'})

            suite = Suite.objects.get(name=suite_name)
            
            new_set = Set.objects.create(
                name=name,
                suite=suite,
                created_at=timezone.now()
            )

            return JsonResponse({'ret': 0, 'msg': '数据集创建成功', 'id': new_set.id})
        except Suite.DoesNotExist:
            return JsonResponse({'ret': 1, 'msg': '指定的Suite不存在'})
        except Exception as e:
            return JsonResponse({'ret': 1, 'msg': f'创建失败: {str(e)}'})
    else:
        return JsonResponse({'ret': 1, 'msg': '请使用POST方法'})

# 数据集上传
def upload_set_file(request):
    if request.method == 'POST':
        try:
            set_id = request.POST.get('set_id')
            file = request.FILES.get('file')

            if not set_id or not file:
                return JsonResponse({'ret': 1, 'msg': '缺少必要参数'})

            set_instance = Set.objects.get(id=set_id)
            
            decoded_file = file.read().decode('utf-8')
            csv_reader = csv.DictReader(io.StringIO(decoded_file))
            
            for row in csv_reader:
                question = Question.objects.create(
                    goal=row.get('goal', ''),
                    target=row.get('target', ''),
                    behavior=row.get('behavior', ''),
                    category=row.get('category', ''),
                    methods=row.get('methods', '无增强')
                )
                set_instance.relation.add(question)

            return JsonResponse({'ret': 0, 'msg': '文件上传成功'})
        except Set.DoesNotExist:
            return JsonResponse({'ret': 1, 'msg': '指定的Set不存在'})
        except Exception as e:
            return JsonResponse({'ret': 1, 'msg': f'上传失败: {str(e)}'})
    else:
        return JsonResponse({'ret': 1, 'msg': '请使用POST方法'})

# 数据集更新
def set_update(request):
    if request.method == 'POST':
        try:
            set_id = request.POST.get('id')
            name = request.POST.get('name')
            suite_name = request.POST.get('suite_name')

            if not set_id or not name or not suite_name:
                return JsonResponse({'ret': 1, 'msg': '缺少必要参数'})

            set_instance = Set.objects.get(id=set_id)
            suite = Suite.objects.get(name=suite_name)

            set_instance.name = name
            set_instance.suite = suite
            set_instance.save()

            return JsonResponse({'ret': 0, 'msg': '数据集更新成功'})
        except Set.DoesNotExist:
            return JsonResponse({'ret': 1, 'msg': '指定的数据集不存在'})
        except Suite.DoesNotExist:
            return JsonResponse({'ret': 1, 'msg': '指定的Suite不存在'})
        except Exception as e:
            return JsonResponse({'ret': 1, 'msg': f'更新失败: {str(e)}'})
    else:
        return JsonResponse({'ret': 1, 'msg': '请使用POST方法'})

# 数据集删除
def set_delete(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            set_id = data.get('id')

            if not set_id:
                return JsonResponse({'ret': 1, 'msg': '缺少必要参数'})

            set_instance = Set.objects.get(id=set_id)
            set_instance.delete()

            return JsonResponse({'ret': 0, 'msg': '数据集删除成功'})
        except Set.DoesNotExist:
            return JsonResponse({'ret': 1, 'msg': '指定的数据集不存在'})
        except Exception as e:
            return JsonResponse({'ret': 1, 'msg': f'删除失败: {str(e)}'})
    else:
        return JsonResponse({'ret': 1, 'msg': '请使用POST方法'})

def test_create(request):
    example = """
    传入参数如下
    {
        "Suite_name" : "testSuite",
        "Test_name" : "Test1",
        "Collection" : "question1.csv",
        "Model" : "gpt-3.5-turbo",
        "Evaluator" : "gpt-3.5-turbo"
        "Cate" : "hallu"
    }
    """
    if request.method == 'POST':
        params = json.loads(request.body)
        suite_name = params['Suite_name']
        test_name = params['Test_name']
        collection = params['Collection']
        model = params['Model']
        evaluator = params['Evaluator']
        suite_instance = Suite.objects.get(name=suite_name)
        collection_instance = Set.objects.get(name=collection)

        # print(request.body)
        test_instance = Test.objects.create(
            name=test_name,
            collection=collection_instance,
            model=model,
            evaluator=evaluator,
            suite=suite_instance,
            state='starting',
            escape_rate='0'
        )
        return JsonResponse({'ret': 0, 'msg': 'Test created successfully'})
    else:
        return JsonResponse({'ret': 1, 'msg': '请使用POST方法'})


def test_show(request):
    example = """
    传入参数如下
    {
        "Suite_name" : "testSuite"
    }
    """
    if request.method == 'GET':
        # print(request.body)
        params = request.GET
        suite_name = params["Suite_name"]
        tests = Test.objects.filter(suite__name=suite_name).values('name', 'state', 'escape_rate', 'created_at')
        return JsonResponse({'ret': 0, 'tests': list(tests)})
    else:
        return JsonResponse({'ret': 1, 'msg': '请使用GET方法'})


def config(request):
    example = """
    传入参数如下
    {
        "Suite_name" : "TestSuite"
    }
    """
    if request.method == 'GET':
        # print(request.body)
        collection1 = list(Set.objects.filter(cate='jailbreak').values_list("name", flat=True))
        collection2 = list(Set.objects.filter(cate='hallucination').values_list("name", flat=True))
        ret = {
            "Config1": {
                "collection": collection1,
                "model": models,
                "evaluator": evaluators,
                "category": "jailbreak"
            },
            "Config2":
            {
                "collection": collection2,
                "model": models,
                "evaluator": evaluators,
                "category": "hallucination"
            }
        }
        return JsonResponse(ret)
    else:
        response = HttpResponse()
        response.status_code = 404
        response.content = "请使用get方法"
        return response


def exe_eva(data):
    # Initialize the MasterKey with the OpenAI API key and model names
    master_key = MasterKey("sk-6ztYKBLUnRd1kViyBelVC5CRrrDwAwzx4AfHdBMozqeD4N5F", execute_model=data["model"],
                           evaluation_model=data["evaluate_model"])
    collection = Set.objects.get(name=data["dataset"])
    related_questions = collection.relation.values()
    res_list = []
    for qs in related_questions:
        mid = dict()
        mid["id"] = qs["id"]
        mid["goal"] = qs["goal"]
        mid["category"] = qs["category"]
        mid["methods"] = qs["methods"]
        res_list.append(mid)
    count = 0
    for index in range(len(res_list)):
        malicious_instruction = res_list[index]["goal"]
        # Execute the jailbreak prompt with the malicious behavior
        jailbreak_executed = master_key.execute_jailbreak_prompt(malicious_instruction)
        res_list[index]["output"] = jailbreak_executed
        # print(f"Jailbreak executed: {jailbreak_executed}")
        # Evaluate the jailbreak prompt
        jailbreak_successful = master_key.evaluate_jailbreak_prompt(malicious_instruction, jailbreak_executed)
        res_list[index]["is_success"] = jailbreak_successful
        if jailbreak_successful:
            count = count + 1
        # print(f"Jailbreak successful: {jailbreak_successful}")
    return res_list, count


def jailbreak_exe(test_instance):
    test_instance.state = "running"
    test_instance.save()
    data = {
        'dataset': test_instance.collection.name,
        'model': test_instance.model,
        'evaluate_model': test_instance.evaluator
    }
    res_list, count = exe_eva(data)
    print(f"{test_instance.name}_{test_instance.suite.name} done!")
    ret = {"data": res_list}
    ret_str = json.dumps(ret)
    file_path = f"{test_instance.name}_{test_instance.suite.name}.json"
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(ret_str)
    rate = count / len(res_list)
    test_instance.escape_rate = f"{rate:.2%}"
    test_instance.state = "finished"
    test_instance.save()
    return


def hallu_exe(test_instance):
    test_instance.state = "running"
    test_instance.save()

    collection = Set.objects.get(name=test_instance.collection.name)
    related_questions = collection.relation.values()
    mid_list = []
    for qs in related_questions:
        mid = dict()
        mid["id"] = qs["id"]
        mid["goal"] = qs["goal"]
        mid["category"] = qs["category"]
        mid["target"] = qs["target"]
        mid["methods"] = qs["methods"]
        mid_list.append(mid)

    output_data = []
    model_name = test_instance.model
    question_data = mid_list
    model_list = [model_name for x in range(len(question_data))]
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        ret_list = executor.map(run_single_evaluation, question_data, model_list)
    for item in ret_list:
        output_data.append(item)
    hallucination_count = answer_parsing(output_data)
    print(f"{test_instance.name}_{test_instance.suite.name} done!")

    ret = {"data": output_data}
    ret_str = json.dumps(ret)
    file_path = f"{test_instance.name}_{test_instance.suite.name}.json"
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(ret_str)
    rate = hallucination_count / len(output_data)
    test_instance.escape_rate = f"{rate:.2%}"
    test_instance.state = "finished"
    test_instance.save()
    return


def test_exec(request):
    if request.method == 'POST':
        params = json.loads(request.body)
        test_name = params['Test_name']
        test_instance = Test.objects.get(name=test_name)
        if test_instance.state != "starting":
            return JsonResponse({'ret': 1, 'msg': "当前测试已运行"})
        if test_instance.collection.cate == "jailbreak":
            x = threading.Thread(target=jailbreak_exe, args=(test_instance,))
            x.start()
        else:
            x = threading.Thread(target=hallu_exe, args=(test_instance,))
            x.start()
        return JsonResponse({'ret': 0, 'msg': '测试开始执行'})
    else:
        return JsonResponse({'ret': 1, 'msg': '请使用POST方法'})


def test_res(request):
    if request.method == 'GET':
        params = request.GET
        test_name = params["Test_name"]
        test = Test.objects.get(name=test_name)
        filename = f"{test_name}_{test.suite.name}.json"
        file_path = f"{filename}"
        try:
            with open(file_path, 'r') as file:
                content = json.load(file)
            return JsonResponse(content)
        except FileNotFoundError:
            return JsonResponse({'ret': 1, 'msg': '结果文件不存在'})
    else:
        return JsonResponse({'ret': 1, 'msg': '请使用GET方法'})
    
def test_dele(request):
    if request.method == 'POST':
        params = json.loads(request.body)
        test_name = params['Test_name']
        try:
            test_instance = Test.objects.get(name=test_name)
            test_instance.delete()
            return JsonResponse({'ret': 0, 'msg': '测试删除成功'})
        except Test.DoesNotExist:
            return JsonResponse({'ret': 1, 'msg': '测试不存在'})
    else:
        return JsonResponse({'ret': 1, 'msg': '请使用POST方法'})