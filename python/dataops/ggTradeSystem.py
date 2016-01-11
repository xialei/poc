# coding:utf-8
# run D:\web\Python\work\Quantitative\ggTradeSystem
import re, sys, time, datetime, zipfile
from dateutil.relativedelta import relativedelta
sys.path.append(r'D:/web/Python/work/PubLib')
import ggPrintReport as P
import ggTradeSystemAct as A
import ToMySQL, file, Mongo, Oracle
from collections import OrderedDict
from copy import deepcopy
from pandas import Series, DataFrame
import numpy as np, pandas as pd, pandas.io.sql as psql, matplotlib.pyplot as plt, matplotlib.dates as dates
# import cProfile
# pr = cProfile.Profile()
# pr.enable()

###################################################################################
#                                                                                 #
#               这是分布处理函数
#                                                                                 #
###################################################################################
#               get函数                                                                                                                                                        #
###################################################################################    
    
def GetRule(Now='209912'):
    global Num, LongProb, ShortProb, LongEr, ShortEr, DayLength, ExtraRule, ProbExp, MaxDayCalc, RollBack
    if Now == '209912':
        ThisRBack = 201
    else:
        ThisRBack = RollBack
    def GetResSql(Num=50, ud='u', Prob=0.6, ExtraRule=0, Er=0, Extra='', ProbExp='P'):
        Select, Where, From = '', '', ''
        if ProbExp == 'P':
            for i in range(1, DayLength + 1, 1):
                Select += ',{i}{ud}p,e{i},{i}{ud}n'.format(ud=ud, i=i)  # {i}{ud}r
                Where += ' or {i}{ud}p>{Prob}'.format(ud=ud, i=i, Prob=Prob)
                From += ',sum({i}{ud}n)/sum({i}un+{i}dn) {i}{ud}p,sum({i}{ud}n) {i}{ud}n,sum(e{i}*num)/sum(num) e{i}'.format(ud=ud, i=i)
        elif ProbExp == 'E':
            if ud == 'u':
                GL = ">"
            elif ud == 'd':
                GL = "<"
            for i in range(1, DayLength + 1, 1):
                Select += ',{i}{ud}p,CASE WHEN ({i}un+{i}dn)>{Num} then e{i} ELSE 0 END'.format(i=i, Num=Num, ud=ud)
                Where += ' or e{i}{GL}{Er}'.format(i=i, GL=GL, Er=Er)
                From += ',sum({i}{ud}p*num)/sum(num) {i}{ud}p,sum({i}un) {i}un,sum({i}dn) {i}dn,sum(e{i}*num)/sum(num) e{i}'.format(ud=ud, i=i)
        Where = Where[3:]
        if ExtraRule > 0:
            if ExtraRule == 2:
                Where1 = '({where}) and '.format(where=Where)
                Where2 = '(type in ({0}))'.format(','.join(Extra))
                Where = Where1 + Where2
            elif ExtraRule == 1:
                Where = 'type in ({0})'.format(','.join(Extra))
                Num = 0
            else:
                print('ExtraRule参数错误')
                exit()
        SimpTable = 'gg.result'
        SimpTime = 'where time between {Back} and {Now} '.format(Now=Now, Back=str(int(Now[0:4]) - ThisRBack) + Now[4:6])
        SimpTable = '(select code,sum(num) num {0} from {1} {2}group by code)'.format(From, SimpTable, SimpTime)
        LongSql = '''SELECT code,type,num{Select} FROM  (select r.*,t.type from {SimpTable} r left join gg.typecode t on  r.code=t.code where num>{Num}) a  where {Where};'''.format(Select=Select, Where=Where, Num=Num, SimpTable=SimpTable)
#         print(LongSql)
        Res = ToMySQL.SqlCommend(LongSql, Local=1)
        return Res
    def GetResMongo(Num=50, ud='u', Prob=0.6, ExtraRule=0, Er=0, Extra='', ProbExp='P'):
        if Debug == 1:
            print('ResMongo Begin')
        db = Mongo.ConMongo("224")
        AllCsv = ''
        Dlist = []
        for i in range(1, DayLength + 1):
            Dlist.append('d' + str(i))
        ResList = []
        # 'typ':{"$in":["121407","200104"]},'typ':"170902",
        LastCode = ''
        Ed, Bg = "{y}-{m}".format(y=Now[0:4], m=Now[4:6]), "{y}-{m}".format(y=int(Now[0:4]) - ThisRBack, m=Now[4:6])
        collection = db.announce_stat.find({"mth": {"$gt":Bg, "$lte":Ed}})
        collection2 = {}
        for res in collection:
            Type = res["typ"]
            Month = res["mth"]
#             if Debug == 1:
#                 if Type=='180101':
#                     print(Type)
            try:
                TypeCn = RuleTypeCode[int(Type)]
            except:
                print("Type Error",Type)
#                 print(res)
                exit()
            if ExtraRule > 0:
                if "'"+TypeCn+"'"  not in  Extra:
                    continue
            if Type not in collection2 :
                collection2[Type] = OrderedDict()
            try:
                collection2[Type][Month] = [res["num"], res["stk"]]
            except:
                collection2[Type][Month] = [0, {}]
                if Debug == 1:
                    print('err1', res["typ"], res["mth"], res)
#         exit()
        for Code in collection2:
            Dl = []
            NumL = []
            for Month in collection2[Code]:
                num = collection2[Code][Month][0]
                NumL.append(num)
            for Dx in Dlist:
                urtL, unmL, drtL, dnmL = [], [], [], []
                for Month in collection2[Code]:
                    stk = collection2[Code][Month][1]
                    if Dx in stk:
                        urtL.append(stk[Dx]["urt"]);unmL.append(stk[Dx]["unm"])
                        drtL.append(stk[Dx]["drt"]);dnmL.append(stk[Dx]["dnm"])
                    else:
                        urtL.append(0);unmL.append(0);drtL.append(0);dnmL.append(0)
                        if Debug == 1:
                            print('err2', stk)
                try:
                    p = sum(unmL) / sum(NumL)
                    e = (sum(urtL) + sum(drtL)) / (sum(unmL) + sum(dnmL))
                    n = sum(unmL)
                    Dl.extend([p, e, n])
                except:
                    if Debug == 1:
                        print('err3', NumL, unmL, urtL, drtL, dnmL)
                    Dl.extend([0, 0, 0])
            TypeCn = RuleTypeCode[int(Code)]
            ResOne = [Code, TypeCn, sum(NumL)]
            ResOne.extend(Dl)
            ResList.append(ResOne)
        if Debug == 1:
            print('ResMongo Begin')
        return ResList
    def MakeRule(Res, Dre=1, ProbExp='P', MaxDayCalc='Auto'):
        for Re in Res:
            if ProbExp == 'P':
                code, gcn, num, MaxProb, MaxRate = Re[0], Re[1], Re[2], Re[3], Re[4]
                if MaxProb == None:
                    MaxProb = 0
                if MaxDayCalc == "Auto":
                    MaxDay = 1
                    for i in range(6, len(Re), 3):
                        try:
                            if (0 if Re[i] == None else Re[i]) > MaxProb and Re[i + 2] > 50:
                                MaxProb, MaxRate = Re[i], Re[i + 1]
                                MaxDay = int((i - 2 + 1) / 2)
                        except:
                            print('error')
                            exit()
                else:
                    MaxDay = MaxDayCalc
                    if (0 if Re[3 * MaxDay] == None else Re[3 * MaxDay]) > MaxProb and Re[2 + 3 * MaxDay] > 50:
                        MaxProb, MaxRate = Re[3 * MaxDay], Re[1 + 3 * MaxDay]
                Rules[str(code) + str(Dre)] = [Dre, MaxDay, round(MaxRate, 4), gcn, round(MaxProb, 4), num]
            elif ProbExp == 'E':
                code, gcn, num, MaxProb, Er = Re[0], Re[1], Re[2], Re[3], Re[4]
                MaxEr = 0
                if Dre == 1:
                    for i in range(3, len(Re), 2):
                        if Re[i + 1] > MaxEr:
                            MaxProb, MaxEr = Re[i], Re[i + 1]
                            MaxDay = int((i - 2 + 1) / 2)
                elif Dre == 2:
                    for i in range(3, len(Re), 1):
                        if Re[i + 1] < MaxEr:
                            MaxProb, MaxEr = Re[i], Re[i + 1]
                            MaxDay = int((i - 2 + 1) / 2)
                if MaxEr != 0:
                    Rules[str(code) + str(Dre)] = [Dre, MaxDay, round(MaxEr, 4) , gcn, round(MaxProb, 4), num]
    Rules = {}
    if ExtraRule == 0:
        if BuyLong == 1:
            Res = GetResSql(Num=Num, ud='u', Prob=LongProb, Er=LongEr, ProbExp=ProbExp)
            MakeRule(Res, Dre=1, ProbExp=ProbExp, MaxDayCalc=MaxDayCalc)
        if BuyShort == 1:
            Res = GetResSql(Num=Num, ud='d', Prob=ShortProb, Er=ShortEr, ProbExp=ProbExp)
            MakeRule(Res, Dre=2, ProbExp=ProbExp, MaxDayCalc=MaxDayCalc)
    elif ExtraRule > 0:
        ExtraRules = file.ExcelToDict(RuleXlsx, Key=0, Val=1, HasTitle=0, StName=ExRuSheet)
        ExtraLong, ExtraShort, ExtraTest = [], [], []
        if 'Seve' in globals().keys():
            i = 0
            for Rule in ExtraRules:
                i += 1
                if i == Seve:
                    ExtraLong.append("'" + Rule + "'")
                    break
        else:
            for Rule in ExtraRules:
                if int(ExtraRules[Rule]) == 1:
                    ExtraLong.append("'" + Rule + "'")
                elif int(ExtraRules[Rule]) == 2:
                    ExtraShort.append("'" + Rule + "'")
                elif int(ExtraRules[Rule]) == 3:
                    ExtraTest.append("'" + Rule + "'")
        if BuyLong == 1:
            if len(ExtraLong) > 0:
                Res = GetResSql(Num=Num, ud='u', Prob=LongProb, ExtraRule=ExtraRule, Extra=ExtraLong, ProbExp=ProbExp)
#                 Res = GetResMongo(Num=Num, ud='u', Prob=LongProb, ExtraRule=ExtraRule, Extra=ExtraLong, ProbExp=ProbExp)
                MakeRule(Res, 1, ProbExp=ProbExp, MaxDayCalc=MaxDayCalc)
            if len(ExtraTest) > 0:
                Res = GetResSql(Num=Num, ud='u', Prob=LongProb, ExtraRule=ExtraRule, Extra=ExtraTest, ProbExp=ProbExp)
                MakeRule(Res, 1, ProbExp=ProbExp, MaxDayCalc=MaxDayCalc)
        if BuyShort == 1:
            if len(ExtraShort) > 0:
                Res = GetResSql(Num=Num, ud='d', Prob=ShortProb, ExtraRule=ExtraRule, Extra=ExtraShort, ProbExp=ProbExp)
                MakeRule(Res, 2, ProbExp=ProbExp, MaxDayCalc=MaxDayCalc)
            if len(ExtraTest) > 0:
                Res = GetResSql(Num=Num, ud='d', Prob=ShortProb, ExtraRule=ExtraRule, Extra=ExtraTest, ProbExp=ProbExp)
                MakeRule(Res, 1, ProbExp=ProbExp, MaxDayCalc=MaxDayCalc)
    if ThisRBack == 201:
        WriteRules(Now, Rules, 'w')
    else:
        WriteRules(Now, Rules, 'a')
    return Rules

