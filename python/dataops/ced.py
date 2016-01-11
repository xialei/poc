# coding=utf-8

from tools import mongoclient

def changeCEDToTimeSeries(db):

    indicators = db['ced_indicator_data']
    
    resultset = indicators.find()
    
    new_indicators = db['ced_indicator_data_new']

    newlist = []
    for row in resultset:
        yd = {}
        v = row.get("v", "")
        for k in v.keys():
            y = k[0:4]
            m = k[4:6]
            if y not in yd:
                md = {}
                yd[y] = md
            else:
                md = yd[y]
           
            md[m] = v[k]
            yd[y] = md
        row['v'] = yd
        newlist.append(row)
        if len(newlist) % 5000 == 0 :
            new_indicators.insert(newlist)
            del newlist[:]
    if len(newlist) > 0 :
        new_indicators.insert(newlist)
    
if __name__ == "__main__":
    changeCEDToTimeSeries(mongoclient.get_db())


