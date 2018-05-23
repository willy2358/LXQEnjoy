//
//  SockPlayer.swift
//  LXQEnjoy
//
//  Created by willy2358 on 2018/5/18.
//  Copyright © 2018年 metalight. All rights reserved.
//

import Foundation

import SwiftyJSON

class SockClient : NSObject, GCDAsyncSocketDelegate {
    
    static let LXQ_PACKET_START : String = "LXQ<(:"
    static let LXQ_PACKET_END : String = ":)>QXL"

    var userId : Int! = 111
    let sockClient = GCDAsyncSocket()
    var serverIP : String!
    var serverPort : UInt16!
    
    var cmdCallbacks = Dictionary<String, ServerRespCallBacks>()
    var connectSuccessCB : (() -> Void)?
    var connectFailCB: ((String) -> Void)?
    
    
    var Status : client_status = client_status.not_connect
    
    var playerDelegate : SockClientDelegate?
    
    public init(serverIP: String, serverPort: UInt16) {
        self.serverIP = serverIP
        self.serverPort = serverPort
    }
    
    func enterRoom(roomId:String, gameId:UInt16, okCallBack : @escaping OKCallBack, failCallback: @escaping FailCallBack) -> Bool {
        let cmd = SockCmds.enter_room
        let packet = [
            "cmdtype":"sockreq",
            "sockreq":cmd,
            "userid":self.userId,
            
            "gameid":gameId,
            "roomid":roomId
        ] as [String:Any]
        
        updateCmdCallbacks(cmdName: cmd, okCallBack: okCallBack, failCallBack: failCallback)
        
        let jsonStr = convertDictionaryToString(dict: packet)
        let data = jsonStr.data(using: String.Encoding.utf8)!
        sockClient.write(data, withTimeout: -1, tag: 0)
        sockClient.readData(withTimeout: -1, tag: 0)
        return true
    }
    
    func joinGame(roomId:String, gameId:UInt16, seatNo:UInt16) {
        let cmd = SockCmds.join_game
        let packet = [
            "cmdtype":"sockreq",
            "sockreq":cmd,
            "userid":self.userId,
            "seatno":seatNo,
            "gameid":gameId,
            "roomid":roomId
            ] as [String:Any]
        
//        updateCmdCallbacks(cmdName: cmd, okCallBack: okCallBack, failCallBack: failCallback)
        
        let jsonStr = convertDictionaryToString(dict: packet)
        let data = jsonStr.data(using: String.Encoding.utf8)!
        sockClient.write(data, withTimeout: -1, tag: 0)
        sockClient.readData(withTimeout: -1, tag: 0)
    }
    
    func updateCmdCallbacks(cmdName:String, okCallBack:@escaping OKCallBack, failCallBack : @escaping FailCallBack) -> Void {
        if cmdCallbacks.keys.contains(cmdName){
            cmdCallbacks[cmdName]?.successCallBack = okCallBack
            cmdCallbacks[cmdName]?.failCallBack = failCallBack
        }
        else{
            let cbs = ServerRespCallBacks(cmdName: cmdName, successCallBack: okCallBack, failCallBack: failCallBack)
            cmdCallbacks[cmdName] = cbs
        }
    }
    
    func convertDictionaryToString(dict:[String:Any]) -> String {
        var result:String = ""
        do {
            //如果设置options为JSONSerialization.WritingOptions.prettyPrinted，则打印格式更好阅读
            let jsonData = try JSONSerialization.data(withJSONObject: dict, options: JSONSerialization.WritingOptions.init(rawValue: 0))
            
            if let JSONString = String(data: jsonData, encoding: String.Encoding.utf8) {
                result = JSONString
            }
            
        } catch {
            result = ""
        }
        return result
    }
    
    
    func connect(successCallBack: @escaping () -> Void, failCallBack: @escaping (String) -> Void) -> Bool {
        sockClient.delegate = self
        sockClient.delegateQueue = DispatchQueue.main
        self.connectSuccessCB = successCallBack
        self.connectFailCB = failCallBack
        
        do{
            try sockClient.connect(toHost: serverIP, onPort: self.serverPort)
            sockClient.readData(withTimeout: -1, tag: 0)
//          Status = client_status.connected
            return true
        }
        catch{
            print(error)
            Status = client_status.connect_failed
            if let cb = self.connectFailCB {
                cb(error.localizedDescription)
            }
//            self.connectFailCB!(error)
            
            return false
        }
    }
    
    
    func socket(_ sock: GCDAsyncSocket, didConnectToHost host: String, port: UInt16) -> Void {
        
        let oldStatus = self.Status
        self.Status = client_status.connected
        print("Connected to socket server")
        if let cb = self.connectSuccessCB{
            cb()
        }
        
        playerDelegate?.onPlayerConnectStateChanged(oldState: oldStatus, newState: self.Status)
        
//        let beat = ["c":"3"]
//        socketWriteDataToServer(body:beat)
        //        socketDidConnectCreatLogin()
        //        socketDidConnectBeginSendBeat()
    }
    
