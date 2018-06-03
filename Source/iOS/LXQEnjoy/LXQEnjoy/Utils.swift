//
//  Utils.swift
//  LXQEnjoy
//
//  Created by willy2358 on 2018/6/1.
//  Copyright © 2018年 metalight. All rights reserved.
//

import Foundation

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



