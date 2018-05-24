//
//  GameEntryViewController.swift
//  LXQEnjoy
//
//  Created by willy2358 on 2018/4/21.
//  Copyright © 2018年 metalight. All rights reserved.
//

import UIKit

import SwiftyJSON

class GameEntryViewController: UIViewController{
    func processServerSuccessResponse(respCmd: String, jsonObj: JSON) {
        
    }
    
    func processServerPush(pushCmd: String, jsonObj: JSON) {
        
    }
    

    var playerSockClient : SockClient?
    
    @IBAction func EnterRoom(_ sender: Any) {
        

//        playerSockClient = SockClient(serverIP: AppConfig.sockServerIP, serverPort: AppConfig.sockServerPort)
//        playerSockClient?.playerDelegate = self
//        NetworkProxy.sockPlayer = playerSockClient
//        playerSockClient?.connect()
        
        
        let myStoryBoard = self.storyboard
        let mjTable = myStoryBoard?.instantiateViewController(withIdentifier: "MJTable")
        self.present(mjTable!, animated: true, completion: nil)
        
//
     
        
        
    }
    
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        
        // Do any additional setup after loading the view.
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    

    /*
    // MARK: - Navigation

    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        // Get the new view controller using segue.destinationViewController.
        // Pass the selected object to the new view controller.
    }
    */
    
    func processServerPush(pushCmd: String, cmdJsonStr: String) {
        
    }
    
    func processServerFailResponse(reqCmd: String, errCode: UInt, errMsg: String) {
        
    }
    
    func processServerSuccessResponse(respCmd: String, result_data: String, data: String) {
        
    }
    
//    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
//        if segue.identifier == "MJTable"{
//            let roomVC = segue.destination as! MahongTableViewController
//            roomVC.setSockPlayer(player: self.player!)
//        }
//    }
    
    func onPlayerConnectStateChanged(oldState: client_status, newState: client_status) {
        if newState == client_status.connected{
            playerSockClient?.enterRoom(roomId: "LX888", gameId: 111,
               okCallBack: {
                    let myStoryBoard = self.storyboard
                
                
                    let mjTable = myStoryBoard?.instantiateViewController(withIdentifier: "MJTable")
                
                
                    self.present(mjTable!, animated: true, completion: nil)
                },
                failCallback: {errCode,errMsg in
                    let alertView = UIAlertView()
                    
                    alertView.title = "提示"
                    
                    alertView.message = "你好，我是007"
                    
                    alertView.addButton(withTitle: "点击我")
                    
//                    NSTimer.scheduledTimerWithTimeInterval(1, target:self, selector:"dismiss:", userInfo:alertView!, repeats:false)
                    
                    alertView.show()
                })
        }
        
        
    }
    

}
