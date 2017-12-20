'use strict'

// const ERROR_OK = 0;
// const ERROR_UNDEFINED = -1;
// const ERROR_INVALID_USERID = 11;
// const ERROR_INVALID_USERNAME = 12;

exports = module.exports = Object.freeze({
    ERROR_OK : 0,
    ERROR_UNDEFINED: -1,
    ERROR_INVALID_USERID: 11,
    ERROR_INVALID_USERNAME: 12,
    ERROR_DEVICE_ALREADY_REGISTERED: 13,   //设备已注册
    ERROR_FAILED_CREATE_USER: 14,          //创建新用户失败
    ERROR_FAILED_LOGIN:15,                 //登录失败
    ERROR_DEVICE_NOT_REGISTERED:16,        //设备未注册

    //cbt : callback return
    cbt_invalid_userid: "invalid userid",
    cbt_invalid_pwd: "invalid password",
    cbt_invalid_device: "invalid device",
    cbt_valid_userid: "valid userid",
    cbt_valid_password: "valid password",
    cbt_valid_device: "valid device",
    cbt_device_found:"found device",
    cbt_device_not_found: "not found device",

    cbt_record_device_ok: "record user device ok",



});

// exports.ERROR_OK = ERROR_OK;                       //success, no error
// exports.ERROR_UNDEFINED = ERROR_UNDEFINED;               //unknown error
// exports.ERROR_INVALID_USERID = ERROR_INVALID_USERID;          // invalid userid
// exports.ERROR_INVALID_USERNAME = ERROR_INVALID_USERNAME;

// exports = module.exports = Object.freeze({
//     TEST_CONST:1222,
//
//     test_func:function (data) {
//         console.log("data:" + data);
//     }
// });
//
// module.exports.func2 = function () {
//     console.log("test func2");
// };
//
// module.exports.MyV = 1222;