def GetEventM(BgTime, EdTime):  # 从Mongo获取数据,暂时不用
#     file.Pnow('GetEventM B:' + str(Time))
    global EventNum
    Event = []
    db = Mongo.ConMongo("200")  # { "upt":Time}
    if BgTime == 0:
        BgTime = EdTime - datetime.timedelta(days=1)
    By, Bm, Bd = BgTime.year, BgTime.month, BgTime.day
    Ey, Em, Ed = EdTime.year, EdTime.month, EdTime.day
    Begin = datetime.datetime(By, Bm, Bd, 9, 30)
    End = datetime.datetime(Ey, Em, Ed, 9, 30)
    End = datetime.datetime(Ey, Em, Ed, 6, 0)
    collection = db.announcement.find({"pdt":{'$gte':Begin, '$lt':End}, "typ":{'$ne':'null'}}, {"secu.cd":1, "typ":1}).sort([("_id", 1)])
    for Eve in collection:
        if 'typ' in Eve:
            try:
                Secu = Eve['secu'][0]['cd']
                Type = Eve['typ']
                Id = Eve['_id']
                if Secu[0] in ['6', '0', '3'] and Secu[-2:] == 'EQ':
                    Event.append({'secu':Secu, 'type':Type, 'id':Id})
            except:
                print (Eve)
#     print('get Event,Num:' + str(len(Event)))
    EventNum += len(Event)
#     file.Pnow('GetEventM E:' + str(Time))
    if len(Event) != 0 :
        return   Event
    else:
        return None
    
def GetEventSql(BgTime, EdTime):
    global EventNum
    Event = []
    if BgTime == 0:
        BgTime = EdTime - datetime.timedelta(days=1)
    By, Bm, Bd = BgTime.year, BgTime.month, BgTime.day
    Ey, Em, Ed = EdTime.year, EdTime.month, EdTime.day
    Bg = datetime.datetime(By, Bm, Bd, 9, 30)
    Ed = datetime.datetime(Ey, Em, Ed, 9, 30)
    Sql = '''SELECT * FROM gg.announcement where (
    secu like '6%_SH_EQ' or  secu like '0%_SZ_EQ'  or  secu like '3%_SZ_EQ') and pdt between '{Bg}' and '{Ed}';'''.format(Bg=Bg, Ed=Ed)
    Res = ToMySQL.SqlCommend(Sql, 1)
    for Eve in Res:
        try:
            Secu = Eve[1]
            Type = Eve[2]
            Id = Eve[0]
            Event.append({'secu':Secu, 'type':Type, 'id':Id})
        except:
            print (Eve)
            sys.exit()
#     print('get Event,Num:'+str(len(Event)))
    EventNum += len(Event)
    if len(Event) != 0 :
        return   Event
    else:
        return None
    
def GetEventList(Events, Rules):
    def RemoveDupEvent(EventList):
        EvnRecode, NewEventList = [], []
        for Event in EventList:
            Secu = str(Event['secu'])
            Type = str(Event['event'])
            if Secu + Type  not in EvnRecode:
                EvnRecode.append(Secu + Type)
                NewEventList.append(Event)
        return NewEventList
    global Signal
    EventList = []
    if Events:
        for Event in Events:
            Type = str(Event['type'])
            if Type + '1' in Rules or Type + '2' in Rules:
                if Type + '1' in Rules:
                    Dre, Day, Max, Prob, Num = Rules[Type + '1'][0], Rules[Type + '1'][1], Rules[Type + '1'][2], Rules[Type + '1'][4], Rules[Type + '1'][5]  # 方向,#持有期间,#最大涨幅
                elif Type + '2' in Rules:
                    Dre, Day, Max, Prob, Num = Rules[Type + '2'][0], Rules[Type + '2'][1], Rules[Type + '2'][2], Rules[Type + '2'][4], Rules[Type + '1'][5]  # 方向,#持有期间,#最大涨幅
                Secu = Event['secu']
                Signal += 1
                EventList.append({'secu':Secu, 'dre':Dre, 'day':Day, 'max':Max, 'event':Type, 'prob':Prob, 'id':Event['id'], 'num':Num})
    EventList = RemoveDupEvent(EventList)  # 去除同一股票,同一天,同一个事件
    return EventList


def GetRTypeCode():
    Sqlp = "SELECT * FROM gg.typecode"
    Res = ToMySQL.SqlCommend(Sqlp, 1)
    RuleTypeCode = file.SQLtoDict(Res)
    return RuleTypeCode

def GerPriceDict(Hold, Wait, EventList, Time, Moke2=False, GetSp=False):
    SecuS, SecuSo, SecuL, SecuLo, SecuD = '', '', [], [], {}
    if Moke2 == False:
        for Secu in Hold:
            if 'secu' in Secu:
                SecuD[Secu['secu']] = {}
        for Secu in Wait: 
            if 'secu' in Secu:   
                SecuD[Secu['secu']] = {}
    else: 
        for Secu in Hold: 
            SecuD[Secu] = {}
    for Secu in EventList:
        if 'secu' in Secu:
            if Secu['secu'] == '300168_SZ_EQ' and Debug == 1:
                print(Secu['secu'])
            SecuD[Secu['secu']] = {}
    if len(SecuD) > 0:
        for k in SecuD:
            SecuL.append("'" + k + "'")
            SecuLo.append("'" + k[0:6] + "'")
        SecuS, SecuSo = ','.join(SecuL) , ','.join(SecuLo) 
        SqlTc = "select secu_code,close_price from equity_price where secu_code in ({0}) and trade_date='{1}' and volume>0".format(SecuS, Time)
        SqlTo = "SELECT ob_seccode_0160,F003N_0160 FROM JUCHAO.TB_TRADE_0160 where OB_SECCODE_0160 in ({Secu})  and OB_TRADEDATE_0160=to_date('{Time}','yyyy-mm-dd') and F004N_0160>0  and F023V_0160 like'A%'".format(Secu=SecuSo, Time=str(Time))
        ResTc = ToMySQL.SqlCommend(SqlTc, 0)
        ResTo = Oracle.OracleSql(SqlTo)
        if len(ResTc) > 0:
            for Tc in ResTc:
#                 if Tc=='000909_SZ_EQ':
#                     print(Tc)
                SecuD[Tc[0]]['C'] = round(float(Tc[1]), 2)
        if len(ResTo) > 0:
            for To in ResTo:
                if To[0][0:1] in ['0', '3']:
                    code = To[0] + '_SZ_EQ'
                elif To[0][0:1] == '6':
                    code = To[0] + '_SH_EQ'
                SecuD[code]['O'] = round(float(To[1]), 2)
        if GetSp:
            SqlSplit = "select secu_code,split_factor from equity_split where secu_code in ({0}) and trade_date='{1}'".format(SecuS, Time)
            ResSp = ToMySQL.SqlCommend(SqlSplit, 0)      
            if len(ResSp) > 0:
                for Sp in ResSp:
                    SecuD[Sp[0]]['Sp'] = float(Sp[1])
        return SecuD
    else:
        return {}

def GetGetRiskFree(bg='2010-01-01', ed='2010-01-31'):
    RiskFreeSql = '''SELECT OB_TRADEDATE_0160 trade_date,F003N_0160 FROM JUCHAO.TB_TRADE_0160 where OB_SECCODE_0160='204001'
AND OB_TRADEDATE_0160 between to_date('{0}','yyyy-mm-dd') and  to_date('{1}','yyyy-mm-dd') order by OB_TRADEDATE_0160'''.format(str(bg), str(ed))
    RiskFreeD = psql.read_sql(RiskFreeSql, con=Oracle.conn, index_col='TRADE_DATE')  
    return RiskFreeD

def GetTimeLine(bg='2010-01-01', ed='2010-01-31'):
    TimeLineSQL = '''SELECT trade_date FROM index_price WHERE secu_code = '000001_SH_IX'
AND trade_date>='{0}' and trade_date<='{1}'  order by  trade_date asc '''.format(bg, ed)
    TimeLine = file.SQLtoList(ToMySQL.SqlCommend(TimeLineSQL, 0), 0)  # SqlCommend(, 0)
    return TimeLine
###################################################################################
#                                                                                 #
#               行动函数                                                                                                                                                            #
#                                                                                 #
###################################################################################   
def ToBuyStock(BuyStockList, t, Time, TodayEachBuy):
    def RemoveOneStock():
        for B in BuyStockList:
            Tp = B[2]
            BuyShare = int(int(ThisStockMoney) / Tp / 100) * 100
            if BuyShare == 0:
                BuyStockList.remove(B)
                ThisStockMoney = ThisStockMoney * TodayEachBuy / (TodayEachBuy - 1)
                RemoveOneStock()
                break
    if t != 0:
        LastTime = TimeLine[t - 1]
        Val = Holding[LastTime]
        MktVal = Val[0]
        for stock in Val[1:]:
            MktVal += stock['todayprice'] * stock['sellshare']
    else:
        MktVal = BegTotMoney
    TotMoney = Holding[Time][0]
    if MktVal * OneDayBuyMax < TotMoney:  # 取剩余资金和目标资金小的作为总买入资金
        BuyMoney = MktVal * OneDayBuyMax
    else:
        BuyMoney = TotMoney
    ThisStockMoney = int(BuyMoney / TodayEachBuy)  # 总资金乘以单日仓位,除以买股个数
    if OneShareBuyMaxCtrl == 1:  # 单一股票上限
        if MktVal * OneShareBuyMax < ThisStockMoney:
            ThisStockMoney = MktVal * OneShareBuyMax
        else:
            ThisStockMoney = ThisStockMoney
#     RemoveOneStock()
    for B in BuyStockList:
        BuyStock(B[0], B[1], B[2], B[3], B[4], B[5], B[6], ThisStockMoney)
        
def BuyStock(Time, Secu, Tp, Day, Dre, Max, Eve, Money):
    global BuySuccess
    TotMoney = Holding[Time][0]
    try:
        Stock = int(Money) / Tp
    except:
        print(Tp)
        sys.exit()
    BuyShare = int(Stock / 100) * 100
    if BuyShare > 0:
        if Dre == 1:
            RemMoney = TotMoney - Tp * BuyShare
        elif Dre == 2:
            RemMoney = TotMoney - Tp * BuyShare * MarginRate
        UpHolding(Time, Secu, Tp, BuyShare, Day, Max, Dre, RemMoney, Eve)
        BuySuccess += 1
    else:
        Error.append(['No Money', Time, Secu, Eve, Tp, Money])
    
def UpHolding(Time, Secu, Tp, BuyShare, Day, Max, Dre, RemMoney, Eve):
#     if Secu=='600562_SH_EQ':
#         print(Secu)
    Holding[Time][0] = RemMoney
    HoldPair = {}
    HoldPair['secu'] = Secu
    HoldPair['buyshare'] = BuyShare
    HoldPair['sellshare'] = BuyShare
    HoldPair['buyprice'] = Tp
    HoldPair['buytime'] = Time
    HoldPair['tagtime'] = Day
    HoldPair['max'] = Max
    HoldPair['dre'] = Dre
    HoldPair['holdtime'] = Day - 1  # 今日已经算一天
    HoldPair['event'] = Eve
    HoldPair['todayprice'] = 0
    Holding[Time].append(HoldPair)
    
