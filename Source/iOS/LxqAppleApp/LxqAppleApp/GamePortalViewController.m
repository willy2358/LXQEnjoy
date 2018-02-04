//
//  GamePortalViewController.m
//  LxqAppleApp
//
//  Created by willy2358 on 2018/1/16.
//  Copyright © 2018年 metalight. All rights reserved.
//

#import "GamePortalViewController.h"

@interface GamePortalViewController ()

@end

@implementation GamePortalViewController

- (void)viewDidLoad {
    [super viewDidLoad];
    
//    self.btnCreateRoom.backgroundColor = UIColor.greenColor;
//    self.btnEnterRoom.backgroundColor = UIColor.blueColor;
    // Do any additional setup after loading the view.
    self.btnEnterRoom.backgroundColor = UIColor.greenColor;
    self.btnCreateRoom.backgroundColor = UIColor.greenColor;
}

- (void)didReceiveMemoryWarning {
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}

/*
#pragma mark - Navigation

// In a storyboard-based application, you will often want to do a little preparation before navigation
- (void)prepareForSegue:(UIStoryboardSegue *)segue sender:(id)sender {
    // Get the new view controller using [segue destinationViewController].
    // Pass the selected object to the new view controller.
}
*/

- (IBAction)enterRoom_Clicked:(id)sender {
    NSLog(@"enterRoom_Clicked room");
}

- (IBAction)createRoom_Clicked:(id)sender {
    
    NSLog(@"Create room");
}
@end
