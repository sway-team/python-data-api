from sqlalchemy import exc,create_engine, MetaData, Table, select,text,func,and_,inspect
from sqlalchemy.orm import sessionmaker,scoped_session,aliased
from comp.tool import json_ret as ret,tprint
from conf.workflow import workflowConfig
from copy import deepcopy
from datetime import datetime
import random
import env,re
from flask import abort

def parse_join(s):
    # left join `character` as c on c.id = f.userb
    #通过正则语句解析 s 语句返回一个字典，格式和ret一样
    ret = {
        'table': '',
        'alias': '',
        'method': '',
        'rfield': '',
        'lfield': ''
    }
    s = s.strip()    # 正则匹配 

    if s.find('join') < 0:
        s = 'join ' + s
    p = re.compile(r'(.*?)join (.+) as (.+) on (.+) = (.+)')
    m = p.match(s)
    if m:
        ret['method'] = m.group(1).strip()
        ret['table'] = m.group(2).replace('`','').strip()
        
        alias = m.group(3).strip()
        rfield = m.group(4).replace('`','').strip()
        lfield = m.group(5).replace('`','').strip()

        if lfield.find(alias+'.') >= 0:
            lfield,rfield = rfield,lfield

        if lfield.find('.') > 0:
            lfield = lfield.split('.')[1]

        if rfield.find('.') > 0:
            rfield = rfield.split('.')[1]

        ret['alias'] = alias
        ret['rfield'] = rfield
        ret['lfield'] = lfield

    else:
        return False

    return ret

