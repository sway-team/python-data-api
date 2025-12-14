from comp.db import Data
from comp.tool import json_ret,rand
from conf.workflow import workflowConfig
from copy import deepcopy
import json,env,math
from urllib.parse import quote_plus
from cachetools import TTLCache



_cache_ttl = 300
if env.ENV == 'dev':
    _cache_ttl = 30

_cache = TTLCache(maxsize=1000, ttl=_cache_ttl)
whiteSet = ['workflow_dataprop','workflow_tree','workflow_datain',\
                    'workflow_dataset','workflow_datafilter','workflow_prototype',\
                        'workflow_instance','workflow_org','workflow_configbox','workflow_framebox','workflow_app','workflow_user']


class DataLogic:

    def __init__(self):
        self._cache = _cache
        self.whiteSet = whiteSet
    # dataConfig = {'data':{'dataset':{
    #     'datatable':'dataset',
    #     'meta':{
    #         'dataType':'mysql',
    #         'count':{
    #             'sql':'select count(*) as num from dataset'
    #         },
    #         'list':{
    #             'where':'',
    #             'order':'',
    #             'limit':''
    #         }
    #     }
    # },'inconfig':{},'dataprop':{}}}

    # count、incordsc、sum、query 待实现

    def func_combo(self, code, param, auth, config={}, funcName="", type=""):
        if type in ['add','update','remove'] and not param:
            return json_ret(1)

        dataConfig = self.checkDataConfig(code, auth)

        if dataConfig['code'] != 0:
            return dataConfig
        # print(code, dataConfig)
        dataset = dataConfig['data']['dataset']
        inconfig = dataConfig['data']['inconfig']
        dataprop = dataConfig['data']['dataprop']
        invalues = dataConfig['data']['invalues']
                
        dbModel = Data(dataset['datatable'], schema=inconfig['db_name'], uri=inconfig['uri'])
        meta = dataset['meta']

        if funcName == 'query':
            query = param['query']
            res = dbModel.query(query)
            return res
        if type == 'list' and 'dataType' in meta and meta['dataType'] == 'sql':
            sql = meta['count']['sql']
            res = dbModel.query(sql)
        else:

            if not 'order' in config and 'db_order' in inconfig :
                config['order'] = inconfig['db_order']

            if 'order' in param:
                config['order'] = param['order']
            
            sqlConfig = self.checkSQLconfig(code, type, dataprop, config)           

            param = self.checkPropConfig(type, param, dataprop, config)

            if type == 'update' and 'updatefield' in param:
                sqlConfig['updatefield'] = param['updatefield']
                del param['updatefield']

            if type == 'index' and 'list' in meta:
                sqlConfig = dict(sqlConfig, **meta['list'])

            if type in meta:
                sqlConfig = dict(sqlConfig, **meta[type])
                sqlConfig = dict(sqlConfig, **config)

            
            if type == 'list' or type == 'index':
                if 'db_remove_type' in inconfig :
                    param[inconfig['db_remove_type']] = '$empty'
                    sqlConfig['status'] = 'ignore'
                if 'status' in sqlConfig and sqlConfig['status'] == 'ignore':
                    del sqlConfig['where']['status']
            elif type == 'add':        
                if 'createtoken' not in param and 'createtoken' in sqlConfig['field']:
                    param['createtoken'] = auth['token']

                sqlConfig['type'] = 'add'
            
            elif type == 'remove': 
                if 'id' not in sqlConfig or sqlConfig['id'] != 'ignore':
                    if 'dataid' in param:
                        param['id'] = param['dataid']
                        del param['dataid']
                    
                    if 'id' not in param or not param['id']:
                        return json_ret(3)

                if sqlConfig['type'] != 'hard' and 'db_remove_type' in inconfig :
                    sqlConfig['type'] = inconfig['db_remove_type']

            if invalues:
                sqlConfigStr = json.dumps(sqlConfig)

                # 遍历 $invalues 的item，得到field和value
                # 如果 $sqlConfigStr 有 field 则替换为 value
                for item in invalues:
                    field = item['field']
                    value = item['value']
                    sqlConfigStr = sqlConfigStr.replace('{{'+field+'}}', value)
                
                sqlConfig = json.loads(sqlConfigStr)

            funcBody = getattr(dbModel, funcName)

            if funcBody:
                # print(sqlConfig)
                ret = funcBody(param, sqlConfig)
            else:
                return False

            if 'handle' in sqlConfig:
                for handle in sqlConfig['handle']:
                    if handle['type'] == 'file':
                        handle['content'] = open('https://s.nowkey.net/workflow/handle/'+dataset['code']+'_handle_'+handle['name']+'.py', 'r').read()
                        # handle['content'] = handle['content'].replace('<?php', '')
                    try:
                        exec(handle['content'])
                        handler = lambda res, config: eval(handle['name']+'(res)')
                        ret = handler(ret, config)
                    except Exception as e:
                        print(e)

            if funcName == 'get_one' or funcName == 'count':
                return ret

            if type == 'index':
                ret['thead'] = dataprop
                ret['dataset'] = dataset

            if param.get('thead') == '1':
                ret['thead'] = dataprop
        
        if 'type' in auth and auth['type'] == '1':
            ret['dataset'] = dataset

        ret['sqlConfig'] = sqlConfig

        return ret


    def get_data_service(self, code, param, auth, config={}):
        ret = self.func_combo(code, param, auth, config, 'get_list', 'index')

        if int(ret['code']) != 0:
            return ret
        
        if int(ret['size']) > 0:
            page_count = math.ceil(int(ret['total'])/int(ret['size']))
        else:
            page_count = 1
            
        pageList = []
        for i in range(page_count):
            pageList.append(i+1)
        


        serRet = {**{
            'search' : param,
            'boxid' : code,
            'page': pageList,
            'tbody' : ret['data']
        }, **ret}

        del serRet['data']

        return serRet

    def get_list(self, code, param, auth, config={}):
        ret = self.func_combo(code, param, auth, config, 'get_list', 'list')
        return ret
    
    def get_info(self, code, param, auth, config={}):
        ret = self.func_combo(code, param, auth, config, 'get_one', 'info')

        if 'code' in ret and 'data' in ret and ret['code'] != 0:
            return ret
        
        ret = json_ret(0, data=ret)
        return ret

    def count(self, code, param, auth, config={}):
        ret = self.func_combo(code, param, auth, config, 'count', 'list')
        ret = json_ret(0, data=ret)
        return ret
    
    def query(self, code, param, auth, config={}):
        ret = self.func_combo(code, param, auth, config, 'query', 'query')
        ret = json_ret(0, data=ret)
        return ret
    def incordsc(self, code, param, auth, config={}):
        ret = self.func_combo(code, param, auth, config, 'incordsc', 'update')
        return ret
    
    def remove_data(self, code, param, auth, config={}):
        ret = self.func_combo(code, param, auth, config, 'remove', 'remove')
        return ret
    
    def update_data(self, code, param, auth, config={}):
        ret = self.func_combo(code, param, auth, config, 'update', 'update')
        return ret
        
    def add_data(self, code, param, auth, config={}):
        ret = self.func_combo(code, param, auth, config, 'update', 'add')
        return ret
    
    def checkSQLconfig(self, code, type = '', dataprop = [], config = []):
        
        if code in self.whiteSet:
            from conf.workflow import defaultField
            dataprop = dataprop + defaultField

        field = [prop['code'] for prop in dataprop]
        infoField = '`'+'`,`'.join(field)+'`'
        updateField = dict.fromkeys(field, '')

        dConfig = {
            'where':dict(updateField, status='0'),
            'order':'updatetime desc'
        }

        if(type == 'list'):
            dConfig = dict(dConfig, **{
                'type':'data+size',
                'size':50,
                # 'field':infoField,
                # 'thead':dataprop
            })
        # elif(type == 'info'):
            # dConfig = dict(dConfig, field=infoField)
        elif(type == 'add' or type == 'update'):
            dConfig = {
                'where':{'id':''},
                'field':updateField
            }
        elif(type == 'remove'):
            dConfig = {
                'type':'soft',
                'where':{'id':''}
            }
        dConfig = dict(dConfig, **config)

        return dConfig

    def checkDataConfig(self, code = "", auth = {}):
        
        if not code or not auth:
            return json_ret(3)

        _cacheKey = 'checkDataConfig:'+code+auth['token']
        if self._cache.get(_cacheKey):
            return self._cache.get(_cacheKey)

        setparam = {'code':code}
        inparam = {}

        if 'type' in auth and auth['type'] != '1' and code not in self.whiteSet:
            setparam['createtoken'] = auth['token']
            inparam['createtoken'] = auth['token']
        
        setres = Data('dataset').get_one(setparam)
        
        if setres is None or 'datain' not in setres:
            return json_ret(1, 'dataset error')

        inparam['code'] = setres['datain']
        inres = Data('datain').get_one(inparam)

        if inres is None:
            return json_ret(1, 'datain error')

        if 'meta' in setres and setres['meta'] is not None:
            setres['meta'] = json.loads(setres['meta'])
        else:
            setres['meta'] = {}

        if inres['stype'] == 'mysql':
            if 'meta' in inres and inres['meta'] is not None:
                inconfig = json.loads(inres['meta'])
                del inres['meta']

            if not inconfig:
                return json_ret(2)
            
            invalues = inconfig.get('values', []);
            
            local = 'dev'

            if env.ENV == 'prod':
                local = 'prod'

            inconfig = inconfig[local]
            
            inconfig['db_pwd'] = quote_plus(inconfig['db_pwd'])

            # if env.ENV == 'dev':
            #     inconfig['db_pwd'] = env.DB_PWD
            inconfig['uri'] = 'mysql+pymysql://{db_user}:{db_pwd}@{db_host}:{db_port}/{db_name}?charset=utf8mb4'.format(**inconfig)

        propres = []

        if 'dataType' in setres['meta'] and setres['meta']['dataType'] == 'sql':
            propres = []
        else:
            if setres['datain'] == 'workflow_db':
                if setres['datatable'] in workflowConfig:
                    propres = deepcopy(workflowConfig[setres['datatable']]['thead'])
            
            if not propres:
                propres = Data('dataprop').get_data({
                    'datasetcode':setres['code']
                }, {
                    'order':'index asc'
                })
            # 需要验证数据表是否存在
            if not propres:
                dao = Data(setres['datatable'], schema=inconfig['db_name'], uri=inconfig['uri'])
                isExist = dao.exists()
                # exit()
                if not isExist:
                    return json_ret(15)
                
                ret = dao.get_columns()
                for key,item in enumerate(ret):
                    pt = {
                        'datasetcode':setres['code'],
                        'code': item['name'],
                        'cname': item['name'],
                        'index': key,
                        'type': 'text'
                    }

                    if 'text' in str(item['type']).lower():
                        pt['type'] = 'textarea'

                    propres.append(pt)
            else:
                for key,prop in enumerate(propres):
                    # prop = propres[key]
                    if 'meta' in prop and prop['meta'] is not None:
                        meta = json.loads(prop['meta'])
                        prop = {**prop, **meta}
                        del prop['meta']
                        propres[key] = prop

        if 'defaultField' in inconfig:
            propres = dict(inconfig['defaultField'].items() + propres.items())

        dataConfig = {
            'dataset':setres,
            'datain':inres,
            'inconfig':inconfig,
            'invalues':invalues,
            'dataprop':propres
        }
        
        result = json_ret(0, data=dataConfig)
        self._cache[_cacheKey] = result

        return result

    def checkPropConfig(self, type, where = {}, dataprop = [], config = []):
        for key,prop in enumerate(dataprop):
            if type == 'add' and 'add' in prop:
                if prop['add'] == 'md5':
                    where[prop['code']] = rand()
                    if 'md5len' in prop:
                        where[prop['code']] = rand()[:prop['md5len']]
            # if type == 'getinfo' and 'getinfo' in prop:
            #     if prop['getinfo'] == 'nl2p':
            #         where[prop['code']] = nl2p(where[prop['code']])
        
        return where