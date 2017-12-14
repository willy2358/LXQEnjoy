
// 'use strict'

const ApiProtocal = exports

// var cmdType = "cmdtype"
// var cmdTypeHttpReq = "httpreq"

// ApiProtocal.Req_NewUser = "newuser"

// var PI = Math.PI;
// exports.area = function (r) {
//     return PI * r * r;
// };
// exports.circumference = function (r) {
//     return 2 * PI * r;
// };

// exports.PI = PI;

// ApiProtocal.DAPI= PI;

var cmd_type_httpreq = "httpreq";
var req_cmd_newuser = "newuser";
var req_param_devid = "devid";

var x = 5;
var addX = function (value) {
    return value + x;
};

exports = module.exports = Object.freeze({

	cmd_type : "cmdtype",
	cmd_type_httpreq : "httpreq",
	req_cmd_newuser : "newuser",
	req_cmd_login:"login",
	req_param_devid : "devid",
	req_userid:"userid",
    get_error_packet: get_error_packet,

});


module.exports.x = x;
module.exports.addX = addX;

var get_error_packet = function (error) {
    return error;
};

module.exports.get_error_packet = get_error_packet;

