'use strict'


exports = module.exports = Object.freeze({

    cmd_type : "cmdtype",
    cmd_type_httpreq : "httpreq",
    cmd_type_httpresp: "httpresp",
    cmd_resp_result: "result",
    cmd_resp_OK: "OK",
    cmd_resp_ERROR: "ERROR",
    cmd_resp_error_msg: "errmsg",
    req_cmd_newuser : "newuser",
    req_cmd_login:"login",
    req_cmd_set_pwd:"set-pwd",
    req_cmd_add_dev: "add_dev",
    req_param_devid: "devid",
    req_param_pwd: "password",
    req_userid:"userid",
    get_error_packet: function (err_code) {
        return "";

    },


});