class Database:

    conf = {}
    dbname = ''
    uri = ''
    db = None
    param_check = True
    
    def __init__(self, dbname:str, schema:str='', 
                 uri:str='', param_check:bool=env.DATABSE_PARAM_CHECK):
        if(uri == ''):
            uri = env.DATABASE_URI
        if(schema == ''):
            schema = env.DATABASE_SCHEMA
        # else:
        #     uri = uri.replace(env.DATABASE_SCHEMA, schema)
        self.uri = uri
        self.schema = schema
        self.dbname = dbname
        self.param_check = param_check
        self.echo = env.DATABSE_ECHO

    def exec(self, sql):
        db = self.get_db()
        Session =scoped_session(sessionmaker(bind=db))
        s = Session()
        
        result = s.execute(sql)
        
        s.commit()
        s.close()

        return result
    
    def join_item(self, sql, table, join_item:dict={}):
        
        if not join_item:
            return sql

        r_table = self.get_table(join_item['table'])
        r_table = aliased(r_table, name=join_item['alias'])
        # table = join(table, user, table.c.createtoken == user.c.token)
        # sql = sql.join(r_table, table.c.get(join_item['lfield']) == r_table.c.get(join_item['rfield']))

        
        if join_item['method'] == 'left':
            sql = sql.outerjoin(r_table, table.c.get(join_item['lfield']) == r_table.c.get(join_item['rfield']))
        else:
            sql = sql.join(r_table, table.c.get(join_item['lfield']) == r_table.c.get(join_item['rfield']))

        # elif join_item['method'] == 'right':
        # elif join_item['method'] == 'inner':
        # elif join_item['method'] == 'full':
        # else:

        return sql


    
    def convert_by_config(self, table, where:dict, config: dict, type: str = ""):

        if type == 'count':
            field = func.count('*')
        elif 'field' in config and config['field'] != "":
            field = text(config['field'])
        else:
            field = text("*")


        if 'alias' in config and config['alias'] != "":
            table = aliased(table, name=config['alias'])
            # for key, val in list(where.items()):
            #     if '.' not in key:
            #         where[config['alias'] + '.' + key] = val
            #         del where[key]
        sql = select(field).select_from(table)
    #    'join': 'left join `character` as c on c.id = f.userb',
        # join需要实现
        if 'join' in config:
            joins = config['join']
            if isinstance(joins, str):
                join_item = parse_join(joins)
                sql = self.join_item(sql, table, join_item)
            else:
                for join in joins:
                    join_item = parse_join(join)
                    sql = self.join_item(sql, table, join_item)
        # where 实现
        sql = self.convert_by_where(sql, table, where, config)

        if 'group' in config:
            sql = sql.group_by(table.c.get(config['group']))
            type = ''

        if type == 'data':
            size = 50
            if config.get('size'):
                if config['size'] != 'max':
                    size = int(config['size'])
                    sql = sql.limit(size)
                    if config.get('p'):
                        p = int(config.get('p', 1))
                        sql = sql.offset(size * (p - 1))
            # sql = sql.slice(size*(p-1), size*p)
            
            if 'order' in config:
                order = config['order'].split(' ')
                if len(order) == 2:

                    if order[0].find('.') >= 0:
                        order[0] = order[0].split('.')[1]

                    if order[0] in table.c:
                        col = table.c.get(order[0])
                        if order[1] == 'asc':
                            sql = sql.order_by(col.asc())
                        elif order[1] == 'desc':
                            sql = sql.order_by(col.desc())  

            if 'id' in table.c:
                sql = sql.order_by(table.c.get('id').asc())  

        return sql



    # "in": test_in,
    # "==": operator.eq,
    # "eq": operator.eq,
    # "equalto": operator.eq,
    # "!=": operator.ne,
    # "ne": operator.ne,
    # ">": operator.gt,
    # "gt": operator.gt,
    # "greaterthan": operator.gt,
    # "ge": operator.ge,
    # ">=": operator.ge,
    # "<": operator.lt,
    # "lt": operator.lt,
    # "lessthan": operator.lt,
    # "<=": operator.le,
    # "le": operator.le,

    def fill(self, filter, o_field, c_type, val):
        if c_type == 'eq':
            filter.append(o_field == val)
        elif c_type == 'like':
            filter.append(o_field.like("%{0}%".format(val)))
        elif c_type == 'egt':
            filter.append(o_field.__ge__(val))
        elif c_type == 'lt':
            filter.append(o_field.__lt__(val))
        elif c_type == 'gt':
            filter.append(o_field.__gt__(val))
        elif c_type == 'between':
            if ',' in val:
                vals = val.split(',')
                filter.append(o_field.between(vals[0], vals[1]))
        elif c_type == 'in':
            # if ',' in val:
            vals = val.split(',')
            filter.append(o_field.in_(vals))
        elif c_type == 'neq':
            if val == '$empty':
                filter.append(o_field != '')
            else:
                filter.append(o_field != val)
        elif c_type == 'regexp':
            filter.append(o_field.op('regexp')(val))
        return filter

    def convert_by_where(self, sql, table, where: dict, config: dict):
        s_field = []
        s_type = []
        filter = []
        if 'search' in config and len(config['search']):
            search_config = config['search']
            for item in search_config:
                s_field.append(item['field'])
                s_type.append(item['type'])
                
        for key in where:
            val = where[key]

            if key in table.c: #and val != ""
                o_field = table.c.get(key)
                if key in s_field:
                    index = s_field.index(key)
                    c_type = s_type[index]
                elif type(val) == list:
                    c_type = val[0]
                    val = val[1]
                else:
                    c_type = 'eq'

                filter = self.fill(filter,o_field,c_type,val)
    
        if len(filter):
            sql = sql.filter(and_(*filter))
        
        return sql
    
    # def convert_by_where(self, sql, table, where: dict):
    #     filter = []
    #     for key in where:
    #         val = where[key]
    #         if key in table.c:
    #             o_field = table.c.get(key)
    #             filter.append(o_field == val)
    #     if len(filter):
    #         sql = sql.filter(and_(*filter))
        
    #     return sql

    def check_params(self, where: dict, param: dict, param_check: bool = False):
        if self.param_check == False and param_check == False:
            return param
        _ret = {}
        for key, val in list(where.items()):
            ikey = key
            # ikey = str(key).replace(".", "_")
            if ikey in param and param[ikey] != "":
                if param[ikey] == '$empty':
                    _ret[key] = ""
                else:
                    _ret[key] = param[ikey]
            elif val != "0" and val == "":
                pass
            else:
                _ret[key] = where[key]
        return _ret
    
    # count,data,one
    def info(self, param: dict, conf: dict={}):
        config = {'where': {}, 'required': '', 'size': 50, 'p': 1, 'search': []}
        config = {**config, **conf}

        if config['required'] != "":
            if config['required'] not in param or param[config['required']] == "":
                return ret(1)
            

        if config['type'] == 'data':
            json = []
        else:
            json = ret(0)
            json = {**json, 'data':[], 'total': 0, 'size': 0, 'p': 1}


        if config['size'] == '0':
            return json
       

        if 'size' in param:
            config['size'] = int(param['size'])
            del param['size']

        if 'p' in param and param['p'] != "":
            config['p'] = int(param['p'])
            del param['p']
            if config['p'] < 1:
                return json
            
        try:

            where = self.check_params(config['where'], param)
            table = self.get_table(self.dbname)
            total = self.count(param, conf)
            
            if total == 0:
                return json
            
            if config['type'] != 'data':
                json = {**json, 'data':[], 'total': total, 'size': config['size'], 'p': config['p']}


            if config.get('check_param_empty') and len(where) == 1 and 'status' in where:
                return json

            sql = self.convert_by_config(table, where, config, 'data')
        # print('sql', sql)
            result = self.exec(sql).mappings().fetchall()
        except Exception as e:
            print(e)
            return abort(500, e.__str__())
        
        result = [{**row} for row in result]

        if config.get('shuffle'):
            random.shuffle(result)

        # 现在是返回了一个数组。但如果 retobject == 1 则返回一个对象，key是数组内每个item数组里的第一个值，value是数组内每个item的值
        if config.get('retobject') and str(config['retobject']) == '1':
            keyList =list(result[0].keys())
            keyName = keyList[0]
            print(keyList, len(keyList), keyName)
            if len(keyList) > 1:
                tempObj = {}
                for item in result:
                    key = item[keyName]
                    tempObj[key] = item
                result = tempObj
            else:
                tempList = []
                for item in result:
                    value = item[keyName]
                    tempList.append(value)
                result = tempList
        
        if config.get('retobjectlist'):
            objKey = config['retobjectlist']
            objectList = []
            for item in result:
                if objKey not in item:
                    continue
                itemKey = item[objKey]
                if itemKey not in objectList:
                    objectList[itemKey] = []
                objectList[itemKey].append(item)

            result = objectList

        if config['type'] == 'data':
            json = result
        else:
            json['data'] = result

        return json



    def count(self, param: dict, conf: dict={}):
        config = {'where': {}}
        config = {**config, **conf}

        where = self.check_params(config['where'], param)

        table = self.get_table(self.dbname)

        sql = self.convert_by_config(table, where, config, 'count')

        result = self.exec(sql).first()

        return result[0]
    
    def sum(self, where: dict, field: str):
        table = self.get_table(self.dbname)
        field = table.c.get(field)
        if field is None:
            return 0
        sql = select(func.sum(field)).select_from(table).filter_by(**where)
        result = self.exec(sql).first()
        return result[0]
    
    def query(self, sql: str):
        result = self.exec(text(sql)).mappings().fetchall()
        return result

    def update(self, param: dict, conf: dict={}):
        config = {'where': {'id':''}, 'type': '', 'required': '', 'field':{}}
        config = {**config, **conf}

        if config['required'] != "":
            if config['required'] not in param or param[config['required']] == "":
                return ret(1)

        u_field = 'id'
        
        table = self.get_table(self.dbname)
        field = self.check_params(config['field'], param)
        sql = ''
        if config['type'] == 'add':
            sql = table.insert().values(**field)
        # elif config['type'] == 'update':
        else:

            print(param, config)
            if 'updatefield' in config:
                u_field = config['updatefield']

            print(u_field, param)
            if u_field not in param or param[u_field] == "":
                return ret(3)
            else:
                config['where'][u_field] = ""
                where = self.check_params(config['where'], param, True)
            
            sql = table.update().filter_by(**where).values(**field)

        # 可实现但还没必要实现
        # if config['type'] == 'addall':
        #     sql = table.insert().values(**field)
        # el
        # elif config['type'] == 'update':
        #     sql = table.update().filter_by(**where).values(**field)
        # elif config['type'] == 'incordec':
        #     if '+' in config:
        #         sql = table.update().filter_by(**where).values(**{config['+'][0]: table.c[config['+'][0]] + config['+'][1]})
        #     elif '-' in config:
        #         sql = table.update().filter_by(**where).values(**{config['-'][0]: table.c[config['-'][0]] - config['-'][1]})
        # else:
            
        try:
            # print(sql)
            result = self.exec(sql)
        except Exception as e:
            print(e)
            return ret(2, e.__str__())
        
        if result.lastrowid:
            field['id'] = result.lastrowid

        if result.rowcount:
            return ret(0, data=field)
        else:
            return ret(2)    

    def remove(self, param: dict, conf: dict):
        config = {'where': {'id': ''}, 'type': 'hard', 'update': {'status': '1'}}
        config = {**config, **conf}

        where = self.check_params(config['where'], param, True)
        print(param, where)
        strWhere = (str(val) for val in where) #一句代码转换
        val = "".join(strWhere)
        if val == "":
            return ret(1)
        if 'required' in config:
            if config['required'] not in where or where[config['required']] == "":
                return ret(1)

        table = self.get_table(self.dbname)       
        
        if config['type'] == 'deleted_at':
            config['update'] = {'deleted_at': datetime.now()}

        if config['type'] == 'hard':
            sql = table.delete().filter_by(**where)
        else:
            sql = table.update().filter_by(**where).values(**config['update'])

        
        print('sql', sql)

        result = self.exec(sql)
        
        if result.rowcount:
            return ret(0, data=where)
        else:
            return ret(2)
          

    def get_db(self):
        # print('get_db', self.uri, self.echo)
        if self.db == None:
            db = create_engine(self.uri,echo=self.echo)
            self.db = db
        return self.db
    
    def exist(self):
        db = self.get_db()
        ret = False
        try:
            ret = inspect(db).has_table(self.dbname, schema=self.schema)
        # except exc.OperationalError:
        #     ret = False
        # except exc.ProgrammingError:
        #     ret = False
        except Exception as e:
            print(e)
            pass

        return ret
    def get_columns(self):
        db = self.get_db()
        return inspect(db).get_columns(self.dbname, schema=self.schema)
    
    def get_table(self, name):

        if name.find('.') >= 0:
            nameList = name.split('.')
            schema = nameList[0]
            name = nameList[1]
        else:
            schema = self.schema

        # print('get_table', name, schema)
        db = self.get_db()
        metadata = MetaData(schema=schema)
        table = Table(name, metadata, autoload_with=db)
        return table

    # def get_columns(self):
    #     table = self.get_table(self.dbname)
    #     return table.columns.keys()

