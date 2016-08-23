# -*- coding: UTF-8 -*-
__author__ = 'Administrator'
import sys,os
sys.path.append(os.path.dirname(os.getcwd())+'\\common')
from Models import *
import EnvInit
import xlrd
import time
import copy
conf=EnvInit.config()

def formatCaseCellStr(toSplitString,sid,cid):
    splitlist=toSplitString[2:].split('.')
    tmpList=[]
    tmpList.append(sid if  splitlist[0]=='' else splitlist[0])
    tmpList.append(cid if  splitlist[1]=='' else splitlist[1])
    tmpList=tmpList+splitlist[2:]
    res = lambda x:".".join(x)
    return res(tmpList)
    # res = lambda x:".".join(x)
    # return res(splitlist)
def getFullPathByName(fn):
    fp=''
    for item in os.listdir(conf.datapath):
        if item.startswith(fn):
            fp=os.path.join(conf.datapath,item)
            return fp
    return fp
def _getAllFn():
    fns = []
    for r,dirs,fl in os.walk(conf.datapath):
        for fn in fl:
            if fn.lower().endswith('xlsx') and not fn.startswith('~$') and fn.lower().startswith('case'):
                fns.append(fn.split('.')[0])
    return fns
def somename(SCol):
    # 得到case对应的行范围
    scl=len(SCol)
    res=[]
    tmp=[]
    rb=0
    re=0
    for index in range(1,scl):
        if getCellValue(SCol[index])!='':
            tmp.append(index)
    for i in range(0,len(tmp)):
        if (i+1)>=len(tmp):
            res.append((tmp[i],scl))
        else:
            res.append((tmp[i],tmp[i+1]))
    return res
def getCellValue(cell):
    try:
        if cell.ctype == 2:
            return str(int(cell.value))
        return cell.value
    except Exception,e:
        print "Error",cell,e
def split(ds):
    tmpl = ds[2:].split('.')
    return tuple(tmpl[:2])
def findDependsCases(case,suites):
    caseList = []
    sid,cid=tuple(case.depends.split('.')[:2])
    for c in suites[sid]:
        if c.cid==cid and c.sid ==sid:
            caseList.insert(0,c)
            if c.depends!="":
                tmpCL=findDependsCases(c,suites)
                caseList=(caseList+tmpCL[::-1])[::-1]
                return caseList
            else:
                return caseList
def isContain(c,cl):
    for tc in cl:
        if tc.cid == c.cid and tc.sid == c.sid:
            return True
    return False
def showCID(dcl):
    r="[ "
    for c in dcl:
        r+=c.cid+','+c.sid+'; '
    r+=' ]'
    return r
def getCaseData(logger,SIDList=None):
    suites = {}
    fns = _getAllFn()
    for fn in fns:
        _getCaseData(fn,suites)
    for sid in suites.keys():
        for case in suites[sid]:
            if case.depends!='':
                dependsCases = findDependsCases(case,suites)
                for c in dependsCases[::-1]:
                    if not isContain(c,suites[sid]):
                        tc = copy.deepcopy(c)
                        suites[sid].insert(0,tc)
    logger.debug("suites build step 1 ok",suites.keys())
    if SIDList != None and len(SIDList)!=0:
        for sid in list(set(suites.keys())-set(SIDList)):
            try:
                suites.pop(sid)
            except:
                pass

    logger.debug("suites build step 2 ok")
    return suites
def _getCaseData(fn,suites):
    CurrentCaseFile = os.path.join(conf.datapath,getFullPathByName(fn))
    xl = xlrd.open_workbook(CurrentCaseFile)
    for st in xl.sheets():
        sCol = st.col(0)
        for rb,re in somename(sCol):
            case=Case()
            sid=getCellValue(st.cell(rb,0))
            for rn in range(rb,re):
                cid=getCellValue(st.cell(rn,1))
                url=getCellValue(st.cell(rn,2))
                method=getCellValue(st.cell(rn,3))
                depends=getCellValue(st.cell(rn,4))
                if depends!='':
                    depends=formatCaseCellStr(depends,sid,cid)
                param_key=getCellValue(st.cell(rn,5))
                param_value=getCellValue(st.cell(rn,6))
                if param_value.find('$$')>=0:
                    param_value='$$'+formatCaseCellStr(param_value,sid,cid)
                assert_res_attr=getCellValue(st.cell(rn,7))
                if assert_res_attr.find('$$')>=0:
                    assert_res_attr='$$'+formatCaseCellStr(assert_res_attr,sid,cid)
                assert_expression=getCellValue(st.cell(rn,8))
                assert_exp_value=getCellValue(st.cell(rn,9))
                if assert_exp_value.find('$$')>=0:
                    assert_exp_value='$$'+formatCaseCellStr(assert_exp_value,sid,cid)
                otheraction=getCellValue(st.cell(rn,10))
                case.newbuild(sid,cid,url,method,depends,param_key,param_value,assert_res_attr,assert_expression,assert_exp_value,otheraction)
            if suites.keys().count(sid)>0:
                suites[sid].append(case)
            else:
                suites[sid]=[case]
if __name__ == '__main__':
    suites = getCaseData()
    for sid in suites.keys():
        print sid,showCID(suites[sid])
    print suites['s_topic_like_1'][-1].asex
    # print formatCaseCellStr("$$..res['topic_id'].len","s_topic_create_1","case_1")
