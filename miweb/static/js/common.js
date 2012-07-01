function BaseType(){
    // member variables
    //this.member_vars = '';

    //this.m2 = [1,2,3];
    // member var, will be copied by sub type.
}
//BaseType.prototype.config = [1,2,3] // static variables
//BaseType.prototype.not_static = 45; // this is not a static var.

function inheritPrototype(subType, superType){
    var prototype = new superType();
    prototype.constructor = subType;
    subType.prototype = prototype;
}

function _(msg){
    return msg;
}
function debug(msg)
{
    var e = $("#debug");
    if(e[0])
        e[0].innerHTML += '<br /><div>' + msg + '</div>';
    //var items = [];
    //$.each(data, function(key, val) {
    //  items.push('<li id="' + key + '">' + val + '</li>');
    //});
    //$('<ul/>', {
    //  'class': 'my-new-list',
    //  html: items.join('')
    //}).appendTo('body');
}
/* Global */
function Global()
{
    BaseType.call(this);
    _this = this;
    this.ui = new Array();
    this.mem = new Array();
    this.init = function(){
        $.ajax({
            url: 'data/global.json',
            dataType: 'text',
            async: false,
            data: {},
        })
  .success(function(data) {
      //alert("second success");
      var obj = $.evalJSON(data);
      _this.ui = obj.ui;
      _this.mem = obj.mem;
  })
  .error(function() { alert("error"); })
  .complete(function() {
      //alert("complete");
  });
    };
    this.toString = function(){
        var str;
        for(p in this){
            if(typeof(this[p]) != "function"){
                str += this[p];
            }
        }
        return str;
    }
}
inheritPrototype(Global, BaseType);
function MiWM_ListenManager(){
    this.listen_map = {}
    this.reply = function(taskid, ret, data, msg){
        if(ret){
            var func_cb = this.listen_map[taskid]
            func_cb(data)
            // data is valid
        }else{
            var
            // msg is valid
        }
    };
    this.add = function(func_cb){
        var id = this.get_id();
        this.listen_map[id] = func_cb;
    }
    this.get_id = function(){
        return this.id_acc++;
    }
}
MiWM_ListenManager.prototype.id_acc = 0;
function MiWM_CommandManager(){
    this.listen_map = {};
    /// TODO;
    this.add = function(func_cb){
        var id = this.get_id();
        this.listen_map[id] = func_cb;
    }
    this.get_id =  function(){
        return this.id_acc++;
    }
}
MiWM_CommandManager.prototype.id_acc = 0;
function MiWorkerManager()
{
    this.listen_manager = new MiWM_ListenManager();
    this.cmd_manager = new MiWM_CommandManager();
    this.worker_map = {};
    this.regist_worker = function(worker){
        this.worker_map[worker.id] = worker;
    };
    this.get_worker_id = function(){
        return this.id_acc++;
    };
}
MiWorkerManager.prototype.id_acc = 0;

function MiWorker(worker_manager)
{
    BaseType.call(this);
    this.wm = worker_manager;
    this.id = this.wm.get_worker_id();
    
    this.wm.regist_worker(this);
    
    this.get_status = function(){};
    this.stop = function(){};
    this.pause = function(){};
    this.resume = function(){};
    this.on_idle = function(){};
    this.issue_workflow = function(workflow){
        work = workflow.start();
        for(s in work){
            c, v = work[s];
            if(c == 'listen'){
                /// deal with listen list
                for()
                self.wm.listen_manager.add(test)
            }
            else if(c == 'cmd'){
                /// deal with cmd
                self.wm.cmd_manager.add(cmd)
            }
            else if(step0['result']){
                /// deal with result
            }
        }
    };
}
inheritPrototype(MiWorker, BaseType);
function MiWorkFlow(cbfunc, cbdata)
{
    BaseType.call(this);
    this.label = 'Nothing';
    this.status = null;
    this.progress = null;
    /// If this workflow finished, this callback will be called, to operate next action.
    this.cbfunc = cbfunc;
    this.cbdata = cbdata;
    this.get_status = function(){
        return [this.status, this.progress];
    };
    this.get_label = function(){return this.label;};
    /// virtual, return { 'listen': ..., 'cmd': ..., 'cmds': ..., 'result': ..., 'data': ...}
    this.start = function(){};
    /// If workflow return 'result' field, this.result will be invoked by MiWorker.
    this.result = function(succ, data){
        this.status = this.label + ' Finished';
        this.progress = 1.0;
        self.cbfunc(self.cbdata, succ, data);
    };
}
inheritPrototype(MiWorkFlow, BaseType);

