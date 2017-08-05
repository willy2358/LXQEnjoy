package com.metalight.lxqenjoy;

import android.content.pm.ActivityInfo;
import android.os.Bundle;
import android.os.Handler;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.LinearLayout;

import java.util.Date;

public class PlayTableActivity extends AppCompatActivity implements ServerDataListener {

    ServerDataProxy _serverProxy;
    Handler _serverMsgHandler;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_play_table);
        //TestSmack();
        _serverMsgHandler = new Handler()
        {
            public void handleMessage(android.os.Message msg) {
                if(msg.what==0x123)
                {
                    showNewCard("10_c");
                }
            };
       };

        _serverProxy = new ServerDataProxy(MyConfig.getServerIP(), MyConfig.getServerPort(), _serverMsgHandler);
        Bundle bundle = this.getIntent().getExtras();
        String ruleId = bundle.getString("ruleId");

        LoadMyImage();

        _serverProxy.execute();
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
        this._serverProxy.SendPlayMessage((new Date()).toString());
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