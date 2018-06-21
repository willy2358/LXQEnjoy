//
//  PlayerRegion.swift
//  LXQEnjoy
//
//  Created by willy2358 on 2018/6/18.
//  Copyright © 2018年 metalight. All rights reserved.
//
import UIKit
import Foundation

class PlayerRegion{
    var Player : PlayerInfo?
    var ProfileImg : UIImageView!
    var CardsPanel : UIView!
    var IsVerticalCardsPanel : Bool = false
    var CardSpace : CGFloat = 0
    var VertCardHeight : CGFloat = 0
    var CmdView : UILabel!
    var IsBanker : Bool = false
    var BankerView : UIView!
    var PendingFlag : UIView!
    
    var PrivateCardFaceImageName : String?
    
    var TableCardImageNameSuffix : String!
    
    init() {
        
    }
    
    public func ShowExedCmd(cmdText: String!) -> Void{
        CmdView.text = cmdText
        CmdView.isHidden = false
    }
    
    public func HideExedCmd(){
        CmdView.isHidden = true
    }
    
    public func ShowPendingFlag(){
        PendingFlag.isHidden = false
    }
    
    public func HidePendingFlag(){
        PendingFlag.isHidden = true
    }
    
    
    public func SetBanker(isBanker : Bool){
        self.IsBanker = isBanker
        if IsBanker {
            self.BankerView?.isHidden = false
        }
        else{
            self.BankerView?.isHidden = true
        }
    }
    
    public func UpdateCardsState(activeCards aCards: [UInt8], freezedCards fCards: [UInt8], publicShownCards sCards: [[UInt8]], private_cards_count  pCount: Int8) {
        if aCards.count > 0 {
            return;
        }
        
        for s in CardsPanel.subviews{
            s.removeFromSuperview()
        }
        
        let cards = NSMutableArray()
        for _ in 0..<pCount{
            let face = UIImageView(image: UIImage(named: PrivateCardFaceImageName!))
            cards.add(face)
        }
        
        for g in sCards {
            for c in g{
                let card = "\(c)" + TableCardImageNameSuffix
                let face = UIImageView(image: UIImage(named: card))
                cards.add(face)
            }
        }
        
        if (!self.IsVerticalCardsPanel){
            let size = CardsPanel.frame.size
            HorzStackSubviews(panel: CardsPanel, subviews: cards, panelSize:size)
        }
        else{
            VertCenterSubviews(container: CardsPanel, subViews: cards, space: self.CardSpace, subViewHeight: VertCardHeight)
        }
    }
}
