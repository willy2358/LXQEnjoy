
Pokers = ["c1","d1", "h1", "s1",
            "c2", "d2", "h2", "s2",
            "c3", "d3", "h3", "s3",
            "c4", "d4", "h4", "s4",
            "c5", "d5", "h5", "s5",
            "c6", "d6", "h6", "s6",
            "c7", "d7", "h7", "s7",
            "c8", "d8", "h8", "s8",
            "c9", "d9", "h9", "s9",
            "c10", "d10", "h10", "s10",
            "c11", "d11", "h11", "s11",
            "c12", "d12", "h12", "s12",
            "c13", "d13", "h13", "s13",
             "j21", "j22"]

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
