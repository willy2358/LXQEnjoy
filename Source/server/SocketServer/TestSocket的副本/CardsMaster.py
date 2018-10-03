
Pokers = ["poker_1_c","poker_1_d", "poker_1_h", "poker_1_s",
             "poker_2_c", "poker_2_d", "poker_2_h", "poker_2_s",
             "poker_3_c", "poker_3_d", "poker_3_h", "poker_3_s",
             "poker_4_c", "poker_4_d", "poker_4_h", "poker_4_s",
             "poker_5_c", "poker_5_d", "poker_5_h", "poker_5_s",
             "poker_6_c", "poker_6_d", "poker_6_h", "poker_6_s",
             "poker_7_c", "poker_7_d", "poker_7_h", "poker_7_s",
             "poker_8_c", "poker_8_d", "poker_8_h", "poker_8_s",
             "poker_9_c", "poker_9_d", "poker_9_h", "poker_9_s",
             "poker_10_c", "poker_10_d", "poker_10_h", "poker_10_s",
             "poker_11_c", "poker_11_d", "poker_11_h", "poker_11_s",
             "poker_12_c", "poker_12_d", "poker_12_h", "poker_12_s",
             "poker_13_c", "poker_13_d", "poker_13_h", "poker_13_s",
             "poker_joker_moon", "poker_joker_sun"]

# MaJiang_Wan = [('wan_1',11),('wan_2',12),('wan_3',13),('wan_4',14),('wan_5',15),('wan_6',16),('wan_7',17),('wan_8',18),('wan_9',19)] * 4
# MaJiang_Suo = [('suo_1',21),('suo_2',22),('suo_3',23),('suo_4',24),('suo_5',25),('suo_6',26),('suo_7',27),('suo_8',28),('suo_9',29)] * 4
# MaJiang_Tong = [('tong_1',31),('tong_2',32),('tong_3',33),('tong_4',34),('tong_5',35),('tong_6',36),('tong_7',37),('tong_8',38),('tong_9',39)] * 4
# MaJiang_Wind = [('wind_east',41),('wind_west',42),('wind_south',43),('wind_north',44)] * 4
# MaJiang_Arrow = [('arrow_zhong',51),('arrow_bai',52),('arrow_fa',53) ] * 4

def_wans = {"wan-1": 11, "wan-2": 12, "wan-3": 13, "wan-4": 14,
        "wan-5": 15, "wan-6": 16, "wan-7": 17, "wan-8": 18, "wan-9": 19}
def_suos = {"suo-1": 21, "suo-2": 22, "suo-3": 23, "suo-4": 24,
        "suo-5": 25, "suo-6": 26, "suo-7": 27, "suo-8": 28, "suo-9": 29}
def_tons = {"ton-1": 31, "ton-2": 32, "ton-3": 33, "ton-4": 34,
        "ton-5": 35, "ton-6": 36, "ton-7": 37, "ton-8": 38, "ton-9": 39}
def_winds = {"wind-east": 41, "wind-west": 43, "wind-south": 45, "wind-north": 47}
def_arrows = {"arrow-zhong": 51, "arrow-bai": 53, "arrow-fa": 55}

majiang_wans = list(def_wans.values()) * 4
majiang_suos = list(def_suos.values()) * 4
majiang_tons = list(def_tons.values()) * 4
majiang_winds = list(def_winds.values()) * 4
majiang_arrows = list(def_arrows.values()) * 4

MaJiang = majiang_wans + majiang_suos + majiang_tons + majiang_winds + majiang_arrows