class Data:

    config = None
    
    def __init__(self, dataname:str, schema:str="", uri:str=""):
        self.dataname = dataname
        if schema == "" and dataname in workflowConfig:
            self.config = deepcopy(workflowConfig[dataname])
        self.model = Database(dataname, schema, uri)
    
    def exists(self):
        ret = self.model.exist()
        return ret
    
    def query(self, sql: str):
        result = self.model.query(sql)
        # 将Row对象转换为字典
        return [{**row} for row in result]
    
    def check_config(self, conf: dict, type:str):
        if self.config != None and type in self.config:
            conf = {**self.config[type],**conf}
        return conf

    def get_one(self, param: dict, conf: dict={}):
        conf = self.check_config(conf, 'info')
        conf = {**conf, **{'type':'data','check_param_empty':True}}
        res = self.model.info(param, conf)
        
        if len(res) > 0:
            return res[0]
        else:
            return ""
    
    def get_data(self, param: dict, conf: dict={}):
        conf = self.check_config(conf, 'list')
        conf = {**conf, **{'type':'data'}}
        ret = self.model.info(param, conf)
        # ret = [{**row} for row in ret]
        return ret
    
    def get_list(self, param: dict, conf: dict={}):
        conf = self.check_config(conf, 'list')
        conf = {**conf, **{'type':'size+data'}}
        ret = self.model.info(param, conf)
        return ret
    
    def update(self, param: dict, conf: dict={}):
        conf = self.check_config(conf, 'update')
        ret = self.model.update(param, conf)
        return ret

    def remove(self, param: dict, conf: dict={}):
        conf = self.check_config(conf, 'remove')                
        ret = self.model.remove(param, conf)
        return ret

    def count(self, param: dict, conf: dict={}):
        return self.model.count(param, conf)
    
    def get_columns(self):
        return self.model.get_columns()
    
row_to_dict = lambda r: {c: r.get(c) for c in r.keys()}
