'use strict'

const ERROR_OK = 0;
const ERROR_UNDEFINED = -1;
const ERROR_INVALID_USERID = 11;
const ERROR_INVALID_USERNAME = 12;

exports = module.exports = Object.freeze({
    ERROR_OK : 0,
    ERROR_UNDEFINED: -1,
    ERROR_INVALID_USERID: 11,
    ERROR_INVALID_USERNAME: 12
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