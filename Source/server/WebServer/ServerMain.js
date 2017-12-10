//ServerMain.js 

var log = require('./log.js');
log.configure();
var logger = log.logger();

var express = require('express');
var app = express();

app.use(log.useLog());


var bodyParser = require("body-parser");
app.use(bodyParser.urlencoded({extended:false}));
app.use(bodyParser.json());

var ApiProtocal = require('./ApiProtocal.js')


var mysql = require('mysql');
var conn = mysql.createConnection({
    host: 'localhost',
    user: 'root',
    password: 'root',
    database:'SqlTest'
});

conn.connect();
// conn.close();



<!-- lang: js -->
/**
 * 替换所有匹配exp的字符串为指定字符串
 * @param exp 被替换部分的正则
 * @param newStr 替换成的字符串
 */
String.prototype.replaceAll = function (exp, newStr) {
    return this.replace(new RegExp(exp, "gm"), newStr);
};

/**
 * 原型：字符串格式化
 * @param args 格式化参数值
 */
String.prototype.format = function(args) {
    var result = this;
    if (arguments.length < 1) {
        return result;
    }

    var data = arguments; // 如果模板参数是数组
    if (arguments.length == 1 && typeof (args) == "object") {
        // 如果模板参数是对象
        data = args;
    }
    for ( var key in data) {
        var value = data[key];
        if (undefined != value) {
            result = result.replaceAll("\\{" + key + "\\}", value);
        }
    }
    return result;
}

// var template1="我是'{0}'，今年{1}了, lucy今年也{1}了";
// var result1=template1.format("loogn",22);
// console.log(result1);

function is_device_already_exist(dev_id){
	temp = "select device from users where device = '{0}'";
	sql = temp.format(dev_id);
	console.log(sql);
	conn.query(sql, function(err, rows, fields){
		if (err){
			logger.error(err);
		}

		if (rows.length > 0){
			return true;
		}
		else{
			return false;
		}
	});
}

function add_new_user(dev_id, callback){
	temp = "insert into users(device) values ('{0}')";
	
	sql = temp.format(dev_id);
	console.log(temp);
	conn.query(sql, function(err, rows, fields){
		var ret = {};
		if (err){
			logger.error(err);
			ret = {'result': false, 'nid': -1}
		}
		else{
			console.log("here");
			console.log(rows.insertId);
			ret = {'result': true, 'nid': rows.insertId}
		}

		callback(ret);
	});
}

function get_user_info(user_id, callback){
	var user = {}
	template = "select username from users where userid = {0}";
	sql = template.format(user_id);
	conn.query(sql, function(err, rows, fields){
		if (rows.length > 0){
			
			user.name = rows[0].username;
			callback(rows[0].username);

		}
	});

	return user;
}


function dispatch_request(req_cmd, req_obj, resp){
	if (req_cmd == ApiProtocal.req_cmd_newuser){
		process_new_user(req_obj, resp)
	}
}

function process_new_user(req_obj, resp) {
	var dev_id = req_obj[ApiProtocal.req_param_devid]
	if (is_device_already_exist(dev_id)){
		resp.end("ERROR:device already registered");
	}
	else{
		add_new_user(dev_id, function(ret){
			console.log(ret);
			if (ret["nid"] > 0){
				get_user_info(ret["nid"], function(data){
					resp.end("new user:" + data);
				});
			}
		});
		
	}
}

app.post('/service', function(req, res){
	try{
		jsonReq = JSON.stringify(req.body);
		var reqObj = JSON.parse(jsonReq);
		if (ApiProtocal.cmd_type_httpreq in reqObj){
			dispatch_request(reqObj[ApiProtocal.cmd_type_httpreq], reqObj, res);
		}
		else{
			res.end("invalid request!")
		}
	}
	catch(err){
		logger.error(err);
	}
});



app.get('/test', function(req, res){
	res.end("Hi, how are you?");
});


var server = app.listen(8081, function () {
	// body...
	var host = server.address().address;
	var port = server.address().port;

	console.log("address visited http://%s:%s", host, port)
});