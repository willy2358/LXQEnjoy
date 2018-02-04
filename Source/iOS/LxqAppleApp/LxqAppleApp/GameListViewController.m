//
//  GameLobbyViewController.m
//  LxqAppleApp
//
//  Created by willy2358 on 2018/1/15.
//  Copyright © 2018年 metalight. All rights reserved.
//

#import "GameListViewController.h"

@interface GameListViewController ()
//-(void)clickGame:(UITapGestureRecognizer *)gestureRecognizer;
- (void)clickGame: (UITapGestureRecognizer *)gestureRecognizer;
@end

@implementation GameListViewController

- (void)viewDidLoad {
    [super viewDidLoad];
    
    [_imgGame1 setUserInteractionEnabled:YES];
    [_imgGame2 setUserInteractionEnabled:YES];
    [_imgGame3 setUserInteractionEnabled:YES];
    [_imgGame1 addGestureRecognizer:[[UITapGestureRecognizer alloc] initWithTarget:self action:@selector(clickGame:)]];
    
    [_imgGame2 addGestureRecognizer:[[UITapGestureRecognizer alloc] initWithTarget:self action:@selector(clickGame:)]];
    
    // Do any additional setup after loading the view.
    
    
}

- (void)clickGame:(UITapGestureRecognizer *)gestureRecognizer
{
    
//    NSLog(@"clicked");
//    UIView *viewClicked=[gestureRecognizer view];
//    if (viewClicked==_imgGame1) {
//        NSLog(@"imageView1");
//    }else if(viewClicked==_imgGame2)
//    {
//        NSLog(@"imageView2");
//    }
    
    UIStoryboard* mainStoryboard = [UIStoryboard storyboardWithName:@"Main" bundle:nil];
    
    UIViewController* registerViewController = [mainStoryboard instantiateViewControllerWithIdentifier:@"gamePortalViewController"];
    
    registerViewController.modalTransitionStyle = UIModalTransitionStyleCoverVertical;
    [self presentViewController:registerViewController animated:YES completion:^{
        NSLog(@"Present Modal View");
    }];
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

@end
