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
    var seatid : Int8? = 0
    var roomId : String = ""
    var gameId : UInt8 = 0
    var roundScore : Int32 = 0 // >0 gained score in one round , <0 lost score
    var totalScore : Int32 = 0
    var profileImg : String?
 
    public init(userid: UInt){
        self.userid = userid
    }
    
    public func setRoundGainScore(score: Int32) -> Void{
        self.roundScore = score
    }
    
    public func getRoundGainScore() -> Int32{
        return self.roundScore
    }
    
    public func getTotalScore() -> Int32{
        return self.totalScore
    }
    
    public func getMyProfileImgPath() -> String{
        guard let img = profileImg else{
            
            return "profile" + String(Int.random(lower: 1, 4))
        }
        
        return img
    }
    
    //all scores are controlled in server 
    public func updateTotalScore(newTotalScore: Int32) -> Void{
        self.totalScore = newTotalScore
    }
    
    class func getPlayerByUserid(userid:UInt) -> PlayerInfo?{
        let player = PlayerInfo(userid: userid)
        return player
    }
    
    class func getMyPlayer() -> PlayerInfo? {
        return PlayerInfo(userid: 111)
    }
}
