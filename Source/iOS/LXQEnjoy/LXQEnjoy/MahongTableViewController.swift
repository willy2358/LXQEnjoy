//
//  MahongTableViewController.swift
//  LXQEnjoy
//
//  Created by willy2358 on 2018/5/14.
//  Copyright © 2018年 metalight. All rights reserved.
//

import UIKit
import SnapKit
import SwiftyJSON

import SDWebImage

class MahongTableViewController: UIViewController, SockClientDelegate{
    
//    var cardsInHand: NSMutableArray = NSMutableArray()
    func onCardsState(cardsUserId: UInt32, activeCards: [UInt8], freezedCards: [UInt8], publicShownCards: [[UInt8]]) {
        
    }
    
    func onPlayersStateChanged(players: [PlayerInfo]) {
        
    }
    
    func onNewBanker(bankPlayer: PlayerInfo) {
        
    }
    
    func onDealCards(receivePlayer: PlayerInfo, cards: [UInt8]) {
        for c in cards{
            let btn = UIButton()
            let img = UIImage(named: String(c))
            btn.tag = Int(c)
            btn.addTarget(self, action:#selector(playCardBtnClicked(_:)), for:.touchUpInside)
            btn.setBackgroundImage(img, for: UIControlState.normal)
            self.cardsInHand.add(btn)
        }
        
        for s in cardsPanel.subviews{
            s.removeFromSuperview()
        }
        
        horzStackSubviews(panel: cardsPanel, subviews: cardsInHand, panelSize:cardsPanelSize)
    }
    
    func onGameStatusChanged(status: String, statusData: String) {
        
    }
    
    func onPlayerPlayCards(player: PlayerInfo, cards: [UInt8]) {
        var cardBtns = [UIButton]()
        for c in cards{
            for cb in self.cardsPanel.subviews{
                if cb.tag == c && !cardBtns.contains(cb as! UIButton){
                    cardBtns.append(cb as! UIButton)
                }
            }
        }
        
        for cb in cardBtns{
            cardsPanel.willRemoveSubview(cb)
            
            self.cardsInHand.remove(cb)
        }
    }
    

    
    
    func onCmdOptions(player: PlayerInfo, cmds: [CmdPush], timeoutSec: Int32, defaultCmd: CmdPush) {
        let cmdBtns = NSMutableArray()
        self.cmdBtns.removeAll()
        for c in cmds{
            
            let btn = UIButton()
            btn.setTitle(c.cmdText, for: UIControlState.normal)
            btn.backgroundColor = UIColor.blue
            self.cmdBtns[btn] = c
            btn.addTarget(self, action:#selector(cmdBtnClicked(_:)), for:.touchUpInside)
            cmdBtns.add(btn)
            centerSubviews(container: self.cmdsPanel, subViews: cmdBtns, subViewWidth: CGFloat(80), space: CGFloat(20))
        }
    }
    
    func onPlayerExedCmd(player: PlayerInfo, cmd: String, cmdParam: [Int32]) {
        let txt = "\(player.userid ?? 000) : \(cmd)"
        self.cmdExedPanel.text = txt
    }
    
    func updateRoomPlayers(players: [PlayerInfo]) {
        
    }
    
    
    var cardsPanelSize : CGSize!
    let cardsInHand : NSMutableArray = NSMutableArray()
    var cardsPanel : UIView!
    var sockPlayer : SockClient!
    var cmdsPanel :UIView!
    var cmdExedPanel : UILabel!
    
    var cmdBtns = [UIButton : CmdPush]()
    
    func processServerSuccessResponse(respCmd: String, jsonObj: JSON) {
        
    }
    
    public func setSockPlayer(player:SockClient) {
        self.sockPlayer = player
        
    }
    
//    func processServerPush(pushCmd: String, jsonObj: JSON) {
//        if pushCmd == SockCmds.push_deal_cards{
//            let cards = jsonObj[SockCmds.cards].arrayValue
//            let newCards = NSMutableArray()
//            for c in cards{
//
//                let btn = UIButton()
//                let img = UIImage(named: String(c.intValue))
//                btn.setBackgroundImage(img, for: UIControlState.normal)
//                newCards.add(btn)
//            }
//            horzStackSubviews(panel: cardsPanel, subviews: newCards, panelSize:cardsPanelSize)
//        }
//    }
    
    func onPlayerConnectStateChanged(oldState: client_status, newState: client_status) {
        
    }
    

    fileprivate func createCardsPanel() {
        let rect = self.view.frame
        let yStart = rect.height * CGFloat(2.0 / 3.0)
        let myAreaHeight = rect.height - yStart
        let myProfileWidth = myAreaHeight
        let space = CGFloat(10)
        let xStart = myProfileWidth + space
        
        
        let cardsPanelWidth = rect.width - myProfileWidth - 2.0 * space
        let cardsPanelHeight = myAreaHeight * CGFloat(0.5)
        
        cardsPanelSize = CGSize(width: cardsPanelWidth, height: cardsPanelHeight)
        let rectPanel = CGRect(origin: CGPoint(x:xStart, y:yStart), size:cardsPanelSize )
        cardsPanel = UIView(frame:rectPanel)
        cardsPanel.backgroundColor = UIColor.yellow
        self.view.addSubview(cardsPanel)
    }
    
    func createOptCmdsPanel() {
        
        cmdsPanel = UIView()
        cmdsPanel.backgroundColor = UIColor.darkGray
        self.view.addSubview(cmdsPanel)
        
        cmdsPanel.snp.makeConstraints{
            (make) -> Void in
            make.height.equalTo(30)
            make.width.equalTo(self.view).multipliedBy(0.5)
            make.bottom.equalTo(cardsPanel.snp.top).offset(-10)
            make.centerX.equalTo(self.view)
        }
    }
    
    func createPlayersPanel() {
        
       let stack = UIStackView()
        stack.axis = UILayoutConstraintAxis.horizontal
        stack.backgroundColor = UIColor.blue
        self.view.addSubview(stack)
        stack.snp.makeConstraints{
            (make) -> Void in
            make.height.equalTo(50)
            make.width.equalTo(self.view).multipliedBy(0.3)
            make.left.equalTo(self.view.snp.left).multipliedBy(0.6)
            make.right.equalTo(self.view)
        }
        stack.spacing = 2
        stack.distribution = UIStackViewDistribution.fillEqually
    
        
        let img = UIImageView()
        img.sd_setImage(with: URL(string: "https://ss0.bdstatic.com/5aV1bjqh_Q23odCf/static/superman/img/logo_top_ca79a146.png"), placeholderImage: UIImage(named: "placeholder.png"))
        stack.addArrangedSubview(img)
        
        let img2 = UIImageView(image: UIImage(named: "profile2"))
        stack.addArrangedSubview(img2)
        
        let img3 = UIImageView(image: UIImage(named: "profile3"))
        stack.addArrangedSubview(img3)
      
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()

        createSeatButtons()
        
        createCardsPanel()

        createOptCmdsPanel()
        
        createPlayerExecutionPanel()
        
        createPlayersPanel()
        
        
        // Do any additional setup after loading the view.
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    func createPlayerExecutionPanel() {
        cmdExedPanel = UILabel()
        self.view.addSubview(cmdExedPanel)
        
        cmdExedPanel.snp.makeConstraints{
            (make) -> Void in
            make.width.equalTo(200.0)
            make.height.equalTo(50.0)
            make.centerX.equalTo(self.view)
            make.centerY.equalTo(self.view)
        }
        
    }
    
    func createSeatButtons() {
        let tableRect = self.view.frame
        let horzSpan = CGFloat(80.0)
        let vertSpan = CGFloat(50.0)
        let btnWidth = 80.0
        let btnHeight = 30.0
        let btnSize = CGSize(width: 80.0, height: 30.0)
        let x = (tableRect.width - btnSize.width)/2.0
        let y = (tableRect.height - btnSize.height)/2.0
        
        let btn1 = UIButton()
        btn1.setTitle(StringRes.Join_game, for: UIControlState.normal)
        btn1.tag = 1
        btn1.addTarget(self, action:#selector(sitDownTabed(_:)), for:.touchUpInside)
        self.view.addSubview(btn1)
        btn1.snp.makeConstraints{(make) -> Void in
            make.top.equalTo(self.view).offset(vertSpan)
            make.left.equalTo(self.view).offset(x)
            make.width.equalTo(btnWidth)
            make.height.equalTo(btnHeight)
        }
        
        let btn2 = UIButton()
        btn2.tag = 2
        btn2.addTarget(self, action:#selector(sitDownTabed(_:)), for:.touchUpInside)
        btn2.setTitle(StringRes.Join_game, for: UIControlState.normal)
        self.view.addSubview(btn2)
        btn2.snp.makeConstraints{ (make) -> Void in
            make.bottom.equalTo(self.view).offset(-vertSpan)
            make.left.equalTo(self.view).offset(x)
            make.width.equalTo(btnWidth)
            make.height.equalTo(btnHeight)
        }
        
        let btn3 = UIButton()
        btn3.tag = 3
        btn3.setTitle(StringRes.Join_game, for: UIControlState.normal)
        btn3.addTarget(self, action:#selector(sitDownTabed(_:)), for:.touchUpInside)
        self.view.addSubview(btn3)
        btn3.snp.makeConstraints{(make) -> Void in
            make.left.equalTo(self.view).offset(horzSpan)
            make.top.equalTo(self.view).offset(y)
            make.width.equalTo(btnWidth)
            make.height.equalTo(btnHeight)
        }
        
        let btn4 = UIButton()
        btn4.tag = 4
        btn4.setTitle(StringRes.Join_game, for: UIControlState.normal)
        btn4.addTarget(self, action:#selector(sitDownTabed(_:)), for:.touchUpInside)
        self.view.addSubview(btn4)
        btn4.snp.makeConstraints{(make) -> Void in
            make.right.equalTo(self.view).offset(-horzSpan)
            make.top.equalTo(self.view).offset(y)
            make.width.equalTo(btnWidth)
            make.height.equalTo(btnHeight)
        }
    
    }
    
    @objc func sitDownTabed(_ button:UIButton){
        let seatNo = button.tag
//        sockPlayer = NetworkProxy.sockPlayer
//        sockPlayer.playerDelegate = self
//        sockPlayer.joinGame(roomId: "LX888", gameId: 111, seatNo: UInt16(seatNo))
//        test_push_cmd_opts()
//        test_push_exed_cmd()
//        test_push_deal_cards()
        guard let playerClient = NetworkProxy.getSockClient() else{
            return
        }
        
        playerClient.playerDelegate = self
        
        playerClient.joinGame(seatNo: UInt16(seatNo),
                              okCallBack: { }) { (_, _) in
            
        }
    }
    
    @objc func cmdBtnClicked(_ button: UIButton) {
        let cmd = self.cmdBtns[button]
        let client = SockClient(serverIP: "testIP", serverPort: 34)
        client.executeCmd(cmdText: (cmd?.cmdText)!, cmdParam: (cmd?.cmdParams)!,
                          okCallBack: {}, failCallback: {_,_ in })
        
    }
    
    @objc func playCardBtnClicked(_ button: UIButton) {
        let card = button.tag
        let cards = [UInt8(card)]

        guard let playerClient = NetworkProxy.getSockClient() else{
            return
        }
        
        playerClient.playCards(cards: cards, okCallBack:{}, failCallback: {_,_ in })
        button.removeFromSuperview()
        self.cardsInHand.remove(button)
    }
    
    func horzStackSubviews(panel:UIView, subviews:NSMutableArray, panelSize:CGSize) -> Void {
        
        let vCount = subviews.count
        let bestRatio:CGFloat = 0.618
        let bestSubviewWidth = bestRatio * panelSize.height
        let viewsWidthSum:CGFloat = CGFloat(vCount) * bestSubviewWidth
        if viewsWidthSum < panelSize.width{
            self.centerSubviews(container: panel, subViews: subviews, containerSize: panelSize, space: 0.0)
        }
        else{
            self.overlapSubviews(container: panel, subViews: subviews, containerSize: panelSize, subViewWidth: bestSubviewWidth)
            
        }
        
    }
    
    func overlapSubviews(container:UIView, subViews:NSMutableArray, containerSize:CGSize, subViewWidth:CGFloat) -> Void {
        let overlapWidth = (containerSize.width - subViewWidth)/CGFloat(subViews.count - 1)
        
        var offset : CGFloat = 0
        for i in 0..<subViews.count{
            let subView = subViews[i] as! UIView
            if !container.subviews.contains(subView){
                container.addSubview(subView)
            }
            
            offset = CGFloat(i) * overlapWidth
            subView.snp.makeConstraints{(make) -> Void in
                make.top.equalTo(container)
                make.left.equalTo(container).offset(offset)
                make.width.equalTo(subViewWidth)
                make.height.equalTo(container)
            }
        }
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
    
    func test_push_deal_cards()  {
        let client = SockClient(serverIP: "testIP", serverPort: 34)
        client.playerDelegate = self
        let test_pack = """
        {"cmdtype": "sockpush", "sockpush": "deal-cards", "cards": [31, 24, 33, 39, 11, 38, 13, 15, 31, 24, 18, 37, 37]}
"""
        client.testServerPack(pack: test_pack)
    }
    
    func centerSubviews(container:UIView, subViews:NSMutableArray, containerSize:CGSize, space:CGFloat = 0) -> Void {
        
        let bestRatio:CGFloat = 0.618
        let bestSubviewWidth = bestRatio * containerSize.height
        let viewsWidthSum:CGFloat = CGFloat(subViews.count) * bestSubviewWidth + CGFloat(subViews.count - 1) * space
        let offsetStart = (containerSize.width - viewsWidthSum)/2
        
        for i in 0..<subViews.count{
            let subView = subViews[i] as! UIView
            if !container.subviews.contains(subView ){
                container.addSubview(subView )
            }

            subView.snp.makeConstraints { (make) -> Void in
                make.top.equalTo(container)
                make.left.equalTo(container).offset(offsetStart + CGFloat(i) * (bestSubviewWidth + space))
                make.width.equalTo(bestSubviewWidth)
                make.height.equalTo(containerSize.height)

            }
        }
    }
    
    
    func centerSubviews(container:UIView, subViews:NSMutableArray, subViewWidth:CGFloat, space:CGFloat = 0) -> Void {
        
//        let bestRatio:CGFloat = 0.618
//        let bestSubviewWidth = bestRatio * containerSize.height
        let containerSize = container.frame.size;
        let viewsWidthSum:CGFloat = CGFloat(subViews.count) * subViewWidth + CGFloat(subViews.count - 1) * space
        let offsetStart = (containerSize.width - viewsWidthSum)/2
        
        for i in 0..<subViews.count{
            let subView = subViews[i] as! UIView
            if !container.subviews.contains(subView ){
                container.addSubview(subView )
            }
            
            subView.snp.makeConstraints { (make) -> Void in
                make.top.equalTo(container)
                make.left.equalTo(container).offset(offsetStart + CGFloat(i) * (subViewWidth + space))
                make.width.equalTo(subViewWidth)
                make.height.equalTo(containerSize.height)
                
            }
        }
    }
    

    
    func processServerFailResponse(reqCmd: String, errCode: UInt, errMsg: String) {
    
    }
    

    /*
    // MARK: - Navigation

    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        // Get the new view controller using segue.destinationViewController.
        // Pass the selected object to the new view controller.
    }
    */

}
