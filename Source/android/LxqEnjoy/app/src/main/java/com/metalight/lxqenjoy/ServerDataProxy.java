package com.metalight.lxqenjoy;

import android.os.AsyncTask;
import android.os.Handler;
import android.util.Log;

import com.metalight.lxqenjoy.Network.TCPClient;

import java.util.ArrayList;
import java.util.List;

/**
 * Created by willy on 2017/6/25.
 */

public class ServerDataProxy extends AsyncTask<String, String, Void> {

    private Handler _handler = null;
    private TCPClient _tcpClient = null;
    private String _serverIP = "";
    private  int _serverPort = 0;

    private static boolean stop = false;
    private static List<ServerDataListener> listeners = new ArrayList<>();

    public static void addDataListener(ServerDataListener listener){
        listeners.add(listener);
    }

    public ServerDataProxy(String serverIP, int port, Handler mHandler){
        _serverIP = serverIP;
        _serverPort = port;
        _handler = mHandler;
    }

    public void SendPlayMessage(String msg){
        if (null != _tcpClient){
            _tcpClient.sendMessage(msg);
        }
    }

//    public static void startRun(final Handler handler){
//        new Thread(new Runnable() {
//            @Override
//            public void run() {
//                //TestSmack();
//
//                while (!stop){
////                    for(ServerDataListener listener : listeners){
////                        listener.OnDataArrived("heelllooo");
////                    }
//                    handler.sendEmptyMessage(0x123);
//                    try {
//                        Thread.sleep(1000);
//                    } catch (InterruptedException e) {
//                        e.printStackTrace();
//                    }
//                }
//            }
//        }).start();
//    }

    @Override
    protected Void doInBackground(String... strings) {
        try{
            _tcpClient = new TCPClient(_handler,_serverIP, _serverPort);
//                    "10.0.2.2",
//                    new TCPClient.MessageCallback() {
//                        @Override
//                        public void callbackMessageReceiver(String message) {
//                            publishProgress(message);
//                        }
//                    });

        }catch (Exception e){
            //Log.d(TAG, "Caught null pointer exception");
            e.printStackTrace();
        }
        _tcpClient.run();
        return null;
    }

//    @Override
//    protected TCPClient doInBackground(String... strings) {
//        return null;
//    }


}
