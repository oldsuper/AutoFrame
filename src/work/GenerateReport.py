__author__ = 'Administrator'
import exceptions
from xml.dom import minidom
import time
import EnvInit
def Report(report,logging=None):
    doc = minidom.Document()
    root = doc.createElement("report")
    doc.appendChild(root)
    for sid in report:
        sidNode = doc.createElement("suite")
        sidNode.setAttribute("sid",sid)
        for sk in report[sid]:
            if type(report[sid][sk]) not in (dict,list):
                sidNode.setAttribute(sk,str(report[sid][sk]))
            else:
                sidNodeDetail = doc.createElement("cases")
                for caseDetail in report[sid][sk]:
                    caseNode = doc.createElement("case")
                    caseNode.setAttribute("caseid",str(caseDetail))
                    for k in report[sid][sk][caseDetail]:
                        caseNode.setAttribute(k,str(report[sid][sk][caseDetail][k]))
                    sidNodeDetail.appendChild(caseNode)
        sidNode.appendChild(sidNodeDetail)
        root.appendChild(sidNode)
    # fn=EnvInit.config.report+time.strftime("%Y%m%d%H%M%S",time.localtime())+".xml"
    fn=EnvInit.config.report+"abc"+".xml"
    f=open(fn,'w')
    doc.writexml(f,"","","")
    f.close()
if __name__ == "__main__":
    res = {
        "s_1":{
            "status":True,
            "cost":0.1,
            "detail":{
                ("c1","s1"):{
                    "status":True,
                    "et":None,
                    "ee":""
                },
                ("c2","s1"):{
                    "status":True,
                    "et":None,
                    "ee":""
                }
            }
        },
        "s_2":{
            "status":False,
            "cost":0.02,
            "detail":{
                ("c1","s2"):{
                    "status":True,
                    "et":None,
                    "ee":""
                },
                ("c2","s2"):{
                    "status":False,
                    "et":exceptions.KeyError,
                    "ee":"ssssssssssssssssssssssssssssssssssssss"
                }
            }
        }
    }

    Report(res)