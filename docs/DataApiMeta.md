# DataApi 后端数据配置文档

本文档为AI生成，仅供参考，详细的需要看具体代码逻辑。

## 📋 对外数据接口

### 基础 API 接口

| 接口 | 方法 | 功能 | 参数 |
|------|------|------|------|
| `/dataset/count` | GET/POST | 数据计数 | dataset, filter, token |
| `/dataset/getlist` | GET/POST | 获取数据列表 | dataset, filter, token |
| `/dataset/getinfo` | GET/POST | 获取单一数据条目 | dataset, filter, token |
| `/dataset/add` | POST | 新增数据 | dataset, filter, token, data |
| `/dataset/update` | POST | 更新数据 | dataset, filter, token, data |
| `/dataset/remove` | POST | 删除数据 | dataset, filter, token, id |

### 通用参数说明

- **dataset**: 数据集代码，对应数据库中的 dataset 表
- **filter**: 过滤器代码，可选，用于数据过滤
- **token**: 用户认证令牌，用于权限验证

## 🔄 数据配置流程

### 1. 创建程序 (workflow_app)
```sql
INSERT INTO workflow_app (code, name, desc, createtoken) 
VALUES ('my_app', '我的应用', '应用描述', 'user_token');
```

### 2. 配置程序的数据源 (workflow_datain)
```sql
INSERT INTO workflow_datain (code, name, stype, meta) 
VALUES ('my_datain', '数据源', 'mysql', '{"dev": {...}}');
```

### 3. 配置程序的数据集 (workflow_dataset)
```sql
INSERT INTO workflow_dataset (code, name, datain, datatable, meta) 
VALUES ('my_dataset', '数据集', 'my_datain', 'my_table', '{"list": {...}}');
```

### 4. 配置数据集的数据字段 (workflow_dataprop) 【可选】
```sql
INSERT INTO workflow_dataprop (datasetcode, code, cname, type, index) 
VALUES ('my_dataset', 'id', 'ID', 'text', 1);
```

### 5. 配置数据过滤器 (workflow_datafilter) 【可选】
```sql
INSERT INTO workflow_datafilter (datasetcode, code, name, meta) 
VALUES ('my_dataset', 'active_only', '仅显示激活数据', '{"list": {...}}');
```

## 🗄️ 数据库配置 (datain meta)

### 开发环境配置
```json
{
  "dev": {
    "db_type": "mysql",
    "db_host": "localhost",
    "db_name": "your_database",
    "db_port": "3306",
    "db_user": "root",
    "db_pwd": "12345678"
  },
  "prod": {
    "db_type": "mysql",
    "db_host": "prod_host",
    "db_name": "prod_database",
    "db_port": "3306",
    "db_user": "prod_user",
    "db_pwd": "prod_password",
    "db_ver": "8",
    "db_remove_type": "deleted_at"
  }
}
```

### 配置参数说明

- **db_type**: 数据库类型，目前只支持 mysql
- **db_host**: 数据库主机地址
- **db_name**: 数据库名称
- **db_port**: 数据库端口
- **db_user**: 数据库用户名
- **db_pwd**: 数据库密码
- **db_ver**: 数据库版本，可选
- **db_remove_type**: 数据移除类型
  - `status`: 软删除，设置 status=1
  - `deleted_at`: 软删除，写入删除时间戳

## 📊 数据集配置 (dataset meta)

### 完整配置示例
```json
{
  "dataType": "dataset",
  "index": {
    "sql": "select * from test",
    "status": "ignore",
    "order": "publish_time desc",
    "combo": [
      {
        "dataType": "mix",
        "dataset": "analy_videostat",
        "searchKey": "id",
        "relateKey": "videoid",
        "comboKey": "source",
        "comboVal": "seeit",
        "list": {
          "where": {
            "videoid": "",
            "status": "0",
            "grab_time": ["gt", "2023-03-20"]
          },
          "field": "videoid,seeit,source"
        }
      }
    ]
  },
  "list": {
    "size": 50,
    "where": {
      "status": 0
    },
    "field": "id,name,desc",
    "order": "updatetime desc"
  },
  "info": {
    "order": "c.updatetime desc",
    "alias": "c",
    "join": [
      "issue as i on i.id = c.issueid",
      "user as u on u.id = c.ownerid"
    ],
    "field": "c.id,c.issueid,c.ownerid,c.title,c.content,c.type,i.name as issuename,u.nick as ownername",
    "search": [
      {
        "field": "type",
        "type": "in"
      }
    ]
  },
  "add": {
    "field": "name,desc,status",
    "required": "name"
  },
  "update": {
    "field": "name,desc,status",
    "required": "id"
  },
  "remove": {
    "type": "soft",
    "where": {
      "id": ""
    }
  }
}
```

### 配置节点说明

#### 1. index 节点 - 后台数据管理
- **sql**: 自定义 SQL 查询
- **status**: 状态过滤，ignore 表示忽略状态字段
- **order**: 排序规则
- **combo**: 数据组合配置

