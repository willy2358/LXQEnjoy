//
//  AppConfig.swift
//  LXQEnjoy
//
//  Created by willy2358 on 2018/5/18.
//  Copyright © 2018年 metalight. All rights reserved.
//

import Foundation

class AppConfig{
    
    class var httpServerUrl:String{
        return "http://127.0.0.1:8080"
    }
    
    class var sockServerIP :String{
        return "127.0.0.1"
    }
    
    class var sockServerPort : UInt16{
        return 9229
    }
}
