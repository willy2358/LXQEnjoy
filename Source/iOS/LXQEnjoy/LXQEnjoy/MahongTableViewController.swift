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
    func onGameRoundEnded(winners: [PlayerInfo], losers: [PlayerInfo]) {
        printLog("onGameRoundEnded")
    }
    
    func onUpdateScores(players: [PlayerInfo]) {
        printLog("onUpdateScores")
    }
    
    
    func onCardsState(cardsUserId userid: UInt32, activeCards aCards: [UInt8], freezedCards fCards: [UInt8], publicShownCards sCards: [[UInt8]], private_cards_count pcc : Int8) {
        
        
        guard let r = self.getPlayerRegion(playerId: UInt(userid)) else{ return}
        r.UpdateCardsState(activeCards: aCards, freezedCards: fCards, publicShownCards: sCards, private_cards_count: pcc)
    }
    
    func onPlayersStateChanged(players: [PlayerInfo]) {
//        let log = "player status:"
        self.updateRoomPlayers(players: players)
    }
    
    func onNewBanker(bankPlayer: PlayerInfo) {
        if PlayerInfo.getMyPlayer()?.userid == bankPlayer.userid{
            canPlayCard = true
        }
        
        let txt = "banker: \(bankPlayer.userid )"
        self.cmdExedPanel.text = txt
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
        
        HorzStackSubviews(panel: cardsPanel, subviews: cardsInHand, panelSize:cardsPanelSize)
    }
    
    func onGameStatusChanged(status: String, statusData: String) {
        let log = "status: \(status), data:\(statusData)"
        print(log)
        
        if status == SockCmds.game_status_new_round{
            self.beginNewRound()
        }
    }
    
    func onPlayerPlayCards(player: PlayerInfo, cards: [UInt8]) {
//        var cardBtns = [UIButton]()
//        for c in cards{
//            for cb in self.cardsPanel.subviews{
//                if cb.tag == c && !cardBtns.contains(cb as! UIButton){
//                    cardBtns.append(cb as! UIButton)
//                }
//            }
//        }
//
//        for cb in cardBtns{
//            cardsPanel.willRemoveSubview(cb)
//
//            self.cardsInHand.remove(cb)
//        }
        let txt = "p: \(player.userid ), cards:\(cards)"
        self.cmdExedPanel.text = txt
    }
    
    
    func beginNewRound() -> Void {
        for s in cardsPanel.subviews{
            s.removeFromSuperview()
        }
        
        self.cardsInHand.removeAllObjects()
        
    }
    
    
    func onCmdOptions(player: PlayerInfo, cmds: [CmdPush], timeoutSec: Int32, defaultCmd: CmdPush) {
        
        for (k,_) in self.cmdBtns {
            k.removeFromSuperview()
        }
        self.cmdBtns.removeAll()
        
        for c in cmds{
            if c.cmdText == SockCmds.push_play_cards{
                self.canPlayCard = true
            }
            else {
                let btn = UIButton()
                btn.setTitle(c.cmdText, for: UIControlState.normal)
                btn.backgroundColor = UIColor.blue
                self.cmdBtns[btn] = c
                btn.addTarget(self, action:#selector(cmdBtnClicked(_:)), for:.touchUpInside)
            }
        }
        let cmds = NSMutableArray()
        for (k, _) in self.cmdBtns{
            cmds.add(k)
        }
        
        HorzCenterSubviews(container: self.cmdsPanel, subViews: cmds, subViewWidth: CGFloat(80), space: CGFloat(20))
    }
    
    func onPlayerExedCmd(player: PlayerInfo, cmd: String, cmdParam: [Int32]?) {
        let txt = "\(player.userid ) : \(cmd)"
        self.cmdExedPanel.text = txt
    }
    
    func updateRoomPlayers(players: [PlayerInfo]) {
        for (_, m) in self.players{
            m.ProfileImg.isHidden = true
        }
        
        for p in players{
            if let sid = p.seatid, sid > 0{
                let usid = UInt8(sid)
                self.players[usid]?.ProfileImg.isHidden = false
                self.players[usid]?.Player = p
//                self.playersProfile[usid]?.isHidden = false
                let imgPath = p.getMyProfileImgPath()
                if imgPath.starts(with: "http"){
                    self.players[usid]?.ProfileImg.sd_setImage(with: URL(string: imgPath), placeholderImage: UIImage(named: "userprofile.png"))
                }
                else{
                    self.players[usid]?.ProfileImg.image = UIImage(named: imgPath)
                }
            }
        }
    }
    
    
    var cardsPanelSize : CGSize!
    let cardsInHand : NSMutableArray = NSMutableArray()
    var cardsPanel : UIView!
    var sockPlayer : SockClient!
    var cmdsPanel :UIView!
    var cmdExedPanel : UILabel!
    var canPlayCard : Bool = false
    var center_img : UIImageView!
    let const_table_center_size  = 100
    
    var imgNorthPlayer : UIImageView!
    var imgSouthPlayer : UIImageView!
    var imgEastPlayer :UIImageView!
    var img2 :UIImageView!
    var cmdBtns = [UIButton : CmdPush]()
    
    var playersProfile  = [UInt8 : UIImageView]() //seatid : profile
    
    //seats order:        1
    //                 4     2
    //                    3
    var players = [UInt8 : PlayerRegion]()
    
    func processServerSuccessResponse(respCmd: String, jsonObj: JSON) {
        
    }
    
    private func getPlayerRegion(playerId: UInt) -> PlayerRegion?{
        for (_, r) in players{
            if let p = r.Player, p.userid == playerId{
                return r
            }
        }
        
        return nil
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
    
    fileprivate func createTopPlayerRegion(_ imgSize: Int) {
        //top
        let imgT = UIImageView(image: UIImage(named: "profile3"))
        self.view.addSubview(imgT)
        imgT.snp.makeConstraints{
            (make) -> Void in
            make.top.equalTo(self.view).offset(10)
            make.left.equalTo(self.view).offset(20)
            make.width.equalTo(imgSize)
            make.height.equalTo(imgSize)
        }
        
        let topCardsPanel = UIView()
        topCardsPanel.backgroundColor = .green
        self.view.addSubview(topCardsPanel)
        topCardsPanel.snp.makeConstraints{
            (make) -> Void in
            make.left.equalTo(imgT.snp.right).offset(20)
            make.top.equalTo(self.view).offset(5)
            make.height.equalTo(50)
            make.width.equalTo(self.view).multipliedBy(0.7)
        }
        
        let topPlayer = PlayerRegion()
        topPlayer.CardsPanel = topCardsPanel
        topPlayer.ProfileImg = imgT
        topPlayer.PrivateCardFaceImageName = "faced_handed"
        topPlayer.TableCardImageNameSuffix = "_faced_table"
        self.players[1] = topPlayer
    }
    
    fileprivate func createLeftPlayerRegion(_ imgSize: Int) {
        //left
        let imgL = UIImageView(image:UIImage(named: "profile3"))
        self.view.addSubview(imgL)
        imgL.snp.makeConstraints{
            (make) -> Void in
            make.left.equalTo(self.view.snp.left).offset(10)
            make.centerY.equalTo(self.view.snp.centerY).offset(-100)
            make.width.equalTo(imgSize)
            make.height.equalTo(imgSize)
        }
//        playersProfile[2] = img2
        
        let leftCardsPanel = UIView()
        leftCardsPanel.backgroundColor = .red
        self.view.addSubview(leftCardsPanel)
        leftCardsPanel.snp.makeConstraints { (make)->Void in
            make.left.equalTo(imgL.snp.right).offset(20)
            make.centerY.equalTo(self.view.snp.centerY)
            make.height.equalTo(self.view).multipliedBy(0.7)
            make.width.equalTo(50)
        }
        
        let leftPlayer = PlayerRegion()
        leftPlayer.CardsPanel = leftCardsPanel
        leftPlayer.ProfileImg = imgL
        leftPlayer.PrivateCardFaceImageName = "left_handed"
        leftPlayer.TableCardImageNameSuffix = "_left_table"
        leftPlayer.IsVerticalCardsPanel = true
        players[4] = leftPlayer
    }
    
    fileprivate func createRightPlayerRegion(_ imgSize: Int) {
        //right
        let imgR = UIImageView(image: UIImage(named: "profile3"))
        self.view.addSubview(imgR)
        imgR.snp.makeConstraints{
            (make) -> Void in
            make.right.equalTo(self.view.snp.right).offset(-10)
            make.centerY.equalTo(self.view).offset(-100)
            make.width.equalTo(imgSize)
            make.height.equalTo(imgSize)
        }
//        playersProfile[4] = imgR
        
        let rightCardsPanel = UIView()
        rightCardsPanel.backgroundColor = .blue
        self.view.addSubview(rightCardsPanel)
        rightCardsPanel.snp.makeConstraints { (make) in
            make.right.equalTo(imgR.snp.left).offset(-20)
            make.centerY.equalTo(self.view.snp.centerY)
            make.width.equalTo(50)
            make.height.equalTo(self.view).multipliedBy(0.7)
        }
        
        let rightPlayerRegion = PlayerRegion()
        rightPlayerRegion.CardsPanel = rightCardsPanel
        rightPlayerRegion.ProfileImg = imgR
        rightPlayerRegion.PrivateCardFaceImageName = "right_handed"
        rightPlayerRegion.TableCardImageNameSuffix = "_right_table"
        rightPlayerRegion.IsVerticalCardsPanel = true
        players[2] = rightPlayerRegion
    }
    
    fileprivate func createBottomMyPlayerRegion(_ imgSize: Int) {
        //my, bottom
        let imgMy = UIImageView(image:UIImage(named: "profile3"))
        self.view.addSubview(imgMy)
        imgMy.snp.makeConstraints{
            (make) -> Void in
            make.left.equalTo(self.view.snp.left).offset(10)
            make.bottom.equalTo(self.view.snp.bottom).offset(-10)
            make.width.equalTo(imgSize + 10)
            make.height.equalTo(imgSize + 10)
        }
//        playersProfile[3] = imgMy
        
        let rect = self.view.frame
        let yStart = rect.height * CGFloat(0.85)
        let myAreaHeight = rect.height - yStart
        let myProfileWidth = myAreaHeight
        let space = CGFloat(10)
        let xStart = myProfileWidth + space
        
        
        let cardsPanelWidth = rect.width - myProfileWidth - 2.0 * space
        let cardsPanelHeight = myAreaHeight * CGFloat(0.8)
        
        cardsPanelSize = CGSize(width: cardsPanelWidth, height: cardsPanelHeight)
        let rectPanel = CGRect(origin: CGPoint(x:xStart, y:yStart), size:cardsPanelSize )
        cardsPanel = UIView(frame:rectPanel)
        cardsPanel.backgroundColor = UIColor.yellow
        self.view.addSubview(cardsPanel)
        
        let myPlayerRegion = PlayerRegion()
        myPlayerRegion.ProfileImg = imgMy
        myPlayerRegion.CardsPanel = cardsPanel
        myPlayerRegion.TableCardImageNameSuffix = "_my_table"
        players[3] = myPlayerRegion
    }
    
    func createPlayerRegions() {
        let imgSize = 36
        
        createTopPlayerRegion(imgSize)
        
        createLeftPlayerRegion(imgSize)
        
        createBottomMyPlayerRegion(imgSize)
        
        createRightPlayerRegion(imgSize)
    }

//    fileprivate func createCardsPanel() {
//        let rect = self.view.frame
//        let yStart = rect.height * CGFloat(0.85)
//        let myAreaHeight = rect.height - yStart
//        let myProfileWidth = myAreaHeight
//        let space = CGFloat(10)
//        let xStart = myProfileWidth + space
//
//
//        let cardsPanelWidth = rect.width - myProfileWidth - 2.0 * space
//        let cardsPanelHeight = myAreaHeight * CGFloat(0.8)
//
//        cardsPanelSize = CGSize(width: cardsPanelWidth, height: cardsPanelHeight)
//        let rectPanel = CGRect(origin: CGPoint(x:xStart, y:yStart), size:cardsPanelSize )
//        cardsPanel = UIView(frame:rectPanel)
//        cardsPanel.backgroundColor = UIColor.yellow
//        self.view.addSubview(cardsPanel)
//
//
//        //top
//
//    }
    
    func rotateTableForMyChoice(selSeatId: UInt8) {
        var rotate = 0
        switch selSeatId {
        case 1:
            rotate = 2
            break
        case 2:
            rotate = 1
            break
        case 3:
            rotate = 0
            break
        case 4:
            rotate = 3
            break
        default:
            break
        }
        
        for _ in 0..<rotate{
            let bak = players[4]?.Player
            players[4]?.Player = players[3]?.Player
            players[3]?.Player = players[2]?.Player
            players[2]?.Player = players[1]?.Player
            players[1]?.Player = bak
        }
        
        let trans = self.center_img.transform
        let newTrans = trans.rotated(by: CGFloat(Double.pi/2.0 * Double(rotate)))
        center_img.transform = newTrans
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
            
//            make.left.equalTo(self.view.snp.left).multipliedBy(0.6)
            make.height.equalTo(50)
            make.width.equalTo(self.view.snp.width).multipliedBy(0.4)
            make.right.equalTo(self.view)
        }
        stack.spacing = 2
        stack.distribution = UIStackViewDistribution.fillEqually
    
        for p in gGameStatus.getRoomPlayers(){
            let pi = p as! PlayerInfo
            let imgPath = pi.getMyProfileImgPath()
            if imgPath.starts(with: "http"){
                let img = UIImageView()
                img.sd_setImage(with: URL(string: imgPath), placeholderImage: UIImage(named: "userprofile.png"))
                stack.addArrangedSubview(img)
            }
            else{
                let img2 = UIImageView(image: UIImage(named: imgPath))
                stack.addArrangedSubview(img2)
            }
        }
//        let img = UIImageView()
//        img.sd_setImage(with: URL(string: "https://ss0.bdstatic.com/5aV1bjqh_Q23odCf/static/superman/img/logo_top_ca79a146.png"), placeholderImage: UIImage(named: "placeholder.png"))
//        stack.addArrangedSubview(img)
//
//        let img2 = UIImageView(image: UIImage(named: "profile2"))
//        stack.addArrangedSubview(img2)
//
//        let img3 = UIImageView(image: UIImage(named: "profile3"))
//        stack.addArrangedSubview(img3)
      
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()

        createTableCenterImage()
        
        createSeatButtons()
        
        createPlayerRegions()
        
//        createCardsPanel()

        createOptCmdsPanel()
        
        createPlayerExecutionPanel()
        
//        createPlayersPanel()
        
        
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
    
    func createTableCenterImage() {
        center_img = UIImageView(image: UIImage(named: "table_center"))
//        let transform = center_img.transform
//        transform.rotated(by: CGFloat(Double.pi/2))
//        center_img.transform = transform
        self.view.addSubview(center_img)
        
        center_img.snp.makeConstraints{
            (make) -> Void in
            make.width.equalTo(const_table_center_size)
            make.height.equalTo(const_table_center_size)
            make.center.equalTo(self.view)
        }
        
    }
    
    func createSeatButtons() {
        let disVert = const_table_center_size / 2 + 20
        let disHorz = const_table_center_size / 2 + 30
        let btnWidth = 80.0
        let btnHeight = 30.0
        
        //top north
        let btn1 = UIButton()
        btn1.setTitle(StringRes.Join_game, for: UIControlState.normal)
        btn1.tag = 1
        btn1.addTarget(self, action:#selector(sitDownTabed(_:)), for:.touchUpInside)
        self.view.addSubview(btn1)
        btn1.snp.makeConstraints{(make) -> Void in
            make.centerX.equalTo(self.center_img.snp.centerX)
            make.centerY.equalTo(self.center_img.snp.centerY).offset(-disVert)
            make.width.equalTo(btnWidth)
            make.height.equalTo(btnHeight)
        }

        //bottom south
        let btn2 = UIButton()
        btn2.tag = 3
        btn2.addTarget(self, action:#selector(sitDownTabed(_:)), for:.touchUpInside)
        btn2.setTitle(StringRes.Join_game, for: UIControlState.normal)
        self.view.addSubview(btn2)
        btn2.snp.makeConstraints{ (make) -> Void in
            make.centerX.equalTo(self.center_img.snp.centerX)
            make.centerY.equalTo(self.center_img.snp.centerY).offset(disVert)
            make.width.equalTo(btnWidth)
            make.height.equalTo(btnHeight)
        }

        //left west
        let btn3 = UIButton()
        btn3.tag = 4
        btn3.setTitle(StringRes.Join_game, for: UIControlState.normal)
        btn3.addTarget(self, action:#selector(sitDownTabed(_:)), for:.touchUpInside)
        self.view.addSubview(btn3)
        btn3.snp.makeConstraints{(make) -> Void in
            make.centerX.equalTo(self.center_img.snp.centerX).offset(-disHorz)
            make.centerY.equalTo(self.center_img.snp.centerY)
            make.width.equalTo(btnWidth)
            make.height.equalTo(btnHeight)
        }

        //right east
        let btn4 = UIButton()
        btn4.tag = 2
        btn4.setTitle(StringRes.Join_game, for: UIControlState.normal)
        btn4.addTarget(self, action:#selector(sitDownTabed(_:)), for:.touchUpInside)
        self.view.addSubview(btn4)
        btn4.snp.makeConstraints{(make) -> Void in
            make.centerX.equalTo(self.center_img.snp.centerX).offset(disHorz)
            make.centerY.equalTo(self.center_img.snp.centerY)
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
                              okCallBack: {
                                self.rotateTableForMyChoice(selSeatId: UInt8(seatNo))
                                
        }) { (_, _) in
            
        }
    }
    
    @objc func cmdBtnClicked(_ button: UIButton) {
        let cmd = self.cmdBtns[button]
        
        guard let playerClient = NetworkProxy.getSockClient() else{
            return
        }
        self.canPlayCard = false
        playerClient.executeCmd(cmdText: (cmd?.cmdText)!, cmdParam: (cmd?.cmdParams)!,
                          okCallBack: {}, failCallback: {_,_ in })
        
    }
    
    @objc func playCardBtnClicked(_ button: UIButton) {
        if !self.canPlayCard{
            return
        }
        let card = button.tag
        let cards = [UInt8(card)]

        guard let playerClient = NetworkProxy.getSockClient() else{
            return
        }
        self.canPlayCard = false
        playerClient.playCards(cards: cards, okCallBack:{}, failCallback: {_,_ in })
        button.removeFromSuperview()
        self.cardsInHand.remove(button)
    }
    
//    func horzStackSubviews(panel:UIView, subviews:NSMutableArray, panelSize:CGSize) -> Void {
//
//        let vCount = subviews.count
//        let bestRatio:CGFloat = 0.618
//        let bestSubviewWidth = bestRatio * panelSize.height
//        let viewsWidthSum:CGFloat = CGFloat(vCount) * bestSubviewWidth
//        if viewsWidthSum < panelSize.width{
//            self.centerSubviews(container: panel, subViews: subviews, containerSize: panelSize, space: 0.0)
//        }
//        else{
//            self.overlapSubviews(container: panel, subViews: subviews, containerSize: panelSize, subViewWidth: bestSubviewWidth)
//
//        }
//
//    }
//
//    func overlapSubviews(container:UIView, subViews:NSMutableArray, containerSize:CGSize, subViewWidth:CGFloat) -> Void {
//        let overlapWidth = (containerSize.width - subViewWidth)/CGFloat(subViews.count - 1)
//
//        var offset : CGFloat = 0
//        for i in 0..<subViews.count{
//            let subView = subViews[i] as! UIView
//            if !container.subviews.contains(subView){
//                container.addSubview(subView)
//            }
//
//            offset = CGFloat(i) * overlapWidth
//            subView.snp.makeConstraints{(make) -> Void in
//                make.top.equalTo(container)
//                make.left.equalTo(container).offset(offset)
//                make.width.equalTo(subViewWidth)
//                make.height.equalTo(container)
//            }
//        }
//    }
    
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
    
    func test_push_game_end() {
        let client = SockClient(serverIP: "testIP", serverPort: 34)
        client.playerDelegate = self
        let test_pack = """
        {"cmdtype": "sockpush", "sockpush": "game-end", "winners": [{"userid": 111, "score": 40}], "losers": [{"userid": 333, "score": -40}]}
"""
        client.testServerPack(pack: test_pack)
        
    }
    
    func test_push_scores() {
        let client = SockClient(serverIP: "testIP", serverPort: 34)
        client.playerDelegate = self
        let test_pack = """
        {"cmdtype": "sockpush", "sockpush": "scores", "scores": [{"userid": 222, "score": 0}, {"userid": 333, "score": -40}, {"userid": 111, "score": 40}]}
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
    
//    func centerSubviews(container:UIView, subViews:NSMutableArray, containerSize:CGSize, space:CGFloat = 0) -> Void {
//
//        let bestRatio:CGFloat = 0.618
//        let bestSubviewWidth = bestRatio * containerSize.height
//        let viewsWidthSum:CGFloat = CGFloat(subViews.count) * bestSubviewWidth + CGFloat(subViews.count - 1) * space
//        let offsetStart = (containerSize.width - viewsWidthSum)/2
//
//        for i in 0..<subViews.count{
//            let subView = subViews[i] as! UIView
//            if !container.subviews.contains(subView ){
//                container.addSubview(subView )
//            }
//
//            subView.snp.makeConstraints { (make) -> Void in
//                make.top.equalTo(container)
//                make.left.equalTo(container).offset(offsetStart + CGFloat(i) * (bestSubviewWidth + space))
//                make.width.equalTo(bestSubviewWidth)
//                make.height.equalTo(containerSize.height)
//
//            }
//        }
//    }
//
//
//    func centerSubviews(container:UIView, subViews:NSMutableArray, subViewWidth:CGFloat, space:CGFloat = 0) -> Void {
//
////        let bestRatio:CGFloat = 0.618
////        let bestSubviewWidth = bestRatio * containerSize.height
//        let containerSize = container.frame.size;
//        let viewsWidthSum:CGFloat = CGFloat(subViews.count) * subViewWidth + CGFloat(subViews.count - 1) * space
//        let offsetStart = (containerSize.width - viewsWidthSum)/2
//
//        for i in 0..<subViews.count{
//            let subView = subViews[i] as! UIView
//            if !container.subviews.contains(subView ){
//                container.addSubview(subView )
//            }
//
//            subView.snp.makeConstraints { (make) -> Void in
//                make.top.equalTo(container)
//                make.left.equalTo(container).offset(offsetStart + CGFloat(i) * (subViewWidth + space))
//                make.width.equalTo(subViewWidth)
//                make.height.equalTo(containerSize.height)
//
//            }
//        }
//    }
    

    
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
