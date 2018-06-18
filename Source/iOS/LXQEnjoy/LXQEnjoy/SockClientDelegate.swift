//
//  PlayerDelegate.swift
//  LXQEnjoy
//
//  Created by willy2358 on 2018/5/19.
//  Copyright © 2018年 metalight. All rights reserved.
//

import Foundation

import SwiftyJSON

protocol SockClientDelegate{
//    func processServerSuccessResponse(respCmd:String, jsonObj:JSON)
//    func processServerFailResponse(reqCmd:String, errCode:UInt, errMsg:String)
//    func processServerPush(pushCmd:String, jsonObj:JSON)
    
    func onPlayerConnectStateChanged(oldState:client_status, newState:client_status)
    
    func onCardsState(cardsUserId: UInt32, activeCards:[UInt8], freezedCards:[UInt8], publicShownCards:[[UInt8]], private_cards_count : Int8)
    func onPlayersStateChanged(players: [PlayerInfo])
    func onNewBanker(bankPlayer: PlayerInfo)
    func onDealCards(receivePlayer:PlayerInfo, cards:[UInt8])
    func onGameStatusChanged(status:String, statusData:String)
    func onPlayerPlayCards(player: PlayerInfo, cards:[UInt8])
    func onCmdOptions(player:PlayerInfo, cmds: [CmdPush], timeoutSec: Int32, defaultCmd: CmdPush)
    func onPlayerExedCmd(player:PlayerInfo, cmd:String, cmdParam:[Int32]?)
    func onGameRoundEnded(winners: [PlayerInfo], losers:[PlayerInfo]) -> Void
    func onUpdateScores(players:[PlayerInfo])
    
}
