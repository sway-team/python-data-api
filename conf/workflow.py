import env

defaultField = [
    {'code': 'id', 'cname': 'id', 'type': 'readonly'},
    {'code': 'type', 'cname': 'type', 'type': 'hidden'},
    {'code': 'status', 'cname': 'status', 'type': 'hidden'},
    {'code': 'createtime', 'cname': 'createtime', 'type': 'hidden'},
    {'code': 'updatetime', 'cname': 'updatetime', 'type': 'hidden'}
]

tableConfig = {
    'configbox': {
        'thead': [
            {'type': 'hidden','cname': 'id','code': 'id'},
            {'type': 'text','cname': 'code','code': 'code'},
            {'type': 'text','cname': 'name','code': 'name'},
            {'type': 'text','cname': 'desc','code': 'desc'},
            {'type': 'text','cname': 'group','code': 'group'},
            {'type': 'json','cname': 'meta','code': 'meta'},
            {'type': 'text','cname': 'token','code': 'token','meta': '{"check":"md5","add":"md5"}'},
            {'type': 'hidden','cname': 'createtoken','code': 'createtoken'}
        ]
    },
    'user': {
        'thead': [
            {'type': 'hidden','cname': 'id','code': 'id'},
            {'type': 'text','cname': 'name','code': 'name'},
            {'type': 'text','cname': 'nick','code': 'nick'},
            {'type': 'text','cname': 'mobile','code': 'mobile'},
            {'type': 'text','cname': 'pwd','code': 'pwd'},
            {'type': 'textarea','cname': 'meta','code': 'meta'},
            {'type': 'text','cname': 'type','code': 'type'},
            {'type': 'text','cname': 'avatar','code': 'avatar'},
            {'type': 'text','cname': 'token','code': 'token','meta': '{"check":"md5","add":"md5"}'},
            {'type': 'text','cname': 'incode','code': 'incode'},
            {'type': 'text','cname': 'expiretime','code': 'expiretime'}
        ]
    },
    'org': {
        'thead': [
            {'type': 'hidden','cname': 'id','code': 'id'},
            {'type': 'text','cname': 'code','code': 'code'},
            {'type': 'text','cname': 'name','code': 'name'},
            {'type': 'text','cname': 'mission','code': 'mission'},
            {'type': 'text','cname': 'vision','code': 'vision'},
            {'type': 'textarea','cname': 'corevalue','code': 'corevalue'},
            {'type': 'textarea','cname': 'meta','code': 'meta'},
            {'type': 'text','cname': 'token','code': 'token','meta': '{"check":"md5","add":"md5"}'},
            {'type': 'hidden','cname': 'createtoken','code': 'createtoken'}
        ]
    },
    'app': {
        'thead': [
            {'type': 'hidden','cname': 'id','code': 'id'},
            {'type': 'text','cname': 'code','code': 'code'},
            {'type': 'text','cname': 'name','code': 'name'},
            {'type': 'text','cname': 'mission','code': 'mission'},
            {'type': 'text','cname': 'vision','code': 'vision'},
            {'type': 'textarea','cname': 'corevalue','code': 'corevalue'},
            {'type': 'textarea','cname': 'meta','code': 'meta'},
            {'type': 'text','cname': 'token','code': 'token','meta': '{"check":"md5","add":"md5"}'},
            {'type': 'hidden','cname': 'createtoken','code': 'createtoken'}
        ]
    },
    
    'framebox':{
        'thead' : [
            {'type':'hidden', 'cname':'id', 'code':'id'},
            {'type':'text', 'cname':'code', 'code':'code'},
            {'type':'text', 'cname':'parentid', 'code':'parentid'},
            {'type':'text', 'cname':'root', 'code':'root'},
            {'type':'text', 'cname':'group', 'code':'group'},
            {'type':'text', 'cname':'cname', 'code':'cname'},
            {'type':'json', 'cname':'meta', 'code':'meta'},
            {'type':'text', 'cname':'index', 'code':'index'},
            {'type':'text', 'cname':'token', 'code':'token','meta': '{"check":"md5","add":"md5"}'},
            {'type':'hidden', 'cname':'createtoken', 'code':'createtoken'},
        ]
        
    },
    'dataset':{
        'thead' : [
            {'type':'hidden', 'cname':'id', 'code':'id'},
            {'type':'text', 'cname':'datain', 'code':'datain'},
            {'type':'text', 'cname':'datatable', 'code':'datatable'},
            {'type':'text', 'cname':'code', 'code':'code', 'href':env.SERVICE_HOST + '/service/getlist?dataset={{code}}&token={{createtoken}}&size=50'},
            {'type':'text', 'cname':'cname', 'code':'cname', 'href':env.PAGE_HOST+'/app/datamanage?dataset={{code}}&token={{createtoken}}'},
            {'type':'json', 'cname':'meta', 'code':'meta'},
            {'type':'text', 'cname':'createtoken', 'code':'createtoken'},
        ]
    },
    'datain':{
        'thead' : [
            {'type':'hidden', 'cname':'id', 'code':'id'},
            {'type':'text', 'cname':'code', 'code':'code'},
            {'type':'json', 'cname':'meta', 'code':'meta'},
            {'type':'text', 'cname':'stype', 'code':'stype'},
            {'type':'text', 'cname':'类型', 'code':'type'},
            {'type':'text', 'cname':'createtoken', 'code':'createtoken'},
        ]
    },
    'dataprop':{
        'thead' : [
            {'type':'hidden', 'cname':'id', 'code':'id'},
            {'type':'text', 'cname':'datasetcode', 'code':'datasetcode'},
            {'type':'text', 'cname':'code', 'code':'code'},
            {'type':'cname', 'cname':'cname', 'code':'cname'},
            {'type':'textarea', 'cname':'meta', 'code':'meta'},
            {'type':'text', 'cname':'类型', 'code':'type'},
            {'type':'text', 'cname':'createtoken', 'code':'createtoken'},
        ]
    },
    'datafilter':{
        'thead' : [
            {'type':'hidden', 'cname':'id', 'code':'id'},
            {'type':'text', 'cname':'datasetcode', 'code':'datasetcode'},
            {'type':'text', 'cname':'code', 'code':'code','href':env.SERVICE_HOST + '/service/getlist?dataset={{datasetcode}}&filter={{code}}&token={{createtoken}}'},
            {'type':'cname', 'cname':'cname', 'code':'cname'},
            {'type':'json', 'cname':'meta', 'code':'meta'},
            {'type':'text', 'cname':'createtoken', 'code':'createtoken'},
        ]
    },
    'tree':{
        'thead' : [
            {'type':'hidden', 'cname':'id', 'code':'id'},
            {'type':'text', 'cname':'code', 'code':'code'},
            {'type':'text', 'cname':'parentid', 'code':'parentid'},
            {'type':'text', 'cname':'group', 'code':'group'},
            {'type':'text', 'cname':'cname', 'code':'cname'},
            {'type':'text', 'cname':'desc', 'code':'desc'},
            {'type':'textarea', 'cname':'meta', 'code':'meta'},
            {'type':'text', 'cname':'index', 'code':'index'},
            {'type':'text', 'cname':'token', 'code':'token','meta': '{"check":"md5","add":"md5"}'},
            {'type':'hidden', 'cname':'createtoken', 'code':'createtoken'},
        ],
        'list' : {
            'order':'index asc'
        }
    },
    'inlog':{
        'thead' : [
            {'type':'hidden', 'cname':'id', 'code':'id'},
            {'type':'text', 'cname':'code', 'code':'code'},
            {'type':'text', 'cname':'content', 'code':'content'},
            {'type':'text', 'cname':'group', 'code':'group'},
            {'type':'text', 'cname':'action', 'code':'action'},
            {'type':'textarea', 'cname':'meta', 'code':'meta'},
            {'type':'hidden', 'cname':'createtoken', 'code':'createtoken'},
        ]
    }
}

