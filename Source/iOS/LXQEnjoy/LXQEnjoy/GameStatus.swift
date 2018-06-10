//
//  GameStatus.swift
//  LXQEnjoy
//
//  Created by willy2358 on 2018/6/10.
//  Copyright © 2018年 metalight. All rights reserved.
//

import Foundation

let gGameStatus = GameStatus()


class GameStatus {
    
    public init(){
        
    }
    
    var roomPlayers = NSMutableArray()
    
    public func getRoomPlayers() -> NSArray {
        return roomPlayers
    }
    
    public func addRoomPlayer(player: PlayerInfo) -> Void{
        roomPlayers.add(player)
    }
    
    public func removeRoomPlayer(player : PlayerInfo) -> Void{
        if roomPlayers.contains(player){
            roomPlayers.remove(player)
        }
    }
}
