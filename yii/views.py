import os
import shutil

from django.core import serializers
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render

from yii.models import *
from yii.until.common import *
from yii.until.spider import *
from yii.until.switch import switch
from yii.until.validatecode import gene_code


# 转换分页数据
def toJson(data, page, limit):
    limitData = serializers.serialize("json", data[(page - 1) * limit:page * limit])
    jsonData = json.loads(limitData)
    dictData = []
    for jData in jsonData:
        dictCur = jData['fields']
        dictCur['pk'] = jData['pk']
        dictCur['create'] = utc2local(dictCur['create'])
        dictCur['modify'] = utc2local(dictCur['modify'])
        dictData.append(dictCur)
    result = {
        'code': 0,
        'msg': "",
        'count': len(data),
        'data': dictData
    }
    return json.dumps(result)


# 前台
def webs(request, type='', id=''):
    url = 'index.html'
    data = {}
    try:
        for case in switch(type):
            if case('essay') and not id.isdigit():
                if not id:
                    id = 'news'
                url = 'essay/index.html'
                category = Dictionary.objects.filter(pid=1, isdel=False)
                dlist = Essay.objects.filter(categoryid=Dictionary.objects.get(key=id).pk, isdel=False).order_by(
                    '-create')
                data = {'category': category, 'list': dlist[:10], 'id': id}
                break
            if case('essay') and id.isdigit():
                url = 'essay/details.html'
                model = Essay.objects.get(pk=id)
                data = {'model': model}
                model.visits = model.visits + 1
                model.save()
                break
            if case('collection'):
                url = 'collection/index.html'
                dlist = Collection.objects.filter(isdel=False).extra(
                    select={
                        'type': 'SELECT `value` FROM yii_dictionary WHERE `id` = `typeid`'
                    }).order_by('-create')
                data = {'list': dlist[:10]}
                break
            if case('feedback'):
                url = 'feedback/index.html'
                break
            if case('about'):
                url = 'about/index.html'
                data = {'list': About.objects.filter(isdel=False).order_by('-sort')}
                break
        if type == '':
            data['index_about'] = Index.objects.get(pk=1)
            data['index_essay'] = Essay.objects.filter(~Q(typeid=16), isdel=False).order_by('-create')[:10]
        # 页脚数据
        data['foot_essay'] = Essay.objects.filter(~Q(typeid=16), isdel=False).order_by('-agrees')[:4]
        data['foot_collection'] = Collection.objects.filter(~Q(typeid=9), isdel=False).order_by('-agrees')[0]
        data['foot_friendlink'] = Collection.objects.filter(typeid=9, isdel=False).order_by('-agrees')[:5]
    except BaseException as ex:
        pass
    return render(request, url, locals())


# 后台
def admin(request, type='admin', id=-1):
    url = 'index.html'
    model = ''
    data = {}
    try:
        for case in switch(type):
            if case('login'):
                url = 'login.html'
                request.session.clear()
                break
            if case('admin'):
                data = {'model': Index.objects.get(pk=1)}
                break
            if case('essay'):
                url = 'essay/list.html'
                break
            if case('edit_essay'):
                url = 'essay/details.html'
                if id != -1:
                    model = Essay.objects.get(pk=id)
                category = Dictionary.objects.filter(pid=1, isdel=False).order_by('-sort')
                type = Dictionary.objects.filter(pid=11, isdel=False).order_by('-sort')
                data = {'model': model, 'type': type, 'category': category}
                break
            if case('collection'):
                url = 'collection/list.html'
                break
            if case('edit_collection'):
                url = 'collection/details.html'
                if id != -1:
                    model = Collection.objects.get(pk=id)
                type = Dictionary.objects.filter(pid=5, isdel=False).order_by('-sort')
                data = {'model': model, 'type': type}
                break
            if case('feedback'):
                url = 'feedback/list.html'
                break
            if case('edit_feedback'):
                url = 'feedback/details.html'
                if id != -1:
                    model = Feedback.objects.get(pk=id)
                data = {'model': model}
                break
            if case('about'):
                url = 'about/list.html'
                break
            if case('edit_about'):
                url = 'about/details.html'
                if id != -1:
                    model = About.objects.get(pk=id)
                type = Dictionary.objects.filter(~Q(pk=14), pid=11, isdel=False).order_by('-sort')
                data = {'model': model, 'type': type}
                break
            if case('dict'):
                url = '_developer/dictionary/list.html '
                break
            if case('edit_dict'):
                url = '_developer/dictionary/details.html'
                if id != -1:
                    model = Dictionary.objects.get(pk=id)
                type = Dictionary.objects.filter(pid=0, isdel=False).order_by('-sort')
                data = {'model': model, 'type': type}
                break
            if case('files'):
                url = '_developer/filemanage/index.html'
                break
    except BaseException as ex:
        pass
    return render(request, 'admin/' + url, locals())


