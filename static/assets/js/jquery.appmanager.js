'use strict';

class DialogManager {

    static modal(options) {
        const defaultOptions = {
            title: '确认',
            content: '确定要执行此操作吗？',
            confirmText: '确定',
            cancelText: '取消',
            widthCss: 'max-w-sm',
            onConfirm: null,
            onCancel: null
        }

        const mergedOptions = {
            ...defaultOptions,
            ...options,
            showClose: false,
            showCancel: true
        }

        return new Promise((resolve, reject) => {
            const dialogHtml = `
                <div id="${mergedOptions.id}" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
                    <div class="bg-white rounded-lg p-6 ${mergedOptions.widthCss} mx-8 shadow-xl w-full max-h-[90vh] overflow-y-auto">
                        <div class="flex justify-between items-center mb-4">
                            <h3 class="text-lg font-semibold text-gray-900">${mergedOptions.title}</h3>
                        </div>
                        <div class="text-gray-600 mb-6">${mergedOptions.content}</div>
                        <div class="flex justify-end space-x-3">
                            <button class="px-4 py-2 text-gray-700 bg-gray-100 rounded-md hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-gray-500">
                                ${mergedOptions.cancelText}
                            </button>
                            <button class="px-4 py-2 text-white bg-red-500 rounded-md hover:bg-red-600 focus:outline-none focus:ring-2 focus:ring-red-500">
                                ${mergedOptions.confirmText}
                            </button>
                        </div>
                    </div>
                </div>
            `

            const dialog = $(dialogHtml)
            $('body').append(dialog)

            const closeDialog = () => {
                dialog.find('button').off('click')
                dialog.hide()
                setTimeout(() => {
                    dialog.remove()
                }, 1000)
            }

            dialog.find('button').eq(0).on('click', () => {
                if (mergedOptions.onCancel) {
                    mergedOptions.onCancel(dialog)
                }
                resolve({action: 'cancel', dialog: dialog})
                closeDialog()
            })

            dialog.find('button').eq(1).on('click', () => {
                if (mergedOptions.onConfirm) {
                    mergedOptions.onConfirm(dialog)
                }
                resolve({action: 'confirm', dialog: dialog})
                closeDialog()
            })
        })
    }

    static confirm(options) {
        const defaultOptions = {
            title: '确认',
            content: '确定要执行此操作吗？',
            confirmText: '确定',
            cancelText: '取消',
            widthCss: 'max-w-sm',
            onConfirm: null,
            onCancel: null
        }

        const mergedOptions = {
            ...defaultOptions,
            ...options,
            showClose: false,
            showCancel: true
        }

        if(options.templateId){
            mergedOptions.content = template(options.templateId + '-template', mergedOptions)
        }

        return new Promise((resolve, reject) => {
            const dialogHtml = `
                <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
                    <div class="bg-white rounded-lg p-6 ${mergedOptions.widthCss} mx-8 shadow-xl w-full">
                        <div class="flex justify-between items-center mb-4">
                            <h3 class="text-lg font-semibold text-gray-900">${mergedOptions.title}</h3>
                        </div>
                        <div class="text-gray-600 mb-6">${mergedOptions.content}</div>
                        <div class="flex justify-end space-x-3">
                            <button class="px-4 py-2 text-gray-700 bg-gray-100 rounded-md hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-gray-500">
                                ${mergedOptions.cancelText}
                            </button>
                            <button class="px-4 py-2 text-white bg-red-500 rounded-md hover:bg-red-600 focus:outline-none focus:ring-2 focus:ring-red-500">
                                ${mergedOptions.confirmText}
                            </button>
                        </div>
                    </div>
                </div>
            `

            const dialog = $(dialogHtml)
            $('body').append(dialog)

            const closeDialog = () => {
                dialog.remove()
            }

            dialog.find('button').eq(0).on('click', () => {
                if (mergedOptions.onCancel) {
                    mergedOptions.onCancel()
                }
                resolve(false)
                closeDialog()
            })

            dialog.find('button').eq(1).on('click', () => {
                if (mergedOptions.onConfirm) {
                    mergedOptions.onConfirm()
                }
                resolve(true)
                closeDialog()
            })
        })
    }