def SellHold(Holding, Time, PriceDict, OC='Open'):
    RemoveL = []
    for i, Hold in enumerate(Holding[Time][1:]):
        Secu, Dre = Hold['secu'], Hold['dre']
        if Secu == '000006_SZ_EQ' and Debug == 1:
            print(Secu)
        if OC == 'Open':
            Day = Hold['holdtime'] - 1
            try:
                Holding[Time][1 + i]['holdtime'] = Day
            except:
                print(Hold)
                sys.exit()
            if Day < 0:
                if Secu in PriceDict and 'O' in PriceDict[Secu]:  # 1天的,n天后开盘卖
                    SellPrice = PriceDict[Secu]['O']
                    if SellPrice:
                        Holding[Time][0] = SellStock(Time, Secu, SellPrice, Holding[Time][0], Hold, Day)
                        RemoveL.append(1 + i)
        elif OC == 'Close':
            Day = Hold['holdtime']
            TagDay = Hold['tagtime']
            if Day == 0 and TagDay != 1:
                if Secu in PriceDict and 'C' in PriceDict[Secu]:  # 不是1天的,n天后收盘卖
                      SellPrice = PriceDict[Secu]['C']
                      if SellPrice:
                          Holding[Time][0] = SellStock(Time, Secu, SellPrice, Holding[Time][0], Hold, Day)
                          RemoveL.append(1 + i)
    Holding[Time] = Remove(RemoveL, Holding[Time])
    return Holding

def StopLoss(Holding, Time):
    if Stoploss > 0:
        RemoveL = []
        for i, Hold in enumerate(Holding[Time][1:]):
            Dre, Secu, BuyPrice, TodayPrice, HoldDay, TagDay, Event = Hold['dre'], Hold['secu'], Hold['buyprice'], Hold['todayprice'], Hold['holdtime'], Hold['tagtime'], Hold['event']
            if (Dre == 1 and TodayPrice / BuyPrice - 1 < -Stoploss and HoldDay > 1) or (Dre == 2 and TodayPrice / BuyPrice - 1 > Stoploss and HoldDay > 1):
                    if Secu == '000400_SZ_EQ' and Debug == 1:
                        print(Secu)
                    SellPrice = TodayPrice
                    Holding[Time][0] = SellStock(Time, Secu, SellPrice, Holding[Time][0], Hold, HoldDay)
                    RemoveL.append(1 + i)
                    Error.append(['StopLoss', Time, Secu, Event, BuyPrice, 0])
        Holding[Time] = Remove(RemoveL, Holding[Time])
    if Stopwin > 0:
        RemoveL = []
        for i, Hold in enumerate(Holding[Time][1:]):
            Dre, Secu, BuyPrice, TodayPrice, HoldDay, TagDay, Event = Hold['dre'], Hold['secu'], Hold['buyprice'], Hold['todayprice'], Hold['holdtime'], Hold['tagtime'], Hold['event']
            if (Dre == 1 and TodayPrice / BuyPrice - 1 > Stopwin and HoldDay > 1) or (Dre == 2 and TodayPrice / BuyPrice - 1 < -Stopwin and HoldDay > 1):
                    if Secu == '000400_SZ_EQ' and Debug == 1:
                        print(Secu)
                    SellPrice = TodayPrice
                    Holding[Time][0] = SellStock(Time, Secu, SellPrice, Holding[Time][0], Hold, HoldDay)
                    RemoveL.append(1 + i)
                    Error.append(['Stopwin', Time, Secu, Event, BuyPrice, 0])
        Holding[Time] = Remove(RemoveL, Holding[Time])
    return Holding       
 
def SellStock(Time, Secu, Tp, TotMoney, Hold, Day):
    global Win, GetTar, Stg, Commission
    Dre, Max, BuyShare, SellShare, BuyTime, BuyPrice, TagTime, Eve = Hold['dre'], Hold['max'], Hold['buyshare'], Hold['sellshare'], Hold['buytime'], Hold['buyprice'], Hold['tagtime'], Hold['event']
    SellTime, SellPrice = Time, Tp
    if Dre == 1:
        SellInflow = SellPrice * SellShare
        if CalcComm:
            SellInflow = SellInflow - int(SellInflow * TaxRate)
            Commission += SellInflow * TaxRate
        RemMoney = TotMoney + SellInflow
        Return = (SellPrice * SellShare) / (BuyPrice * BuyShare) - 1
        if Return > Max:
            GetTar += 1
    elif Dre == 2:
        MarginMoney = BuyPrice * BuyShare * MarginRate
        SellInflow = MarginMoney + BuyPrice * BuyShare - SellPrice * SellShare
        if CalcComm:
            SellInflow = SellInflow - int(SellInflow * TaxRate)
            MaringInterest = BuyPrice * BuyShare * MarginRate * MarginIr * Day / 365
            Commission += SellInflow * TaxRate + MaringInterest
        RemMoney = TotMoney + SellInflow
        Return = (1 - (SellPrice * SellShare) / (BuyPrice * BuyShare))
        if Return > -Max:
            GetTar += 1
    if Return > 0:
        Win += 1
    Length = TagTime - Day
    UpStg(Secu, BuyTime, BuyPrice, BuyShare, SellTime, SellPrice, SellShare, Return, Dre, Length, Eve, TagTime)
    return RemMoney
    
def WaitStock(Time, Secu, Lp, Day, Dre, Max, Eve):
    Waiting[Time].append({'secu':Secu, 'day':Day, 'max':Max, 'baseprice':Lp, 'dre':Dre, 'event':Eve})

def UpStg(Secu, BuyTime, BuyPrice, BuyShare, SellTime, SellPrice, SellShare, Return, Dre, Length, Eve, TagTime):
    global Stg
    StgPair = OrderedDict()
    StgPair['Secu'] = Secu
    StgPair['Dre'] = Dre
    StgPair['BuyTime'] = BuyTime
    StgPair['BuyPrice'] = BuyPrice
    StgPair['BuyShare'] = BuyShare
    StgPair['SellTime'] = SellTime
    StgPair['SellPrice'] = SellPrice
    StgPair['SellShare'] = SellShare
    StgPair['Event'] = Eve
    StgPair['TagDay'] = TagTime
    StgPair['Length'] = Length
    StgPair['Return'] = round(Return, 4)
    Stg.append(StgPair)
###################################################################################
#                                                                                 #
#               Price函数                                                                                                                                                        #
#                                                                                 #
###################################################################################       
def ClosePrice(Secu, Time, Tp=True, Sp=False, Moke2=False):
    if Tp:
        Sqlp = "select close_price from equity_price where secu_code='{Secu}' and trade_date='{Time}'  and volume>0".format(Secu=Secu, Time=Time)
    else:
        Sqlp = "select close_price from equity_price where secu_code='{Secu}' and trade_date<'{Time}'  and volume>0 order by trade_date desc  limit 1".format(Secu=Secu, Time=Time)

    Res = ToMySQL.SqlCommend(Sqlp, 0)
    if len(Res) > 0:
        Price = file.SQLtoVar(Res)
        if Sp:
            Sqls = "select split_factor from equity_split where secu_code='{Secu}' and trade_date='{Time}'".format(Secu=Secu, Time=Time)
            SpFatcor = ToMySQL.SqlCommend(Sqls, 0)
            if len(SpFatcor) > 0:
                Price = Price * file.SQLtoVar(SpFatcor)
#                 if Moke2:
#                     Price = Price * file.SQLtoVar(SpFatcor) * file.SQLtoVar(SpFatcor) 
        return round(float(Price), 2)
    else:
        Price = False
        return Price
    
def OpenPrice(Secu, Time):
    SqlOp = "SELECT F003N_0160 FROM JUCHAO.TB_TRADE_0160 where OB_SECCODE_0160='{Secu}'  and OB_TRADEDATE_0160=to_date('{Time}','yyyy-mm-dd') and F004N_0160>0  and F023V_0160 like'A%'".format(Secu=Secu[0:6], Time=str(Time))
    Res = Oracle.OracleSql(SqlOp)
    if len(Res) > 0:
        Price = file.SQLtoVar(Res)
        return round(float(Price), 2)
    else:
        Price = False
        return Price
    
def UpDataLastPrice2(SecuCode, Time, PriceDict):
    if SecuCode in PriceDict and 'C' in PriceDict[SecuCode]:
        Tp = PriceDict[SecuCode]['C']
        return Tp
    else:
        return ClosePrice(SecuCode, Time, Tp=False)  # #  Sp  =  True? 更改股数,不更改价格
    
def Remove(RemoveL, Tag):
    NewTag = []
    for i, T in enumerate(Tag):
        if i not in RemoveL:
            NewTag.append(T)
    return NewTag

###################################################################################
def PriceFloorCalc(Secu, Time):
    Pf = PriceFloor
    SqlSt = '''select F002V_0116 from  (select F002V_0116 from tb_company_0116 where ob_orgid_0116=(
select ob_secid_0007 from tb_public_0007 where ob_seccode_0007='{Secu}' and F003V_0007 like'A%') and OB_VARYDATE_0116<to_date('{Time}','yyyy-mm-dd') order by  OB_VARYDATE_0116 desc )   where rownum=1'''.format(Secu=Secu[0:6], Time=str(Time))
    ResSt = Oracle.OracleSql(SqlSt)
    if len(ResSt) > 0:
        St = file.SQLtoVar(ResSt)
        if 'S' in St:
            Pf = Pf / 2
    return Pf

def UpDateRule(Rules, Time):
    global LastMonth
    ThisMoth = (Time - relativedelta(months=1)).month
    if ThisMoth != LastMonth:
        LastYMonth = Time - relativedelta(months=1)
        LastMonth = LastYMonth.month
        Now = LastYMonth.strftime('%Y%m')
        Rules = GetRule(Now)      
    return Rules    
def UpDateChuQuan(Holding, Time):
    SecuL = []
    for i, Hold in enumerate(Holding[Time][1:]):
        Secu = Hold['secu']
        SecuL.append("'" + Secu + "'")
    if len(SecuL) > 0:
        Sqls = "select secu_code,split_factor from equity_split where secu_code in ({0}) and trade_date='{1}'".format(",".join(SecuL), Time)
        ChuQuanDict = file.SQLtoDict(ToMySQL.SqlCommend(Sqls, 0), 0, 1)
        for i, Hold in enumerate(Holding[Time][1:]):
            Secu = Hold['secu']
            if Secu in ChuQuanDict:
                  Share = Hold['sellshare']
                  NewShare = int(Share / ChuQuanDict[Secu])
                  Holding[Time][1 + i]['sellshare'] = NewShare
    return Holding


def FreeCashRiskFree(Holding, Time):
    if Time in RiskFreeD.index:
        Holding[Time][0] = (1 + RiskFreeD.ix[Time].values[0] / TradingDay / 100) * Holding[Time][0]
    return Holding



###################################################################################
#               其他打印                                                                                                                                                      #
###################################################################################
def PrintPrecent(t, Time, Pprecent):
    Pprecent = True
    if Pprecent:
        try:
            if t % (int(len(TimeLine) / 10)) == 0:
                FinPre = str(round(t / len(TimeLine) * 100)) + '%'
                Status = str(Time) + " : " + FinPre
                file.Pnow(Status)
        except:
            a = 1
