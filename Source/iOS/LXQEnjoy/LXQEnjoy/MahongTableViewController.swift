//
//  MahongTableViewController.swift
//  LXQEnjoy
//
//  Created by willy2358 on 2018/5/14.
//  Copyright © 2018年 metalight. All rights reserved.
//

import UIKit
import SnapKit

class MahongTableViewController: UIViewController, PlayerDelegate {
    func onPlayerConnectStateChanged(oldState: client_status, newState: client_status) {
        
    }
    

    override func viewDidLoad() {
        super.viewDidLoad()

        let rect = CGRect(x:0, y:10, width:150, height:60)
        let myView = UIView(frame:rect)
        myView.backgroundColor = UIColor.red
        self.view.addSubview(myView)
        
        let views = NSMutableArray()
        let btn1 = UIButton()
        let img1 = UIImage(named: "23")
        btn1.setBackgroundImage(img1, for: UIControlState.normal)
        views.add(btn1)
        
        let btn2 = UIButton()
        let img2 = UIImage(named: "13")
        btn2.setBackgroundImage(img2, for: UIControlState.normal)
        views.add(btn2)
        
        let btn3 = UIButton()
        let img3 = UIImage(named: "13")
        btn3.setBackgroundImage(img3, for: UIControlState.normal)
        views.add(btn3)
        
        let btn4 = UIButton()
        let img4 = UIImage(named: "13")
        btn4.setBackgroundImage(img4, for: UIControlState.normal)
        views.add(btn4)

        let btn5 = UIButton()
        let img5 = UIImage(named: "13")
        btn5.setBackgroundImage(img5, for: UIControlState.normal)
        views.add(btn5)
        
        let btn6 = UIButton()
        let img6 = UIImage(named: "13")
        btn6.setBackgroundImage(img6, for: UIControlState.normal)
        views.add(btn6)

        
        
        let size = CGSize(width: 150, height: 60)
        
        horzStackSubviews(panel: myView, subviews: views, panelSize:size)
        
        
        
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
            self.centerSubviews(container: panel, subViews: subviews, containerSize: panelSize, space: 10.0)
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
                make.left.equalTo(view).offset(offsetStart + CGFloat(i) * (bestSubviewWidth + space))
                make.width.equalTo(bestSubviewWidth)
                make.height.equalTo(containerSize.height)

            }
        }
    }
    
    func processServerPush(pushCmd: String, cmdJsonStr: String) {
   
    }
    
    func processServerFailResponse(reqCmd: String, errCode: UInt, errMsg: String) {
    
    }
    
    func processServerSuccessResponse(respCmd: String, result_data: String, data: String) {
 
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
