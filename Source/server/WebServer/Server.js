
var log = require('./log.js');
log.configure();
var logger = log.logger();
var uuid = require('uuid');

var errors = require('./errors.js');

var express = require('express');
var app = express();

app.use(log.useLog());

var bodyParser = require("body-parser");
app.use(bodyParser.urlencoded({extended:false}));
app.use(bodyParser.json());


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

function generate_session_token(userid) {

    var vid = uuid.v1();

    return vid;
}

function create_error_resp_str(cmd, errCode, errMsg) {
    if (errMsg == undefined){
        errMsg = errors.get_error_desc(errCode);
    }

    var pack = create_error_resp_pack(cmd, errMsg, errCode);

    return JSON.stringify(pack);
}

function create_error_resp_pack(cmd, errMsg, errCode) {
    var pack = {
        cmdtype: api_protocal.cmd_type_httpresp,
        httpresp: cmd,
        result: api_protocal.cmd_resp_ERROR,
        errmsg: errMsg,
        errcode:errCode
    };

    return pack;
}

function create_successs_resp_pack(cmd, result_name, result_data) {
    var ret_name = result_name||"";
    var pack = {
        cmdtype: api_protocal.cmd_type_httpresp,
        httpresp:cmd,
        result:api_protocal.cmd_resp_OK,
        "result-data":ret_name,
    }

    if (ret_name.length > 0 && result_data != undefined){
        pack[ret_name] = result_data;
    }

    return pack;
}

function create_success_resp_str(cmd, result_name, result_data) {
    pack = create_successs_resp_pack(cmd, result_name, result_data);

    return JSON.stringify(pack);
}

function dispatch_request(req_cmd, req_obj, resp){
    if (req_cmd == api_protocal.req_cmd_newuser){
        process_new_user(req_obj, resp)
    }
    else if (req_cmd == api_protocal.req_cmd_login){
        process_login(req_obj, resp);
    }
    else if (req_cmd == api_protocal.req_cmd_set_pwd){
        process_set_password(req_obj, resp);
    }
    else if (req_cmd == api_protocal.req_cmd_add_dev){
        process_add_device(req_obj, resp);
    }
    else if (req_cmd == api_protocal.req_cmd_get_games){
        process_get_games(req_obj, resp);
    }
    else if (req_cmd == api_protocal.req_cmd_new_room){
        process_new_room(req_obj, resp);
    }
}

function logger_undefined_err(err_code, err){

}

function process_get_games(req_obj, resp){
    var cmd = req_obj[api_protocal.cmd_type_httpreq];
    try{
        var sql = "select gameid, game_name,min_players, max_players, server_ip, server_port, region, type from game";
        conn.query(sql, function(err, result){
            if (err){
               var resp_str = create_error_resp_str(cmd, errors.ERROR_UNDEFINED, err);
               resp.end(resp_str);
            }
            else{
               var gs = [];
               for(var i = 0; i < result.length; i++){
                   var game = {
                       gameid : result[i].gameid,
                       game_name: result[i].game_name,
                       game_type: result[i].type,
                       min_players:result[i].min_players,
                       max_players:result[i].max_players,
                       server_ip:result[i].server_ip,
                       server_port:result[i].server_port,
                       region:result[i].region
                   }
                   gs.push(game);
               }

               var resp_str = create_success_resp_str(cmd, api_protocal.resp_games, gs);
               resp.end(resp_str);
           }
        });
    }
    catch (err){
        response_undefined_err(cmd, err, resp);
    }
}

function response_undefined_err(reqcmd, err, resp){
    // var err_code = generate_error_code_for_undefined_err(err);
    // var resp_pack = create_error_response(err_code);
    logger_undefined_err(errors.ERROR_UNDEFINED, err);
    var resp_str = create_error_resp_str(reqcmd, errors.ERROR_UNDEFINED, err);
    resp.end(resp_str);
}