def PrintCostTime() :
    All = '\n' + '*' * 75 + '\n' + '总耗时  {0} 秒'.format(int(time.clock() - StartTime))
    print (All)
    WriteReport(SotName='Summary', Content=All, Mode='a')
###################################################################################
#                                                                                 #
#               这是报告生成                                                                                                                                              #
#                                                                                 #
###################################################################################
def WriteReport(SotName='', Content='', Mode='w', Mode2='write'):
    if Mode2 == 'write':
        if type(Content) == DataFrame:
            Content.to_csv(Mulu + '{0}{1}.csv'.format(SotName, FileName), mode=Mode, sep="\t")
        else:
            file.WriteACSV(Mulu + '{0}{1}.csv'.format(SotName, FileName), Content, Mode, 'gbk')
    elif Mode2 == 'figure':
        plt.savefig(Mulu + '{0}{1}.png'.format(SotName, FileName), figsize=(28.0, 5.0), dpi=200, bbox_inches='tight')
    elif Mode2 == 'zip':
        f = zipfile.ZipFile(Mulu + 'Zip/All{0}.zip'.format(FileName), 'w', zipfile.ZIP_DEFLATED) 
        f.write(Mulu + '{0}{1}.csv'.format('Summary', FileName), 'Summary.csv')
        f.write(Mulu + '{0}{1}.csv'.format('Error', FileName), 'Error.csv')
        f.write(Mulu + '{0}{1}.csv'.format('HoldDetail', FileName), 'HoldDetail.csv')
        f.write(Mulu + '{0}{1}.csv'.format('Return', FileName), 'Return.csv')
        f.write(Mulu + '{0}{1}.csv'.format('Hold', FileName), 'Hold.csv')
        f.write(Mulu + '{0}{1}.csv'.format('TradeHistory', FileName), 'TradeHistory.csv')
        f.write(Mulu + '{0}{1}.csv'.format('Rules', FileName), 'Rules.csv')
        f.write(Mulu + '{0}{1}.png'.format('Graph', FileName), 'Graph.png')
        f.write(Mulu + '{0}{1}.png'.format('Graph2', FileName), 'Graph2.png')
        f.close() 
    elif Mode2 == 'read':
        res = pd.read_csv(Mulu + '{0}{1}.csv'.format(SotName, FileName), encoding='gbk')
        return res
def CopyFile():
    def Copy(SotName, ExName):
        FromF = Mulu + '{0}{1}.{2}'.format(SotName, FileName, ExName)
        ToF = Mulu + '{0}/{0}{1}.{2}'.format(SotName, FileName, ExName)
        file.CopyFile(FromF, ToF)
    Copy(SotName='Summary', ExName='csv')
    Copy(SotName='Graph', ExName='png')
    Copy(SotName='TradeHistory', ExName='csv')
    
def ConvPre(Rate, Pre=True, Digit=2):
    if Pre:
        Rate = str(round(Rate * 100, Digit)) + '%'
    else:
        Rate = round(Rate , Digit)
    return Rate

 
def PrintStgStatics(Print=True):
    global Statistic, Dstg
    if len(Stg) > 0:
        Dstg = DataFrame(Stg)
        Statistic = DataFrame()
        R = Series()
        Dstg['ReturnV'] = Dstg['BuyPrice'] * Dstg['BuyShare'] * Dstg['Return']
        Dstg['Comm'] = np.round(Dstg['SellPrice'] * Dstg['SellShare'] * TaxRate, decimals=2)
        Statistic['Count'] = Dstg['Event'].groupby(Dstg['Event']).count()
    #     Statistic['Up'] = Dstg[Dstg['Return'] >= 0]['Return'].groupby(Dstg['Event']).count()
    #     Statistic['Down'] = Dstg[Dstg['Return'] < 0]['Return'].groupby(Dstg['Event']).count()
        Statistic['MeanRate'] = np.around(Dstg['Return'].groupby(Dstg['Event']).mean() * 100, decimals=2)
        Statistic['SumReturn'] = Dstg['ReturnV'].groupby(Dstg['Event']).sum().astype('int')
        Statistic['SumComm'] = Dstg['Comm'].groupby(Dstg['Event']).sum().astype('int')
        Statistic['SumNet'] = Statistic['SumReturn'] - Statistic['SumComm']
        Statistic.insert(0, 'Ratio', (Dstg[Dstg['Return'] >= 0]['Return'].groupby(Dstg['Event']).count().div(Statistic['Count'], fill_value=0) * 100).astype('int'))
        Statistic = Statistic.fillna(0)
        for Event in Statistic.index:
            EventCn = RuleTypeCode[int(Event)] if int(Event) != 0 else  '其他'
            if int(Event) != 0:
                R[Event] = EventCn
            else:
                R[str(Event)] = EventCn
        Statistic.insert(6, 'Cn', R)
        Statistic.sort()
        if Print:
            print(Statistic)
        WriteReport(SotName='Summary', Content=Statistic, Mode='a')

def PrintHoldDetail(Write=False):
    global Holding, LongShortRatio
    LongShortRatio = Series()
    All = 'date,secu,price,buytime,share,long/short\n'
    for time  in Holding:
        Val = Holding[time]
        Cash = Val[0]
        MktVal = Cash
        LongMktVal, ShortMktVal = 0, 0
        Line1 = ''
        for Hold in Val[1:]:
            if Hold['dre'] == 1:
               StkVal = Hold['todayprice'] * Hold['sellshare']
               LongMktVal += StkVal
            elif Hold['dre'] == 2:
                StkVal = Hold['todayprice'] * Hold['sellshare'] / MarginRate
                ShortMktVal += StkVal
            MktVal += StkVal
            Line1 += ',{0},{1},{2},{3},{4}\n'.format(Hold['secu'], Hold['buytime'], Hold['buyprice'], Hold['todayprice'], Hold['sellshare'], Hold['dre'])
        try:
            LongShortRatio[time] = LongMktVal / (LongMktVal + ShortMktVal)
        except:
            LongShortRatio[time] = 1
        Line0 = '{0},{1},{2}\n'.format(time, int(Cash), int(MktVal))
        All += Line0 + Line1
#     print(All)
    if Write:
        WriteReport(SotName='HoldDetail', Content=All)

def PrintHold(Write=False):
    global Holding, TimeL, MktValL, HoldRatio
    TimeL = []
    MktValL = []
    HoldRatio = Series()
    All = 'date,Cash,MarketValue,HoldingRatio\n'
    for time in Holding:
        Val = Holding[time]
        Cash = Val[0]
        MktVal = Cash
        for stock in Val[1:]:
           MktVal += stock['todayprice'] * stock['sellshare']
        TimeL.append(time)
        MktValL.append(MktVal)
        HoldR = 1 - int(Cash) / int(MktVal)
        HoldRatio[time] = HoldR
        HoldRS = str(round(HoldR * 100, 2)) + '%'
        Line = [time, int(Cash), int(MktVal), HoldRS ]
        All += ",".join(str(l) for l in Line) + '\n'
#     print(All)  
    if Write:
        WriteReport(SotName='Hold', Content=All)
        
def PrintStg(Write=False):
    global Stg, TurnOver, Dstg
    TurnOver = 0
    All = 'Secu,Long/Short,Buytime,BuyPrice,BuyShare,SellTime,SellPrice,SellShare,Event,EventCn,TagDay,HoldDay,Rate,Return\n'
    for P  in Stg:
        Secu = P['Secu']
        BuyTime = P['BuyTime']
        BuyPrice = P['BuyPrice']
        BuyShare = P['BuyShare']
        SellTime = P['SellTime']
        SellPrice = P['SellPrice']
        Dre = P['Dre']
        SellShare = P['SellShare']
        Event = P['Event']
        EventCn = RuleTypeCode[int(P['Event'])] if int(P['Event']) != 0 else  '其他'
        Length = P['Length']
        TagDay = P['TagDay']
        Rate = str(round(P['Return'] * 100, 2)) + "%"
        Return = int(P['BuyPrice'] * P['BuyShare'] * P['Return'])
        Line = [Secu, Dre, BuyTime, BuyPrice, BuyShare, SellTime, SellPrice, SellShare, Event, EventCn , TagDay, Length, Rate, Return]
        Line = ",".join(str(l) for l in Line) + '\n'
        All += Line
        TurnOver += int(P['SellPrice'] * P['SellShare'])
    if Write:
        WriteReport(SotName='TradeHistory', Content=All)
        
def PrintReturn():
    def GetIndexD():
        IndexD = DataFrame()
        if int(Begin[0:4]) < 2005:
            IndexSQL1 = '''SELECT trade_date ,close_price HS300 FROM index_price WHERE secu_code = '000300_SH_IX'
AND trade_date>='2005-01-04' and trade_date<='{0}'  order by  trade_date asc '''.format(End)
            IndexSQL2 = '''SELECT trade_date ,close_price SZZS FROM index_price WHERE secu_code = '000001_SH_IX'
AND trade_date<='2005-01-04' and trade_date>='{0}'  order by  trade_date asc '''.format(Begin)
            IndexD1 = psql.read_sql(IndexSQL1, con=ToMySQL.Conn208, index_col='trade_date')
            IndexD2 = psql.read_sql(IndexSQL2, con=ToMySQL.Conn208, index_col='trade_date')
            IndexD1 = IndexD1.pct_change()
            IndexD2 = IndexD2.pct_change()
            IndexD['HS300'] = IndexD1['HS300'].add(IndexD2['SZZS'], fill_value=0)
            IndexD['Portfolio'] = MktVals.pct_change()
            IndexD['Portfolio'][0] = MktVals[0] / BegTotMoney - 1
        else:
            if NoramlIndex:
                IndexSQL = '''SELECT trade_date ,close_price HS300 FROM index_price WHERE secu_code = '000300_SH_IX'
AND trade_date>='{0}' and trade_date<='{1}'  order by  trade_date asc '''.format(Begin, End)
                IndexD = psql.read_sql(IndexSQL, con=ToMySQL.Conn208, index_col='trade_date')
            else:
                IndexSQL = '''SELECT trade_date ,close_price HS300 FROM index_price WHERE secu_code = '000001_SH_IX'
AND trade_date>='{0}' and trade_date<='{1}'  order by  trade_date asc '''.format(Begin, End)
                IndexD = psql.read_sql(IndexSQL, con=ToMySQL.ConnLocal, index_col='trade_date')
            IndexD['Portfolio'] = MktVals
            IndexD = IndexD.pct_change()
            IndexD['Portfolio'][0] = MktVals[0] / BegTotMoney - 1
        return IndexD
    global Begin, End, AbsReturn, RelativReturn, IndexD, ReturnCsv
    MktVals = Series(MktValL, index=TimeL)
    IndexD = GetIndexD()
    AbsReturn = (1 + IndexD).cumprod() - 1
    AbsReturn.index = AbsReturn.index.to_datetime()
    RiskFreeS = (1 + RiskFreeD['F003N_0160'] / TradingDay / 100).cumprod() - 1
#     RiskFreeS.reindex(AbsReturn.index,method='pad')
    AbsReturn['RiskFree'] = RiskFreeS
    RelativReturn = DataFrame()
    RelativReturn['Portfolio'] = AbsReturn['Portfolio'] - AbsReturn['HS300']
    RelativReturn['RiskFree'] = AbsReturn['RiskFree'] - AbsReturn['HS300']
    ReturnCsv = IndexD.copy()
    ReturnCsv.insert(2, 'GC001', RiskFreeD['F003N_0160'] / TradingDay / 100)
    ReturnCsv.insert(3, 'HS300 Net Worth', AbsReturn['HS300'] + 1)
    ReturnCsv.insert(4, 'Portfolio Net Worth', AbsReturn['Portfolio'] + 1)
    ReturnCsv.insert(5, 'GC001 Net Worth', AbsReturn['RiskFree'] + 1)
    WriteReport(SotName='Return', Content=ReturnCsv)

