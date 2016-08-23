# -*- coding: UTF-8 -*-
__author__ = 'Administrator'
import sys,os
sys.path.append(os.getcwd()+'\\common')
sys.path.append(os.getcwd()+'\\work')
from Httpclient import request
import DataProvider
import GenerateReport
from Asserts import *
import EnvInit
import json
import time
import Models
import re
import MyLog
def main(sids,logger):
    SuiteList = DataProvider.getCaseData(logger,sids)
    logger.debug("run SuiteIDs:",SuiteList.keys())
    report = {}
    # report {sid:{status:pass/fail,cost:time,detail:{case:pass/fail/norun}}} **update 2016-2-16
    conf=EnvInit.config()
    # print conf.host
    # sys.exit()
    for sid in SuiteList.keys():
        logger.debug("++++++"+sid+"++++++"+"begin")
        begintime=time.time()
        report[sid]={}
        for case in SuiteList[sid]:
            for pk in case.param.keys():
                if case.param[pk].startswith('$$'):
                    logger.debug('debug main ',case.param[pk])
                    tmpList = case.param[pk][2:].split('.')
                    tmpSid = tmpList[0]
                    tmpCid = tmpList[1]
                    tmpAttrList,tmpFun = getAttrList(case.param[pk],re.compile('\[(.+?)\]'))
                    for tc in SuiteList[sid]:
                        if tc.cid ==tmpCid and tc.sid == tmpSid:
                            case.param[pk]=tc.getResValue(tmpAttrList)
                            logger.debug( "main ...................... update ",case.__hash__())

                tc=Models.contain(case.param[pk],Models.RESERVEDWORD.keys())
                if tc!=None:
                    case.param[pk]=Models.RESERVEDWORD[tc](case.param[pk])
            logger.debug("main param.....",case.cid,case.sid,case.param)
            r,c = request(case,conf,logger)
            logger.debug("main response..",c)
            if r['status']!='200':
                report[sid]={'status':False,
                             'cost':time.time()-begintime,
                             'detail':{(case.cid,case,sid):False}}
                break
            case.res = c
            assertobj = AssertMain(c,case.asex,case.param,logger)
            logger.debug("main assertobj...",assertobj)
            if assertobj['status']:
                report[sid]['status']=True
                if report[sid].keys().count('detail')>0:
                    report[sid]['detail'][(case.cid,case.sid)]=assertobj
                else:
                    report[sid]['detail']={(case.cid,case.sid):assertobj}
            else:
                report[sid]['status']=False
                report[sid]['cost']=time.time()-begintime
                report[sid]['detail'][(case.cid,case.sid)]=assertobj
                break
            if case.otherAction!='':
                logger.debug( case.otherAction)
                eval(case.otherAction)
        if report[sid].keys().count('status')==0:
            report[sid]['status']=True
            report[sid]['cost']=time.time()-begintime
        logger.debug("++++++",sid,"++++++","end")
    logger.debug( report)
    logger.debug("dump report file begin")
    GenerateReport.Report(report)
    logger.debug("dump report file end")
def usage():
    print '''
SYNOPSIS
    python main.py [option] [parameters]
DESCRIPTION
    -s [suiteID or suiteID1,suiteID2...]
        only run testcase which are in SuiteIDs
    -h
        display help and exit
    '''
    sys.exit()
if __name__=='__main__':
    import getopt
    sids = []
    if len(sys.argv)>1:
        try:
            opts,args = getopt.getopt(sys.argv[1:],"hs:")
            for op,value in opts:
                if op=="-s":
                    sids = value.split(',')
                elif op=="-h":
                    usage()
        except:
            usage()

    logger = MyLog.Logger()
    logger.debug('start ...')
    main(sids,logger)