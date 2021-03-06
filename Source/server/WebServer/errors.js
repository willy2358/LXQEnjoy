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
    ERROR_TO_MAX_ALLOWED_ROOMS:17,         //用户达到最大允许创建数
    ERROR_FAILED_TO_CREATE_ROOM: 18,       //创建房间失败
    ERROR_PWD_NOT_RIGHT:19,                //密码不正确

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
    cbt_room_created_ok: "room created ok",
    cbt_room_created_failed:"room created failed",

    get_error_desc:function (errCode) {

        if (errCode === this.ERROR_INVALID_USERID){
            return "Invalid user id";
        }
        else if (errCode === this.ERROR_INVALID_USERNAME){
            return "Invalid user name";
        }
        else if (errCode == this.ERROR_DEVICE_ALREADY_REGISTERED){
            return "Device has been already registered";
        }
        else if (errCode == this.ERROR_FAILED_CREATE_USER){
            return "Failed to create user";
        }
        else if (errCode === this.ERROR_FAILED_LOGIN){
            return "Failed to login";
        }
        else if (errCode === this.ERROR_DEVICE_NOT_REGISTERED){
            return "Not registered device";
        }
        else if (errCode === this.ERROR_TO_MAX_ALLOWED_ROOMS){
            return "Reached the max allowed rooms for one user ";
        }
        else if (errCode === this.ERROR_FAILED_TO_CREATE_ROOM){
            return "Failed to create room";
        }
        else if (errCode === this.ERROR_PWD_NOT_RIGHT){
            return "Password is not right";
        }
        else {
            return "Undefined error";
        }
    },

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