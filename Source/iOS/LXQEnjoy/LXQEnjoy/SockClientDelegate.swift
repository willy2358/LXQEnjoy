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
    func processServerSuccessResponse(respCmd:String, jsonObj:JSON)
    func processServerFailResponse(reqCmd:String, errCode:UInt, errMsg:String)
    func processServerPush(pushCmd:String, jsonObj:JSON)
    
    func onPlayerConnectStateChanged(oldState:client_status, newState:client_status)
}
