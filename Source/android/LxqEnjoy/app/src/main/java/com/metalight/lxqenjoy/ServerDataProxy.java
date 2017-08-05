package com.metalight.lxqenjoy;

import android.os.Handler;

import java.util.ArrayList;
import java.util.List;

/**
 * Created by willy on 2017/6/25.
 */

public class ServerDataProxy {

    private static boolean stop = false;
    private static List<ServerDataListener> listeners = new ArrayList<>();

    public static void addDataListener(ServerDataListener listener){
        listeners.add(listener);
    }

    public static void startRun(final Handler handler){
        new Thread(new Runnable() {
            @Override
            public void run() {
                //TestSmack();

                while (!stop){
//                    for(ServerDataListener listener : listeners){
//                        listener.OnDataArrived("heelllooo");
//                    }
                    handler.sendEmptyMessage(0x123);
                    try {
                        Thread.sleep(1000);
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }
                }
            }
        }).start();
    }

//    @Override
//    public void run() {
//        //延迟两秒更新
//        try {
//            Thread.sleep(2000);
//        } catch (InterruptedException e) {
//            // TODO Auto-generated catch block
//            e.printStackTrace();
//        }
//        handler.sendEmptyMessage(0x123);
//    }

//    public static void stop(){
//        stop = true;
//    }
}
