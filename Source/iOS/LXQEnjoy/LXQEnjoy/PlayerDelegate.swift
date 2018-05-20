//
//  PlayerDelegate.swift
//  LXQEnjoy
//
//  Created by willy2358 on 2018/5/19.
//  Copyright © 2018年 metalight. All rights reserved.
//

import Foundation

protocol PlayerDelegate{
    func processServerSuccessResponse(respCmd:String, result_data: String, data: String)
    func processServerFailResponse(reqCmd:String, errCode:UInt, errMsg:String)
    func processServerPush(pushCmd:String, cmdJsonStr: String)
    
    func onPlayerConnectStateChanged(oldState:client_status, newState:client_status)
}