    // 简单的alert方法，显示一个不影响页面操作的轻量级弹窗
    static alert(message, options = {}) {
        const defaultOptions = {
            title: '提示',
            content: message,
            confirmText: '确定',
            onConfirm: null
        }

        const mergedOptions = {
            ...defaultOptions,
            ...options,
            showClose: false,
            showCancel: false
        }

        return new Promise((resolve) => {
            const dialogHtml = `
                <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
                    <div class="bg-white rounded-lg p-6 max-w-sm w-full mx-8 shadow-xl">
                        <div class="flex justify-between items-center mb-4">
                            <h3 class="text-lg font-semibold text-gray-900">${mergedOptions.title}</h3>
                        </div>
                        <div class="text-gray-600 mb-6">${mergedOptions.content}</div>
                        <div class="flex justify-end space-x-3">
                            <button class="px-4 py-2 text-white bg-red-500 rounded-md hover:bg-red-600 focus:outline-none focus:ring-2 focus:ring-red-500">
                                ${mergedOptions.confirmText}
                            </button>
                        </div>
                    </div>
                </div>
            `

            const dialog = $(dialogHtml)
            $('body').append(dialog)

            const closeDialog = () => {
                dialog.remove()
            }

            dialog.find('button').on('click', () => {
                if (mergedOptions.onConfirm) {
                    mergedOptions.onConfirm()
                }
                resolve()
                closeDialog()
            })
        })
    }
    
    static tip(message, options = {}) {
        const defaultOptions = {
            type: 'warning',
            duration: 3000,       // 显示时长，毫秒
            position: 'top',      // 位置: top, bottom, center
            offset: 30           // 距离边缘的偏移量
        };
        
        const settings = {...defaultOptions, ...options};
        
        // 创建提示元素
        const tipId = 'tip-' + Date.now();
        const tip = document.createElement('div');
        tip.id = tipId;
        
        // 设置基础样式
        tip.style.cssText = `
            position: fixed;
            z-index: 9999;
            background-color: white;
            color: #374151;
            padding: 6px 8px;
            border-radius: 8px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            min-width: 60%;
            max-width: 80%;
            pointer-events: none;
            transform: translateY(-100%);
            opacity: 0;
            transition: transform 0.3s ease, opacity 0.3s ease;
            display: flex;
            align-items: center;
        `;
        
        // 根据类型调整颜色
        if (settings.type === 'success') {
            tip.style.backgroundColor = '#48bb78';
            tip.style.color = 'white';
        } else if (settings.type === 'warning') {
            tip.style.backgroundColor = '#ed8936';
            tip.style.color = 'white';
        } else if (settings.type === 'error') {
            tip.style.backgroundColor = '#f56565';
            tip.style.color = 'white';
        }
        
        // 设置位置
        if (settings.position === 'top') {
            tip.style.top = settings.offset + 'px';
            tip.style.left = '50%';
            tip.style.transform = 'translateX(-50%) translateY(-100%)';
        } else if (settings.position === 'bottom') {
            tip.style.bottom = settings.offset + 'px';
            tip.style.left = '50%';
            tip.style.transform = 'translateX(-50%) translateY(100%)';
        } else if (settings.position === 'center') {
            tip.style.top = '50%';
            tip.style.left = '50%';
            tip.style.transform = 'translate(-50%, -50%) translateY(-100%)';
        }
        
        // 设置内容
        tip.innerHTML = `
            <div style="flex: 1;">
                ${message}
            </div>
        `;
        
        // 添加到body
        document.body.appendChild(tip);
        
        // 显示动画
        requestAnimationFrame(() => {
            tip.style.transform = settings.position === 'center' 
                ? 'translate(-50%, -50%)' 
                : 'translateX(-50%)';
            tip.style.opacity = '1';
        });
        
        // 自动关闭
        if (settings.duration > 0) {
            setTimeout(() => {
                tip.style.transform = settings.position === 'center'
                    ? 'translate(-50%, -50%) translateY(-100%)'
                    : 'translateX(-50%) translateY(-100%)';
                tip.style.opacity = '0';
                
                setTimeout(() => {
                    if (tip.parentNode) {
                        tip.parentNode.removeChild(tip);
                    }
                }, 300);
            }, settings.duration);
        }
        
        return tipId;
    }   
}

class FormManager {
    constructor(){}

