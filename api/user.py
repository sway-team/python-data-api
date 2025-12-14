from flask import Blueprint,abort
from flask import request
from comp.base import BaseClass
from comp.tool import json_ret as ret,md5
from comp.smsJDlogic import SmsLogic
from api.dataset import Dataset
import json,random,re,time,hashlib
import env

router = Blueprint('user_router', __name__)
@router.route("/<path>", methods=["GET", "POST"], endpoint="go")
def go(path):
    if path in ['sendsms','login', 'reg', 'current']:
        func = getattr(Api(), path)
        if func:
            return func(request)
    else:
        return abort(404)

class Api(BaseClass):

    def __init__(self):
        self.token = env.ADMIN_TOKEN

    def post_dataset(self, path, param):
        token = self.token
        param['_dtoken'] = token
        
        res = ret(1)
        dataset = param.get('dataset')
        
        func = getattr(Dataset(), path)
        if func:
            res = func(param)
            res = self.apiToJson(res)
            
        return res
    
    def sendsms(self, request):
        param = self.get_param(request)
        checked = self.check_required("mobile", param)
        
        if not checked:
            return ret(1)
        
        mobile = param.get('mobile')

        smsLogic = SmsLogic(self.token, 'workflow_sms')
        res = smsLogic.send_code(mobile)

        return res
    
    def login(self, request):
        param = self.get_param(request)
        checked = self.check_required("mobile,pwd", param)

        if not checked:
            return ret(1, 'param error')

        user = {}

        if re.match(r'^\d{11}$', param['mobile']):
            user = self.post_dataset('getinfo', {
                'mobile': param['mobile'],
                'pwd':md5(param['pwd']),
                'dataset':'workflow_user'
            })
        else:
            user = self.post_dataset('getinfo', {
                'name': param['mobile'],
                'pwd':md5(param['pwd']),
                'dataset':'workflow_user'
            })

        if not user.get('data'):
            return ret(7, '用户或密码错误')
                
        del user['data']['pwd']
        # 生成用户token
        user_data = user.get('data')
        
        # 设置过期时间（可以根据参数选择1天或30天）
        expire_days = 30 if param.get('isremember') else 1
        expiretime = int(time.time() + expire_days * 24 * 3600)
        # 生成用户token，加入过期时间
        user_token = md5(str(user_data['id']) + str(time.time()) + str(expiretime))        
        # 更新用户token和过期时间
        result = self.post_dataset('update', {
            'id': user_data['id'],
            'incode': user_token,
            'expiretime': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(expiretime)),
            'dataset':'workflow_user'
        })

        if result.get('code') != 0:
            return ret(3)
        
        user_data['token'] = user_token
        user_data['redirect'] = env.PAGE_HOST + '/app/usercenter'

        return ret(0, data=user_data)

    
    def reg(self, request):
        param = self.get_param(request)
        checked = self.check_required("mobile,pwd", param) #,code

        if not checked:
            return ret(1)

        if env.ENV == 'prod':

            mobile = param['mobile']

            if not re.match(r'^\d{11}$', mobile):
                return ret(10, '手机号格式错误')

            smsLogic = SmsLogic(self.token, 'workflow_sms')

            is_sms_checked = smsLogic.check(mobile, param['code'])

            if not is_sms_checked:
                return ret(1, '验证码错误')
        

        result = self.post_dataset('getinfo', {
            'mobile': param['mobile'],
            'dataset':'workflow_user'
        })

        if result.get('data'):
            return ret(12, '用户已存在')
        
        param['pwd'] = md5(param['pwd'])
        # 更新用户token
        result = self.post_dataset('add', {
            'name': param['name'],
            'nick': param['name'],
            'mobile': param['mobile'],
            'pwd': param['pwd'],
            'dataset':'workflow_user'
        })

        return result

    def current(self, request):
        param = self.get_param(request)
        checked = self.check_required("currentToken", param)
        if not checked:
            return ret(1)
        
        user = self.checkUserToken()
        
        if not user:
            return ret(1)

        if user.get('meta'):
            meta = user['meta']
            meta['currentToken'] = param['currentToken']
        else:
            meta = {
                'currentToken': param['currentToken']
            }

        res = self.post_dataset('update', {
            'dataset': 'workflow_user',
            'id': user['id'],
            'meta': json.dumps(meta)
        })

        if res.get('code') == 0:
            self.flushUserToken()

        return res


    def addUpdateData(self, dataset, param, where):

        result = self.post_dataset(dataset, 'getinfo', where)

        if not result.get('data'):
            result = self.post_dataset(dataset, 'add', param)
        else:
            param['id'] = result['data']['id']
            result = self.post_dataset(dataset, 'update', param)

        return result


    # def getAppUserByOpenid(self, request, config):
    #             # auth_header = request.headers.get('Authorization')
    #     if request.headers.get('openid'):
    #         openid = request.headers.get('openid')
    #         print(openid)
    #         da = Dataset()
    #         result = da.getinfo({
    #             'openid': openid,
    #             **config
    #         })
    #         result = self.apiToJson(result)
    #         user_data = None
    #         if result.get('data'):
    #             user_data = result.get('data')
    #             if user_data.get('pwd'):
    #                 del user_data['pwd']
    #             if user_data.get('mobile'):
    #                 user_data['mobile'] = '******' + user_data['mobile'][-4:]
    #         return user_data
    #     return None

    # def userUpdate(self, request):
    #     param = self.get_param(request)

    #     token = '3923bb6c65a1f9b1b998c9e84fde2018'        
    #     prefix = self.token_prefix[token]
    #     dataset = f'{prefix}_users'

    #     config = {
    #         'dataset': dataset,
    #         'token': token
    #     }

    #     user = self.getAppUserByOpenid(request, config)
    #     if not user or not user.get('id'):
    #         return ret(13)
    #     da = Dataset()
    #     param['id'] = user['id']

    #     # $param['avatar'] = $avatarUrl;
    #     res = da.update({**param, **config})
    #     res = self.apiToJson(res)

    #     if res['code'] == 0:
    #         res = da.getinfo({
    #             'id': user['id'],
    #             **config
    #         })
    #         res = self.apiToJson(res)
    #     return res