# -*- coding: UTF-8 -*-
__author__ = 'Administrator'
import sys,os
sys.path.append(os.getcwd()+'\\common')
sys.path.append(os.getcwd()+'\\work')
import logging
import logging.config
import os
import sys
import TestLog
import MyLog
def t(*arg,**args):
    print arg
    print args
def json2xml(root,content):
    from xml.etree.ElementTree import Element
    if type(content) == str or type(content) == unicode:
        e = Element(root)
        e.text = content
        return e

    e = Element(root)
    for key in content:
        if type(content[key]) == list:
            for one in content[key]:
                e.append(json2xml(key,one))
        else:
            e.append(json2xml(key,content[key]))
    return e
def dict2xml(r,d):
    if type(d) in (int,float,bool,str,unicode):
        e=minidom.Document().createElement(r)
        return e
    e=minidom.Document().createElement(r)
    if type(d)==list:
        print "eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee"
    if type(d)==dict:
        for k in d:
            if type(d[k])==list:
                for i in d[k]:
                    e.appendChild(dict2xml(str(k),i))
            else:
                e.appendChild(dict2xml(str(k),d[k]))
    return e
if __name__=='__main__':
    report = {
        "s_topic_create":{
            "status":True,
            "cost":0.09,
            "detail":{
                ("case_1","s_1"):{
                    "status":True,
                    "el":""
                },
                ("case_2","s_1"):{
                    "status":True,
                    "el":""
                },
            }
        },
        "s_t_c_2":{
            "status":False,
            "cost":0.001,
            "detail":{
                ("c_10","s_2"):{
                    "status":False,
                    "el":"error!"
                }
            }
        }
    }
    # et = json2xml("root",report)
    from xml.dom import minidom
    # doc = minidom.Document()
    # rootNode = doc.createElement("root")
    # print type(rootNode)
    # doc.appendChild(rootNode)
    # bookNodeList = doc.createElement("books")
    # bookNode = doc.createElement("book")
    # bookNode.setAttribute("name","dxp")
    # bookNode.setAttribute("price","12.3")
    # bookNodeList.appendChild(bookNode)
    # rootNode.appendChild(bookNodeList)
    d=dict2xml("report",report)

    f = open('test.xml','w')
    d.writexml(f, "\t", "", "")
    f.close()
    # logging.config.fileConfig('../conf/logging.conf')
    # root_logger = logging.getLogger('root')
    # root_logger.debug('test root logger...')
    # #
    # logger = logging.getLogger('main')
    # # logger = MyLog.Logger()
    # logger.info([1234,123123,[111],{1:2}])
    # # logger.info('start import module \'mod\'...')
    # #
    # # logger.debug('let\'s test mod.testLogger()')
    # #
    # # root_logger.info('finish test...')
    # # TestLog.run(logging.getLogger('main.TestLog.run'))
    # # TestLog.run(logger)
    # t(1)
    # t(1,2)
    # t(1,2,3,4)
