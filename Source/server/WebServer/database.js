'use strict'
const database = exports

const table_user = "user"
const field_userid = "userid"
const field_username = "username"

const field_device = "device"
const field_device_valid = "valid"

const table_user_device = "user_device"

const username_start_number = 122363;


var mysql = require('mysql');
var connection = mysql.createConnection({
    host: 'localhost',
    user: 'root',
    password: 'root',
    database:'SqlTest'
});

connection.connect();

exports.query = function(sql){

}

exports.execute = function (sql) {
	// body...
}




connection.connect();
//查询
connection.query('SELECT username from users', function(err, rows, fields) {
    if (err) throw err;
    console.log('The solution is: ', rows[0].username);
});
//关闭连接
connection.end();