    static getFormData(parent, isChange, notEmpty) {
        var ret = {};
        var elList = parent.find('[name]');
        var cacheItem = parent.data('cache');
        var formItem = {};
        var checkedNames = [];
        var radioNames = [];

        $.each(elList, function(i, el){
            el = $(el);
            var value = el.val();
            var name = el.attr('name');
            var type = el.attr('type');
            if(type == 'checkbox'){
                checkedNames.push(name);
                return;
            }else if(type == 'radio'){
                radioNames.push(name);
                return;
            }
            
            formItem[name] = value;

            if(isChange && cacheItem){
                if(cacheItem[name] != value){
                    ret[name] = value;
                }
            }else if(notEmpty){
                if(value != ''){
                    ret[name] = value;
                }              
            }else{
                ret[name] = value;
            }
        });


        if(radioNames.length){
            radioNames = $.unique(radioNames)
            $.each(radioNames, function(i, name){
                ret[name] = parent.find('[name="'+name+'"]:checked').val();
            });
        }

        if(checkedNames.length){
            checkedNames = $.unique(checkedNames)
            $.each(checkedNames, function(i, name){
                parent.find('[name="'+name+'"]:checked').each(function(index, input){
                    input = $(input);
                    var val = input.val();
                    if(!ret[name]){
                        ret[name] = [];
                    }
                    ret[name].push(val);
                });
            });
        }

        if(!$.isEmptyObject(ret)){
            if(formItem['id']){
                ret['id'] = formItem['id'];  
            }
        }

        return ret;
    };

    static setFormData(parent, item, letChange) {
        var elList = parent.find('[name]');
        var formItem = {};

        $.each(elList, function(i, el){
            el = $(el);
            var val = el.val();
            var name = el.attr('name');
            formItem[name] = val;
        }); 

        if(!item || $.isArray(item)){
            parent.data('cache',formItem);
            return false;
        }

        $.each(elList, function(i, el){
            el = $(el);
            var name = el.attr('name');
            var type = el.attr('type');

            if(type == 'radio'){
                return;
            }

            if(typeof item == 'string'){
                el.val(item);
            }else if(item[name]){
                el.val(item[name]);
            }

            if(type == 'textarea' || type == 'select'){
                el.trigger('change');
            }
            
            formItem[name] = el.val();
        });
        
        !letChange && parent.data('cache',formItem);
    };

    static disabled(parent, disList, able) {
        var elList = parent.find('[name]');
        $.each(elList, function(i, el){
            if($.inArray($(el).attr('name'), disList) != -1){
                if(able){
                    $(el).attr('disabled', 'disabled')
                }else{
                    $(el).removeAttr('disabled');
                }
            }
        });
    };

    static emptyFormData(parent) {
        var elList = parent.find('[name]');
        var item = {};
        $.each(elList, function(i, el){
            el = $(el);
            var type = el.attr('type');
            el.val("");
            item[el.attr('name')] = "";
            if(type == 'textarea'){
                el.trigger('change');
            }
        });
        console.log(item);
        parent.data('cache',item);
    };
    
    
}