function process_new_room(req_obj, resp){
    var cmd = req_obj[api_protocal.cmd_type_httpreq];
    try{
        var userid = req_obj[api_protocal.req_userid];
        var gameid = req_obj[api_protocal.game_id];
        var gps_cheat_proof = req_obj[api_protocal.req_room_same_gps_exclude];
        var ip_cheat_proof = req_obj[api_protocal.req_room_same_ip_exclude];
        var game_rounds = req_obj[api_protocal.req_room_game_round_num];
        var fee_stuff_id = req_obj[api_protocal.req_room_game_fee_stuff_id];
        var fee_amount_per_player = req_obj[api_protocal.req_room_game_fee_per_player];
        var fee_creator_pay_all = req_obj[api_protocal.req_room_game_fee_creator_pay_all];
        var stake_stuff_id = req_obj[api_protocal.req_room_game_stake_stuff_id];
        var stake_base_score = req_obj[api_protocal.req_room_game_stake_base_score];

        var sql = "select count(room_no) as num from room where userid={0}";

        sql = sql.format(userid);
        conn.query(sql, function(err, results){
            if (err){
                console.log(err);
                response_undefined_err(cmd, err, resp);
            }
            else{
                var n = results[0].num;
                if (n >= 9){
                    var resp_pack = create_error_resp_str(cmd, errors.ERROR_TO_MAX_ALLOWED_ROOMS);
                    resp.end(resp_pack);
                }
                else{
                    var room_number = (db.room_start_number + userid * 10) + n;
                    create_new_room_for_user(userid, gameid, room_number, game_rounds, ip_cheat_proof, gps_cheat_proof,
                    fee_stuff_id, fee_amount_per_player, fee_creator_pay_all, stake_stuff_id, stake_base_score,
                    function(err){
                        response_undefined_err(cmd, err, resp);
                    },
                    function(ret_msg){
                        if(ret_msg == errors.cbt_room_created_failed){
                            var resp_pack = create_error_resp_str(cmd, errors.ERROR_FAILED_TO_CREATE_ROOM);
                            resp.end(resp_pack);
                        }
                        else{
                            room = {
                                "room_num":room_number
                            }

                            var resp_str = create_success_resp_str(cmd, api_protocal.resp_room, room);
                            resp.end(resp_str);
                        }
                    });
                }
            }
        });
    }
    catch (err){
        response_undefined_err(cmd, err, resp);
    }
}

function create_new_room_for_user(userid, gameid, room_number, round_num, ip_exclude, gps_exclude,
                                  fee_stuff_id, fee_amount_per_player, fee_creator_pay_all, stake_stuff_id, stake_base_score,
                                  err_callback, result_callback){
    try{
        var sql = "insert into room(userid, gameid, room_no, round_num, ex_ip_cheat, ex_gps_cheat" +
            ",fee_stuff_id, fee_amount_per_player, fee_creator_pay_all, stake_stuff_id, stake_base_score) values({0},{1},{2},{3},{4},{5}" +
            ",{6},{7},{8},{9},{10})";
        sql = sql.format(userid, gameid, room_number,round_num, ip_exclude, gps_exclude,
            fee_stuff_id, fee_amount_per_player, fee_creator_pay_all, stake_stuff_id, stake_base_score);
        conn.query(sql, function(err, result){
           if(err){
               if(err_callback){
                   err_callback(err);
               }
           }
           else if(result_callback){
               result_callback(errors.cbt_room_created_ok);
           }
        });
    }
    catch(err){
        if(err_callback){
            err_callback(err);
        }
    }
}

function process_set_password(req_obj, resp){
    try{
        var newPwd = req_obj[api_protocal.req_param_pwd];
        var userid = req_obj[api_protocal.req_userid];
        var devid = req_obj[api_protocal.req_param_devid];
        var cmd = req_obj[api_protocal.cmd_type_httpreq];

        is_device_valid(userid, devid,
            function (err) {
                resp_pack = create_error_resp_str(cmd, errors.ERROR_UNDEFINED, String(err));
                resp.end(resp_pack);
            },
            function (ret_msg) {
                if (ret_msg === errors.cbt_valid_device) {
                    var temp = "update user set password = '{0}' where userid={1}";
                    sql = temp.format(newPwd, userid);
                    conn.query(sql, function (err, result) {
                        if (err) {
                            logger.error(err);
                            var resp_pack = create_error_resp_str(cmd, errors.ERROR_UNDEFINED, String(err));
                            resp.end(resp_pack);
                        }
                        else {
                            var resp_pack = create_success_resp_str(cmd, "");
                            resp.end(resp_pack);
                        }
                    });
                }
                else {
                    var resp_pack = create_error_resp_str(cmd, errors.ERROR_DEVICE_NOT_REGISTERED);
                    resp.end(resp_pack);
                }
            });
    }
    catch (err){
        logger.exception(err);
    }
}

