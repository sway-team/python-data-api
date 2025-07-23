from flask import Blueprint,abort
from flask import request
from comp.base import BaseClass
from comp.tool import json_ret as ret, unset, DatetimeEncoder
import json
from comp.db import Data
from comp.datalogic import DataLogic
import hashlib

router = Blueprint('frame_router', __name__)
@router.route("/<path>", methods=["GET", "POST"], endpoint="go")
def go(path):
    if path in ['getframe','getconfig']:
        func = getattr(Frame(), path)
        if func:
            return func(request)
    else:
        return abort(404)

class Frame(BaseClass):
    
    def param_filter(self, param, configName='list'):
        config = {}
        if 'filter' in param and param['filter'] != '':
            filterItem = Data('datafilter').get_one({
                'datasetcode':param['dataset'],
                'code':param['filter'],
                'createtoken':param['token']
            })
            if not filterItem:
                return config
            fconfig = json.loads(filterItem['meta'])
            if not fconfig:
                return config
            config = fconfig[configName]
        
        if '_dconfig' in param:
            dconfig = json.loads(param['_dconfig'])
            config = dict(config, **dconfig)
        
        unset(param, '_dconfig,filter,dataset,token')

        return config
    # 后续版本开发，先注释掉
    # def getframe(self, request):
    #     param = request.args
    #     user = self.checkToken(param['token'])
    #     cacheIndex = param['token'].'_'.$param['root'].'_'.$param['group']
    #     cachePath = RUNTIME_PATH."Cache/Frame/"
    #     cacheFrame = F(cacheIndex, "", $cachePath); 
    #     if(!empty($cacheFrame) && time() - $cacheFrame['limitTime'] < $cacheFrame['cacheTime']){
    #         $this->ajaxReturn($cacheFrame);
    #         return;
    #     }
    #     $config = $this->paramFilter($param);
    #     res = self.getDataList('workflow_framebox', [
    #         'root'=>$param['root'],'group'=>join(',', $gparam)
    #     ], $user, $config);
    #     return ret(0, res)
    
    def getconfig(self, request):
        param = self.get_param(request)
        checked = self.check_required("token,group", param)
        if not checked:
            return ret(1, 'param error')
        user = self.check_token(param.get("token"))
        if not user:
            return ret(1, 'token error')
        
        param['createtoken'] = user['token']

        md5 = hashlib.md5(param.__str__().encode()).hexdigest()
        
        cacheKey = "frame_getconfig_"+md5
        
        if self._cache.get(cacheKey):
            print('read cache:'+cacheKey)
            return self._cache.get(cacheKey)

        config = self.param_filter(param)
        


        res = DataLogic().get_list('workflow_configbox', param, user, config)

        self._cache[cacheKey] = res

        return res