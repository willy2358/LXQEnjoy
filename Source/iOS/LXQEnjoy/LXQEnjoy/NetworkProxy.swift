//
//  NetworkProxy.swift
//  LXQEnjoy
//
//  Created by willy2358 on 2018/5/18.
//  Copyright © 2018年 metalight. All rights reserved.
//

import Foundation

class NetworkProxy{
    
    static let sharedInst = NetworkProxy.init()
    
    static var sockPlayer : SockPlayer?
    private init(){
        
    }
    
//    class func getSockPlayer() -> SockPlayer? {
//        let inst = NetworkProxy.sharedInst
//        if nil == inst.sockPlayer{
//            let serverIP = AppConfig.sockServerIP
//            let port = AppConfig.sockServerPort
//            let sockPlayer = SockPlayer(serverIP: serverIP, serverPort: port)
//            if sockPlayer.connect(){
//                inst.sockPlayer = sockPlayer
//            }
//        }
//        return inst.sockPlayer
//    }
}
