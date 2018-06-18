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
    
    var PrivateCardFaceImageName : String?
    
    var TableCardImageNameSuffix : String!
    
    init() {
        
    }
    
    public func UpdateCardsState(activeCards aCards: [UInt8], freezedCards fCards: [UInt8], publicShownCards sCards: [[UInt8]], private_cards_count  pCount: Int8) {
        if (!self.IsVerticalCardsPanel){
            if aCards.count < 1 && pCount > 0{
                for s in CardsPanel.subviews{
                    s.removeFromSuperview()
                }
                
                let cards = NSMutableArray()
                for _ in 0..<pCount{
                    let face = UIImageView(image: UIImage(named: PrivateCardFaceImageName!))
                    cards.add(face)
                }
                
                let size = CardsPanel.frame.size
                HorzStackSubviews(panel: CardsPanel, subviews: cards, panelSize:size)
            }
        }
        else{
            let cards = NSMutableArray()
            for _ in 0..<pCount{
                let face = UIImageView(image: UIImage(named: PrivateCardFaceImageName!))
                cards.add(face)
            }
            
            VertCenterSubviews(container: CardsPanel, subViews: cards, space: self.CardSpace)
        }
    }
}
