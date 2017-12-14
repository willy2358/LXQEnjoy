'use strict'
const database = exports

var table_user = "user"
var field_userid = "userid"
var field_username = "username"

var field_device = "device"
var field_device_valid = "valid"

var table_user_device = "user_device"

var username_start_number = 122363;

module.exports = Object.freeze({

    username_start_number:122363,

    table_user : "user",
    field_userid : "userid",
    field_username : "username",

    table_user_device:"user_device",
    field_device:"device",
    field_device_valid : "valid",


});
//
// var mysql = require('mysql');
// var connection = mysql.createConnection({
//     host: 'localhost',
//     user: 'root',
//     password: 'root',
//     database:'SqlTest'
// });
//
// connection.connect();
//
// exports.query = function(sql){
//
// }
//
// exports.execute = function (sql) {
// 	// body...
// }




// connection.connect();
// //查询
// connection.query('SELECT username from users', function(err, rows, fields) {
//     if (err) throw err;
//     console.log('The solution is: ', rows[0].username);
// });
// //关闭连接
// connection.end();