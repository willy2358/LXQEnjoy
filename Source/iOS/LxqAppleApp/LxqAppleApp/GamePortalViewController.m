//
//  GamePortalViewController.m
//  LxqAppleApp
//
//  Created by willy2358 on 2018/1/16.
//  Copyright © 2018年 metalight. All rights reserved.
//

//@import CocoaAsyncSocket;
#import "GamePortalViewController.h"
#import "GCDAsyncSocket.h"

@interface GamePortalViewController () <GCDAsyncSocketDelegate>

- (BOOL) ConnectToServerIP: (NSString *) n withPort: (int) port;


@end

@implementation GamePortalViewController
{
    //    NSString * serverIP;
    //    NSInteger serverPort;
    GCDAsyncSocket *_socket;
}



@synthesize serverPort;
@synthesize serverIP;

- (void)viewDidLoad {
    [super viewDidLoad];
    
    //    self.btnCreateRoom.backgroundColor = UIColor.greenColor;
    //    self.btnEnterRoom.backgroundColor = UIColor.blueColor;
    // Do any additional setup after loading the view.
    self.btnEnterRoom.backgroundColor = UIColor.greenColor;
    self.btnCreateRoom.backgroundColor = UIColor.greenColor;
    
    self.serverIP = @"127.0.0.1";
    self.serverPort = 9229;
    
    //    NSString *host = @"133.33.33.1";
    //    int port = 1212;
    
    dispatch_queue_t mainQueue = dispatch_get_main_queue();
    
    _socket = [[GCDAsyncSocket alloc] initWithDelegate:self delegateQueue:mainQueue];
    //创建一个socket对象
    
//    GCDAsyncSocket *_socket = [[GCDAsyncSocket alloc] initWithDelegate:self delegateQueue:dispatch_get_global_queue(DISPATCH_QUEUE_PRIORITY_DEFAULT, 0)];
    
    //连接
    NSError *error = nil;
    if(![_socket connectToHost:self.serverIP onPort:self.serverPort error:&error]){
        NSLog(@"%@",error);
    }
    else{
        
    }
    
//    if (error) {
//        NSLog(@"%@",error);
//    }
    
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

#pragma mark 断开连接
-(void)socketDidDisconnect:(GCDAsyncSocket *)sock withError:(NSError *)err{
    if (err) {
        NSLog(@"连接失败");
    }else{
        NSLog(@"正常断开");
    }
}


#pragma mark 数据发送成功
-(void)socket:(GCDAsyncSocket *)sock didWriteDataWithTag:(long)tag{
    NSLog(@"%s",__func__);
    
    //发送完数据手动读取，-1不设置超时
    [sock readDataWithTimeout:-1 tag:tag];
}

#pragma mark 读取数据
-(void)socket:(GCDAsyncSocket *)sock didReadData:(NSData *)data withTag:(long)tag{
    NSString *receiverStr = [[NSString alloc] initWithData:data encoding:NSUTF8StringEncoding];
    NSLog(@"%s %@",__func__,receiverStr);
}

- (void)socket:(GCDAsyncSocket *)sock didConnectToHost:(NSString *)host port:(UInt16)port
{
//    DDLogInfo(@"socket:%p didConnectToHost:%@ port:%hu", sock, host, port);
    
    //    DDLogInfo(@"localHost :%@ port:%hu", [sock localHost], [sock localPort]);
    
#if USE_SECURE_CONNECTION
    {
        // Connected to secure server (HTTPS)
        
        // Configure SSL/TLS settings
        NSMutableDictionary *settings = [NSMutableDictionary dictionaryWithCapacity:3];
        
        // If you simply want to ensure that the remote host's certificate is valid,
        // then you can use an empty dictionary.
        
        // If you know the name of the remote host, then you should specify the name here.
        //
        // NOTE:
        // You should understand the security implications if you do not specify the peer name.
        // Please see the documentation for the startTLS method in GCDAsyncSocket.h for a full discussion.
        
        [settings setObject:@"www.paypal.com"
                     forKey:(NSString *)kCFStreamSSLPeerName];
        
        // To connect to a test server, with a self-signed certificate, use settings similar to this:
        
        //    // Allow expired certificates
        //    [settings setObject:[NSNumber numberWithBool:YES]
        //                 forKey:(NSString *)kCFStreamSSLAllowsExpiredCertificates];
        //
        //    // Allow self-signed certificates
        //    [settings setObject:[NSNumber numberWithBool:YES]
        //                 forKey:(NSString *)kCFStreamSSLAllowsAnyRoot];
        //
        //    // In fact, don't even validate the certificate chain
        //    [settings setObject:[NSNumber numberWithBool:NO]
        //                 forKey:(NSString *)kCFStreamSSLValidatesCertificateChain];
        
        DDLogInfo(@"Starting TLS with settings:\n%@", settings);
        
        [sock startTLS:settings];
        
        // You can also pass nil to the startTLS method, which is the same as passing an empty dictionary.
        // Again, you should understand the security implications of doing so.
        // Please see the documentation for the startTLS method in GCDAsyncSocket.h for a full discussion.
        
    }
#else
    {
        // Connected to normal server (HTTP)
        //        NSData *data = [[NSData alloc] init];
        NSString *aString = @"1234abcd";
        NSData *aData = [aString dataUsingEncoding: NSUTF8StringEncoding];
        [sock writeData:aData withTimeout:5 tag:2];
    }
#endif
}

- (IBAction)enterRoom_Clicked:(id)sender {
    NSLog(@"enterRoom_Clicked room");
}

- (IBAction)createRoom_Clicked:(id)sender {
    
    NSLog(@"Create room");
}

- (BOOL) ConnectToServerIP:(NSString *)n withPort:(int)port
{
    return TRUE;
}
@end