def PrintError(Write=False):
    All = 'Type,Time,Secu,Event,EventCn,Price,Money\n'
    for Err in Error:
        Line = [Err[0], Err[1], Err[2], Err[3], RuleTypeCode[int(Err[3])] if int(int(Err[3])) != 0 else  '其他', Err[4], Err[5]]
        Line = ",".join(str(l) for l in Line) + '\n'
        All += Line 
#     print(All)
    if Write:
        WriteReport(SotName='Error', Content=All)
        
def PrintEventList(Write=False):
    All = 'time,secu,tagday,prob,event,eventcn,eventnum\n'
    for Time in Eventing:
        Events = Eventing[Time]
        for E in Events:
            Secu = E['secu']
            Day = E['day']
            Event = E['event']
            EventCn = RuleTypeCode[int(Event)] if int(Event)!= 0 else  '其他'
            Prob = E['prob']
            Num = E['num']
            Line = [Time.date(), Secu, Day, Prob, Event, EventCn, Num]
            Line = ",".join(str(l) for l in Line) + '\n'
            All += Line 
    print(All)
    if Write:
        WriteReport(SotName='EventList', Content=All)
        
def WriteRules(Rmonth, Rules, Mode):
    Y = int(Rmonth[0:4])
    M = int(Rmonth[4:6])
    ThisTime = datetime.date(Y, M, 1) + relativedelta(months=1)
    Rmonth = ThisTime.strftime('%Y%m')
    All = 'Month,Event,Cn,Long/Short,MaxData,Prob,ExceptReturn,Number\n'
    for i  in sorted(Rules.items(), key=lambda Rules:Rules[0]):
        Line = [Rmonth, i[0][0:6], i[1][3], i[1][0], i[1][1], ConvPre(i[1][4]), ConvPre(i[1][2]), i[1][5]]
        Line = ",".join(str(l) for l in Line) + '\n'
        All += Line
    WriteReport(SotName='Rules', Content=All, Mode=Mode)
    

def Pg():
    global AbsReturn, RelativReturn, HoldRatio, LongShortRatio
#     AbsReturn['abs']=AbsReturn['Portfolio']-AbsReturn['Market']
    fig, axes = plt.subplots(nrows=2, ncols=2)
    fig.set_size_inches(18.5, 10.5)
    Gp = (AbsReturn + 1).plot(ax=axes[0, 0], ylim=[-0.5, 6], color=['g', 'r', 'b'])
    Rp = (RelativReturn + 1).plot(ax=axes[1, 0], ylim=[-0.5, 6], color=['r', 'b'])
    Hp = HoldRatio.plot(ax=axes[0, 1], ylim=[0, 1], color='k')
    Ls = LongShortRatio.plot(ax=axes[1, 1], ylim=[0, 1], color='k')
    Gp.set_title('Absolute Return Net Worth');
    Gp.set_xlabel("")
    Rp.set_title('Relative Return Net Worth')
    Rp.set_xlabel("")
    Hp.set_title('Positions Rate')
    Ls.set_title('Long/Short Rate')
    Gp.xaxis.set_major_formatter(dates.DateFormatter('%y-%m'))
    Rp.xaxis.set_major_formatter(dates.DateFormatter('%y-%m'))
    Hp.xaxis.set_major_formatter(dates.DateFormatter('%y-%m'))
    Ls.xaxis.set_major_formatter(dates.DateFormatter('%y-%m'))
    WriteReport(SotName='Graph', Content=plt, Mode2='figure')
    
def Pg2():
    BgY, EdY = AbsReturn.index[0].year, AbsReturn.index[-1].year
    if int((EdY - BgY + 1) ** 0.5) - (EdY - BgY + 1) ** 0.5 == 0:
        Sqare = int((EdY - BgY + 1) ** 0.5) 
    else:
        Sqare = int((EdY - BgY + 1) ** 0.5) + 1
    if Sqare * (Sqare - 1) >= EdY - BgY + 1: 
        rSqare = Sqare - 1 
    else:
        rSqare = Sqare
    fig, axes = plt.subplots(nrows=rSqare, ncols=Sqare)
    fig.set_size_inches(9.25 * Sqare, 5.258 * rSqare)
    AbsREach = IndexD
    AbsREach.index = AbsREach.index.to_datetime()
    x, y = 0, 0
    for Year in range(BgY, EdY + 1):
        if y >= Sqare:
            x += 1
            y = 0
        if x == y == 0:
            legend = True
        else:
            legend = False
        if rSqare == Sqare == 1:
            A = ((1 + AbsREach[str(Year)]).cumprod()).plot(color=['g', 'r'], legend=legend)
        else:
            A = ((1 + AbsREach[str(Year)]).cumprod()).plot(ax=axes[x, y], color=['g', 'r'], legend=legend)
        A.set_title(str(Year));
        A.xaxis.set_major_formatter(dates.DateFormatter('%y-%m'))
        y += 1
    WriteReport(SotName='Graph2', Content=plt, Mode2='figure')    
    plt.clf()

def PrintSummary(Print=True):
    global TurnOver, AbsReturn, IndexD
    def AnnualizedRate(Rate, TotolDay):
        if Rate > -1:
            Rate = (1 + Rate) ** (365 / TotolDay.days) - 1
        else:
            Rate = (1 + Rate) ** (365 / TotolDay.days) - 1
        return Rate
    def IrRatio(IndexD, ReAnnualReturn):
        TrackError = (IndexD['Portfolio'] - IndexD['HS300']).std() * (TradingDay ** 0.5)
        Ir = ReAnnualReturn / TrackError
        return Ir
    def MaxDrawDown(AbsReturn):
        A = AbsReturn['Portfolio'].fillna(0) + 1
        ToTime = np.argmax(np.maximum.accumulate(A) - A)
        FromTime = np.argmax(A[:ToTime])
        MaxRurn = 1 - A[ToTime] / A[FromTime]
        return [-MaxRurn, str(FromTime)[0:10], str(ToTime)[0:10]]
    def Beta(ReturnCsv):
        A = ReturnCsv.fillna(0)
        cov = np.cov(A['HS300'], A['Portfolio'])
        beta = cov[1, 0] / cov[0, 0]
        return beta
    def Std(ReturnCsv):
        A = ReturnCsv.fillna(0)
        std = A['Portfolio'].std()
        return std
    def EndMoney(AbsReturn):
        Endmoney = int((AbsReturn['Portfolio'][-1:].values[0] + 1) * BegTotMoney)
        return Endmoney
    All = []
    All.append('*' * 75)
    TotolDay = AbsReturn.index[-1] - AbsReturn.index[0]
    Endmoney = EndMoney(AbsReturn)
    All.append('Begin:{0},End:{1},TotolDay:{2},EndMoney:{3}'.format(Begin, End, TotolDay.days, Endmoney))
    All.append('*' * 75)
    All.append('DayLength:{0},OneDayBuyMax:{1},OneShareBuyMax:{2}'.format(DayLength, round(OneDayBuyMax, 2), round(OneShareBuyMax, 2)))
    All.append('*' * 75)
    All.append('ProbExp:{0},LongProb:{1},ShortProb:{2},LongEr:{3},ShortEr:{4}'.format(ProbExp, LongProb, ShortProb, LongEr, ShortEr))
    All.append('*' * 75)
    All.append('BuyLong:{0},BuyShort:{1},RuleType:{2},ExtraRule:{3},RollBack:{4}'.format(BuyLong, BuyShort, ExtraRule, ExRuSheet if ExtraRule > 0 else 0, RollBack))
    All.append('*' * 75)
    All.append('EventNum:{0},Signal:{1},BuySuccess:{2},Win:{3},GetTar:{4}'.format(EventNum, Signal, BuySuccess, Win, GetTar))
    All.append('*' * 75)
    TurnOverRate = ConvPre(TurnOver / BegTotMoney, False)
    CommRatio = ConvPre(Commission / BegTotMoney)
    All.append('TurnOverRate:{0},TurnOver:{1},Commission:{2},CommissionRatio:{3}'.format(TurnOverRate, TurnOver, int(Commission), CommRatio))
    All.append('*' * 75)
    AbAnnualReturn = AnnualizedRate(AbsReturn[-1:]['Portfolio'].values[0], TotolDay)
    ReAnnualReturn = AbAnnualReturn - AnnualizedRate(AbsReturn[-1:]['HS300'].values[0], TotolDay)
    All.append('AbsAnnualReturn:{0},RelAnnualReturn:{1}'.format(ConvPre(AbAnnualReturn), ConvPre(ReAnnualReturn)))
    All.append('*' * 75)
    Ir, beta, std, MaxDr = IrRatio(IndexD, ReAnnualReturn), Beta(ReturnCsv), Std(ReturnCsv), MaxDrawDown(AbsReturn)
    All.append('Std:{0},IR:{1},Beta:{2},MaxDrawDown:{3} {4} to {5}'.format(ConvPre(std), ConvPre(Ir, False), ConvPre(beta, False), ConvPre(MaxDr[0]), MaxDr[1], MaxDr[2]))
    All.append('*' * 75)
    if Print:
        print("\n".join(All))
    WriteReport(SotName='Summary', Content="\n".join(All) + "\n")

def PrintReport(Print=True):
    global Stg, Holding, ret_index
    PrintStg(True)
    PrintHold(True)
    PrintHoldDetail(True)
    PrintError(True)
    PrintReturn()
    Pg()
    Pg2()
    PrintSummary(Print)
    PrintStgStatics(Print) 
    CopyFile()
    WriteReport(Mode2='zip')
    PrintCostTime()
def MakeFileName():
    if BuyLong == 1:
        if BuyShort == 1:
            LS = 3
        else:
            LS = 1
    else:
        LS = 2
    if LS == 1:
        Pe = '{EP},{LP},{LE}'.format(EP=ProbExp, LP=LongProb, LE=LongEr)
    elif LS == 2:
        Pe = '{EP},{SP},{SE}'.format(EP=ProbExp, SP=ShortProb, SE=ShortEr)
    elif LS == 3:
        Pe = '{EP},{LP},{SP},{LE},{SE}'.format(EP=ProbExp, LP=LongProb, SP=ShortProb, LE=LongEr, SE=ShortEr)
    FileName = '_{B}_{E}_LS={LS}_D={Dl}_L={Limit}_Pe={Pe}_R={Er},{Rb}'.format(
        B=Begin[2:-2],
        E=End[2:-2],
        LS=LS,
        Dl=DayLength,
        Limit='{},{},{}'.format(round(OneDayBuyMax, 2), round(OneShareBuyMax, 2), Stoploss),
        Pe=Pe,
        Er=str(ExtraRule) + '_' + ExRuSheet if ExtraRule > 0 else 0,
        Rb=RollBack)
    return FileName

