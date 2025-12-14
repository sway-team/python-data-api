from flask import request
from comp.tool import rand
from comp.db import Database,Data
import json
from cachetools import TTLCache, cached
import env

_cache_ttl = 300
if env.ENV == 'dev':
    _cache_ttl = 30

_cache = TTLCache(maxsize=1000, ttl=_cache_ttl)

class BaseClass:

    _cache = _cache

    def checkUserToken(self):
        
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]

            if not token:
                return None
            
            if self._cache.get('checkUserToken:'+token):
                return self._cache.get('checkUserToken:'+token)
            
            user = self.getUser(token)

            self._cache['checkUserToken:'+token] = user
            return user
            
        return None

    def flushUserToken(self):
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            
            if not token:
                return False
            
            user = self.getUser(token)

            self._cache['checkUserToken:'+token] = user
            return user

        return False        
    
    def getUser(self, token):
        user = {}
        config = {
            'type':'data',
            'field':'id,nick,avatar,token,type,meta'
        }
            
        user = Data('user').get_one({'incode':token}, config)

        if user:
            if user.get('meta'):
                meta = json.loads(user['meta'])
                if meta.get('currentToken'):
                    user['currentToken'] = meta['currentToken']
                user['meta'] = meta
            else:
                user['meta'] = {}
        
        return user


    def apiToJson(self, data):
        if isinstance(data, tuple):
            data = data[0]
        if isinstance(data, str):
            data = json.loads(data)
        return data
        
    def get_param(self, request):
        param = {}
        if isinstance(request, dict):
            param = request
        elif request.method == 'GET':
            param = request.args.to_dict()
        else:
            param = request.form.to_dict()
            if not param:
                postdata = request.get_data()
                if postdata != b'':
                    try:
                        param = json.loads(postdata)
                    except:
                        pass
            else:
                if param.get('jsondata'):
                    try:
                        param['jsondata'] = json.loads(param['jsondata'])
                    except:
                        pass
        return param

    def check_token(self, token):
        _cacheKey = 'checkToken:'+token
        if self._cache.get(_cacheKey):
            return self._cache.get(_cacheKey)
        
        user = Data("user").get_one({"token":token})
        if not user:
            user = Data("app").get_one({"token":token})
            if not user:
                return None

        self._cache[_cacheKey] = user

        return user
    
    def checkUserOpenid(self, openid):
        user = Data('user').get_one({'token':openid}, {
            'type':'data',
            'field':'id,nick,avatar,token,type,meta'
        })
        if user:
            return user
        return None
    
    def check_required(self, keysstr, param):
        keys = keysstr.split(",")
        for key in keys:
            if key not in param:
                return False
        return True

    def get_client_ip(self):
        if 'X-Forwarded-For' in request.headers:
            ip = request.headers['X-Forwarded-For']
        elif 'X-Real-IP' in request.headers:
            ip = request.headers['X-Real-IP']
        else:
            ip = request.remote_addr
        return ip

    def inlog(self, param):        
        param['code'] = rand()
        param['ip'] = self.get_client_ip()
        if 'meta' in param:
            param['meta'] = json.dumps(param['meta'])

        # print(param)
        info = Database("inlog", param_check=False).update(param, {'type':'add'})
        return info
