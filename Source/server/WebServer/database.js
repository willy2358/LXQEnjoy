'use strict'
const database = exports

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