package com.metalight.lxqenjoy;

import java.util.ArrayList;
import java.util.List;

/**
 * Created by willy on 2017/6/13.
 */
/*
   Terms:
   Deal: 发牌
   Hand: 一手牌，
   shuffle： 洗牌,
   cut切牌,
   deal发牌,
   sort理牌,
   draw摸牌,
   play打出,
   discard弃牌
   跟注是I'm in或者是call
增加赌注是raise
不跟是fold
Check让牌
Call跟注：跟随其他玩家押上平等的注额。
Bet押注：押上筹码
Pot底池
点数一般是用figure,花色用pattern.

he 6 of diamonds 还有扑克中的术语,也许你用得到↓ deck of cards 一幅牌 face card 花牌 play straight 出顺子 flush 同花
 straight flush 同花顺 single 单张 pair 一对 shuffle 洗牌 cut 倒牌 deal 分牌 banker / dealer 庄家 hand 手,家 to lead 居首
 to lay 下赌 to follow suit 出同花牌 to trump 出王牌 to overtrump 以较大的王牌胜另一张王牌 to win a trick 赢一圈
 to pick up,to draw 偷 stake 赌注 to stake 下赌注 to raise 加赌注 to see 下同样赌注 bid 叫牌 to bid / to call 叫牌 to bluff 虚张声势
 royal flush 同花大顺 straight flush 同花顺 straight 顺子 four of a kind 四张相同的牌 full house 三张相同和二张相同的牌
 three of a kind 三张相同的牌 two pairs 双对子 one pair 一对,对子 show one's hand 摊牌
call one's bluff 要对方摊牌 out of sorts 牌不齐,不能用 sweep the board 是指赢得桌上全部的赌注,也作sweep the table
 */

//玩法
public class PlayRule {
    public enum PlayActions{
        Draw,    //摸牌
        Call,    //跟注
        Raise,   //加注
    }
    private String _name;
    private String _id;

    private List<Card> _cards = new ArrayList<Card>();

    private List<PlayPattern> _playPatterns = new ArrayList<>();

    //最少玩家人数
    public int PlayerMinNumber;
    //最多玩家人数
    public int PlayerMaxNumber;
    //底牌，留牌张数
    public int CarsNumNotDeal;
    //起牌是否为暗牌，玩家不知道牌面
    public boolean InitBlind;

    private int _imgId;
    private String _imgUrl;

    public PlayRule(int imgId, String name){
        _imgId = imgId;
        _name = name;
        _id = "1212";
    }

    public String getName(){
        return _name;
    }

    public String getId(){
        return _id;
    }

    public int  getImgId(){
        return _imgId;
    }

    public void LoadCards()
    {
        _cards.add(new Card("poker_3_c", 1));
        _cards.add(new Card("poker_3_d", 1));
        _cards.add(new Card("poker_3_h", 1));
        _cards.add(new Card("poker_3_s", 1));

        _cards.add(new Card("poker_4_c", 2));
        _cards.add(new Card("poker_4_d", 2));
        _cards.add(new Card("poker_4_h", 2));
        _cards.add(new Card("poker_4_s", 2));

        _cards.add(new Card("poker_5_c", 3));
        _cards.add(new Card("poker_5_d", 3));
        _cards.add(new Card("poker_5_h", 3));
        _cards.add(new Card("poker_5_s", 3));

        _cards.add(new Card("poker_6_c", 4));
        _cards.add(new Card("poker_6_d", 4));
        _cards.add(new Card("poker_6_h", 4));
        _cards.add(new Card("poker_6_s", 4));

        _cards.add(new Card("poker_7_c", 5));
        _cards.add(new Card("poker_7_d", 5));
        _cards.add(new Card("poker_7_h", 5));
        _cards.add(new Card("poker_7_s", 5));

        _cards.add(new Card("poker_8_c", 6));
        _cards.add(new Card("poker_8_d", 6));
        _cards.add(new Card("poker_8_h", 6));
        _cards.add(new Card("poker_8_s", 6));

        _cards.add(new Card("poker_9_c", 7));
        _cards.add(new Card("poker_9_d", 7));
        _cards.add(new Card("poker_9_h", 7));
        _cards.add(new Card("poker_9_s", 7));

        _cards.add(new Card("poker_10_c", 8));
        _cards.add(new Card("poker_10_d", 8));
        _cards.add(new Card("poker_10_h", 8));
        _cards.add(new Card("poker_10_s", 8));

        _cards.add(new Card("poker_11_c", 9));
        _cards.add(new Card("poker_11_d", 9));
        _cards.add(new Card("poker_11_h", 9));
        _cards.add(new Card("poker_11_s", 9));

        _cards.add(new Card("poker_12_c", 10));
        _cards.add(new Card("poker_12_d", 10));
        _cards.add(new Card("poker_12_h", 10));
        _cards.add(new Card("poker_12_s", 10));

        _cards.add(new Card("poker_13_c", 11));
        _cards.add(new Card("poker_13_d", 11));
        _cards.add(new Card("poker_13_h", 11));
        _cards.add(new Card("poker_13_s", 11));

        _cards.add(new Card("poker_1_c", 12));
        _cards.add(new Card("poker_1_d", 12));
        _cards.add(new Card("poker_1_h", 12));
        _cards.add(new Card("poker_1_s", 12));

        _cards.add(new Card("poker_2_c", 13));
        _cards.add(new Card("poker_2_d", 13));
        _cards.add(new Card("poker_2_h", 13));
        _cards.add(new Card("poker_2_s", 13));

        _cards.add(new Card("poker_joker_moon", 14));
        _cards.add(new Card("poker_joker_sun", 15));
    }

    public void loadPlayPatterns(){
        PlayPattern p = new PlayPattern(new FigurePattern_Single());
        _playPatterns.add(p);

        p = new PlayPattern(new FigurePattern_Pair());
        _playPatterns.add(p);

        p = new PlayPattern(new FigurePattern_Triple(), new FigurePattern_Single());
        _playPatterns.add(p);

        p = new PlayPattern(new FigurePattern_Triple(), new FigurePattern_Pair());
        _playPatterns.add(p);

        p = new PlayPattern(new FigurePattern_Quadruple(), 5);
        _playPatterns.add(p);

        p = new PlayPattern(new FigurePattern_Quadruple(), new FigurePattern_Single(2, 2));
        _playPatterns.add(p);

        p = new PlayPattern(new FigurePattern_Quadruple(), new FigurePattern_Pair(2,2));
        _playPatterns.add(p);

        p = new PlayPattern(new FigurePattern_Quadruple(), new FigurePattern_Pair(), new FigurePattern_Single());
        _playPatterns.add(p);

        p = new PlayPattern(new FigurePattern_OrderedStraight(new FigurePattern_Single(5), "3", "14"));
        _playPatterns.add(p);
    }
}
