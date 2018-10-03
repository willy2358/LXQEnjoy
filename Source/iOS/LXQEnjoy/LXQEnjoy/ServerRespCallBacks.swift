//
//  ServerRespCallBacks.swift
//  LXQEnjoy
//
//  Created by willy2358 on 2018/5/20.
//  Copyright © 2018年 metalight. All rights reserved.
//

import Foundation

typealias OKCallBack = () -> Void
typealias FailCallBack = (_ errCode:Int, _ errMsg:String) -> Void

struct ServerRespCallBacks {
    var cmdName : String = ""
    
    var successCallBack : OKCallBack
    var failCallBack : FailCallBack
    
//    func init(cmdName : String) {
//        self.cmdName = cmdName
//    }
    
    
}
