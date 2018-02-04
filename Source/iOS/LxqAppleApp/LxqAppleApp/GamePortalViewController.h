//
//  GamePortalViewController.h
//  LxqAppleApp
//
//  Created by willy2358 on 2018/1/16.
//  Copyright © 2018年 metalight. All rights reserved.
//

#import <UIKit/UIKit.h>

@interface GamePortalViewController : UIViewController
@property (weak, nonatomic) IBOutlet UIButton *btnEnterRoom;
@property (weak, nonatomic) IBOutlet UIButton *btnCreateRoom;

- (IBAction)enterRoom_Clicked:(id)sender;
- (IBAction)createRoom_Clicked:(id)sender;
//@property (weak, nonatomic) IBOutlet UIButton *btnEnterRoom;

@end
