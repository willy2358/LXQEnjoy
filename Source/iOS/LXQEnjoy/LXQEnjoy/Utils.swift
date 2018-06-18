//
//  Utils.swift
//  LXQEnjoy
//
//  Created by willy2358 on 2018/6/1.
//  Copyright © 2018年 metalight. All rights reserved.
//

import Foundation
import UIKit

func printLog(_ item: Any, _ file: String = #file, _ line: Int = #line, _ function: String = #function) {
    let debug = true
    if debug {
        print(file + ":\(line):" + function, item)
    }
}

func printErrorLog(_ item: Any, _ file: String = #file, _ line: Int = #line, _ function: String = #function) {
    let debug = true
    if debug {
        print(file + ":\(line):" + function, item)
    }
}

public extension Int {
    public static func random(lower: Int = 0, _ upper: Int = Int.max) -> Int {
        return lower + Int(arc4random_uniform(UInt32(upper - lower + 1)))
    }
    
//    public static func random(range: Range<Int>) -> Int {
//        return random(range.startIndex, range.endIndex)
//    }
}

func HorzStackSubviews(panel:UIView, subviews:NSMutableArray, panelSize:CGSize) -> Void {
    
    let vCount = subviews.count
    let bestRatio:CGFloat = 0.618
    let bestSubviewWidth = bestRatio * panelSize.height
    let viewsWidthSum:CGFloat = CGFloat(vCount) * bestSubviewWidth
    if viewsWidthSum < panelSize.width{
        HorzCenterSubviews(container: panel, subViews: subviews, containerSize: panelSize, space: 0.0)
    }
    else{
        OverlapSubviews(container: panel, subViews: subviews, containerSize: panelSize, subViewWidth: bestSubviewWidth)
        
    }
}

func OverlapSubviews(container:UIView, subViews:NSMutableArray, containerSize:CGSize, subViewWidth:CGFloat) -> Void {
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

func HorzCenterSubviews(container:UIView, subViews:NSMutableArray, containerSize:CGSize, space:CGFloat = 0) -> Void {
    
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

func VertCenterSubviews(container: UIView, subViews: NSMutableArray, space:CGFloat){
    let containerSize = container.frame.size
    let bestRatio:CGFloat = 0.618
    let bestSubviewHeight = bestRatio * containerSize.width
    let viewsHeightSum:CGFloat = CGFloat(subViews.count) * bestSubviewHeight + CGFloat(subViews.count - 1) * space
    let offsetStart = (containerSize.width - viewsHeightSum)/2
    
    for i in 0..<subViews.count{
        let subView = subViews[i] as! UIView
        if !container.subviews.contains(subView ){
            container.addSubview(subView )
        }
        
        subView.snp.makeConstraints { (make) -> Void in
            make.left.equalTo(container)
            make.top.equalTo(container).offset(offsetStart + CGFloat(i) * (bestSubviewHeight + space))
            
            make.width.equalTo(container)
            make.height.equalTo(bestSubviewHeight)
        }
    }
}


func HorzCenterSubviews(container:UIView, subViews:NSMutableArray, subViewWidth:CGFloat, space:CGFloat = 0) -> Void {
    
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