###################################################################################
#                                                                                 #
#               其他Moke函数                                                                                                                                            #
#                                                                                 #
###################################################################################    
def TopNum(BuyStockList, Top):
    TopNumL = []
    BuyStockList2 = []
    for Stock in BuyStockList:
        TopNumL.append(Stock[5])
    TopNumL.sort(reverse=True)
    TopNumL = TopNumL[0:Top]
    for Stock in BuyStockList:
        if Stock[5] in TopNumL and len(BuyStockList2) < Top:
            BuyStockList2.append(Stock)
    return BuyStockList2

def UpPortHold(BuyStockOne):
    HoldPair = {}
    HoldPair['split'] = 0
    HoldPair['buytime'] = BuyStockOne[0]
    HoldPair['secu'] = BuyStockOne[1]
    HoldPair['buyprice'] = BuyStockOne[2]
    HoldPair['todayprice'] = BuyStockOne[2]
    HoldPair['holdtime'] = BuyStockOne[3]  # 按昨收盘算,今日不算第一天
    HoldPair['tagtime'] = BuyStockOne[3]
    HoldPair['dre'] = BuyStockOne[4]
    HoldPair['event'] = BuyStockOne[6]
    HoldPair['prob'] = BuyStockOne[7]
    HoldPair['id'] = str(BuyStockOne[8])
    PortHold[BuyStockOne[0]]['T0'].append(HoldPair)
    
def AddT0Port(BuyStockList, Time):
    for B in BuyStockList:
        UpPortHold(B)

def GerSplitDict(Hold, Wait, EventList, Time, Moke2=False):
    SecuS, SecuSo, SecuL, SecuLo, SecuD = '', '', [], [], {}
    if Moke2 == False:
        for Secu in Hold:
            if 'secu' in Secu:
                SecuD[Secu['secu']] = {}
        for Secu in Wait: 
            if 'secu' in Secu:   
                SecuD[Secu['secu']] = {}
    else: 
        for Secu in Hold: 
            SecuD[Secu] = {}
    for Secu in EventList:
        if 'secu' in Secu:
            if Secu['secu'] == '300168_SZ_EQ' and Debug == 1:
                print(Secu['secu'])
            SecuD[Secu['secu']] = {}
    if len(SecuD) > 0:
        for k in SecuD:
            SecuL.append("'" + k + "'")
        SecuS, SecuSo = ','.join(SecuL) , ','.join(SecuLo)

        SqlTc = "select secu_code,close_price from equity_price where secu_code in ({0}) and trade_date='{1}' and volume>0".format(SecuS, Time)
        SqlTo = "SELECT ob_seccode_0160,F003N_0160 FROM JUCHAO.TB_TRADE_0160 where OB_SECCODE_0160 in ({Secu})  and OB_TRADEDATE_0160=to_date('{Time}','yyyy-mm-dd') and F004N_0160>0  and F023V_0160 like'A%'".format(Secu=SecuSo, Time=str(Time))
        ResTc = ToMySQL.SqlCommend(SqlTc, 0)
        ResTo = Oracle.OracleSql(SqlTo)
        if len(ResTc) > 0:
            for Tc in ResTc:
                SecuD[Tc[0]]['C'] = round(float(Tc[1]), 2)
        if len(ResTo) > 0:
            for To in ResTo:
                if To[0][0:1] in ['0', '3']:
                    code = To[0] + '_SZ_EQ'
                elif To[0][0:1] == '6':
                    code = To[0] + '_SH_EQ'
                SecuD[code]['O'] = round(float(To[1]), 2)
        return SecuD
    else:
        return {}
def GetTimeDf(Begin, End):
    TimeLineSQL = '''SELECT trade_date,close_price FROM index_price WHERE secu_code = '000300_SH_IX'
    AND trade_date>='{0}' and trade_date<='{1}'  order by  trade_date asc '''.format(Begin, End)
    TimeLineT0SQL = '''SELECT close_price FROM index_price WHERE secu_code = '000300_SH_IX'
    AND trade_date<'{0}'  order by  trade_date desc limit 1 '''.format(Begin)
    TimeLine = file.SQLtoList(ToMySQL.SqlCommend(TimeLineSQL, 0), 0) 
    TimeData = file.SQLtoDict(ToMySQL.SqlCommend(TimeLineSQL, 0), 0) 
    TimeDict = OrderedDict() 
    for i, Time in enumerate(TimeLine):
        if i > 0:
            T0 = TimeData[TimeLine[i - 1]]
        else:
            T0 = file.SQLtoVar(ToMySQL.SqlCommend(TimeLineT0SQL, 0)) 
        T1 = round(TimeData[Time] / T0 - 1, 4)
        if len(TimeLine) > i + 1  :
            T2 = round(TimeData[TimeLine[i + 1]] / T0 - 1, 4)
        else:
            T2 = 'Nan'
        if len(TimeLine) > i + 2 :
            T3 = round(TimeData[TimeLine[i + 2]] / T0 - 1, 4)
        else:
            T3 = 'Nan'
        if len(TimeLine) > i + 3 :
            T4 = round(TimeData[TimeLine[i + 3]] / T0 - 1, 4) 
        else :
            T4 = 'Nan'
        if len(TimeLine) > i + 4 :
            T5 = round(TimeData[TimeLine[i + 4]] / T0 - 1, 4) 
        else:
            T5 = 'Nan'
        TimeDict[Time] = [T1, T2, T3, T4, T5]

    TimeDf = DataFrame(TimeDict, index=['T1', 'T2', 'T3', 'T4', 'T5'], dtype=np.dtype(np.float64))
    TimeDf = TimeDf.T
    return TimeDf
          
def StatPortHold():
    global T0p, T1p, T2p, T3p, T4p, T5p
    All = 'Day,Secu,HoldDays,Event,EventCn,Prob,T0,T1,T2,T3,T4,T5,Return\n'
    for Time in PortHold:
        Today = PortHold[Time]
        ThisDay = ''
        Cccode, CcDay, CcEvent, CcProb, T0pL, T1pL, T2pL, T3pL, T4pL, T5pL, ZhangFuL = [], [], [], [], [], [], [], [], [], [], []
        T0p, T1p, T2p, T3p, T4p, T5p, ZhangFu = '', '', '', '', '', '', ''
        for Secu in Today['T0']:
            Cccode.append(Secu['secu'])
            CcDay.append(Secu['tagtime'])
            CcEvent.append(Secu['event'])
            CcProb.append(Secu['prob'])
            T0pL.append(Secu['todayprice'])
        for TNa in range(1, 6):
            if 'T' + str(TNa) in Today:
                for Secu in Today['T' + str(TNa)]:
                    locals()["T" + str(TNa) + "pL"].append(Secu['todayprice'])
        for i, Code in   enumerate(Cccode):
            Secu = Cccode[i]
            TagTime = CcDay[i]
            Event = CcEvent[i]
            Prob = CcProb[i]
            for TNb in range(0, 6):
                if i < len(locals()["T" + str(TNb) + "pL"]):
                    globals()["T" + str(TNb) + "p"] = locals()["T" + str(TNb) + "pL"][i]
                else:
                    globals()["T" + str(TNb) + "p"] = False
            if T5p and T0p:
                ZhangFu = T5p / T0p - 1
                ZhangFuL.append(ZhangFu)
            try:
                thisline = ",".join([str(Time), Secu, str(TagTime), str(Event),  RuleTypeCode[int(Event)] if int(Event)!= 0 else  '其他', str(Prob), str(T0p), str(T1p), str(T2p), str(T3p), str(T4p), str(T5p), ConvPre(ZhangFu) + '\n'])
            except:
                thisline = ""
            ThisDay += thisline
        if len(ZhangFuL) > 0:
            Mean = sum(ZhangFuL) / len(ZhangFuL)
        else:
            Mean = 0
        Title = '{0},HoldDays,Event,EventCn,T0,T1,T2,T3,T4,T5,{1}\n'.format(Time, ConvPre(Mean, False, 4))
#         All += Title + ThisDay
        All += ThisDay
#     print(All)
    WriteReport(SotName='PortHold', Content=All)
    Dstg = WriteReport('PortHold', '', '', 'read')
    Dstg['r2'] = Dstg['T5'] / Dstg['T0'] - 1
    Statistic = DataFrame()
    R = Series()
    Statistic['Count'] = Dstg['Event'].groupby(Dstg['Event']).count()
    Statistic['Up'] = Dstg[Dstg['r2'] >= 0]['r2'].groupby(Dstg['Event']).count()
    Statistic['Down'] = Dstg[Dstg['r2'] < 0]['r2'].groupby(Dstg['Event']).count()
    Statistic['MeanRate'] = np.around(Dstg['r2'].groupby(Dstg['Event']).mean() * 100, decimals=2)
    Statistic.insert(0, 'Ratio', (Statistic['Up'].div(Statistic['Count'], fill_value=0) * 100).astype('int'))
    Statistic = Statistic.fillna(0)
    Statistic['Cn'] = 'NA'
    for Event in Statistic.index:
        EventCn =  RuleTypeCode[int(Event)] if int(Event)!= 0 else  '其他'
        Statistic.loc[Event, 'Cn'] = EventCn
    Statistic.sort()
    WriteReport(SotName='Summary', Content=Statistic, Mode='w')
def PrintPortHold():
    All = 'Day\tsecu.sc\tsecu.d\tsecu.ac\tsecu.up\tsecu.id\tsecu.src\n'
    for Time in PortHold:
        Today = PortHold[Time]
        ThisDay = ''
        Cccode, CcDay, CcEvent, CcProb, CcId, CcTyp = [], [], [], [], [], []
        for Secu in Today['T0']:
            Cccode.append(str(Secu['secu']))
            CcDay.append(str(Secu['tagtime']))
            CcEvent.append(str(Secu['event']))
            CcProb.append(str(Secu['prob']))
            CcId.append(str(Secu['id']))
            CcTyp.append('1')
        try:
            thisline = "\t".join([str(Time), ",".join(Cccode), ",".join(CcDay), ",".join(CcEvent), ",".join(CcProb) , ",".join(CcId), ",".join(CcTyp) + '\n'])
        except:
            thisline = ""
        ThisDay += thisline
        All += ThisDay
    WriteReport(SotName='PortHold', Content=All)

def StatPortReturn():
    global PortReturnDf, TimeDf
    TowReturn = {}
    PortReturnDf = DataFrame(PortReturn)
    PortReturnDf = PortReturnDf.T
    TowReturn['PortAbsReturn'] = PortReturnDf
    PortReturnDf = PortReturnDf - TimeDf
    PortReturnDf = np.round(PortReturnDf, decimals=4)
    TowReturn['PortRelReturn'] = PortReturnDf
    TowReturn['IndexReturn'] = TimeDf
    for Rer in TowReturn:
        RR = TowReturn[Rer]
        Dayu = RR[RR > 0].count().sum()
        Dengyu = RR[RR == 0].count().sum()
        Xiaoyu = RR[RR < 0].count().sum()
        RatioDayu = ConvPre(Dayu / (Dayu + Dengyu + Xiaoyu))
        RatioDengyu = ConvPre(Dengyu / (Dayu + Dengyu + Xiaoyu))
        RatioXiaoyu = ConvPre(Xiaoyu / (Dayu + Dengyu + Xiaoyu))
        Ratio = '{0}:Postive:{1},Equal:{2},Negative:{3}'.format(Rer, RatioDayu, RatioDengyu, RatioXiaoyu)
        WriteReport(SotName=Rer, Content=Ratio + '\n')
        WriteReport(SotName=Rer, Content=RR, Mode='a')
        print('*' * 75)
        print(Ratio)
