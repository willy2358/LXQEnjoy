package com.metalight.lxqenjoy.Network;

import android.os.Handler;
import android.util.Log;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.net.InetAddress;
import java.net.Socket;

/**
 * Created by willy on 2017/8/1.
 */

public class TCPClient {
    public static final int SOCK_CONNECTING = 1;
    public static final int SOCK_SENDING_DATA = 2;
    public static final int SOCK_RECEIVED_DATA = 3;
    public static final int SOCK_ERROR = 4;
    public static final int SOCK_DISCONNECTD_BY_SERVER = 5;
    public static final int SOCK_CLOSE_CONNECT = 6;

    private static final String            TAG             = "TCPClient"     ;
    private final Handler mHandler                          ;
    private              String _serverIP, incomingMessage;
    BufferedReader in;
    PrintWriter out;
    private  MessageCallback  listener = null;
    private  boolean  mRun = false;
    private int _serverPort = 0;


    /**
     * TCPClient class constructor, which is created in AsyncTasks after the button click.
     * @param mHandler Handler passed as an argument for updating the UI with sent messages
     * @param serverIp String retrieved from IpGetter class that is looking for ip number.
     */
    public TCPClient(Handler mHandler, String serverIp, int port) {
        //this.listener         = listener;
        this._serverIP = serverIp;
        this.mHandler         = mHandler;
        this._serverPort = port;
    }

    /**
     * Public method for sending the message via OutputStream object.
     * @param message Message passed as an argument and sent via OutputStream object.
     */
    public void sendMessage(String message){
        if (out != null && !out.checkError()) {
            out.println(message);
            out.flush();
            mHandler.sendEmptyMessageDelayed(SOCK_SENDING_DATA, 1000);
            Log.d(TAG, "Sent Message: " + message);
        }
    }

    /**
     * Public method for stopping the TCPClient object ( and finalizing it after that ) from AsyncTask
     */
    public void stopClient(){
        Log.d(TAG, "Client stopped!");
        mRun = false;
    }

    public void run() {
        mRun = true;
        try {
            // Creating InetAddress object from _serverIP passed via constructor from IpGetter class.
            InetAddress serverAddress = InetAddress.getByName(_serverIP);
            Log.d(TAG, "Connecting...");

            /**
             * Sending empty message with static int value from MainActivity
             * to update UI ( 'Connecting...' ).
             *
             * @see com.example.turnmeoff.MainActivity.CONNECTING
             */
            mHandler.sendEmptyMessageDelayed(SOCK_CONNECTING,1000);

            /**
             * Here the socket is created with hardcoded port.
             * Also the port is given in IpGetter class.
             *
             * @see com.example.turnmeoff.IpGetter
             */
            Socket socket = new Socket(serverAddress, _serverPort);


            try {

                // Create PrintWriter object for sending messages to server.
                out = new PrintWriter(new BufferedWriter(new OutputStreamWriter(socket.getOutputStream())), true);

                //Create BufferedReader object for receiving messages from server.
                in = new BufferedReader(new InputStreamReader(socket.getInputStream()));

                Log.d(TAG, "In/Out created");

                //Sending message with command specified by AsyncTask
                //this.sendMessage(command);

                //
                //mHandler.sendEmptyMessageDelayed(MainActivity.SENDING,2000);

                //Listen for the incoming messages while mRun = true
                while (mRun) {
                    incomingMessage = in.readLine();
//                    if (incomingMessage != null && listener != null) {
//
//                        /**
//                         * Incoming message is passed to MessageCallback object.
//                         * Next it is retrieved by AsyncTask and passed to onPublishProgress method.
//                         *
//                         */
//                        listener.callbackMessageReceiver(incomingMessage);
//
//                    }
//                    incomingMessage = null;
                    Log.d(TAG, "Received Message: " +incomingMessage);
                }



            } catch (Exception e) {

                Log.d(TAG, "Error", e);
                mHandler.sendEmptyMessageDelayed(SOCK_ERROR, 1000);

            } finally {

                out.flush();
                out.close();
                in.close();
                socket.close();
                mHandler.sendEmptyMessageDelayed(SOCK_SENDING_DATA, 3000);
                Log.d(TAG, "Socket Closed");
            }

        } catch (Exception e) {

            Log.d(TAG, "Error", e);
            mHandler.sendEmptyMessageDelayed(SOCK_ERROR, 2000);
        }

    }

    public boolean isRunning() {
        return mRun;
    }

    /**
     * Callback Interface for sending received messages to 'onPublishProgress' method in AsyncTask.
     *
     */
    public interface MessageCallback {
        /**
         * Method overriden in AsyncTask 'doInBackground' method while creating the TCPClient object.
         * @param message Received message from server app.
         */
        public void callbackMessageReceiver(String message);
    }
}
