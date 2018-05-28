//
//  GameEntryViewController.swift
//  LXQEnjoy
//
//  Created by willy2358 on 2018/4/21.
//  Copyright © 2018年 metalight. All rights reserved.
//

import UIKit

import SwiftyJSON

class GameEntryViewController: UIViewController, SockClientDelegate{
    func onPlayerExedCmd(player: PlayerInfo, cmd: String, cmdParam: [Int32]) {
        print("onPlayerExedCmd")
    }
    
//    func processServerSuccessResponse(respCmd: String, jsonObj: JSON) {
//        
//    }
//    
//    func processServerFailResponse(reqCmd: String, errCode: UInt, errMsg: String) {
//        
//    }
//    
//    func processServerPush(pushCmd: String, jsonObj: JSON) {
//        
//    }
    
    func onCardsState(cardsUserId: UInt32, activeCards: [UInt8], freezedCards: [UInt8], publicShownCards: [[UInt8]]) {
        print("onCardsState")
    }
    
    func onPlayersStateChanged(players: [PlayerInfo]) {
        print("onPlayersStateChanged")
    }
    
    func onNewBanker(bankPlayer: PlayerInfo) {
        print("onNewBanker")
    }
    
    func onDealCards(receivePlayer: PlayerInfo, cards:[UInt8]) {
        print("onDealCards")
    }
    
    func onGameStatusChanged(status: String, statusData: String) {
        print("onGameStatusChanged")
    }
    
    func onPlayerPlayCards(player: PlayerInfo, cards: [UInt8]) {
        print("onPlayerPlayCards")
    }
    
    func onCmdOptions(player: PlayerInfo, cmds: [CmdPush], timeoutSec: Int32, defaultCmd: CmdPush) {
        print("onCmdOptions")
    }
    

    

    var playerSockClient : SockClient?
    
    @IBAction func EnterRoom(_ sender: Any) {
        
        
//        test_push_cards_state()
//        test_push_game_players()
//        test_push_new_banker()
//        test_push_deal_cards()
//        test_push_play_cards()
//        test_push_cmd_opts()
//        test_push_exed_cmd()
//        return;

//        playerSockClient = SockClient(serverIP: AppConfig.sockServerIP, serverPort: AppConfig.sockServerPort)
//        playerSockClient?.playerDelegate = self
//        NetworkProxy.sockPlayer = playerSockClient
//        playerSockClient?.connect()
        
        
        let myStoryBoard = self.storyboard
        let mjTable = myStoryBoard?.instantiateViewController(withIdentifier: "MJTable")
        self.present(mjTable!, animated: true, completion: nil)


     
        
        
    }
    
    func test_push_cmd_opts() {
        let client = SockClient(serverIP: "testIP", serverPort: 34)
        client.playerDelegate = self
        let test_pack = """
        {"cmdtype": "sockpush", "sockpush": "cmd-opts", "cmd-opts": [{"cmd": "peng", "cmd-param": [31]}, {"cmd": "mo pai", "cmd-param": []}], "resp-timeout": -1, "def-cmd": {"cmd": "mo pai", "cmd-param": []}}
"""
        client.testServerPack(pack: test_pack)
        
    }
    
    func test_push_exed_cmd() {
        let client = SockClient(serverIP: "testIP", serverPort: 34)
        client.playerDelegate = self
        let test_pack = """
        {"cmdtype": "sockpush", "sockpush": "exed-cmd", "exed-cmd": "peng", "cmd-param": [31], "userid": 333}
"""
        client.testServerPack(pack: test_pack)
        
    }
    
    func test_push_play_cards() {
        let client = SockClient(serverIP: "testIP", serverPort: 34)
        client.playerDelegate = self
        let test_pack = """
        {"cmdtype": "sockpush", "sockpush": "play-cards", "userid": 222, "cards": [31], "player-state": "normal"}
"""
        client.testServerPack(pack: test_pack)
        
    }
    
    func test_push_new_banker()  {
        let client = SockClient(serverIP: "testIP", serverPort: 34)
        client.playerDelegate = self
        let test_pack = """
        {"cmdtype": "sockpush", "sockpush": "new-banker", "userid": 222}
"""
        client.testServerPack(pack: test_pack)
    }
    
    func test_push_deal_cards()  {
        let client = SockClient(serverIP: "testIP", serverPort: 34)
        client.playerDelegate = self
        let test_pack = """
        {"cmdtype": "sockpush", "sockpush": "deal-cards", "cards": [31, 24, 33, 39, 11, 38, 13, 15, 31, 24, 18, 37, 37]}
"""
        client.testServerPack(pack: test_pack)
    }
    
    
    func test_push_cards_state()  {
        let client = SockClient(serverIP: "testIP", serverPort: 34)
        client.playerDelegate = self
        let test_pack = """
        {"cmdtype": "sockpush", "sockpush": "cards-state", "userid": 333, "active-cards": [39, 11, 38, 13, 15, 24, 18, 37, 37, 14, 23], "frozen-cards": [31, 31, 31], "shown-cards-groups": [[31, 31, 31]]}
"""
        client.testServerPack(pack: test_pack)
    }
    
    func test_push_game_players()  {
        let client = SockClient(serverIP: "testIP", serverPort: 34)
        client.playerDelegate = self
        let test_pack = """
        {"cmdtype": "sockpush", "sockpush": "game-players", "players": [{"userid": 111, "seated": 1}, {"userid": 222, "seated": 1}, {"userid": 333, "seated": 0}]}
"""
        client.testServerPack(pack: test_pack)
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
    
//    func processServerPush(pushCmd: String, cmdJsonStr: String) {
//
//    }
//
//    func processServerFailResponse(reqCmd: String, errCode: UInt, errMsg: String) {
//
//    }
//
//    func processServerSuccessResponse(respCmd: String, result_data: String, data: String) {
//
//    }
    
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