def PrintMoke():
    StatPortReturn()
#     StatPortHold()
    PrintPortHold()

###################################################################################
#                                                                                 #
#               这是模拟全流程
#                                                                                 #
###################################################################################

def Moke(Pprecent=True):
    global StartTime
    StartTime = time.clock()
    print('*' * 75)
    global EventNum, Signal, BuySuccess, Win, GetTar, Holding, Rules
    for t, Time in enumerate(TimeLine):
        if Time == datetime.date(2014, 6, 25) and Debug == 1:
            print(Time)
        PrintPrecent(t, Time, Pprecent)
        Events = GetEventSql(TimeLine[t - 1] if t > 0 else 0, Time)
        Rules = UpDateRule(Rules, Time)
        if t != 0:
            Holding[Time] = deepcopy(Holding[TimeLine[t - 1]])
            Waiting[Time] = deepcopy(Waiting[TimeLine[t - 1]])
            TotMoney = Holding[Time][0]
        else:
            Holding[Time] = [BegTotMoney]
            Waiting[Time] = []
        #################################### 生成事件策略
        EventList = GetEventList(Events, Rules)
        Eventing[Time] = EventList
        #################################### 股价表
        PriceDict = GerPriceDict(Holding[Time][1:], Waiting[Time], EventList, Time)
        #################################### 处理除权(改变持股数量)
        Holding = UpDateChuQuan(Holding, Time)
        #################################### 持有股票,卖出判断 并卖出
        Holding = SellHold(Holding, Time, PriceDict, OC='Open')
        #################################### 待买入股票,买入判断
        RemoveL = []
        BuyStockList = []
        for i, Wait in enumerate(Waiting[Time]):
            Secu, Max, Day, Dre, Eve = Wait['secu'], Wait['max'], Wait['day'] - 1, Wait['dre'], Wait['event']
            if Day > 0:
                if Secu == '300168_SZ_EQ':
                    print(Secu)
                if Secu in PriceDict and 'O' in PriceDict[Secu]:
                    BuyP = PriceDict[Secu]['O']
                    if BuyP:
                        Lp = ClosePrice(Secu, Time, Tp=False, Sp=True)
                        FuDu = round(BuyP / Lp - 1, 4)
                        if Dre == 1:
                            if FuDu < PriceFloorCalc(Secu, Time):
                              #  if Max > FuDu:#此条件待研究
                                BuyStockList.append([Time, Secu, BuyP, Day, Dre, Max, Eve])
                                RemoveL.append(i)
                        elif Dre == 2:
                            if FuDu > -PriceFloorCalc(Secu, Time):
                               #  if  Max < FuDu :#此条件待研究
                                BuyStockList.append([Time, Secu, BuyP, Day, Dre, Max, Eve])
                                RemoveL.append(i)
                else:
                    Waiting[Time][i]['day'] = Day
            elif Day == 0:
                RemoveL.append(i)
        Waiting[Time] = Remove(RemoveL, Waiting[Time])
        for Wait in Waiting[Time]:
            Secu , BuyP = Wait['secu'], Wait['baseprice']
            Error.append(['Wait Floor', Time, Secu, Eve, BuyP, 0])
        #################################### 新事件,买入判断
        for Event in EventList:
            Secu, Dre, Day, Max, Eve = Event['secu'] , Event['dre'], Event['day'], Event['max'], Event['event']
            if Secu == '300168_SZ_EQ' and Debug == 1:
                print(Secu)
            if Secu in PriceDict and 'O' in PriceDict[Secu]:
                Tp = PriceDict[Secu]['O']
                Lp = ClosePrice(Secu, Time, Tp=False, Sp=True)  # 昨收盘,除权后
                if Tp and Lp:
                    D = 0
                    FuDu = round(Tp / Lp - 1, 4)
                    if Dre == 1:
                        if  D < Day and FuDu < PriceFloorCalc(Secu, Time):
#                             if Max > FuDu:#此条件待研究
                                BuyStockList.append([Time, Secu, Tp, Day, Dre, Max, Eve])
                        else:
                            WaitStock(Time, Secu, Lp, Day, Dre, Max, Eve)
                            Error.append(['Wait Floor', Time, Secu, Eve, Tp, 0])
                    elif Dre == 2:
                        if D < Day and FuDu > -PriceFloorCalc(Secu, Time):
#                             if Max < FuDu:#此条件待研究
                                BuyStockList.append([Time, Secu, Tp, Day, Dre, Max, Eve])
                        else:
                            WaitStock(Time, Secu, Lp, Day, Dre, Max, Eve)
                            Error.append(['Wait Floor', Time, Secu, Eve, Tp, 0])
        #################################### 买入股票
#         BuyStockList = TopNum(BuyStockList, Top)  # 测试
        TodayEachBuy = len(BuyStockList)
        if TodayEachBuy > 0:
            ToBuyStock(BuyStockList, t, Time, TodayEachBuy)
        #################################### 持有股票,卖出判断 并卖出
        Holding = SellHold(Holding, Time, PriceDict, OC='Close')
        #################################### 更新持股的最新收盘价
        for i, Hold in enumerate(Holding[Time][1:]):
            Secu = Holding[Time][i + 1]['secu']
            if Secu == '300168_SZ_EQ' and Debug == 1:
                print(Secu)
            Holding[Time][i + 1]['todayprice'] = UpDataLastPrice2(Secu, Time, PriceDict)
        ################################### 止损
        Holding = StopLoss(Holding, Time)
        #################################### 现金收取无风险收益
#         Holding = FreeCashRiskFree(Holding, Time)
    PrintReport(Pprecent) 

###################################################################################
#                                                                                 #
#               任务函数                                                                                                                                                      #
#                                                                                 #
###################################################################################    
def ToDayStock():
    Time = datetime.datetime.now()
    def NowF(Time):
        LastYMonth = Time - relativedelta(months=1)
        LastMonth = LastYMonth.month
        Now = LastYMonth.strftime('%Y%m')
        return Now
    Rules = GetRule(NowF(Time))      
    Events = GetEventM(Time - relativedelta(days=3), Time)
    EventList = GetEventList(Events, Rules)
    EventList = sorted(EventList, key=lambda EventList: EventList['prob'], reverse=True)
    Eventing[Time] = EventList
    PrintEventList()
    
def MultTask(Way):
    global OneDayBuyMax, OneShareBuyMax, RollBack, DayLength, LongProb, BuyLong, BuyShort, FileName, MaxDayCalc, Rules
    MTime = time.clock()
    Way = Way
    Mult = {'RollBack':[1, 2, 3, 4, 5, 6, 7, 8, 9 , 10],
          'OneDayBuyMaxS':[1, 2, 3, 4, 5, 6, 7, 8, 9 , 10],
          'OneShareBuyMax':[1, 2, 3, 4, 5, 6, 7, 8, 9 , 10],
          'DayLength':[1, 2, 3, 4, 5, 6, 7, 8, 9 , 10, 11, 12, 13, 14, 15, 16, 17, 18, 19 , 20, 21, 22, 23, 24, 25, 26, 27, 28, 29 , 30],
          'LongProb':[0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8],
          'BuyLong':[0, 1] ,
          'BuyShort':[0, 1] ,
          'Stoploss':[0, 0.05, 0.1, 0.15, 0.2],
          'Stopwin':[0, 0.05, 0.1, 0.15, 0.2],
          'ExRuSheet':['R1', 'R1B', 'R2', 'R2B', 'R3', 'R3B', 'S1', 'S2'],
          "ExtraRule":[0, 1, 2],
          'MaxDayCalc':[1, 2, 3, 4, 5, 6, 7, 8, 9 , 10, 11, 12, 13, 14, 15, 16, 17, 18, 19 , 20, 21, 22, 23, 24, 25, 26, 27, 28, 29 , 30],
          'Seve':[1, 2, 3, 4, 5, 6, 7, 8, 9 , 10, 11, 12, 13, 14, 15, 16, 17, 18, 19 , 20, 21, 22, 23, 24, 25, 26, 27, 28, 29 , 30, 31, 32, 33]
          , }
    for i in Mult[Way]:
        global Holding, Waiting, Eventing, Stg, Error, MonthRule, MktValL, TimeL, EventNum, Signal, BuySuccess , Win, GetTar, Commission
        globals()[Way] = i
        print('For Each {0}: Pamamter {1}'.format(Way, i))
        Holding, Waiting, Eventing, Stg, Error, MonthRule = OrderedDict(), OrderedDict(), OrderedDict(), [], [], OrderedDict()
        MktValL, TimeL = [], []
        EventNum, Signal, BuySuccess , Win, GetTar = 0, 0, 0, 0, 0
        Commission = 0
        if 'Seve' in globals().keys():
            ExtraRules = file.ExcelToDict(RuleXlsx, Key=0, Val=1, HasTitle=0, StName=ExRuSheet)
            j = 0
            for Rule in ExtraRules:
                j += 1
                if j == Seve:
                    i = Rule
        FileName = MakeFileName()  
        FileName += '_{0}={1}'.format(Way, i)
        Rules = GetRule() 
        Moke(Pprecent=False)  # 模拟:
    print('\n' + '*' * 75 + '\n' + '总耗时  {0} 秒'.format(int(time.clock() - MTime)))
###################################################################################
#                                                                                 #
#               这是Moke3                                                          #                                                                                    #
#                                                                                 #
###################################################################################   
            
