# -*- coding: UTF-8 -*-
__author__ = 'Administrator'
import time
import json
def AddTimeStamp(s):
    return s+str(time.time())
RESERVEDWORD={'$CREATETIMESTAMP()':AddTimeStamp}
class Case(object):
    def __init__(self):
        self.cid=''
        self.url=''
        self.method=''
        self.depends=''
        self.param={}
        self.asex=[]
        self.res=None
        self.otherAction=''
        # addr = [file,sheet,rowbegin,rowend]
        self.addr=[]
        self.sid=''
    '''
    def build(self,CaseFile,SheetName,rowBegin,rowEnd,host):
        if os.path.isfile(CaseFile):
            CurrentCaseFile=CaseFile
        else:
            CurrentCaseFile=getFullPathByName(CaseFile)
        xf=xlrd.open_workbook(CurrentCaseFile)
        sheet=xf.sheet_by_name(SheetName)
        row=sheet.row(rowBegin)
        self.cid = getCellValue(row[1])
        self.url = host+getCellValue(row[2])
        self.method = getCellValue(row[3])
        self.depends = getCellValue(row[4])
        for nrow in range(rowBegin,rowEnd):
            if getCellValue(sheet.cell(nrow,5))!='':
                v = getCellValue(sheet.cell(nrow,6))
                if v.startswith('$CREATETIMESTAMP()'):
                    v+=str(time.time())
                self.param[getCellValue(sheet.cell(nrow,5))]=v
            if getCellValue(sheet.cell(nrow,7))!='':
                self.asex.append(getCellValue(sheet.cell(nrow,7)))
    '''
    def newbuild(self,sid,cid,url,method,depends,param_key,param_value,assResAttr,assExpression,assExpValue,otheraction):
        # print "debug","sid",sid,"cid",cid,"url",url,"method",method,"depends",depends,"param_key",param_value,"param_value",asex,otheraction
        if sid!='':
            self.sid=sid
        if cid!='':
            self.cid=cid
        if url!='':
            self.url=url
        if method!='':
            self.method=method
        if depends!='':
            self.depends=depends
        if param_key!='':
            k=param_key
            v=param_value
            # try:
            #     tc=contain(param_value,RESERVEDWORD.keys())
            #     if tc!=None:
            #         v=RESERVEDWORD[tc]
            #     else:
            #         v=param_value
            # except:
            #     print "param_value",param_value,"cid",cid,"sid",sid
            tc=contain(param_value,RESERVEDWORD.keys())
            if tc!=None:
                v=RESERVEDWORD[tc](param_value)
            else:
                v=param_value
            self.param[k]=v
        if assResAttr!='':
            self.asex.append((assResAttr,assExpression,assExpValue))
        if otheraction!='':
            self.otherAction=otheraction
    def show(self):
        toPrintStr = ''
        for attr in self.__dict__:
            toPrintStr+=attr+':'+str(self.__getattribute__(attr))+';\n'
        print "show:",toPrintStr[:-1]
        print self.__hash__()
    def getResValue(self,attrList):
        # attrList : ["topic","topic_id",0]
        j=json.loads(self.res)
        js = "j"
        for attr in attrList:
            js+='['+attr+']'
        return eval(js)
def contain(s,l):
    if type(s)!=type(''):
        s=str(s)
    for i in l:
        if s.find(i)>=0:
            return i
    return None
if __name__ == '__main__':
    pass