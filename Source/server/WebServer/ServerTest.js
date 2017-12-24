
var request = require('request')

var newUserReq = {
	cmdtype:"httpreq",
	httpreq: "newuser",
	devid: "wqrrrq21",
}

var loginReq = {
    cmdtype:"httpreq",
    httpreq:"login",
    userid:22,
    devid:"wqrrrq",
}

var setPwdReq ={
    cmdtype:"httpreq",
    httpreq:"set-pwd",
    password:"rwrv232",
    userid:22,
    devid:"wqrrrq",
}

var addDevReq ={
    cmdtype:"httpreq",
    httpreq:"add-dev",
    password:"rwrv232",
    userid:22,
    devid:"22dev2",
}

var getGamesReq = {
    "cmdtype":"httpreq",
    httpreq:"getgames",
}

var createRoomReq = {
    cmdtype:"httpreq",
    httpreq:"newroom",
    userid:22,
    gameid:111,
    same_ip_exclude:1,
    near_gps_exclude:0,
    round_num:8,
    fee_stuff_id:11,
    fee_amount_per_player:1,
    fee_creator_pay_all:0,
    stake_stuff_id:11,
    stake_base_score:5

}

var myJSONObject = {"key1":"value1", "key2":"value2"};

request({
    url: "http://0.0.0.0:8081/service",
    method: "POST",
    json: true,   // <--Very important!!!
    body: newUserReq,
}, function (error, response, body){
    console.log(response);
    console.log("body");
    console.log(body);
});

// request('http://0.0.0.0:8081/test', function(error, response, body){
// 	console.log('error:',error);
// 	console.log('statusCode:', response && response.statusCode);
// 	console.log('body:', body);
// });

// request.post('http://0.0.0.0:8081/believe', {form:{"name":'value'}});