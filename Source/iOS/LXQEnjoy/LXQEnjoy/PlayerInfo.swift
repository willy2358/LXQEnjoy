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
    var userid : UInt?
    var seated : UInt8?  //1, seated; 0: unseated
 
    public init(){
        
    }
    
    class func getPlayerByUserid(userid:UInt) -> PlayerInfo?{
        let player = PlayerInfo()
        return player
    }
    
    class func getMyPlayer() -> PlayerInfo? {
        return PlayerInfo()
    }
}