function process_add_device(req_obj, resp){
    try{
        var dev_id = req_obj[api_protocal.req_param_devid];
        var userid = req_obj[api_protocal.req_userid];
        var pwd = req_obj[api_protocal.req_param_pwd];
        var cmd = req_obj[api_protocal.cmd_type_httpreq];

        is_password_right(userid, pwd,
            function (err) {
                var resp_pack = create_error_resp_str(cmd, errors.ERROR_UNDEFINED, err);
                resp.end(err);
            },
            function (ret_msg) {
                if (ret_msg !== errors.cbt_valid_password){
                    var resp_pack = create_error_resp_str(cmd, errors.ERROR_PWD_NOT_RIGHT);
                    resp.end(resp_pack);
                }
                else {
                    is_device_valid(userid, dev_id,
                        function (err) {
                            var resp_pack = create_error_resp_str(cmd, errors.ERROR_UNDEFINED, String(err));
                            resp.end(resp_pack);
                        },
                        function (ret_msg) {
                            if (ret_msg !==errors.cbt_valid_device){
                                record_user_device(userid, dev_id,
                                    function (err) {
                                        var resp_pack = create_error_resp_str(cmd, errors.ERROR_UNDEFINED, String(err));
                                        resp.end(resp_pack);
                                    },
                                    function (ret_msg) {
                                        var resp_pack = create_success_resp_str(cmd);
                                        resp.end(resp_pack);
                                    }
                                );
                            }
                            else{
                                var resp_pack = create_error_resp_str(cmd, errors.ERROR_DEVICE_ALREADY_REGISTERED);
                                resp.end(resp_pack);
                            }
                        }
                    );
                }
            }
        );
    }
    catch (err){
        logger.exception(err);
    }
}

function is_user_exist(userid, err_callback, result_callback) {
    var temp = "select count(userid) from user where userid = {0}";
    var sql = temp.format(userid);
    conn.query(sql, function (err, result) {
        if(err && err_callback){
            err_callback(err);
        }
        else if (result_callback){
            if(result.length > 0){
                result_callback(errors.cbt_valid_userid);
            }
            else{
                result_callback(errors.cbt_invalid_userid);
            }
        }
    });
}

function is_device_valid(userid, devid, err_callback, result_callback) {
    is_user_exist(userid, err_callback,
        function (ret_msg) {
            if (result_callback){
                if (ret_msg == errors.cbt_valid_userid){
                    var temp = "select count(userid) as cid from user_device where userid={0} and device='{1}'";
                    var sql = temp.format(userid, devid);
                    conn.query(sql, function (err, result) {
                        if (err){
                            if (err_callback){
                                err_callback(err);
                            }
                        }
                        else{
                            if (result['cid'] > 0){
                                result_callback(errors.cbt_valid_device);
                            }
                            else{
                                result_callback(errors.cbt_invalid_device);
                            }
                        }
                    });
                }
                else{
                    result_callback(errors.cbt_invalid_userid);
                }
        }

    });

}

function is_password_right(userid, password, err_callback, result_callback) {
    is_user_exist(userid, err_callback, function (ret) {
        if (ret == errors.cbt_valid_userid){
            var tmp = "select count(userid) as uid from user where userid={0} and password='{1}'";
            sql = tmp.format(userid, password);
            conn.query(sql, function(err, result){
               if (err){
                   if (err_callback){
                       err_callback(err);
                   }
               }
               else if (result_callback){
                   if (result.length > 0){
                       result_callback(errors.cbt_valid_password);
                   }
                   else{
                       result_callback(errors.cbt_invalid_pwd);
                   }
               }
            });
        }
        else {
            result_callback(errors.cbt_invalid_userid);
        }
    });
}

function is_dev_register(userid, devid, callback){
    var tmp = "select count(*) from user_device where userid={0} and device='{1}'";
    var sql = tmp.format(userid, devid);
    conn.query(sql, function(err, result){

    })
}

function process_new_user(req_obj, resp) {
    try{
        var dev_id = req_obj[api_protocal.req_param_devid]
        var cmd = req_obj[api_protocal.cmd_type_httpreq];
        get_is_device_already_registered(dev_id,
            function(err){
                resp_str = create_error_resp_str(cmd, errors.ERROR_UNDEFINED, err);
                logger.error(err);
                resp.end(resp_str);
            },
            function (ret_msg) {
                if (ret_msg === errors.cbt_device_found){
                    resp_str = create_error_resp_str(cmd, errors.ERROR_DEVICE_ALREADY_REGISTERED);
                    logger.error(resp_str);
                    resp.end(resp_str);
                }
                else{
                    add_new_user(dev_id,
                        function(err){
                            var resp_str = create_error_resp_str(cmd, errors.ERROR_FAILED_CREATE_USER, String(err));
                            logger.error(resp_str);
                            resp.end(resp_str);
                        },
                        function(userObj){
                            var resp_str = create_success_resp_str(cmd, api_protocal.resp_user, userObj);
                            resp.end(resp_str);
                        }
                    );
                }
            });
    }
    catch (err){
        logger.exception(err)
    }
}


