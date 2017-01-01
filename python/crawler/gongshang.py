# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import httptool
import time
import xlwt as excel
import random

# import sys
# 使得 sys.getdefaultencoding() 的值为 'utf-8'  
# reload(sys)  # reload 才能调用 setdefaultencoding 方法  
# sys.setdefaultencoding('utf-8')  # 设置 'utf-8'  

baseurl = "https://www.sgs.gov.cn/notice/"

def crawlerjob():
    try:
        f = open("../raw/gongshang.txt", "r");
        
        all_baseinfo = []
        all_investors = []
        all_investorinfo = []
        all_changeitems = []
        all_members = []
        all_punish = []
        
        for line in f:
            parts = line.split(' ')
            if len(parts) == 3:
                baseinfo, investors, investinfo, changeitems, members, punish = crawlcompany(parts[0], parts[1], parts[2])
                all_baseinfo = all_baseinfo + baseinfo
                all_investors = all_investors + investors
                all_investorinfo = all_investorinfo + investinfo
                all_changeitems = all_changeitems + changeitems
                all_members = all_members + members
                all_punish = all_punish + punish
                time.sleep(random.randint(1, 10))
            else:
                print parts
        
        write_to_excel(all_baseinfo, all_investors, all_investorinfo, all_changeitems, all_members, all_punish)
            
    except Exception, e:
        print "Exception in crawlerjob ", e
    return None

# 基本信息
# 注册号, 企业名称, 类型, 法定代表人, 注册资本, 成立日期, 住所, 经营期限自, 经营期限至, 经营范围, 登记机关, 发照日期, 经营状态
def crawlcompany(companyid, company, url):
    
    baseinfo = []
    investors = []
    investorinfo = []
    changeitems = []
    members = []
    punishs = []
    try:
        html = httptool.getResponseHtml(url)
        
        soup = BeautifulSoup(html)
        
        if company == '_':
            name = soup.find(name="h2")
            company = name.getText().replace('&nbsp;','').strip()
            
        #=======================================================================
        # baseinfo
        #=======================================================================
        profile_html = soup.find(name="table", attrs={'class':'detailsList mTop'})
        profile_info = profile_html.findAll(name="td", attrs={'class':'left'})
        
        baseprofile = [companyid, company]
        for e in profile_info :
            baseprofile.append(e.getText())
        baseinfo.append(list(baseprofile))
        
        print 'start to craw investors'
        #=======================================================================
        # investors
        #=======================================================================
        investor_html = soup.find(name="table", attrs={'class':'detailsList mTop', 'id':'investor'})
        investor_rows = investor_html.findAll(name="tr")
        
        size = len(investor_rows)
        if size > 3:
            investor_rows = investor_rows[2:size - 1]
            rowid = 1
            for row in investor_rows:
                cols = row.findAll(name="td")
                investor = [companyid]
                investorid = companyid + '_' + str(rowid)
                investor.append(investorid)
                for i in range(4):
                    investor.append(cols[i].getText())
                investors.append(list(investor))
                
                alink = cols[4].find(name="a", attrs={'target':'_blank'})
                investorinfo = investorinfo + craw_investor_info(investorid, alink.get('href'))
                
                rowid = rowid + 1
        
        print 'start to craw changeitems'
        #=======================================================================
        # changeitems
        #=======================================================================
        changeitems_html = soup.find(name="table", attrs={'class':'detailsList mTop', 'id':'changeItem'})
        changeitems_rows = changeitems_html.findAll(name="tr")
        
        size = len(changeitems_rows)
        if size > 3:
            changeitems_rows = changeitems_rows[2:size - 1]
            for row in changeitems_rows:
                cols = row.findAll(name="td")
                changeinfo = [companyid]
                for i in range(4):
                    changeinfo.append(cols[i].getText())
                changeitems.append(list(changeinfo))
        
        print 'start to craw members'
        #=======================================================================
        # members
        #=======================================================================
        members_html = soup.find(name="table", attrs={'class':'detailsList mTop', 'id':'member'})
        members_rows = members_html.findAll(name="tr")
        
        size = len(members_rows)
        if size > 3:
            members_rows = members_rows[2:size - 1]
            for row in members_rows:
                cols = row.findAll(name="td")
                memberinfo = [companyid]
                for i in range(3):
                    memberinfo.append(cols[i].getText())
                members.append(list(memberinfo))
                if len(cols) == 6:
                    memberinfo = [companyid]
                    for i in range(3):
                        memberinfo.append(cols[i + 3].getText())
                    members.append(list(memberinfo))
        
        print 'start to craw punish'            
        #=======================================================================
        # punish
        #=======================================================================
        punish_div = soup.find(name="div", attrs={'id':'punishDiv'})
        punish_html = punish_div.find(name="table", attrs={'class':'detailsList mTop'})
        punish_rows = punish_html.findAll(name="tr")
        
        size = len(punish_rows)
        if size > 2:
            punish_rows = punish_rows[2:size]
            for row in punish_rows:
                cols = row.findAll(name="td")
                punishinfo = [companyid]
                for i in range(7):
                    punishinfo.append(cols[i].getText())
                punishs.append(punishinfo)
                        
    except Exception, e:
        print "Exception in crawlcompany ", e
    return baseinfo, investors, investorinfo, changeitems, members, punishs



