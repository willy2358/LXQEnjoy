package com.metalight.lxqenjoy;

/**
 * Created by willy on 2017/6/25.
 */

public class FigurePattern {
    protected int _minOccur = 1;
    protected int _maxOccur = -1; //-1 unlimited

    public  FigurePattern(){

    }
    public FigurePattern(int minOccur){
       _minOccur = minOccur;
    }

    public FigurePattern(int minOccur, int maxOccur){
        _minOccur = minOccur;
        _maxOccur = maxOccur;
    }
}
