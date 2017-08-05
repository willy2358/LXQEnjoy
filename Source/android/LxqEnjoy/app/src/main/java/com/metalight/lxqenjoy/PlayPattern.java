package com.metalight.lxqenjoy;

import java.util.ArrayList;
import java.util.List;

/**
 * Created by willy on 2017/6/25.
 */

//出牌类型，比如3带1，同花顺，
public class PlayPattern {

    public String PlayAudio;
    public String PlayGif;

    //此种牌型打出时所对赔注的影响
    public String PlayWeight;

    public int _power = 0;
    private List<FigurePattern> _patterns = new ArrayList<>();

    public PlayPattern(FigurePattern pattern){
        _patterns.add(pattern);
    }

    public PlayPattern(FigurePattern pattern, int power){
        _patterns.add(pattern);
        _power = power;
    }

    public PlayPattern(FigurePattern pattern1, FigurePattern pattern2){
        _patterns.add(pattern1);
        _patterns.add(pattern2);
    }

    public PlayPattern(FigurePattern pattern1, FigurePattern pattern2, int power){
        _patterns.add(pattern1);
        _patterns.add(pattern2);
        _power = power;
    }

    public PlayPattern(FigurePattern pattern1, FigurePattern pattern2, FigurePattern pattern3){
        _patterns.add(pattern1);
        _patterns.add(pattern2);
        _patterns.add(pattern3);
    }

    public PlayPattern(FigurePattern pattern1, FigurePattern pattern2, FigurePattern pattern3, int power){
        _patterns.add(pattern1);
        _patterns.add(pattern2);
        _patterns.add(pattern3);
        _power = power;
    }

    public int getPower(){
        return _power;
    }

    public void setPowser(int power){
        _power = power;
    }
}