function update_user_login_token(userid, dev_id, err_callback, ret_callback) {
    var temp = "select userid from user_login where userid={0}";
    var sql = temp.format(userid);
    conn.query(sql, function (err, result) {
        if (err){
            if (err_callback){
                err_callback(err);
            }
        }
        else{
            token = generate_session_token(userid);
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
                    if(err_callback){
                        err_callback(err);
                    }
                }
                else if(ret_callback){
                    ret_callback(token);
                }
            })
        }
    })
}

function get_is_device_already_registered(dev_id, err_callback, ret_callback) {
    var template = "select device from user_device where device = '{0}'";
    var sql = template.format(dev_id);
    console.log(sql);
    conn.query(sql, function (err, result) {
        if (err){
            if (err_callback){
                err_callback(err);
            }
        }
        else if (ret_callback){
            if (result.length > 0){
                ret_callback(errors.cbt_device_found);
            }
            else{
                ret_callback(errors.cbt_device_not_found);
            }
        }
    });
}

function record_user_device(userid, dev_id, err_callback, ret_callback) {
    var temp = "insert into user_device(userid, device) values({0},'{1}');";
    var sql = temp.format(userid, dev_id);
    conn.query(sql, function (err, resutl) {
        if (err){
            if (err_callback){
                err_callback(err);
            }
        }
        else if (ret_callback){
            ret_callback(errors.cbt_record_device_ok);
        }
    });
}

function add_new_user(dev_id, err_callback, ret_callback){
    var temp = "select count({0}) as cid from {1}";
    var sql = temp.format(db.field_userid, db.table_user);
    console.log(sql);
    conn.query(sql, function(err, result){
        if (err){
            if (err_callback){
                err_callback(err);
            }
        }
        else{
            var username = "LX" + (result[0].cid + db.username_start_number + 1)
            var sql = "insert into {0}({1}) values('{2}')".format(db.table_user, db.field_username, username);
            conn.query(sql, function (err, result) {
                if (err) {
                    if (err_callback){
                        err_callback(err);
                    }
                }
                else {
                    var newId = result.insertId;
                    var sql = "insert into {0}({1},{2}) values ({3},'{4}');".format(db.table_user_device,
                        db.field_userid, db.field_device, newId, dev_id);
                    conn.query(sql, function (err, result) {
                        if (err){
                            if (err_callback){
                                err_callback(err);
                            }
                        }
                        else if (ret_callback){
                            var newUser = {
                                "userid":newId,
                                "username":username
                            };
                            ret_callback(newUser);
                        }
                    });
                }
            });
        }
    });
}

function get_user_info(user_id, callback){
    var template = "select username from {0} where userid = {1}";
    var sql = template.format(db.table_user, user_id);
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
    var cmd = req_obj[api_protocal.cmd_type_httpreq];
    var sql = temp.format(user_id, device);
    conn.query(sql, function (err, result) {
        if (err){
            var resp_str = create_error_resp_str(cmd, errors.ERROR_UNDEFINED, String(err));
            logger.error(err);
            resp.end(resp_str);
        }
        else {
            if (result.length > 0) {
                update_user_login_token(user_id, device,
                    function(err){
                        var resp_str = create_error_resp_str(cmd, errors.ERROR_UNDEFINED,  String(err));
                        logger.error(resp_str);
                        resp.end(resp_str);
                    },
                    function (token) {
                    if (token){
                        var loginObj = {
                            "session-token":token,
                            "user-info":{
                                "userid":user_id,
                            }
                        };
                        var resp_str = create_success_resp_str(cmd, api_protocal.resp_login, loginObj);
                        resp.end(resp_str);

                    }
                    else{
                        var resp_str = create_error_resp_str(cmd, errors.ERROR_FAILED_LOGIN, "Invalid token");
                        resp.end(resp_str);
                    }
                });
            }
            else{
                var err_resp = create_error_resp_str(cmd, errors.ERROR_DEVICE_NOT_REGISTERED);
                resp.end(err_resp);
            }
        }
    });
}