    //    func socketWriteDataToServer(body: Dictionary<String, Any>) {
    //        // 1: do   2: try?    3: try!
    //        guard let data:Data = try? Data(JSONSerialization.data(withJSONObject: body,
    //                                                               options: JSONSerialization.WritingOptions(rawValue: 1))) else { return }
    //        print(body)
    ////        clientSocket.write(data, withTimeout: -1, tag: 0)
    ////        clientSocket.readData(to: GCDAsyncSocket.crlfData(), withTimeout: -1, tag: 0)
    //    }
    
    func socketWriteDataToServer(body: Dictionary<String, Any>) {
        // 1: do   2: try?    3: try!
        guard let data:Data = try? Data(JSONSerialization.data(withJSONObject: body,
                                                               options: JSONSerialization.WritingOptions(rawValue: 1))) else { return }
        print(body)
        sockClient.write(data, withTimeout: -1, tag: 0)
        sockClient.readData(to: GCDAsyncSocket.crlfData(), withTimeout: -1, tag: 0)
    }
    
    func socket(_ sock: GCDAsyncSocket, didRead data: Data, withTag tag: Int) -> Void {

        let str =  String(data:data,encoding: String.Encoding.utf8)
        print("received:" + str!)
        guard var pack_text = str else{
            print("Invalid socket data")
            return;
        }
        print("------once read")
        
        if pack_text.contains(SockClient.LXQ_PACKET_START) && pack_text.contains(SockClient.LXQ_PACKET_END){
            let pattern :String = "LXQ<\\(:([\\w\\W]*?):\\)>QXL"
            
            guard let regex = try? NSRegularExpression(pattern: pattern, options: []) else {
                return
            }
            
            let results =  regex.matches(in: pack_text, options: [], range: NSRange(location: 0, length: pack_text.characters.count))
            
            print("entry count:" + String(results.count) )
            let nsText = pack_text as NSString
            for result in results {
                
                let resp = nsText.substring(with: result.range) as NSString
                let range = NSMakeRange(SockClient.LXQ_PACKET_START.count, result.range.length - 12)
                let cmd = resp.substring(with:range)
                print("server cmd:" + cmd)
                self.processServerCmd(respJson: cmd)
               
            }
            
        }
        sockClient.readData(withTimeout: -1, tag: 0)
    }
    
    func processCmdResponse(cmd:String, respJson:JSON) {
        
        if !cmdCallbacks.keys.contains(cmd){
            return
        }
        
        let result = respJson["result"].stringValue
        if result == "OK" && nil != cmdCallbacks[cmd]?.successCallBack{
            cmdCallbacks[cmd]?.successCallBack()
        }
        else{
            let errCode = respJson["errcode"].intValue
            let errMsg = respJson["errmsg"].stringValue
            cmdCallbacks[cmd]?.failCallBack(errCode, errMsg)
        }
    }
    
    func processServerCmd(respJson:String) {
       
        let jsonData = respJson.data(using : String.Encoding.utf8)
        var jsonObj : JSON?
        do{
            jsonObj = try JSON(data: jsonData!)
        }
        catch{
            
        }

        let cmdType = jsonObj?["cmdtype"].stringValue
        var cmd : String!
        if cmdType == "sockresp"{
            cmd = jsonObj?["sockresp"].stringValue
            
//            let result = jsonObj?["result"].stringValue
//            guard result! == "OK" else{
//                //ToDo show error popup
//                return
//            }
            if jsonObj?["result"].stringValue == "OK"{
                playerDelegate?.processServerSuccessResponse(respCmd: cmd, jsonObj: jsonObj!)
            }
            else {
                playerDelegate?.processServerFailResponse(reqCmd: cmd, errCode: (jsonObj?["errcode"].uInt)!, errMsg: (jsonObj?["errmsg"].stringValue)!)
            }
            
           
            processCmdResponse(cmd: cmd, respJson: jsonObj!)
        }
        else if cmdType == "sockpush"{
            cmd = jsonObj?["sockpush"].stringValue
          
            playerDelegate?.processServerPush(pushCmd: cmd, jsonObj: jsonObj!)
        }
    }
    
    func socket(_ sock: GCDAsyncSocket, didWriteDataWithTag tag: Int) -> Void {
        //        prin
        print("written")
    }
    
    // 断开连接
    func socketDidDisconnect(_ sock: GCDAsyncSocket, withError err: Error?) -> Void {
        //        socketDidDisconectBeginSendReconnect()
        print("disconnected")
    }
    
    
}
