from flask import Blueprint,abort
from flask import request
from comp.base import BaseClass
from comp.tool import json_ret as ret, unset, DatetimeEncoder
import json
from comp.db import Data
from comp.datalogic import DataLogic

router = Blueprint('dataset_router', __name__)
@router.route("/<path>", methods=["GET", "POST"], endpoint="go")
def go(path):
    if path in ['getlist','getinfo','add','update','remove','count', 'func']:
        func = getattr(Dataset(), path)
        if func:
            return func(request)
    else:
        return abort(404)

class Dataset(BaseClass):
    
    def param_filter(self, param, configName='list'):
        
        config = {}

        if 'filter' in param and param['filter'] != '':
            _cacheKey = 'param_filter:'+param['dataset']+param['filter']+param['_dtoken']
            if self._cache.get(_cacheKey):
                config = self._cache.get(_cacheKey)
            else:
                filterItem = Data('datafilter').get_one({
                    'datasetcode':param['dataset'],
                    'code':param['filter'],
                    'createtoken':param['_dtoken']
                })

                if not filterItem:
                    return config
                
                fconfig = json.loads(filterItem['meta'])
                
                if not fconfig:
                    return config
                
                config = fconfig[configName]
                self._cache[_cacheKey] = config
        
        if '_dconfig' in param:
            dconfig = json.loads(param['_dconfig'])
            config = dict(config, **dconfig)
        
        unset(param, '_dconfig,filter,dataset,_dtoken')

        return config

    # // searchKey:搜索key值str
    # // searchParam:搜索参数obj
    # // comboParam:取原搜索参数key值[]
    # // relateKey:关联合并数据的参数搜索key值str
    # // comboKey:混合key
    # // dataType:mix,list,default
    # // mix 分组多分类数据用 关联的key值为索引，comboKey为key，comboKeySuffix为key前缀，comboVal为val值
    # // list 分组数据用 关联的key值为索引
    # {
    #     "searchKey": "id",
    #     "dataset": "db_user_task",
    #     "relateKey": "exercise_id",
    #     "comboKey": "count",
    #     "dataType": "list"
    #   },

    def _combo_proc_list(self, combo, comboData):
        listObj = {}
        for item in comboData:
            relateValue = item[combo['relateKey']]
            if relateValue not in listObj:
                listObj[relateValue] = []
            listObj[relateValue].append(item)

        return listObj

    def combo_builder(self, param, resData, comboList, user):
        daLogic = DataLogic()
        for combo in comboList:
            # 拿索引去重
            values = [item[combo['searchKey']] for item in resData]
            values = list(set(values))
            # 将列表转换为字符串，逗号分隔
            values = ','.join([str(v) for v in values])
            
            searchParam = combo.get('searchParam', {})
            # 合并输入参数
            if 'comboParam' in combo:
                for key, value in combo['comboParam'].items():
                    combo['comboParam'][key] = param[key]
                searchParam = dict(searchParam, **combo['comboParam'])

            searchParam[combo['relateKey']] = values
            comboConfig = combo.get('list', {})
            comboConfig['search'] = [{'field':combo['relateKey'], 'type':'in'}]
            comboConfig['size'] = ''

            comboType = combo.get('dataType', 'list')
            comboData = {}

            if comboType == 'sql':
                query = combo.get('query', '')

                if not query:
                    return resData

                if 'where' not in query:
                    query = query.split(combo['dataset'])
                    query = query[0] + combo['dataset'] + ' where ' + combo['relateKey'] + ' in (' + values + ') ' + query[1]
                searchParam['query'] = query
                comboRes = daLogic.query(combo['dataset'], searchParam, user, comboConfig)
                comboData = comboRes.get('data')

                if not comboData:
                    continue
            else:
                comboRes = daLogic.get_list(combo['dataset'], searchParam, user, comboConfig)
                comboData = comboRes.get('data')

            if not comboData:
                continue

                # if comboType == 'mix':
                #     listObj = {}
                #     for item in comboData:
                #         index = item[combo['relateKey']]
                #         if 'comboKeySuffix' not in combo:
                #             combo['comboKeySuffix'] = ""
                #         if index not in listObj:
                #             listObj[index] = {}
                #         listObj[index][item[combo['comboKey']]+combo['comboKeySuffix']] = item[combo['comboVal']]
                #     comboData = listObj
            
            listObj = comboData
            if type(comboData) == list:
                listObj = self._combo_proc_list(combo, comboData)

            for key, item in enumerate(resData):
                fieldValue = item[combo['searchKey']]
                if 'comboKey' in combo:
                    ckey = combo['comboKey']
                    if listObj.get(fieldValue):
                        # if comboType =='mix':
                        #     resData[key] = dict(resData[key], **listObj[fieldValue])
                        # else:
                        resData[key][ckey] = listObj[fieldValue]
                    else:
                        resData[key][ckey] = []

                elif listObj.get(fieldValue):
                    resData[key] = dict(resData[key], **listObj[fieldValue])
        
        return resData



    
    def func_combo(self, request, funcName):
        param = self.get_param(request)
        checked = self.check_required("_dtoken,dataset", param)
        if not checked:
            return ret(1, 'param error')
        user = self.check_token(param.get("_dtoken"))
        if not user:
            return ret(1, '_dtoken error')
        code = param.get("dataset")
        config = self.param_filter(param)
        is_empty = True
        for val in param:
            if not val and val!= '0':
                pass
            else:
                is_empty = False
                break
        if is_empty:
            return ret(1)
        
        if funcName == 'func':
            if code == 'workflow_dataset_query':
                iddata = json.loads(param['data'])
                dataset = iddata['dataset']
                res = DataLogic().query(dataset, iddata, user)
                return res

            if code == 'workflow_dataset_incordsc':
                iddata = json.loads(param['data'])
                dataset = iddata['dataset']
                idparam = iddata['param']
                idconfig = iddata['conf']
                res = DataLogic().incordsc(dataset, idparam, user, idconfig)
                return res
        
        funcBody = getattr(DataLogic(), funcName)
        if funcBody:
            resJson = funcBody(code, param, user, config)
            if funcName in ['get_list', 'get_data_service'] and 'combo' in config and resJson['data']:
                resJson['data'] = self.combo_builder(param, resJson['data'], config['combo'], user)
        else:
            resJson = ret(15)

        if 'sqlConfig' in resJson:
            sqlConfig = resJson['sqlConfig']
            del resJson['sqlConfig']
            config['sqlConfig'] = sqlConfig

        loginfo = self.__log(user['token'], funcName, json.dumps(config, cls=DatetimeEncoder), code, param)
        resJson['logid'] = loginfo['code']
                
        resJson = json.dumps(resJson, cls=DatetimeEncoder)

        return resJson
    
    def func(self, request):
        ret = self.func_combo(request, 'func')
        return ret, {'Content-Type':'application/json'}
    

    def add(self, request):
        ret = self.func_combo(request, 'add_data')
        return ret, {'Content-Type':'application/json'}
    
    def update(self, request):
        ret = self.func_combo(request, 'update_data')
        return ret, {'Content-Type':'application/json'}
    
    def remove(self, request):
        ret = self.func_combo(request, 'remove_data')
        return ret, {'Content-Type':'application/json'}

    def getlist(self, request):
        ret = self.func_combo(request, 'get_list')
        return ret, {'Content-Type':'application/json'}
    
    def getinfo(self, request):
        ret = self.func_combo(request, 'get_info')
        return ret, {'Content-Type':'application/json'}
    
    def count(self, request):
        ret = self.func_combo(request, 'count')
        return ret, {'Content-Type':'application/json'}

    def getservice(self, request):
        code = request.get('dataset')
        ret = self.func_combo(request, 'get_data_service')
        return ret, {'Content-Type':'application/json'}

    
    def __log(self, token, action, content, code, param):
        loginfo = {'data':{'code':'dev'}}
        loginfo = self.inlog({
            'createtoken':token,
            'group':'DataApi',
            'action':action,
            'content':content,
            'meta':{
                'code':code,
                'where':param
            }
        })
        return loginfo
    

