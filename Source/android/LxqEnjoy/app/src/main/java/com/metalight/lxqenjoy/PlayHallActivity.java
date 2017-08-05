package com.metalight.lxqenjoy;

import android.content.Intent;
import android.content.pm.ActivityInfo;
import android.os.Bundle;
import android.support.design.widget.FloatingActionButton;
import android.support.design.widget.Snackbar;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.view.LayoutInflater;
import android.view.View;
import android.widget.HorizontalScrollView;
import android.widget.ImageView;
import android.widget.LinearLayout;

import java.util.ArrayList;
import java.util.List;

public class PlayHallActivity extends AppCompatActivity {
    private LayoutInflater mInflater;
    private LinearLayout mGallery;
    private List<PlayRule> _playRules = new ArrayList<>();

    private HorizontalScrollView mHorizontalScrollView;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_play_hall);
        Toolbar toolbar = (Toolbar) findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);

        FloatingActionButton fab = (FloatingActionButton) findViewById(R.id.fab);
        fab.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Snackbar.make(view, "Replace with your own action", Snackbar.LENGTH_LONG)
                        .setAction("Action", null).show();
            }
        });

        mInflater = LayoutInflater.from(this);
        initPlayRules();
        initView();
        mHorizontalScrollView = (HorizontalScrollView) findViewById(R.id.id_horizontalScrollView);

    }
    //设置横屏
    @Override
    protected void onResume(){
        if(getRequestedOrientation()!= ActivityInfo.SCREEN_ORIENTATION_LANDSCAPE){
            setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_LANDSCAPE);
        }
        super.onResume();
    }

    private void initPlayRules()
    {
        _playRules.add(new PlayRule(R.mipmap.ic_action_achievement, "do di zhu"));
        _playRules.add(new PlayRule(R.mipmap.ic_action_add, "Majiang"));
        _playRules.add(new PlayRule(R.mipmap.ic_action_achievement, "AAAA"));
        _playRules.add(new PlayRule(R.mipmap.ic_action_alarm, "do di zhu"));
        _playRules.add(new PlayRule(R.mipmap.ic_action_anchor, "do di zhu"));
        _playRules.add(new PlayRule(R.mipmap.ic_action_alarm, "do di zhu"));
        _playRules.add(new PlayRule(R.mipmap.ic_action_amazon, "do di zhu"));
        _playRules.add(new PlayRule(R.mipmap.ic_action_amazon, "do di zhu"));
    }

    private void initView()
    {
        mGallery = (LinearLayout) findViewById(R.id.id_gallery);
        for (int i = 0; i < _playRules.size(); i++)
        {
            PlayRule rule = _playRules.get(i);
            View view = mInflater.inflate(R.layout.activity_index_gallery_item, mGallery, false);
            ImageView img = (ImageView) view.findViewById(R.id.id_index_gallery_item_image);
            img.setTag(rule);
            img.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View view) {
                    PlayRule rule = (PlayRule) view.getTag();
                    loadPlayTable(rule);
                }
            });
            img.setImageResource(rule.getImgId());
            mGallery.addView(view);
        }
    }

    private void loadPlayTable(PlayRule rule){
//        Intent intent = new Intent(this, PlayTableActivity.class);
//        Bundle bundle=new Bundle();
//        bundle.putString("ruleId", rule.getId());
//        intent.putExtras(bundle);
//        startActivity(intent);
    }
}