#### 2. list 节点 - 列表数据
- **size**: 每页数据量
- **where**: 查询条件
- **field**: 返回字段
- **order**: 排序规则

#### 3. info 节点 - 详情数据
- **alias**: 表别名
- **join**: 表连接配置
- **field**: 返回字段
- **search**: 搜索配置

#### 4. add 节点 - 新增数据
- **field**: 可编辑字段
- **required**: 必填字段

#### 5. update 节点 - 更新数据
- **field**: 可编辑字段
- **required**: 必填字段

#### 6. remove 节点 - 删除数据
- **type**: 删除类型 (soft/hard)
- **where**: 删除条件

## 🔗 数据组合配置 (combo)

### 组合类型

#### 1. mix 类型 - 混合数据
```json
{
  "dataType": "mix",
  "dataset": "analy_videostat",
  "searchKey": "id",
  "relateKey": "videoid",
  "comboKey": "source",
  "comboKeySuffix": "inc",
  "comboVal": "seeinc",
  "list": {
    "where": {
      "videoid": "",
      "status": "0"
    },
    "field": "videoid,seeinc,source"
  }
}
```

#### 2. list 类型 - 列表数据
```json
{
  "dataType": "list",
  "dataset": "user_comments",
  "searchKey": "id",
  "relateKey": "userid",
  "list": {
    "where": {
      "userid": "",
      "status": "1"
    },
    "field": "id,content,createtime"
  }
}
```

#### 3. sql 类型 - 自定义 SQL
```json
{
  "dataType": "sql",
  "dataset": "custom_data",
  "searchKey": "id",
  "relateKey": "parent_id",
  "query": "SELECT * FROM custom_table WHERE parent_id IN ({ids})"
}
```

### 组合参数说明

- **dataType**: 组合类型 (mix/list/sql)
- **dataset**: 关联数据集
- **searchKey**: 主表关联字段
- **relateKey**: 关联表关联字段
- **comboKey**: 组合键名
- **comboKeySuffix**: 组合键后缀
- **comboVal**: 组合值字段
- **list**: 关联数据配置

## 🔍 搜索配置 (search)

### 搜索类型

```json
{
  "search": [
    {
      "field": "name",
      "type": "like"
    },
    {
      "field": "status",
      "type": "in"
    },
    {
      "field": "createtime",
      "type": "between"
    }
  ]
}
```

### 支持的搜索类型

- **eq**: 等于
- **like**: 模糊匹配
- **in**: 包含
- **between**: 范围查询
- **gt**: 大于
- **lt**: 小于
- **gte**: 大于等于
- **lte**: 小于等于
- **neq**: 不等于

## 🎯 使用示例

### 1. 基础数据查询
```javascript
// 获取用户列表
const response = await fetch('/dataset/getlist', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + token
  },
  body: JSON.stringify({
    dataset: 'user_list',
    token: token
  })
});
```

### 2. 带过滤器的查询
```javascript
// 获取激活状态的用户
const response = await fetch('/dataset/getlist', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + token
  },
  body: JSON.stringify({
    dataset: 'user_list',
    filter: 'active_only',
    token: token
  })
});
```

### 3. 数据新增
```javascript
// 新增用户
const response = await fetch('/dataset/add', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + token
  },
  body: JSON.stringify({
    dataset: 'user_list',
    token: token,
    name: '张三',
    email: 'zhangsan@example.com',
    status: 1
  })
});
```

## ⚙️ 高级配置

### 1. 动态配置覆盖
```javascript
// 通过 _dconfig 参数动态覆盖配置
const response = await fetch('/dataset/getlist', {
  method: 'POST',
  body: JSON.stringify({
    dataset: 'user_list',
    token: token,
    _dconfig: JSON.stringify({
      size: 100,
      order: 'id desc'
    })
  })
});
```

### 2. 缓存配置
系统使用 TTLCache 进行配置缓存，默认缓存时间 300 秒：
```python
_cache = TTLCache(maxsize=1000, ttl=300)
```

### 3. 权限控制
- 非管理员用户只能访问自己创建的数据集
- 白名单数据集允许所有用户访问
- 支持基于 token 的权限验证

## 🚨 注意事项

1. **数据库连接**: 确保数据库服务正常运行
2. **权限验证**: 所有请求都需要有效的 token
3. **字段映射**: 确保配置的字段在数据库表中存在
4. **SQL 注入**: 系统已内置 SQL 注入防护
5. **性能优化**: 大量数据查询建议使用分页

## 🔧 故障排除

### 常见错误码
- **1**: 参数错误
- **2**: 数据库操作失败
- **3**: 必填参数缺失
- **15**: 数据表不存在

### 调试技巧
1. 检查数据库连接配置
2. 验证数据集和过滤器配置
3. 查看系统日志获取详细错误信息
4. 使用数据库客户端直接测试 SQL 查询





