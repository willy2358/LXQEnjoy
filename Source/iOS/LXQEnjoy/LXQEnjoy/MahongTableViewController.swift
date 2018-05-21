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

class MahongTableViewController: UIViewController, PlayerDelegate {
    
    var cardsPanelSize : CGSize!
    let cardsInHand : NSMutableArray = NSMutableArray()
    var cardsPanel : UIView!
    var sockPlayer : SockPlayer!
    
    func processServerSuccessResponse(respCmd: String, jsonObj: JSON) {
        
    }
    
    public func setSockPlayer(player:SockPlayer) {
        self.sockPlayer = player
        
    }
    
    func processServerPush(pushCmd: String, jsonObj: JSON) {
        if pushCmd == SockCmds.push_deal_cards{
            let cards = jsonObj[SockCmds.param_cards].arrayValue
            let newCards = NSMutableArray()
            for c in cards{
                
                let btn = UIButton()
                let img = UIImage(named: String(c.intValue))
                btn.setBackgroundImage(img, for: UIControlState.normal)
                newCards.add(btn)
            }
            horzStackSubviews(panel: cardsPanel, subviews: newCards, panelSize:cardsPanelSize)
        }
    }
    
    func onPlayerConnectStateChanged(oldState: client_status, newState: client_status) {
        
    }
    

    override func viewDidLoad() {
        super.viewDidLoad()

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
        cardsPanel.backgroundColor = UIColor.clear
        self.view.addSubview(cardsPanel)
        sockPlayer = NetworkProxy.sockPlayer
        sockPlayer.playerDelegate = self
        sockPlayer.joinGame(roomId: "LX888", gameId: 111)

        
        
        
        
        
        // Do any additional setup after loading the view.
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
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
    
    func centerSubviews(container:UIView, subViews:NSMutableArray, containerSize:CGSize, space:CGFloat = 0) -> Void {
        
        let bestRatio:CGFloat = 0.618
        let bestSubviewWidth = bestRatio * containerSize.height
        let viewsWidthSum:CGFloat = CGFloat(subViews.count) * bestSubviewWidth + CGFloat(subViews.count - 1) * space
        let offsetStart = (containerSize.width - viewsWidthSum)/2
        
        for i in 0..<subViews.count{
            let subView = subViews[i] as! UIView
            if !container.subviews.contains(subView as! UIView){
                container.addSubview(subView as! UIView)
            }

            subView.snp.makeConstraints { (make) -> Void in
                make.top.equalTo(container)
                make.left.equalTo(container).offset(offsetStart + CGFloat(i) * (bestSubviewWidth + space))
                make.width.equalTo(bestSubviewWidth)
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
