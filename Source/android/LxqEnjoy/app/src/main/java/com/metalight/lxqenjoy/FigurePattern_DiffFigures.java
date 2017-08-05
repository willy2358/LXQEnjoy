package com.metalight.lxqenjoy;

/**
 * Created by willy on 2017/6/27.
 */

public class FigurePattern_DiffFigures extends FigurePattern {
    public FigurePattern_DiffFigures(){

    }

    public FigurePattern_DiffFigures(int minOccur) {
        super(minOccur);
    }

    public FigurePattern_DiffFigures(int minOccur, int maxOccur){
        super(minOccur, maxOccur);
    }

    //有相同花色的牌张数
    public int SamePatternCardNumber;
}
