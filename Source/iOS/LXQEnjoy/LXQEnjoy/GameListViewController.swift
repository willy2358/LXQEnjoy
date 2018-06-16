//
//  GameListViewController.swift
//  LXQEnjoy
//
//  Created by willy2358 on 2018/4/1.
//  Copyright © 2018年 metalight. All rights reserved.
//

import UIKit
import SnapKit


class GameListViewController: UIViewController{
    
    let stack = UIStackView()
    let serverIP = "127.0.0.1"
    let port :UInt16 = 9229

    
    override func viewDidLoad() {
        super.viewDidLoad()

//        var player = NetworkProxy.getSockPlayer()
        
        stack.axis = UILayoutConstraintAxis.horizontal
        stack.distribution = UIStackViewDistribution.fillEqually
        stack.spacing = 20
        stack.alignment = UIStackViewAlignment.fill
        view.addSubview(stack)
//
        stack.snp.makeConstraints { (make) -> Void in
            make.top.equalTo(view).offset(80)
            make.left.equalTo(view).offset(60)
            make.bottom.equalTo(view).offset(-60)
            make.right.equalTo(view).offset(-80)
        }

        let gameId = 1000
        var images : [String]=["game1.jpg","game2.jpg","game3.jpg"]
        
        for i in 0...2 {
            let btn = UIButton()
            btn.tag = gameId + i
            btn.addTarget(self, action:#selector(tapped(_:)), for:.touchUpInside)
//            btn.addTarget(self, action: "gameBtnClicked:", for: UIControlEvents.touchUpInside)
            let img = UIImage(named: images[i])
            btn.setBackgroundImage(img, for: UIControlState.normal)
            stack.addArrangedSubview(btn)
        }

    }
    
    @objc func tapped(_ button:UIButton){
        print(button.tag)
//        let gameEntry = GameEntryViewController()
//        self.presentedViewController(gameEntry, animated: true, completion: nil)
//
        let myStoryBoard = self.storyboard
//        let anotherView = myStoryBoard.instanceViewControllerWithIdentifier("post")
//        let gameEntry = myStoryBoard?.instantiateInitialViewController("post")
        let gameEntry = myStoryBoard?.instantiateViewController(withIdentifier: "game_entry")
        self.present(gameEntry!, animated: true, completion: nil) //(gameEntry!, animated: true, completion: nil)
    }
    
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        print("hello")
    }

    func gameBtnClicked(sender:UIButton?){
        
        let tag = sender?.tag;
        print("gameid \(String(describing: tag)) ")
        
        let gameEntry = GameEntryViewController()
        self.present(gameEntry, animated: true, completion: nil)
        

        
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

}