//---------------- Timer -------------------------------
function Http()
{
    this.request = function(url, data){
        var _ret;
        //var data = $.toJSON({'func': func_name, 'param': param});
        //this.send_data(data);
        $.ajax({
            url: url,
            dataType: 'text',
            async: false,
            data: data,
        })
        .success(function(data) {
            //alert("actserver success");
            _ret = data;
        })
        .error(function() { alert("actserver error"); })
        .complete(function() {
            //alert("complete");
        });
        return _ret;
    };
}
function ResultFormat(format){
    /// if ret is true: data is valid
    /// else if ret is false: msg is valid
    /// if function is short operation, data is result.
    /// else if function is long operation, data is unique id.
    try{
        var obj = $.evalJSON(format);
    }catch(error){
        alert('ResultFormat Error: ' + error.message + '\n' + format);
    }
    this.id = obj['id'];
    this.ret = obj['ret'];
    this.data = obj['data'];
    this.msg = obj['msg'];
}
function MiRaise(msg){
    var m = 'MiRaise: ' + msg;
    alert(m);
    throw new Error(m);
}
function Client()
{
    this.init = function(){};
    this.http = new Http();
    __act_server = function(func, params){
        var url = func;
        var data = {'params': $.toJSON(params)};
        var ret = this.http.request(url, data);
        return new ResultFormat(ret);
    }
    this.act_short = function(func, params){
        var ret_fmt = __act_server(func, params);
        return ret_fmt;
    }
    this.act_long = function(func, params){
        var ret_fmt = __act_server(func, params);
        return ret_fmt;
    }
}
function TaskManager(worker_manager)
{
    BaseType.call(this);
    this.wm = worker_manager;
    this.run_tmid = -1;
    this.beat_cnt = 0;
    this.run_show = false;
    this.client = new Client();
    this.client.init();
    this.task_q_has_send = new Array();
    this.task_q_not_send = new Array();
    this.heart_beat = function(){
        this.beat_cnt += 1;
        if(this.cur_id >= 0){
            if(this.beat_cnt % 2 == 0){
                this.probe_and_show();
            }
            this.probe_results();
        }
        this.put_action();
    };
    this.probe_results = function(){
        var ret_fmt = this.client.act_short('get_results', null);
        debug('get_results: ' + ret);
        /// debug... to raise every error return.
        if(ret_fmt.ret){
            this.wm.listen_manager.reply(ret_fmt.id, ret_fmt.ret, ret_fmt.data, ret_fmt.msg);
        }else{
            MiRaise('get_results error! ret: ' + ret_fmt.ret + ' data: ' + ret_fmt.data + ' msg: ' + ret_fmt.fmt);
        }
        
    };
    this.put_action = function(){
        //if(self.cur_id >= 0) return false;
        // get an task.
        
        if(this.wm.cmd_manager.get_length() == 0) return false;
        task = this.wm.cmd_manager.pop_task();
        ret_fmt = self.client.act_long(task.get_func(), task.get_params());
        if(ret_fmt.ret){
            // data is valid, but it usually have nothing.
        }else{
            MiRaise('act_long error occor! error msg ' +  ret_fmt.msg);
        }
        return true;
    };
    this.probe_and_show = function(){
        if(!this.run_show){
            return false;
        }
        var ret = this.client.act_short('probe_step', null);
        debug('probe_and_show: ' + ret);
        /// TODO: get result from server.
    };
    this.born = function(objname){
        setInterval(objname + '.heart_beat()',1000);
    };
}
inheritPrototype(TaskManager, BaseType)
//---------------- Iterface -------------------------
// Interface class is for checking if an instance object implements all methods of required interface
var Interface = function(name, methods) {
    if(arguments.length != 2) {
        throw new Error("Interface constructor expects 2 arguments, but exactly provided for " + arguments.length + " arguments.");
    }
    this.name = name;
    this.methods = [];
    for(var i = 0;i < methods.length; i++) {
        if(typeof methods[i] != "string") {
            throw new Error("Interface constructor expects to pass a string method name.");
        }
        this.methods.push(methods[i]);
    }
}
//static class method
Interface.ensureImplements = function(instance) {
    if(arguments.length < 2) {
        throw new Error("Function Interface.ensureImplements expects at least 2 arguments, but exactly passed for " + arguments.length + " arguments.");
    }
    for(var i = 1, len = arguments.length; i < len; i++) {
        var interface = arguments[i];
        if(interface.constructor != Interface) {
            throw new Error("Function Interface.ensureImplements expects at least 2 arguments to be instances of Interface.");
        }
        for(var j = 0, mLen = interface.methods.length; j < mLen; j++) {
            var method = interface.methods[j];
            if(!instance[method] || typeof instance[method] != "function") {
                throw new Error("Function Interface.ensureImplements: object doesn't implements " + interface.name + ". Method " + method + " wasn't found.");
            }
        }
    }
}


