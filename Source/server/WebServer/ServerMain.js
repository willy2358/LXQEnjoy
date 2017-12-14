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

var database = require('./database.js')


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
//
// function is_device_already_exist(dev_id){
// 	temp = "select device from users where device = '{0}'";
// 	sql = temp.format(dev_id);
// 	console.log(sql);
// 	conn.query(sql, function(err, rows, fields){
// 		if (err){
// 			logger.error(err);
// 		}
//
// 		if (rows.length > 0){
// 			return true;
// 		}
// 		else{
// 			return false;
// 		}
// 	});
// }

function get_is_device_already_registered(dev_id, callback) {
	var template = "select device from {0} where {1} = '{2}'";
	var sql = template.format(database.table_user_device, database.field_device, dev_id);
	console.log(sql);
	conn.query(sql, function (err, result) {
        if (err){
            logger.error(err);
            return;
        }

        if (null != callback){
            if(result.length > 0){
                callback(true);
            }
            else{
                callback(false);
            }
        }
    });
}

function add_new_user(dev_id, callback){
	var temp = "select count({0}) as cid from {1}";
	var sql = temp.format(database.field_userid, database.table_user);
	console.log(sql);
	conn.query(sql, function(err, result){
		if (err){
			logger.error(err);
            callback(-1);
		}
		else{
		    var username = "LX" + (result[0].cid + database.username_start_number + 1)
            var sql = "insert into {0}({1}) values('{2}')".format(database.table_user, database.field_username, username);
		    conn.query(sql, function (err, result) {
                if (err) {
                    logger.error(err);
                }
                else {
                    var newId = result.insertId;
                    var sql = "insert into {0}({1},{2}) values ({3},'{4}');".format(database.table_user_device,
                        database.field_userid, database.field_device, newId, dev_id);
                    conn.query(sql, function (err, rows, fields) {
                        if (err){
                            callback(-1);
                        }
                        else{
                            callback(newId);
                            logger.info("new user id created:" + newId);
                        }
                    });
                }
            });
		}
	});
}

function get_user_info(user_id, callback){
	var template = "select username from {0} where userid = {1}";
	var sql = template.format(database.table_user, user_id);
	conn.query(sql, function(err, result){
		if (err){
			logger.error(err)
		}
		else if (result.length > 0){
			var username = result[0].username;
			if (null != callback){
                callback(username);
			}
		}
	});
}


function dispatch_request(req_cmd, req_obj, resp){
	if (req_cmd == ApiProtocal.req_cmd_newuser){
		process_new_user(req_obj, resp)
	}
	else if (req_cmd == ApiProtocal.req_cmd_login){
		process_login(req_obj, resp);
	}
}

function process_new_user(req_obj, resp) {
	try{
        var dev_id = req_obj[ApiProtocal.req_param_devid]
        get_is_device_already_registered(dev_id, function (registed) {
            if (registed){
                resp.end(ApiProtocal.get_error_packet("device has already been registered"));
            }
            else{
                add_new_user(dev_id, function(usrid){
                    if (usrid > 0){
                        get_user_info(usrid, function(data){
                            resp.end("new user:" + data + ",userid:" + usrid);
                        });
                    }
                });
            }
        });
	}
	catch (err){
		Logger.exception(err)
	}
}

function create_error_repsonse(errMsg) {
	return errMsg;
}

function create_sucess_response(msg) {
	return msg;
}

function generate_session_token() {
	return "fsfewer";
}

function update_user_login_token(userid, dev_id, callback) {
	var temp = "select userid from user_login where userid={0}";
	var sql = temp.format(userid);
	conn.query(sql, function (err, result) {
		if (err){
			logger.error(err);
			// callback(err, )
		}
		else{
			token = generate_session_token();
			if (result.length > 0){
				temp = "update user_login set device='{0}',session_token='{1}' where userid={2}";
				sql = temp.format(dev_id, token, userid);
			}
			else{
                temp = "insert into user_login(userid, device, session_token) values({0},'{1}','{2}');";
                sql = temp.format(userid, dev_id, token);
			}
			conn.query(sql, function (err, result) {
				if(err){
					logger.error(err);
				}
				else{
					callback(token);
				}
            })
		}
    })
}

function process_login(req_obj, resp) {
	var temp = "select userid from user_device where userid={0} and device='{1}'";
	var user_id = req_obj[ApiProtocal.req_userid];
	var device = req_obj[ApiProtocal.req_param_devid];
	var sql = temp.format(user_id, device);
	conn.query(sql, function (err, result) {
		if (err){
			logger.error(err);
		}
		else {
            if (result.length > 0) {
            	update_user_login_token(user_id, device, function (token) {
					if (token){
                        resp_pack = create_sucess_response("userid:" + user_id + ",session-token:" + token);
                        resp.end(resp_pack);
					}
					else{
						resp.end("Failed to login");
					}
                });
            }
            else{
            	err_resp = create_error_repsonse("Not registered device");
            	resp.end(err_resp);
			}
        }
    });
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