class NetManager {
    constructor(){}
    static getUrlParam(paramName) {
        const urlParams = new URLSearchParams(window.location.search);
        return urlParams.get(paramName);
    }
    static async get(url, data, headers) {
        if(data){
            url += '?' + $.param(data)
        }
        const ret = await fetch(url, {
            method: 'GET',
            headers: Object.assign({
                'Content-Type': 'application/json',
            }, headers),
        })
        .then(response => response.json())
        .catch(error => {
            // console.error('Network error:', error.message)
            return {code:-1, msg:'网络错误:'+error.message}
        });
        // const ret = await response.json();
        return ret
    }
    static async post(url, data, headers) {
        const ret = await fetch(url, {
            method: 'POST',
            headers: Object.assign({
                'Content-Type': 'application/json',
            }, headers),
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .catch(error => {
            return {code:-1, msg:'网络错误:'+error.message}
        });
        return ret
    }
}

class Timer {
    constructor(){}
    static countdown(seconds, onProgress, onComplete) {
        let remainingTime = seconds;
        
        // 立即执行一次回调，显示初始状态
        if (typeof onProgress === 'function') {
            onProgress(remainingTime);
        }
        
        const timer = setInterval(() => {
            remainingTime--;
            
            if (remainingTime <= 0) {
                clearInterval(timer);
                if (typeof onComplete === 'function') {
                    onComplete();
                }
            } else if (typeof onProgress === 'function') {
                onProgress(remainingTime);
            }
        }, 1000);

        return timer;
    }
    static format(date, format='MM月dd日') {
        if(typeof(date) == 'string'){
            date = new Date(date);
        }
        if(!date instanceof Date){
            return false;
        }
        const o = {
            'M+': date.getMonth() + 1,
            'd+': date.getDate(),
            'h+': date.getHours(),
            'm+': date.getMinutes(),
            's+': date.getSeconds(),
            'q+': Math.floor((date.getMonth() + 3) / 3),
            'S': date.getMilliseconds()
        };
        // 增加中文月份
        // const months = ['一月', '二月', '三月', '四月', '五月', '六月', '七月', '八月', '九月', '十月', '十一月', '十二月'];
        // if (/(M+)/.test(format)) {
        //     format = format.replace(RegExp.$1, (RegExp.$1.length === 1) ? (date.getMonth() + 1) : months[date.getMonth()]);
        // }
        if (/(y+)/.test(format)) {
            format = format.replace(RegExp.$1, (date.getFullYear() + '').substr(4 - RegExp.$1.length));
        }
        for (const k in o) {
            if (new RegExp('(' + k + ')').test(format)) {
                format = format.replace(RegExp.$1, RegExp.$1.length === 1 ? o[k] : ('00' + o[k]).substr(('' + o[k]).length));
            }
        }
        return format;
    }
}

class AppElement {

    element = new Map

    constructor(app, root, conf) {
        
        this.app = app
        this.root = root
        this.conf = conf
        if (conf.theme) {
            this.root.addClass(conf.theme)
        }
        this.data = conf.data;
        this.init();
    }

    setConf(conf){
        this.conf = {...this.conf, ...conf}
    }


    scan(){
        const that = this 
        that.root.find('[element]').each(function(){
            const node = $(this)
            const elementId = node.attr('element')
            that.element.set(elementId, node)
            node.removeAttr('element')
        })
    }

    init() {}
}



class AppManager{
    constructor(root, conf) {
        this.root = root;
        this.conf = $.extend({}, AppManager.defaults, conf);
        this.inited = false;
        this.firstScan = true;
        this.init()
        this.bindEvent()
        AppManager.apps.push(this)
        // AppManager.appInstance.set(this.conf.id, this)
    }

    static elementClass = new Map
    static actionClass = new Map
    // static appInstance = new Map
    static apps = []

    static registerElement(name, elementClass) {
        console.log('registerElement', name)
        if (AppManager.elementClass.get(name)) {
            console.error(`${name} 组件已注册`)
            return false;
        }
        this.elementClass.set(name, elementClass);
    }

    static registerAction(name, func) {
        console.log('registerAction', name)
        if (AppManager.actionClass.get(name)) {
            console.error(`${name} 行为已注册`)
            return false;
        }
        this.actionClass.set(name, func);
    }

    element = new Map
    elementData = new Map
    instance = new Map
    checkTemplateLoaded = new Map


    event(event, func){
        $(this).on('event:' + event, func);
    }
    offevent(event, func){
        $(this).off('event:' + event, func);
    }

    trigger(event, args){
        console.log('app-trigger: event:'+event, args)
        $(this).trigger('event:'+event, args);
    }

    bindEvent(){
        const that = this;
        $(that.root).on('click', 'a[event], button[event]', function(e){
            var node = $(this)
            var event = node.attr('event')
            if(!event){
                return
            }
            $(that).trigger('event:'+event, [e, node])
            return true;
        });
    }

    bindAction(name, that){
        const func = AppManager.actionClass.get(name)
        if(!func){
            return false
        }
        return func.bind(that)
    }


    init() {
        // 从本地存储获取 token
        const token = localStorage.getItem('userToken');
        if (token) {
            this.userToken = token;
            console.log('getUserToken', token)
        }
    }

    setUserToken(token) {
        console.log('setUserToken', token)
        if (token) {
            // 保存到实例和本地存储
            this.userToken = token;
            localStorage.setItem('userToken', token);
        } else {
            // 如果 token 为空，清除存储
            this.userToken = null;
            localStorage.removeItem('userToken');
        }
    }

    async get(path, data){
        if(path && path.indexOf('http') == -1 && this.conf.netHost){
            path = this.conf.netHost + path
        }
        var headers = {}
        if(this.userToken){
            headers = {
                'Authorization': 'Bearer ' + this.userToken
            }
        }
        return await NetManager.get(path, data, headers)
    }

    async post(path, data){
        const that = this
        that.loading(true)  
        if(path && path.indexOf('http') == -1 && this.conf.netHost){
            path = this.conf.netHost + path
        }
        var headers = {}
        if(this.userToken){
            headers = {
                'Authorization': 'Bearer ' + this.userToken
            }
        }
        return await NetManager.post(path, data, headers).then(res=>{
            that.loading(false)
            return res
        })
    }
    modal(conf){
        if(conf.templateId){
            conf.content = this.template(conf.templateId, conf)
        }
        return DialogManager.modal(conf)
    }

    mixObjAttr(mixObj){
        var mixList = mixObj.mix;
        var config = this.conf;
        var pageInfo = config.data['page:info'];
        var auth = pageInfo['user'];
        $.each(mixList, function(key2, item2){
            var itemObj = mixObj;

            if(item2.dir == 'param'){
                itemObj = mixObj.param;
            }

            var field = item2.field;

            if(item2.func == 'auth_id'){
                itemObj[field] = auth.id;
            }else if(item2.func == 'page_info'){
                itemObj[field] = pageInfo[field];
            }else if(item2.func == 'page_data'){
                itemObj[field] = config.data[item2.key];
                if(itemObj[field]['data']){
                    itemObj[field] = itemObj[field]['data'];
                }
            }else if(item2.func == 'page_search'){
                itemObj[field] = NetManager.getUrlParam(field);
            }else if(item2.func == 'overwrite'){
                itemObj[item2.target] = mixObj[item2.source];
            }
        });
    }

    goPage(pageid){
        var path = this.conf.path.page[pageid]
        if(!path){
            return false
        }
        if(this.conf.host){
            path = this.conf.host + path
        }
        window.location.href = path
    }

    async start() {
        var isOk = true
        if(this.conf.dataSource){
            isOk = await this.loadData()
        }
        isOk = await this.scan()
        // this.render()
        this.inited = isOk
        return isOk
    }

    loading(show){
        let loading = this.element.get('loading')
        if(!loading){
            return
        }
        if(show){
            loading.show()
        }else{
            loading.hide()
        }
    }
    async loadData() {
        const that = this
        return that.get(that.conf.dataSource).then((res)=>{
            if(res.code != 0){
                if(res.code == 13 && that.conf.checkTokenUrl){
                    location.href = that.conf.checkTokenUrl
                }else if(res.redirect){
                    location.href = res.redirect
                }else{
                    AppManager.alert(res.msg)
                }
                return;
            }

            Object.assign(that.conf.data, res.data)
            if(res.data['page:attr']){
                Object.assign(that.conf.attr, res.data['page:attr'])
                delete that.conf.data['page:attr']
            }

            let pageInfo = res.data['page:info']
            if(pageInfo && pageInfo.theme){
                $('body').attr('data-theme', pageInfo.theme);
            }
        })
        // .catch((res)=>{
        //     console.log(res)
        // })
    }

    setData(name, key, data){
        if(!this.conf.data[name]){
            this.conf.data[name] = {}
        }
        if(!key){
            this.conf.data[name] = data
            return true
        }
        this.conf.data[name][key] = data
        return true
    }

    async scan(){
        var that = this
        var conf = that.conf;
        var nodes = $('.app_element');
        var templateNames = []
        $.each(nodes, function(index, node){
            node = $(node);
            if(node.attr('slot')){
                return
            }
            let name = node.prop('tagName').toLowerCase();
            let element = node.attr('data-element');
            if(element){
                name = element
            }
            templateNames.push(name);

            let itemElement = node.attr('data-item-element')
            itemElement && templateNames.push(itemElement)
        });

        if(that.firstScan){
            nodes = $('template, script[type="text/html"]');
            $.each(nodes, function(index, node){
                let name = node.id.toLowerCase().replace('-template','');
                that.checkTemplateLoaded.set(name,node);    
            });
    
            templateNames = templateNames.concat(conf.templateNames)
            that.firstScan = false
        }
        
        if(templateNames.length){
            templateNames = $.unique(templateNames)
            console.log('loadTemplate', templateNames)
            await that.loadTemplate(templateNames)
            that.render()
        }

        if($('.app_element').length){
            return await that.scan()
        }
        
        return true
    }
    reloadByName(name, newData={}){
        const that = this
        var conf = that.conf;
        // 遍历 that.elementData，找到所有element为 name 的元素
        let elements = []
        that.elementData.forEach((data, id)=>{
            if(data.element == name){
                that.reloadById(id)
            }
        })
    }
    reloadById(id, newData={}){
        const that = this
        var conf = that.conf;
        let parent = that.element.get(id)
        if(!parent){
            return false
        }
        let data = that.elementData.get(id)
        if(data.initData){
            data = $.extend({}, data, conf.data[data.initData], newData)
        }
        let newNode = $(that.template(data.element, data))
        console.log(data.element, data, newNode)
        newNode.attr('data-comp', data.element)
        parent.replaceWith(newNode);

        let elementClass =AppManager.elementClass.get(data.element);
        if(elementClass){
            var oldClass = that.instance.get(data.id)
            oldClass.distory && oldClass.distory()
            that.instance.set(data.id, new elementClass(that, newNode, data))
        }
        that.element.set(data.id, newNode)
        that.elementData.set(data.id, data)

        that.render()
    }

    render(){
        var that = this;
        var conf = that.conf;
        var nodes = $('.app_element');
        $.each(nodes, function(index, node){
            node = $(node);
            if(node.attr('slot')){
                return
            }
            let name = node.prop('tagName').toLowerCase();
            let data = node.data()
            if(data.element){
                name = data.element
            }else{
                data.element = name
            }

            if(conf.attr[name]){
                data = $.extend({}, conf.attr[name],  data)
            }

            if(data.initData){
                data = $.extend({}, conf.data[data.initData], data)
            }

            // console.log(name, data)

            if(data.notInit == 'true'){
                node.remove()
                return
            }

            let newNode = $(that.template(name, data))
            if(!data.id){
                data.id = 'app_node_'+Math.random().toString(36).substr(2, 9)
                newNode.prop('id', data.id)
            }
            
            let content = node.html()
            if(content){
                data.content = content
                let contentEl = $(content)
                contentEl.find('[slot="true"]').each(function(index, node){
                    $(node).removeAttr('slot')
                })
                contentEl = contentEl.removeAttr('slot');
                newNode.find('slot').replaceWith(contentEl);
            }
            if(data.style){
                newNode[0].style = data.style 
            }
            newNode.attr('data-comp', name)
            node.replaceWith(newNode);

            let elementClass =AppManager.elementClass.get(name);
            let action = elementClass
            if(elementClass){
                action = new elementClass(that, newNode, data)
                that.instance.set(data.id, action)
            }
            that.element.set(data.id, newNode)
            that.elementData.set(data.id, data)
        });
    }
    template(name, data) {
        if(!this.checkTemplateLoaded.get(name)){
            console.error('template not exist! name:'+name)
            return ''
        }
        return template(name + '-template', data);
    }

    async loadTemplate(templateNames) {
        let that = this
        let conf = that.conf;
        const promises = templateNames.map(item => {
            if(that.checkTemplateLoaded.get(item)){
                return Promise.resolve();
            }
            let path = conf.path.tpl + item + '.html'+'?v='+conf.v;
            console.log(path)

            return $.ajax({
                method:'GET',
                url:path, 
                dataType:'html'
            }).then(templateHtml => {
                templateHtml = templateHtml.replace(/>\s+</g, '><').replace(/>\s+{/g, '>{').replace(/}\s+</g, '}<');
                // 用原生方法将模板添加到body
                let nodes = $(templateHtml).filter(function () {
                    return this.nodeType === 1;
                });
                nodes.appendTo(that.root);
                nodes.each((index, node)=>{
                    let tagName = node.tagName.toLowerCase();
                    if(tagName == 'template' || (tagName == 'script' && node.type == 'text/html')){
                        let name = node.id.toLowerCase().replace('-template','');
                        that.checkTemplateLoaded.set(name,node);    
                    }
                })
            }).catch(error => {
                console.error(`加载模板 ${item} 失败:`, error);
                // 将失败的Promise转换为resolved状态
                return Promise.resolve();
            });
        });
        await Promise.all(promises);
        return that;
    }
}
AppManager.formatDate = Timer.format
AppManager.Element = AppElement
AppManager.getUrlParam = NetManager.getUrlParam
AppManager.getFormData = FormManager.getFormData
AppManager.setFormData = FormManager.setFormData
AppManager.disabled = FormManager.disabled
AppManager.emptyFormData = FormManager.emptyFormData
AppManager.alert = DialogManager.alert
AppManager.tip = DialogManager.tip
AppManager.confirm = DialogManager.confirm
// AppManager.modal = DialogManager.modal
// 默认配置
AppManager.defaults = {
    v:Math.ceil(Math.random()*100000),//Math.random().toString(36).substr(2, 9)
    templateNames: [],
    data:{},
    attr:{},
    path: {
        page:{},
        tpl: ''
    }
};
window.AppManager = AppManager;

