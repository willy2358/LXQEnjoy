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
    
    var sockPlayer : SockClient?
    private init(){
        
    }
    
    class func getSockClient() -> SockClient? {
        let inst = NetworkProxy.sharedInst
        if nil == inst.sockPlayer{
            let serverIP = AppConfig.sockServerIP
            let port = AppConfig.sockServerPort
            let sockPlayer = SockClient(serverIP: serverIP, serverPort: port)
            
            if sockPlayer.connect(
                successCallBack: {() -> Void in inst.sockPlayer = sockPlayer },
                failCallBack: { (m) ->Void in  }){
                inst.sockPlayer = sockPlayer
            }
        }
        return inst.sockPlayer
    }
}
