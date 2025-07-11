import time,random,json
from comp.tool import json_ret as ret
from api.dataset import Dataset
from jdcloud_sdk.core.credential import Credential
from jdcloud_sdk.services.sms.client.SmsClient import SmsClient
from jdcloud_sdk.services.sms.apis.BatchSendRequest import BatchSendParameters, BatchSendRequest
 
import env

class SmsLogic:

    def apiToJson(self, data):
        if isinstance(data, tuple):
            data = data[0]
        if isinstance(data, str):
            data = json.loads(data)
        return data
    
    def post_dataset(self, path, param):
        token = self.token
        param['token'] = token
        
        res = ret(1)
        dataset = param.get('dataset')
        
        func = getattr(Dataset(), path)
        if func:
            res = func(param)
            res = self.apiToJson(res)
            
        return res
    def __init__(self, token, dataset):
        self.token = token
        self.dataset = dataset
        self.regionId = env.JD_REGION_ID
        self.access_key = env.JD_ACCESS_KEY
        self.secret_key = env.JD_SECRET_KEY
        self.credential = Credential(self.access_key, self.secret_key)
        self.client = SmsClient(self.credential)

    def send_code_sms(self, mobile, msg):
        try:
            # 设置模板Id
            templateId = env.JD_SMS_CODE_TEMPLATE_ID
            # 设置签名Id
            signId = env.JD_SMS_CODE_SIGN_ID
            # 设置发送手机号
            phoneList = [mobile]
            parameters = BatchSendParameters(regionId=self.regionId, templateId=templateId, signId=signId, phoneList=phoneList)
            parameters.setParams([msg])
            request = BatchSendRequest(parameters)
            resp = self.client.send(request)
            if resp.error is not None:
                print(resp.error.code, resp.error.message)
                return False
            if resp.result.get('message') == '执行成功':
                return True
        except Exception as e:
            print(e)
        
        return False


    def check(self, mobile, code='', is_remove=False):

        res = self.post_dataset('getinfo', {
            'mobile': mobile,
            'code': code,
            'dataset':self.dataset
        })

        if not res.get('data'):
            return False

        if time.time() < time.mktime(time.strptime(res['data']['expiretime'], '%Y-%m-%d %H:%M:%S')):
            return True
        
        if is_remove:
            ret = self.post_dataset('remove', {
                'mobile': mobile,
                'dataset':self.dataset,
                '_dconfig': json.dumps({
                    'type': 'hard',
                    'where': {
                        'mobile': ''
                    },
                    'id': 'ignore'
                })
            })

            print('remove',ret)

        return False

    def send_code(self, mobile):

        if self.check(mobile, '', True):
            return ret(11)
        
        code = random.randint(1000, 9999)

        res = self.post_dataset('update', {
            'mobile': mobile,
            'code': code,
            'expiretime': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() + 600)),
            'dataset':self.dataset,
            '_dconfig': json.dumps({
                'type': 'add'
            })
        })

        if res.get('code') != 0:
            return res

        is_success = self.send_code_sms(mobile, code)

        if is_success:
            return ret(0, '发送成功，请在手机短信中查收验证码', is_success)
        else:
            return ret(3, '发送失败')