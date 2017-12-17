
var log = require('./log.js');
log.configure();
var logger = log.logger();

var express = require('express');
var app = express();

app.use(log.useLog());

var bodyParser = require("body-parser");
app.use(bodyParser.urlencoded({extended:false}));
app.use(bodyParser.json());

// var api_protocal = require('./api_protocal.js');
//
// var database = require('./database.js');

var api_protocal = require("./api-protocal.js");
var db = require('./db.js');
var utils = require('./utils.js');

var conn = db.conn();


app.post('/service', function(req, res){
    try{
        jsonReq = JSON.stringify(req.body);
        var reqObj = JSON.parse(jsonReq);
        if (api_protocal.cmd_type_httpreq in reqObj){
            dispatch_request(reqObj[api_protocal.cmd_type_httpreq], reqObj, res);
        }
        else{
            res.end("invalid request!")
        }
    }
    catch(err){
        logger.error(err);
    }
});

var server = app.listen(8081, function () {
    // body...
    var host = server.address().address;
    var port = server.address().port;

    console.log("address visited http://%s:%s", host, port)
});

function generate_session_token() {
    return "fsfewer";
}

function create_error_repsonse(errMsg) {
    return errMsg;
}

function create_sucess_response(msg) {
    return msg;
}

function dispatch_request(req_cmd, req_obj, resp){
    if (req_cmd == api_protocal.req_cmd_newuser){
        process_new_user(req_obj, resp)
    }
    else if (req_cmd == api_protocal.req_cmd_login){
        process_login(req_obj, resp);
    }
}

function process_new_user(req_obj, resp) {
    try{
        var dev_id = req_obj[api_protocal.req_param_devid]
        get_is_device_already_registered(dev_id, function (registed) {
            if (registed){
                resp.end(api_protocal.get_error_packet("device has already been registered"));
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
        logger.exception(err)
    }
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


function process_login(req_obj, resp) {
    var temp = "select userid from user_device where userid={0} and device='{1}'";
    var user_id = req_obj[api_protocal.req_userid];
    var device = req_obj[api_protocal.req_param_devid];
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
