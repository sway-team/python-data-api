from flask import Blueprint,abort
from flask import request
from comp.base import BaseClass
from api.frame import Frame
from api.dataset import Dataset
from comp.db import Data
from comp.tool import json_ret as ret, merge_deep, md5
import time
import env
import json
from copy import deepcopy

ApiIndex = {   
    'getservice':'获取服务',
    'getlist':'获取列表',
    'getinfo':'获取详情',
    'add':'新增',
    'update':'更新',
    'remove':'删除',
    'count':'统计'
}

pageIndex = {   
    'usercenter':{'id':'usercenter', 'href': '/app/usercenter', 'name': '个人中心', 'icon': 'fa-solid fa-list'},
    'datamanage':{'id':'datamanage', 'href': '/app/datamanage?dataset=workflow_dataset', 'name': '数据管理', 'icon': 'fa-solid fa-file-code'},
    'templatemanage':{'id':'templatemanage', 'href': '/app/templatemanage', 'name': '模板管理', 'icon': 'fa-solid fa-file-code'},
    'logstat':{'id':'logstat', 'href': '/app/logstat', 'name': '日志统计', 'icon': 'fa-solid fa-file-lines'}
}

router = Blueprint('service_router', __name__)
@router.route("/<path>", methods=["GET", "POST"], endpoint="go")
def go(path):

    if path in ApiIndex:
        api = Api()
        param = api.get_param(request)
        checked = api.check_required('dataset', param)
        if not checked:
            return ret(1)
        
        if not param.get('token'):
            user = api.checkUserToken()
            if not user:
                return ret(13)
                    
            if param.get('dataset') == 'workflow_app':
                param['createtoken'] = user['token']
                param['token'] = user['token']
            elif user.get('currentToken'):
                param['createtoken'] = user['currentToken']
                param['token'] = user['currentToken']
            else:
                param['createtoken'] = user['token']
                param['token'] = user['token']
            
        print('service',param)
        return Api().post_dataset(path, param)
    
    elif path in pageIndex.keys():
        return Api().getPageData(request, path)
    elif path == 'current':
        return Api().current(request)
    else:
        return abort(404)

