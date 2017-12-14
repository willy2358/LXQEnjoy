
var request = require('request')

var newUserReq = {
	cmdtype:"httpreq",
	httpreq: "newuser",
	devid: "wqrrrq",
}

var loginReq = {
    cmdtype:"httpreq",
    httpreq:"login",
    userid:20,
    devid:"wqrrrq",
}

var myJSONObject = {"key1":"value1", "key2":"value2"};

request({
    url: "http://0.0.0.0:8081/service",
    method: "POST",
    json: true,   // <--Very important!!!
    body: loginReq,
}, function (error, response, body){
    console.log(response);
});

// request('http://0.0.0.0:8081/test', function(error, response, body){
// 	console.log('error:',error);
// 	console.log('statusCode:', response && response.statusCode);
// 	console.log('body:', body);
// });

// request.post('http://0.0.0.0:8081/believe', {form:{"name":'value'}});