for datasetcode, tableItem in tableConfig.items():
    for index, thead in enumerate(tableItem['thead']):
        thead['datasetcode'] = datasetcode
        thead['index'] = index

def buildTableConfig(tableConfig):
    modelConfig ={}
    for tableName, tableItem in tableConfig.items():

        field = [thead['code'] for thead in tableItem['thead']]
        infoField = '`'+'`,`'.join(field)+'`'
        updateField = dict.fromkeys(field, '')

        modelConfig[tableName] = {
            'list':{
                'type':'data',
                'where':{**updateField, 'status':'0'},
                'order':'updatetime desc',
                'field':infoField
            },
            'index':{
                'type':'service',
                'size':'50',
                'where':{**updateField, 'status':'0'},
                'order':'updatetime desc',
                'field':infoField,
                'thead':tableItem['thead']
            },
            'info':{
                'where':{**updateField, 'status':'0'},
                'order':'updatetime desc',
                'field':infoField
            },
            'update':{
                'where':{'id':''},
                'field':updateField
            },
            'remove':{
                'type':'soft',
                'where':{'id':''}
            },
            'config':{
                'display':'Admin/manage'
            },
            'data':{}
        }

        for key, config in modelConfig[tableName].items():
            if key in tableItem:
                modelConfig[tableName][key] = {**config, **tableItem[key]}

        modelConfig[tableName]['thead'] = tableItem['thead']

    return modelConfig

workflowConfig = buildTableConfig(tableConfig)

