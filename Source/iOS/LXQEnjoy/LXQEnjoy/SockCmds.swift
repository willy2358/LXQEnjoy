//
//  SockCmds.swift
//  LXQEnjoy
//
//  Created by willy2358 on 2018/5/20.
//  Copyright © 2018年 metalight. All rights reserved.
//

import Foundation

class SockCmds{
    static let enter_room = "enter-room"
    
    static let leave_room = "leave-room"
    
    static let join_game = "join-game"
    
    static let leave_game = "leave-game"
    
    static let push_game_players = "game-players"
    
    static let push_deal_cards = "deal-cards"
    
    static let push_cards_state = "cards-state"
    
    static let push_new_banker = "new-banker"
    
    static let param_cards = "cards"
    
    static let pack_part_cmd_type = "cmdtype"
    static let pack_part_push = "sockpush"
    static let pack_part_resp = "sockresp"
    static let pack_part_result = "result"
    static let result_ok = "OK"
    static let result_error = "ERROR"
    static let error_code = "errcode"
    static let error_msg = "errmsg"
    static let userid = "userid"
    static let card_state_active_cards = "active-cards"
    static let card_state_frozen_cards = "frozen-cards"
    static let card_state_shown_cards = "shown-cards-groups"
    static let game_players = "players"
    static let game_player_seated = "seated"
    
    
}



