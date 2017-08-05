package com.metalight.lxqenjoy;

import android.content.pm.ActivityInfo;
import android.os.Bundle;
import android.os.Handler;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.LinearLayout;

public class PlayTableActivity extends AppCompatActivity implements ServerDataListener {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_play_table);
        //TestSmack();
        Handler handler = new Handler()
        {
            public void handleMessage(android.os.Message msg) {
                if(msg.what==0x123)
                {
                    //tv.setText("更新后的TextView");
                    showNewCard("10_c");
                }
            };
       };
//        final ConnectionConfiguration connectionConfig = new ConnectionConfiguration(
//                "192.168.1.78", Integer.parseInt("5222"), "csdn.shimiso.com");

        // 允许自动连接
        //connectionConfig.setReconnectionAllowed(true);
        //connectionConfig.setSendPresence(true);

//        Connection connection = new XMPPConnection(connectionConfig);
//        try {
//            AbstractXMPPConnection conn2 = new XMPPTCPConnection("user2", "user2", "192.168.1.6");
//            conn2.connect();
//        } catch (XmppStringprepException e) {
//            e.printStackTrace();
//        } catch (InterruptedException e) {
//            e.printStackTrace();
//        } catch (IOException e) {
//            e.printStackTrace();
//        } catch (SmackException e) {
//            e.printStackTrace();
//        } catch (XMPPException e) {
//            e.printStackTrace();
//        }
        ServerDataProxy.addDataListener(this);

        Bundle bundle = this.getIntent().getExtras();
        //接收name值
        String ruleId = bundle.getString("ruleId");

        LoadMyImage();

        ServerDataProxy.startRun(handler);
    }




    //设置横屏
    @Override
    protected void onResume(){
        if(getRequestedOrientation()!= ActivityInfo.SCREEN_ORIENTATION_LANDSCAPE){
            setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_LANDSCAPE);
        }
        super.onResume();
    }

    public void onTestClick(View view){
//        XMPPTCPConnectionConfiguration config = XMPPTCPConnectionConfiguration.builder()
//                .setUsernameAndPassword("user1", "user1")
//                .setXmppDomain("win-2dstoe8tald")
//                .setHost("win-2dstoe8tald")
//                .setPort(5222)
//                .build();
        //TestSmack();

//        String strTmp="点击Button03";
//        Ev1.setText(strTmp);
//        LinearLayout myArea = (LinearLayout)findViewById(R.id.myZone);
//        LinearLayout.LayoutParams param1 = (LinearLayout.LayoutParams)myArea.getLayoutParams();
//
//        int height = myArea.getHeight();
//
//        FrameLayout myProfileLayout = (FrameLayout)findViewById(R.id.myProfileArea);
//        LinearLayout.LayoutParams params = (LinearLayout.LayoutParams) myProfileLayout.getLayoutParams();
//        params.width = myProfileLayout.getHeight();
//        //params.width = params.height;
//
//
//        myProfileLayout.setLayoutParams(params);
        //showNewCard("10_c");
    }

    private void LoadMyImage(){
        ImageView img = (ImageView) findViewById(R.id.myImage);
        img.setImageResource(R.mipmap.ic_action_achievement);
    }

    public int getResourceId(String pVariableName, String pResourcename, String pPackageName)
    {
        try {
            return getResources().getIdentifier(pVariableName, pResourcename, pPackageName);
        } catch (Exception e) {
            e.printStackTrace();
            return -1;
        }
    }

    private void showNewCard(String cardId) {
        String cardImg = "poker_" + cardId;
        int resId = getResourceId(cardImg,"mipmap",getPackageName());

        Button btnCard = new Button(this);
        btnCard.setBackgroundResource(resId);
        btnCard.setWidth(100);
        btnCard.setHeight(100);

        LinearLayout cardArea = (LinearLayout)findViewById(R.id.myCardArea);

        LinearLayout.LayoutParams lp1 = new LinearLayout.LayoutParams(LinearLayout.LayoutParams.WRAP_CONTENT, LinearLayout.LayoutParams.WRAP_CONTENT);

        if (cardArea.getChildCount() > 0)
        {
            lp1.setMargins(-150,0,0,0);
            //lp1.leftMargin = (int)(getResources().getDimension(R.dimen.activity_horizontal_margin) * (-50.0));
        }
//        else
//        {
//            lp1.setMargins(-150,-50,0,0);
//        }
        try {
            cardArea.addView(btnCard, lp1);
        }
        catch (Exception e){
            e.getStackTrace();
        }
    }

    int testCount = 0;
    @Override
    public void OnDataArrived(String data) {
        if (testCount < 10){
            showNewCard("10_c");
        }
        testCount++;
    }
}