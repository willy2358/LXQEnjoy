//
//  PlayerInfo.swift
//  LXQEnjoy
//
//  Created by willy2358 on 2018/5/23.
//  Copyright © 2018年 metalight. All rights reserved.
//

import Foundation

class PlayerInfo{
    var alias : String?
    var userid : UInt
    var seatid : UInt8?  //1, seated; 0: unseated
    var roomId : String = ""
    var gameId : UInt8 = 0
 
    public init(userid: UInt){
        self.userid = userid
    }
    
    class func getPlayerByUserid(userid:UInt) -> PlayerInfo?{
        let player = PlayerInfo(userid: userid)
        return player
    }
    
    class func getMyPlayer() -> PlayerInfo? {
        return PlayerInfo(userid: 111)
    }
}
