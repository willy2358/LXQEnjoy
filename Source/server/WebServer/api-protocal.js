'use strict'


exports = module.exports = Object.freeze({

    cmd_type : "cmdtype",
    cmd_type_httpreq : "httpreq",
    cmd_type_httpresp: "httpresp",
    cmd_resp_result: "result",
    cmd_resp_OK: "OK",
    cmd_resp_ERROR: "ERROR",
    cmd_resp_error_msg: "errmsg",
    req_cmd_newuser : "newuser",
    req_cmd_login:"login",
    req_cmd_set_pwd:"set-pwd",
    req_cmd_add_dev: "add-dev",
    req_cmd_get_games: "getgames",
    req_cmd_new_room: "newroom",
    req_param_devid: "devid",
    req_param_pwd: "password",
    req_userid:"userid",
    req_room_same_ip_exclude:"same_ip_exclude",
    req_room_same_gps_exclude:"near_gps_exclude",
    req_room_game_round_num :"round_num",
    req_room_game_fee_stuff_id:"fee_stuff_id",
    req_room_game_fee_per_player:"fee_amount_per_player",
    req_room_game_fee_creator_pay_all:"fee_creator_pay_all",
    req_room_game_stake_stuff_id: "stake_stuff_id",
    req_room_game_stake_base_score:"stake_base_score",


    game_id: "gameid",
    game_name: "gamename",
    game_min_players:"min_players",
    game_max_players: "max_players",
    game_type:"gametype",
    get_error_packet: function (err_code) {
        return "";

    },


});