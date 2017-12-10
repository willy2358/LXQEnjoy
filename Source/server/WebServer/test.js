// var http = require("http");
// var express = require("express")

// var ApiProtocal = require('./ApiProtocal.js')

// console.log(ApiProtocal.cmdTypeHttpReq)
// console.log(ApiProtocal.DAPI)

// console.log(ApiProtocal.cmdType)

// console.log(ApiProtocal.cmdTypeHttpReq)

// console.log(ApiProtocal.req_param_devid)
// http.createServer(function(request, response) {
//     response.writeHead(200, {
//         "Content-Type" : "text/plain"
//     });
//     response.write("Welcome to Nodejs");
//     response.end();
// }).listen(8000, "127.0.0.1");

// console.log("Creat server on http://127.0.0.1:8000/");

// 作者：一月筠
// 链接：http://www.jianshu.com/p/5bf6f83e80e8
// 來源：简书
// 著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

//////key testing in dictionary
// var myDict = {"name":"many", "age":23};
// if("name" in myDict){
// 	console.log("name is in dict");
// }
// else{
// 	console.log("name is not in dict");
// }

// if ("gender" in myDict){
// 	console.log("gender is in dict");
// }
// else{
// 	console.log("gender is not in dict");
// }


//////test logger
// var log4js = require('log4js');
// var logger = log4js.getLogger();
// logger.debug("Time:", new Date());
// logger.info("hellooo");

var express = require('express');
var app = express();

// var log4js = require('log4js');
// log4js.configure({
// 	appenders:[
// 	{	type: 'console'	},
// 	{
// 		type: 'file',
// 		filename: 'logs/access.log',
// 		maxLogSize: 1024,
// 		backup: 3,
// 		category: 'normal'
// 	}]
// });
// var logger = log4js.getLogger('normal');
// logger.setLevel('INFO');
// app.use(log4js.connectLogger(logger, {level:'auto'}));

// var log4js = require('log4js');
// log4js.configure({
//   appenders: [
//     { type: 'console' }, //控制台输出
//     {
//       type: 'file', //文件输出
//       filename: 'logs/access.log', 
//       maxLogSize: 1024,
//       backups:3,
//       category: 'normal' 
//     }
//   ]
// });
// var logger = log4js.getLogger('normal');
// logger.setLevel('INFO');

// logger.info("this is from logger");
// var log4js = require('log4js');
// log4js.configure({
//   appenders: { 
//   	console: { type: 'console' },
//   	cheese: { type: 'file', filename: './logs/cheese.log' } },
//   categories: { default: { appenders: ['cheese', 'console' ], level: 'error' } }
// });
// var logger = log4js.getLogger();
// logger.level = 'info';
// logger.debug("Some debug messages");
// logger.error("this is an error")

// var log = require('./log.js');

// log.configure();
// var logger = log.logger();

// logger.error("heelollfs");


// var fs = require('fs');

// app.get('/listUsers', function(req, res){
// 	fs.readFile(__dirname + "/" + "users.json", 'utf8', function(err, data){
// 		console.log(data);
// 		res.end(data);
// 	})
// });

//////test connect to mysql 
// var mysql = require('mysql');
// var connection = mysql.createConnection({
//     host: 'localhost',
//     user: 'root',
//     password: 'root',
//     database:'SqlTest'
// });

// connection.connect();
// //查询
// connection.query('SELECT username from users', function(err, rows, fields) {
//     if (err) throw err;
//     console.log('The solution is: ', rows[0].username);
// });
// //关闭连接
// connection.end();


// <!-- lang: js -->
// /**
//  * 替换所有匹配exp的字符串为指定字符串
//  * @param exp 被替换部分的正则
//  * @param newStr 替换成的字符串
//  */
// String.prototype.replaceAll = function (exp, newStr) {
//     return this.replace(new RegExp(exp, "gm"), newStr);
// };

// /**
//  * 原型：字符串格式化
//  * @param args 格式化参数值
//  */
// String.prototype.format = function(args) {
//     var result = this;
//     if (arguments.length < 1) {
//         return result;
//     }

//     var data = arguments; // 如果模板参数是数组
//     if (arguments.length == 1 && typeof (args) == "object") {
//         // 如果模板参数是对象
//         data = args;
//     }
//     for ( var key in data) {
//         var value = data[key];
//         if (undefined != value) {
//             result = result.replaceAll("\\{" + key + "\\}", value);
//         }
//     }
//     return result;
// }

// var template1="我是'{0}'，今年{1}了, lucy今年也{1}了";
// var result1=template1.format("loogn",22);
// console.log(result1);

function test(){
	// return {"name":"hello", "id":12};
	return {'name':"hello", id:12};
}

var ret = test();
console.log(ret["name"]);