def craw_investor_info(investorid, url):
    
    invests = []
    try:
        html = httptool.getResponseHtml(baseurl + url)
        
        soup = BeautifulSoup(html)
        
        investinfo_html = soup.find(name="table", attrs={'class':'detailsList mTop'})
        investinfo_rows = investinfo_html.findAll(name="tr", recursive=False)
        
        size = len(investinfo_rows)
        
        if size > 1:
            investinfo_rows = investinfo_rows[1:size]
            for row in investinfo_rows:
                cols = row.findAll(name="td", recursive=False)
                t2 = cols[2].find(name="table", attrs={'class':'detailsList mTop'})
                group_rows = t2.findAll(name="tr", recursive=False)
                for grouprow in group_rows:
                    group_cols = grouprow.findAll(name="td", recursive=False)
                    t3 = group_cols[3].find(name="table", attrs={'class':'detailsList mTop'})
                    invest_times = t3.findAll(name="tr", recursive=False)
                    for inv in invest_times:
                        inv_cols = inv.findAll(name="td", recursive=False)
                        investinfo = [investorid]
                        investinfo.append(group_cols[0].getText())
                        investinfo.append(group_cols[1].getText())
                        investinfo.append(group_cols[2].getText())
                        investinfo.append(inv_cols[0].getText())
                        investinfo.append(inv_cols[1].getText())
                        investinfo.append(inv_cols[2].getText())
                        invests.append(list(investinfo))
    
    except Exception, e:
        print "Exception in craw_investor_info ", e
    return invests

def write_to_excel(baseinfo, investors, investinfo, changeitems, members, punish):
    
    wb = excel.Workbook()
    
    print 'write baseinfo'
    sheet_info = wb.add_sheet("baseinfo".decode('utf-8'))
    baseinfo.insert(0, "companyid,companyname,注册号,企业名称,类型,法定代表人,注册资本,成立日期,住所,经营期限自,经营期限至,经营范围,登记机关,发照日期,经营状态".split(','))
    size = len(baseinfo)
    for i in range(size):
        cols = len(baseinfo[0])
        for j in range(cols):
            try:
                sheet_info.write(i, j, baseinfo[i][j].decode('utf-8'))
            except:
                print i

    print 'write investors'
    sheet_investor = wb.add_sheet("investors".decode('utf-8'))
    investors.insert(0, "companyid,investorid,投资人类型,投资人,证照类型,证照号码".split(','))
    size = len(investors)
    for i in range(size):
        cols = len(investors[0])
        for j in range(cols):
            try:
                sheet_investor.write(i, j, investors[i][j].decode('utf-8'))
            except:
                print i
    
    print 'write investinfo'
    sheet_investinfo = wb.add_sheet("investinfo".decode('utf-8'))
    investinfo.insert(0, "investorid,认缴出资额,出资方式,出资时间,实缴出资额,出资方式,出资时间".split(','))
    size = len(investinfo)
    cols = len(investinfo[0])
    for i in range(size):
        for j in range(cols):
            try:
                sheet_investinfo.write(i, j, investinfo[i][j].decode('utf-8'))
            except:
                print i
    
    print 'write changeitem'            
    sheet_change = wb.add_sheet("changeItems".decode('utf-8'))
    changeitems.insert(0, "companyid,变更事项,变更前内容,变更后内容,变更日期".split(','))
    size = len(changeitems)
    for i in range(size):
        cols = len(changeitems[0])
        for j in range(cols):
            try:
                sheet_change.write(i, j, changeitems[i][j].decode('utf-8'))
            except:
                print i
    
    print 'write members'
    sheet_member = wb.add_sheet("members".decode('utf-8'))
    members.insert(0, "companyid,序号,姓名,职务".split(','))
    size = len(members)
    for i in range(size):
        cols = len(members[0])
        for j in range(cols):
            try:
                sheet_member.write(i, j, members[i][j].decode('utf-8'))
            except:
                print i
    
    print 'write punish'
#   punish
    sheet_punish = wb.add_sheet("punish".decode('utf-8'))
    punish.insert(0, "companyid,序号,处罚决定书文号,违法行为,处罚依据,处罚结果,处罚机关,处罚决定书签发日期".split(','))
    size = len(punish)
    for i in range(size):
        cols = len(punish[0])
        for j in range(cols):
            try:
                sheet_punish.write(i, j, punish[i][j].decode('utf-8'))
            except:
                print i
                
    fn = 'D:/company.xls'
    wb.save(fn)

def test():
    for i in range(3):
        print random.randint(1, 5)
    d = '浦东'
    print d.decode('GBK').encode('utf-8')
    print d.decode('utf-8')
    a = ['1', '2', 3, 4, 5]
    b = ["a", 'b']
    print a[2:4]
    print a[:3]
    print a[3:]
    print a + b
    print a
    alist = []
    alist.append(list(a))
    alist.append(list(b))
    print alist[1][1]
        
if __name__ == '__main__':
    crawlerjob()
#     test()
    


