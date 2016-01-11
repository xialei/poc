# coding=utf-8

from tools import mongoclient

import xlrd

def importProducts(db):

    data = xlrd.open_workbook('../raw/yhyc.xlsx')
    table = data.sheets()[0]
    nrows = table.nrows
    
    doclist = []
    
    for rownum in range(1, nrows):
        cols = table.row_values(rownum)
        document = {}
        document['_id'] = long(cols[3])
        document['name'] = cols[4]
        document['cat'] = long(cols[1])
        
        pic = cols[10]
        if pic != '':
            document['pic'] = str(long(cols[10]))
        else:
            print rownum, 'no pic'
        
        taglist = str(cols[8]).replace('.0', '').rstrip(';').split(';')
        if len(taglist) == 1 and taglist[0] == '':
            document['tags'] = []
        else:
            document['tags'] = map(int, taglist)
        
        reflist = str(cols[9]).replace('.0', '').rstrip(';').split(';')
        if len(reflist) == 1 and reflist[0] == '':
            document['ref'] = []
        else:
            document['ref'] = map(long, reflist)
            
        document['desc'] = cols[11]
        document['sts'] = 1
        doclist.append(document)
        
        
    if len(doclist) > 0 :
        products = db['products']
        products.insert(doclist)

def importItems(db):

    data = xlrd.open_workbook('../raw/yhyc.xlsx')
    table = data.sheet_by_name(u'items')
    nrows = table.nrows
    
    doclist = []
    
    for rownum in range(1, nrows):
        cols = table.row_values(rownum)
        
        document = {}
        document['_id'] = long(cols[0])
        document['name'] = cols[1]
        document['pid'] = long(cols[2])
        document['sid'] = long(cols[3])
        document['inv'] = long(cols[4])
        document['spec'] = []
        document['fav'] = long(cols[6])
        document['sale'] = long(cols[7])
        document['mp'] = cols[8]
        document['pp'] = cols[9]
        document['sts'] = 1
        doclist.append(document)
        
    if len(doclist) > 0 :
        items = db['items']
        items.insert(doclist)

def importUsers(db):

    data = xlrd.open_workbook('../raw/yhyc.xlsx')
    table = data.sheets()[3]
    nrows = table.nrows
    
    doclist = []
    for rownum in range(1, nrows):
        cols = table.row_values(rownum)
        
        document = {}
        document['_id'] = long(cols[0])
        document['name'] = cols[1]
        document['password'] = str(cols[2]).replace('.0', '')
        document['mobi'] = str(long(cols[3]))
        document['mail'] = cols[4]
        
        address = {}
        address['recip'] = cols[6]
        address['addr'] = cols[7]
        address['mobi'] = str(long(cols[8]))
        address['tel'] = str(cols[9])
        document['address'] = [address]
        
        document['fav'] = map(long, cols[10].split(';'))
        document['ac'] = cols[11]
        document['cart'] = map(long, cols[12].split(';'))
        document['sts'] = 1
        doclist.append(document)
        
    if len(doclist) > 0 :
        users = db['users']
        users.insert(doclist)

def importWorkshops(db):

    data = xlrd.open_workbook('../raw/yhyc.xlsx')
    table = data.sheet_by_name(u'workshops')
    nrows = table.nrows
    
    doclist = []
    
    for rownum in range(1, nrows):
        cols = table.row_values(rownum)
        
        document = {}
        document['_id'] = long(cols[0])
        document['name'] = cols[1]
        document['owner'] = str(cols[2])
        document['idcard'] = str(cols[3])
        document['city'] = cols[4]
        document['dist'] = cols[5]
        document['addr'] = cols[6]
        document['mobi'] = str(long(cols[7]))
        document['tel'] = str(cols[8])
        document['start'] = str(cols[9]).replace('.0', '')
        document['cat'] = map(int, str(cols[10]).replace('.0', '').split(';'))
        document['shequ'] = map(long, str(cols[11]).split(';'))
        document['sts'] = 1
        doclist.append(document)
        
    if len(doclist) > 0 :
        workshops = db['workshops']
        workshops.insert(doclist)

def importShequ(db):

    data = xlrd.open_workbook('../raw/yhyc.xlsx')
    table = data.sheet_by_name(u'shequ')
    nrows = table.nrows
    
    doclist = []
    for rownum in range(1, nrows):
        cols = table.row_values(rownum)
        
        document = {}
        document['_id'] = long(cols[0])
        document['name'] = cols[1]
        document['py'] = str(cols[2])
        document['city'] = cols[3]
        document['dist'] = cols[4]
        document['addr'] = cols[5]
        document['desc'] = ''
        document['sts'] = 1
        doclist.append(document)
        
    if len(doclist) > 0 :
        shequ = db['shequ']
        shequ.insert(doclist)

def importTags(db):

    data = xlrd.open_workbook('../raw/yhyc.xlsx')
    table = data.sheets()[2]
    nrows = table.nrows
    
    doclist = []
    
    for rownum in range(1, nrows):
        cols = table.row_values(rownum)
        document = {}
        document['_id'] = int(cols[0])
        document['code'] = int(cols[0])
        document['name'] = cols[1]
        doclist.append(document)
        
    if len(doclist) > 0 :
        tags = db['tags']
        tags.insert(doclist)
                
def test():
    data = xlrd.open_workbook('../raw/yhyc.xlsx')
    table = data.sheets()[0]
    print table.row_values(1)
    print type(table.cell(1, 1).value)
    print long(table.cell(1, 1).value)
    print map(int, [100, 110])
    print str(100)
    print '10;'.split(';')
    print ''.split(';')
    print [''] == ['']
    print [''][0] == ''
    
if __name__ == "__main__":
    db = mongoclient.get_db()
    importUsers(db)
#     importTags(db)
#     importShequ(db)
#     importWorkshops(db)
#     importProducts(db)
#     importItems(db)
#     test()