# 接口
def api(request, type='login'):
    if type != 'login' and type != 'get_code' and 'select' not in type and \
                    type != 'edit_feedback' and type != 'edit_agree' and not request.session.get('nickname'):
        return HttpResponse(json.dumps({"result": 'no user login'}), content_type='application/json')
    result = None
    try:
        for case in switch(type):
            if case('login'):
                if request.method == 'POST':
                    data = request.POST['data']
                    if data is not None:
                        data = json.JSONDecoder().decode(data)
                        code = data['code']
                        if code == request.session.get('code'):
                            account = data['account']
                            pwd = encrypt(data['pwd'])
                            obj = User.objects.get(Q(email=account) | Q(phone=account))
                            if obj is not None and obj.password == pwd:
                                if obj.status == 1:
                                    request.session['nickname'] = obj.nickname
                                    result = json.dumps({"result": "success"})
                                else:
                                    result = json.dumps({"result": "该账号已被限制登录"})
                        else:
                            result = json.dumps({"result": "验证码错误"})
                break
            if case('get_code'):
                gene_code(request)
                result = json.dumps({"result": "success"})
                break
            if case('select_dict'):
                page = request.GET.get('page')
                limit = request.GET.get('limit')
                data = Dictionary.objects.filter(isdel=False).extra(
                    select={
                        'ptype': 'SELECT `value` FROM yii_dictionary t2 WHERE t2.`id` = `yii_dictionary`.pid'}).order_by(
                    '-create')
                result = toJson(data, int(page), int(limit))
                break
            if case('delete_dict'):
                if request.method == 'POST':
                    ids = request.POST['ids']
                    if ids is not None:
                        list = [int(x) for x in ids.split(',') if x]
                        Dictionary.objects.filter(pk__in=list).update(isdel=True)
                        result = json.dumps({"result": "success"})
                break
            if case('edit_dict'):
                if request.method == 'POST':
                    model = request.POST['model']
                    if model is not None:
                        model = json.JSONDecoder().decode(model)
                        obj = Dictionary()
                        if model['pk'] is not None and model['pk']:
                            obj = Dictionary.objects.get(pk=model['pk'])
                        obj.pid = int(model['pid'])
                        obj.key = str(model['key'])
                        obj.value = str(model['value'])
                        obj.sort = int(model['sort'])
                        obj.remarks = str(model['remarks'])
                        obj.save()
                        result = json.dumps({"result": "success"})
                break
            if case('select_files'):
                path = request.GET.get('path')
                if path is not None and path and '/' in path.replace("/", "", 1):
                    data = []
                    pathDir = os.listdir(os.path.dirname(__file__) + '\\' + path)
                    for allDir in pathDir:
                        data.append({
                            'name': os.path.splitext(allDir)[0],
                            'dir': path,
                            'path': os.path.join('%s/%s' % (path, allDir)),
                            'extension': str(os.path.splitext(allDir)[1]).replace('.', '')
                        })
                    result = json.dumps({"data": data})
                break
            if case('upload_files'):
                if request.method == 'POST':
                    file_obj = request.FILES.get('file')
                    dir_name = request.GET.get('dir')
                    if file_obj is not None and dir_name is not None:
                        extension = os.path.splitext(file_obj.name)[1]
                        if extension not in '.exe|.EXE':
                            file_name = '%d%s' % (int(round(time.time() * 1000)), extension)
                            file_full_path = os.path.dirname(__file__) + dir_name + '/' + file_name
                            dest = open(file_full_path, 'wb+')
                            dest.write(file_obj.read())
                            dest.close()
                            result = json.dumps({
                                "code": 0,
                                "msg": "success",
                                "data": {"src": dir_name + '/' + file_name, "title": file_name}
                            })
                break
            if case('delete_files'):
                if request.method == 'POST':
                    ids = request.POST['ids']
                    if ids is not None:
                        for file in ids.split(','):
                            if file:
                                file_path = os.path.dirname(__file__) + file
                                if os.path.exists(file_path):
                                    if os.path.isfile(file_path):
                                        os.remove(file_path)
                                    elif os.path.isdir(file_path):
                                        shutil.rmtree(file_path, True)
                        result = json.dumps({"result": "success"})
                break
            if case('create_dir'):
                if request.method == 'POST':
                    dir_name = request.POST['name']
                    if dir_name is not None:
                        os.mkdir(os.path.dirname(__file__) + dir_name)
                result = json.dumps({"result": "success"})
                break
            if case('select_essay'):
                page = request.GET.get('page')
                limit = request.GET.get('limit')
                categoryid = request.GET.get('categoryid')
                data = Essay.objects.filter(isdel=False)
                if categoryid is not None:
                    data = data.filter(categoryid=categoryid)
                data = data.extra(
                    select={
                        'type': 'SELECT `value` FROM yii_dictionary WHERE `id` = `typeid`',
                        'category': 'SELECT `value` FROM yii_dictionary WHERE `id` = `categoryid`'
                    })
                result = toJson(data.order_by('-create'), int(page), int(limit))
                break
            if case('delete_essay'):
                if request.method == 'POST':
                    ids = request.POST['ids']
                    if ids is not None:
                        list = [int(x) for x in ids.split(',') if x]
                        Essay.objects.filter(pk__in=list).update(isdel=True)
                        result = json.dumps({"result": "success"})
                break
            if case('edit_essay'):
                if request.method == 'POST':
                    model = request.POST['model']
                    if model is not None:
                        model = json.JSONDecoder().decode(model)
                        obj = Essay()
                        if model['pk'] is not None and model['pk']:
                            obj = Essay.objects.get(pk=model['pk'])
                        obj.categoryid = int(model['categoryid'])
                        obj.typeid = int(model['typeid'])
                        obj.seotitle = str(model['seotitle'])
                        obj.seokeywords = str(model['seokeywords'])
                        obj.seodescription = str(model['seodescription'])
                        obj.sources = str(model['sources'])
                        obj.imagesurl = str(model['imagesurl'])
                        obj.filesurl = str(model['filesurl'])
                        obj.sort = int(model['sort'])
                        obj.remarks = str(model['remarks'])
                        obj.save()
                        result = json.dumps({"result": "success"})
                break
            if case('select_collection'):
                page = request.GET.get('page')
                limit = request.GET.get('limit')
                data = Collection.objects.filter(isdel=False).extra(
                    select={
                        'type': 'SELECT `value` FROM yii_dictionary WHERE `id` = `typeid`'
                    }).order_by('-create')
                result = toJson(data, int(page), int(limit))
                break
            if case('delete_collection'):
                if request.method == 'POST':
                    ids = request.POST['ids']
                    if ids is not None:
                        list = [int(x) for x in ids.split(',') if x]
                        Collection.objects.filter(pk__in=list).update(isdel=True)
                        result = json.dumps({"result": "success"})
                break
            if case('edit_collection'):
                if request.method == 'POST':
                    model = request.POST['model']
                    if model is not None:
                        model = json.JSONDecoder().decode(model)
                        obj = Collection()
                        if model['pk'] is not None and model['pk']:
                            obj = Collection.objects.get(pk=model['pk'])
                        obj.typeid = int(model['typeid'])
                        obj.title = str(model['title'])
                        obj.imagesurl = str(model['imagesurl'])
                        obj.url = str(model['url'])
                        obj.sort = int(model['sort'])
                        obj.remarks = str(model['remarks'])
                        obj.save()
                        result = json.dumps({"result": "success"})
                break
            if case('select_about'):
                page = request.GET.get('page')
                limit = request.GET.get('limit')
                data = About.objects.filter(isdel=False).extra(
                    select={
                        'type': 'SELECT `value` FROM yii_dictionary WHERE `id` = `typeid`'
                    }).order_by('-create')
                result = toJson(data, int(page), int(limit))
                break
            if case('delete_about'):
                if request.method == 'POST':
                    ids = request.POST['ids']
                    if ids is not None:
                        list = [int(x) for x in ids.split(',') if x]
                        About.objects.filter(pk__in=list).update(isdel=True)
                        result = json.dumps({"result": "success"})
                break
            if case('edit_about'):
                if request.method == 'POST':
                    model = request.POST['model']
                    if model is not None:
                        model = json.JSONDecoder().decode(model)
                        obj = About()
                        if model['pk'] is not None and model['pk']:
                            obj = About.objects.get(pk=model['pk'])
                        obj.typeid = int(model['typeid'])
                        obj.title = str(model['title'])
                        obj.url = str(model['url'])
                        obj.filesurl = str(model['filesurl'])
                        obj.content = str(model['content'])
                        obj.sort = int(model['sort'])
                        obj.save()
                        result = json.dumps({"result": "success"})
                break
            if case('select_feedback'):
                page = request.GET.get('page')
                limit = request.GET.get('limit')
                data = Feedback.objects.filter(isdel=False).order_by('-create')
                result = toJson(data, int(page), int(limit))
                break
            if case('delete_feedback'):
                if request.method == 'POST':
                    ids = request.POST['ids']
                    if ids is not None:
                        list = [int(x) for x in ids.split(',') if x]
                        Feedback.objects.filter(pk__in=list).update(isdel=True)
                        result = json.dumps({"result": "success"})
                break
            if case('edit_feedback'):
                if request.method == 'POST':
                    model = request.POST['model']
                    if model is not None:
                        model = json.JSONDecoder().decode(model)
                        current_date = datetime.datetime.now().date()
                        if Feedback.objects.filter(isdel=False, ip=model['ip'], create__range=(
                                current_date, current_date + datetime.timedelta(days=1))).count() > 4:
                            result = json.dumps({"result": "feedback too many"})
                        else:
                            obj = Feedback()
                            if model['pk'] is not None and model['pk']:
                                obj = Feedback.objects.get(pk=model['pk'])
                            obj.ip = str(model['ip'])
                            obj.city = str(model['city'])
                            obj.content = str(model['content'])
                            obj.replycontent = str(model['replycontent'])
                            obj.save()
                            result = json.dumps({"result": "success"})
                break
            if case('edit_index'):
                if request.method == 'POST':
                    model = request.POST['model']
                    if model is not None:
                        model = json.JSONDecoder().decode(model)
                        obj = Index()
                        if model['pk'] is not None and model['pk']:
                            obj = Index.objects.get(pk=model['pk'])
                        obj.title = str(model['title'])
                        obj.logourl = str(model['logourl'])
                        obj.imagesurl = str(model['imagesurl'])
                        obj.keywords = str(model['keywords'])
                        obj.description = str(model['description'])
                        obj.save()
                        result = json.dumps({"result": "success"})
                break
            if case('get_news'):
                if request.method == 'POST':
                    list = getJRTTNews()
                    for model in list:
                        ss = model.seotitle
                        if not Essay.objects.filter(spiderid=model.spiderid, isdel=False).exists():
                            model.save()
                    result = json.dumps({"result": "success"})
                break
            if case('edit_agree'):
                if request.method == 'POST':
                    model = request.POST['model']
                    if model is not None:
                        model = json.JSONDecoder().decode(model)
                        objs = AgreeLog.objects.filter(ip=model['ip'], articleid=int(model['articleid']))
                        obj = None
                        result = 'success'
                        if objs.count() > 0:
                            obj = objs[0]
                        change = 0
                        if obj is None or obj.pk is None or obj.pk == '':
                            change = 1
                            obj = AgreeLog()
                            article = Essay.objects.get(pk=model['articleid'])
                            if model['status'] == '1':
                                article.agrees = article.agrees + 1
                            elif model['status'] == '2':
                                article.disagrees = article.disagrees + 1
                            article.save()
                            obj.status = int(model['status'])
                        else:
                            article = Essay.objects.get(pk=model['articleid'])
                            if obj.status == 0:
                                change = 1
                                obj.status = int(model['status'])
                                if model['status'] == '1':
                                    article.agrees = article.agrees + 1
                                elif model['status'] == '2':
                                    article.disagrees = article.disagrees + 1
                            elif obj.status == 1 and model['status'] == '1':
                                change = -1
                                obj.status = 0
                                article.agrees = article.agrees - 1
                            elif obj.status == 2 and model['status'] == '2':
                                change = -1
                                obj.status = 0
                                article.disagrees = article.disagrees - 1
                            else:
                                change = 0
                                result = 'failed'
                                obj.status = obj.status
                            article.save()
                        obj.articleid = str(model['articleid'])
                        obj.ip = str(model['ip'])
                        obj.save()
                        result = json.dumps({"result": result, "change": change})
                break
    except BaseException as ex:
        result = json.dumps({"result": ex.args})
    return HttpResponse(result, content_type='application/json')