class Api(BaseClass):

    def post_dataset(self, path, param):
        # token = env.ADMIN_TOKEN
        # param['token'] = token
        
        res = ret(1)
        dataset = param.get('dataset')
        
        func = getattr(Dataset(), path)
        if func:
            res = func(param)
            res = self.apiToJson(res)

        if int(res.get('code')) == 0 and path == 'getlist':
            if dataset == 'workflow_app':
                fields = 'id,code,name,desc,mission,vision,corevalue,meta'
                res['thead'] = self._get_thead(fields, res['thead'])

        return res

    def post_frame(self, path, param):
        token = env.ADMIN_TOKEN
        param['token'] = token
        
        res = ret(1)
        
        func = getattr(Frame(), path)
        if func:
            res = func(param)
            res = self.apiToJson(res)

        return res
    
    def _get_thead(self, fields, thead):
        retThead = []
        fields = fields.split(',')
        for item in thead:
            if item['code'] in fields:
                retThead.append(item)
        return retThead
    
    def _get_tree(self, param):
        tree = Data('tree').get_data(param)
        for item in tree:
            item['href'] = env.PAGE_HOST + item.get('desc')
            item['id'] = item.get('code')
            item['name'] = item.get('cname')

        return tree
    
    def _get_app(self, param):
        appData = Data('app').get_data(param)
        return appData
    
    def _get_nav_list(self, param, path, user):
        pageList = []
        pageList.append({
            'name':'个人中心',
            'id':'usercenter',
            'type':'href',
            'url':env.PAGE_HOST + '/app/usercenter',
            'active':path == 'usercenter'
        })

        token = ''
        
        if user.get('meta') and user['meta'].get('currentToken'):
            token = user['meta'].get('currentToken')


        app_list = self._get_app({'createtoken':user['token']})
        for app in app_list:
            item = {
                'name':app['name'],
                'id':app['code'],
                'type':'app',
                'url':'javascript:void(0)',
                'token':app['token'],
                'active':False
            }
            if token == app['token'] and path != 'usercenter':
                item['active'] = True
            pageList.append(item)

        return pageList

    def getPageData(self, request, path):

        param = self.get_param(request)

        user = self.checkUserToken()

        if not user:
            return ret(13)

        start_time = time.time()

        pageData = self.getFrameConfig(path, param)

        if 'code' in pageData and pageData['code'] != 0:
            return pageData

        pageData = self.getPageConfig(path, param, pageData);

        if 'code' in pageData and pageData['code'] != 0:
            return pageData

        pageData['page:attr']['topbar']['user'] = user

        pageData['page:attr']['topbar']['data'] = self._get_nav_list(param, path, user)

        scale_time = time.time() - start_time;
        pageData['page:info']['used_time'] = scale_time;
        
        return ret(0, None, pageData)
    
    def getFrameConfig(self, path, param):

        cacheKey = md5(f'frame_config:{path}:{json.dumps(param)}')

        if self._cache.get(cacheKey):
            return self._cache.get(cacheKey)

        pageItem = pageIndex[path]     

        pageData = {
            'page:info':{
                'id':path,
                'title':pageItem['name'],
                'pageTitle':env.APP_NAME
            },
            'page:attr':{
                'topbar':{
                    'title':env.APP_NAME,
                    'data': [],
                    'user': {}
                },
                'toolbar':{}
            }
        }

        res = self.post_frame('getconfig', {'group':'common,'+path})

        if res.get('code') != 0:
            return res

        serviceData = {};
        for item in res['data']:
            item['meta'] = item['meta'].replace('{{$SERVICE_HOST}}', env.SERVICE_HOST)
            item['meta'] = item['meta'].replace('{{$PAGE_HOST}}', env.PAGE_HOST)
            serviceData[item['code']] = json.loads(item['meta'])
        
        pageData = merge_deep(pageData, serviceData)

        if 'page:attr' in pageData['page:info']:
            pageData['page:attr'] = merge_deep(pageData['page:attr'], pageData['page:info']['page:attr'])
            del pageData['page:info']['page:attr']

        self._cache[cacheKey] = pageData

        return pageData

    def getPageConfig(self, pageIndex='none', param={}, pageData={}):
        if hasattr(self, pageIndex):
            pageData = getattr(self, pageIndex)(param, pageData)
        return pageData
    
    def datamanage(self, param, pageData):
        checked = self.check_required('dataset', param)

        if not checked:
            res = ret(3)
            res['redirect'] = f'{env.PAGE_HOST}/app/datamanage?dataset=workflow_dataset'
            return res

        dataset = param['dataset']

        topMenu = self._get_tree({'group':'datamanage'})
        for item in topMenu:
            item['icon'] = item['meta']
            if dataset == item['code']:
                item['active'] = True

        pageData['top:menu'] = {"data":topMenu}

        pageData['data:list'] = {
            'param':{
                'dataset':dataset,
                'p':1
            },
            'data':{
                'code':-1,
                'msg':'数据加载中...'
            },
            'url':f'{env.SERVICE_HOST}/service/getservice',
            'updateUrl':f'{env.SERVICE_HOST}/service/update',
            'addUrl':f'{env.SERVICE_HOST}/service/add',
            'removeUrl':f'{env.SERVICE_HOST}/service/remove'
        }

        return pageData
    
    def usercenter(self, param, pageData):

        user = self.checkUserToken()
        if not user:
            return ret(13)
        

        topMenu = self._get_tree({'group':'usercenter'})
        for item in topMenu:
            if 'usercenter' == item['code']:
                item['active'] = True
                break

        pageData['top:menu'] = {"data":topMenu}

        pageData['app:list'] = {
            'url': '/service/getlist',
            'itemElement': 'app-card',
            'param': {
                'dataset': 'workflow_app','p':1,'size':5,'thead':'1'
            }
        }

        return pageData



    