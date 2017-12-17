'use strict'
var mysql = require('mysql');

var connection;

exports = module.exports = Object.freeze({

    username_start_number:122363,

    table_user : "user",
    field_userid : "userid",
    field_username : "username",

    table_user_device:"user_device",
    field_device:"device",
    field_device_valid : "valid",

    conn:function () {
        if (!connection){
            connection = mysql.createConnection({
                ost: 'localhost',
                user: 'root',
                password: 'root',
                database:'SqlTest'
            });
        }

        return connection;
    }
});

// var mysql = require('mysql');
// var connection = mysql.createConnection({
//     host: 'localhost',
//     user: 'root',
//     password: 'root',
//     database:'SqlTest'
// });
//
// connection.connect();