def Moke3(Pprecent=True):
    print('*' * 75)
    global EventNum, Signal, BuySuccess, Win, GetTar, Holding, Rules
    global StartTime
    StartTime = time.clock()
    for t, Time in enumerate(TimeLine):
        if Time == datetime.date(2014, 6, 30) and Debug == 1:
            print(Time)
        PortHold[Time] = {}
        PortReturn[Time] = {}
        PrintPrecent(t, Time, Pprecent)
        Events = GetEventM(TimeLine[t - 1] if t > 0 else 0, Time)  # GetEventSql , GetEventM
        Rules = UpDateRule(Rules, Time)
        #################################### 生成事件策略
        EventList = GetEventList(Events, Rules)
        Eventing[Time] = EventList
        #################################### 生成事件策略
        PricePortHold = []
        for Tback in range(1, 6):
            if t - Tback >= 0:
                ThisTime = TimeLine[t - Tback]
                PortHold[ThisTime]
                for Secu in PortHold[ThisTime]['T0']:
                    PricePortHold.append(Secu['secu'])
        PriceDict = GerPriceDict(PricePortHold, "", EventList, Time, Moke2=True, GetSp=True)
        ############################################################################# 待买入股票,买入判断
        BuyStockList = []
        ############################################################################# 新事件,买入判断
        for Event in EventList:
            Secu, Dre, Day, Max, Eve, Prob, Id = Event['secu'] , Event['dre'], Event['day'], Event['max'], Event['event'], Event['prob'], Event['id']
            if Secu in PriceDict and 'O' in PriceDict[Secu]:
                if Secu == '300051_SZ_EQ' and Debug == 1:
                    print(Secu)
                Tp = PriceDict[Secu]['O']
                Lp = ClosePrice(Secu, Time, Tp=False, Sp=False, Moke2=True)
                if Tp and Lp:
                    D = 0
                    FuDu = round(Tp / Lp - 1, 4)
                    if Dre == 1:
                        if  D < Day:
                            BuyStockList.append([Time, Secu, Lp, Day, Dre, Max, Eve, Prob, Id])  # Tp改为Lp
                    elif Dre == 2:
                        if D < Day:
                            BuyStockList.append([Time, Secu, Lp, Day, Dre, Max, Eve, Prob, Id])  # Tp改为Lp
        ############################################################################# 买入股票
        BuyStockList = TopNum(BuyStockList, Top)
        PortHold[Time]['T0'] = []
        if len(BuyStockList) > 0:
            AddT0Port(BuyStockList, Time)
        #################################### 更新持股的最新收盘价
        for Tback in range(1, 6):
            if t + 1 - Tback >= 0:
                HoldToday = PortHold[TimeLine[t + 1 - Tback]]
                FuDuL = []
                Tprint = str(Tback)
                HoldToday['T' + Tprint] = deepcopy(HoldToday['T' + str(int(Tprint) - 1)])
                for j, Secu in  enumerate(HoldToday['T' + Tprint]):
                    ThisSecuTn = HoldToday['T' + Tprint][j]
                    if ThisSecuTn['holdtime'] > 0:
                        if ThisSecuTn['secu'] in PriceDict and 'Sp' in PriceDict[ThisSecuTn['secu']] :
                            ThisSecuTn['split'] = PriceDict[ThisSecuTn['secu']]['Sp']
                        ThisSecuTn['todayprice'] = UpDataLastPrice2(ThisSecuTn['secu'], Time, PriceDict)
                        if ThisSecuTn['split'] != 0:
                            ThisSecuTn['todayprice'] = round(ThisSecuTn['todayprice'] / ThisSecuTn['split'], 3)
                        ThisSecuTn['holdtime'] = ThisSecuTn['holdtime'] - 1 
                    else:
                        ThisSecuTn['todayprice'] = HoldToday['T' + str(int(Tprint) - 1)][j]['todayprice']
                    T0p = HoldToday['T0'][j]['todayprice']
                    FuDuL.append(ThisSecuTn['todayprice'] / ThisSecuTn['buyprice'] - 1)
                    HoldToday['T' + Tprint][j] = ThisSecuTn
                if len(HoldToday['T0']) > 0:
                    TnReturn = sum(FuDuL) / len(HoldToday['T0'])
                    PortReturn[TimeLine[t + 1 - Tback]]['T' + Tprint] = ConvPre(TnReturn, False, 4)
                else:
                    PortReturn[TimeLine[t + 1 - Tback]]['T' + Tprint] = 0
    PrintMoke()
###################################################################################
#                                                                                 #
#               这是Moke5                                                          #                                                                                    #
#                                                                                 #
###################################################################################   
    
def Moke5(Pprecent=True):
    global StartTime
    StartTime = time.clock()
    print('*' * 75)
    global EventNum, Signal, BuySuccess, Win, GetTar, Holding, Rules
    for t, Time in enumerate(TimeLine):
        if Time == datetime.date(2014, 6, 25) and Debug == 1:
            print(Time)
        PrintPrecent(t, Time, Pprecent)
        Events = A.GetEventCount(TimeLine[t - 1] if t > 0 else 0, Time)
        if t != 0:
            Holding[Time] = deepcopy(Holding[TimeLine[t - 1]])
            Waiting[Time] = deepcopy(Waiting[TimeLine[t - 1]])
            TotMoney = Holding[Time][0]
        else:
            Holding[Time] = [BegTotMoney]
            Waiting[Time] = []
        #################################### 生成事件策略
        EventList = A.GetEventListM5(Events, 1)
        Eventing[Time] = Events
        #################################### 股价表
        PriceDict = GerPriceDict(Holding[Time][1:], Waiting[Time], EventList, Time)
        #################################### 处理除权(改变持股数量)
        Holding = UpDateChuQuan(Holding, Time)
        #################################### 持有股票,卖出判断 并卖出
        Holding = SellHold(Holding, Time, PriceDict, OC='Open')
        #################################### 待买入股票,买入判断
        RemoveL = []
        BuyStockList = []
        for i, Wait in enumerate(Waiting[Time]):
            Secu, Max, Day, Dre, Eve = Wait['secu'], Wait['max'], Wait['day'] - 1, Wait['dre'], Wait['event']
            if Day > 0:
                if Secu == '300168_SZ_EQ':
                    print(Secu)
                if Secu in PriceDict and 'O' in PriceDict[Secu]:
                    BuyP = PriceDict[Secu]['O']
                    if BuyP:
                        Lp = ClosePrice(Secu, Time, Tp=False, Sp=True)
                        FuDu = round(BuyP / Lp - 1, 4)
                        if Dre == 1:
                            if FuDu < PriceFloorCalc(Secu, Time):
                              #  if Max > FuDu:#此条件待研究
                                BuyStockList.append([Time, Secu, BuyP, Day, Dre, Max, Eve])
                                RemoveL.append(i)
                        elif Dre == 2:
                            if FuDu > -PriceFloorCalc(Secu, Time):
                               #  if  Max < FuDu :#此条件待研究
                                BuyStockList.append([Time, Secu, BuyP, Day, Dre, Max, Eve])
                                RemoveL.append(i)
                else:
                    Waiting[Time][i]['day'] = Day
            elif Day == 0:
                RemoveL.append(i)
        Waiting[Time] = Remove(RemoveL, Waiting[Time])
        for Wait in Waiting[Time]:
            Secu , BuyP = Wait['secu'], Wait['baseprice']
            Error.append(['Wait Floor', Time, Secu, Eve, BuyP, 0])
        #################################### 新事件,买入判断
        for Event in EventList:
            Secu, Dre, Day, Max, Eve = Event['secu'] , Event['dre'], Event['day'], Event['max'], Event['event']
            if Secu == '300168_SZ_EQ' and Debug == 1:
                print(Secu)
            if Secu in PriceDict and 'O' in PriceDict[Secu]:
                Tp = PriceDict[Secu]['O']
                Lp = ClosePrice(Secu, Time, Tp=False, Sp=True)  # 昨收盘,除权后
                if Tp and Lp:
                    D = 0
                    FuDu = round(Tp / Lp - 1, 4)
                    if Dre == 1:
                        if  D < Day and FuDu < PriceFloorCalc(Secu, Time):
    #                             if Max > FuDu:#此条件待研究
                                BuyStockList.append([Time, Secu, Tp, Day, Dre, Max, Eve])
                        else:
                            WaitStock(Time, Secu, Lp, Day, Dre, Max, Eve)
                            Error.append(['Wait Floor', Time, Secu, Eve, Tp, 0])
                    elif Dre == 2:
                        if D < Day and FuDu > -PriceFloorCalc(Secu, Time):
    #                             if Max < FuDu:#此条件待研究
                                BuyStockList.append([Time, Secu, Tp, Day, Dre, Max, Eve])
                        else:
                            WaitStock(Time, Secu, Lp, Day, Dre, Max, Eve)
                            Error.append(['Wait Floor', Time, Secu, Eve, Tp, 0])
        #################################### 买入股票
        BuyStockList = TopNum(BuyStockList, Top)  # 测试
        TodayEachBuy = len(BuyStockList)
        if TodayEachBuy > 0:
            ToBuyStock(BuyStockList, t, Time, TodayEachBuy)
        #################################### 持有股票,卖出判断 并卖出
        Holding = SellHold(Holding, Time, PriceDict, OC='Close')
        #################################### 更新持股的最新收盘价
        for i, Hold in enumerate(Holding[Time][1:]):
            Secu = Holding[Time][i + 1]['secu']
            if Secu == '300168_SZ_EQ' and Debug == 1:
                print(Secu)
            Holding[Time][i + 1]['todayprice'] = UpDataLastPrice2(Secu, Time, PriceDict)
        ################################### 止损
        Holding = StopLoss(Holding, Time)
        #################################### 现金收取无风险收益
    #         Holding = FreeCashRiskFree(Holding, Time)
    PrintReport(Pprecent)   
###################################################################################
#                                                                                 #
#               这是各种参数                                                                                                                                               #
#                                                                                 #
###################################################################################    
Num, DayLength, ProbExp = 50, 26, 'P'  # AtuoRule参数:
LongProb, ShortProb, LongEr, ShortEr = 0.65, 0.65, 0.03, 0.1  # 预期概率或预期收益
ExtraRule, ExRuSheet, RollBack = 1, 'R2B', 1  # ExtraRule:0:自动规则,1.自定义规则,2,自动规则和自定义规则
BegTotMoney, OneDayBuyMax, OneShareBuyMax = 1000000, 1 / 3 , 1 / 10  # 持仓策略:, 1 / 3 , 1 / 10
Begin, End = '2009-1-1', '2014-10-1'  # 计算周期: '2009-1-1', '2014-10-1' '2005-01-01', '2009-01-01'
BuyLong, BuyShort, Stoploss = 1, 0, 0.1  # 控制变量 :多,空,止损
CalcComm, OneShareBuyMaxCtrl = 1, 1  # 控制变量 :0,1
###################################################################################
#               这是全局变量 (不修改)                                                  #
###################################################################################
PriceFloor, TaxRate, CommissionRate2, MarginRate, MarginIr = 0.095, 0.001, 0.0002, 1, 0  # 其他参数
FileName = MakeFileName()
Holding, Waiting, Eventing, Stg, Error, MonthRule = OrderedDict(), OrderedDict(), OrderedDict(), [], [], OrderedDict()
MktValL, TimeL = [], []
EventNum, Signal, BuySuccess , Win, GetTar = 0, 0, 0, 0, 0
Commission, LastMonth, TradingDay = 0, 99, 250
Mulu = r'D:/web/Python/work/Quantitative/Result/'
RuleXlsx = r'D:/web/Python/work/Quantitative/ExtraRule/Rule.xlsx'
###################################################################################
#               这是Moke变量  (不修改)                                                 #
###################################################################################
Debug = 1
NoramlIndex = True  # 采用hs300/采用更精确的价格记住指数
Top = 10;Stopwin = 0
MaxDayCalc = 'Auto'  # 'Auto'
################################################################################### 
RuleTypeCode = GetRTypeCode()     
################################################################################### 

MokeMode = 1
if MokeMode == 1:
    TimeLine, RiskFreeD = GetTimeLine(Begin, End), GetGetRiskFree(Begin, End)
    Rules = GetRule()   
    Moke() 
elif MokeMode == 2:
    PortHold, PortReturn = OrderedDict(), OrderedDict()
    TimeLine = GetTimeLine(Begin, End)
    CalcComm = 0
    Mulu = r'D:/web/Python/work/Quantitative/Result/Moke3/'
    Rules = GetRule() 
    TimeDf = GetTimeDf(Begin, End)
    Moke3()
elif MokeMode == 3:
    ExtraRule, ExRuSheet, RollBack = 2, 'R2B', 3  
    Num, DayLength, ProbExp = 50, 5, 'P'  # AtuoRule参数:
    LongProb = 0.5
    MaxDayCalc = 5
    ToDayStock()
elif MokeMode == 4:
    Begin, End = '2011-1-1', '2014-11-30'  # '2014-10-24', '2014-11-24'#'2009-1-1', '2014-10-1'
    TimeLine, RiskFreeD = GetTimeLine(Begin, End), GetGetRiskFree(Begin, End)
    MultTask('Seve')
elif MokeMode == 5:
    TimeLine, RiskFreeD = GetTimeLine(Begin, End), GetGetRiskFree(Begin, End)
    Moke5()  # 数量模拟,未完成
# pr.dump_stats('D:/log0.txt')
