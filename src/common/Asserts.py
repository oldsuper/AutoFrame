# -*- coding: UTF-8 -*-
__author__ = 'Administrator'
import json
import sys
import exceptions
import re
def AssertErrorReturn(JsonObj):
    for k in JsonObj.keys():
        if k.lower().find('error'):
            return False
    return True
def AssertExpression(JsonObj,AssertStr):
    return True

def AssertMain(obj,AssertObj,RequestParam,logger):
    # 检查函数
    # 包括：返回值是否可以转化成json格式，是否包含errorcode（错误的返回），表达式验证是否通过
    # 表达式验证支持参见
        # 1.assert 返回信息中 code 是否为0 ok
        # 2.assert 返回信息中 是否为含有error ok
        # 3.aseert 返回信息中 数组的大小是否正确 jobj['attr'][...].__len__() > 0
        # 4.assert 返回信息中 字符串长度是否正确 jobj['attr0']['attr1'][...].__len__() > 0
        # 5.assert 返回信息中 包含某个key jobj['attr'][...][被检查的attrname] != None
    AssResObj={'status':True,
               'errorType':None,
               'errormsg':''}
    # assert not json obj
    # 如果json不能成功解析返回对象，直接返回
    logger.debug("assert main begin")
    try:
        jobj = json.loads(obj)
    except Exception,e:
        return raiseErr(type(e),e.message)
    else:
        if type(jobj)!=type({}):
            return raiseErr(exceptions.ValueError,"not dict type")
    # assert response contains errorcodes
    # 如果返回信息对象keys中包含error字段
    for k in jobj.keys():
        if k.lower().find('error')>=0:
            # print k
            return raiseErr(exceptions.KeyError,"Find Error Keys")
    if len(AssertObj)==0:
        AssResObj['errormsg']='No AssertObj'
        return AssResObj
    # assert AssertObj
    for assert_res_attr,assert_expression,assert_exp_value in AssertObj:
        # assert_res_attr,assert_expression,assert_exp_value = AssertObj
        attrReQ =  re.compile('\[(.+?)\]')
        functionReQ =  re.compile('\((.+?)\)')

        if assert_exp_value.startswith("$$"):
            # 预期结果(假定)只有两种可能 1、数值，2、请求dict中的某字段值
            assert_exp_eval_str = evalStr(assert_exp_value,attrReQ,'RequestParam')
            try:
                exp_value = str(eval(assert_exp_eval_str))
            except Exception,e:
                return raiseErr(type(e),e.message+'\t'+'exp_value = eval(assert_exp_eval_str); %s')
        else:
            exp_value = assert_exp_value
            # exp_value 可能是空字符串或者null，遇到再说吧
            # if assert_exp_value.lower() == 'null':
            #     exp_value = 'None'
            # else:
            #     exp_value = assert_exp_value

        if assert_res_attr.startswith("$$"):
            # 实际返回可以有： 1、某一字段的值 2、某一字段的函数值
            assert_res_attr_eval_str = evalStr(assert_res_attr,attrReQ,'jobj')
            try:
                res_value = str(eval(assert_res_attr_eval_str))
            except Exception,e:
                return raiseErr(type(e),e.message+'\t'+'res_value = eval(assert_res_attr_eval_str)')
        else:
            res_value = assert_res_attr
        if eval('res_value'+assert_expression+'exp_value'):
            return AssResObj
        else:
            # print 'res_value'+assert_expression+'exp_value'
            # print eval('res_value'+assert_expression+'exp_value')
            return raiseErr(exceptions.ValueError,"assert_exp_value is not correct. assert_res_attr is %s ,type is %s;assert_expression is %s; assert_exp_value is %s ,type is %s" % (res_value,str(type(res_value)),assert_expression,exp_value,str(type(exp_value))))
def getAttrList(s,tq):
    splitList = s.split('.')
    attrlist = [] if re.findall(tq,splitList[2]).__len__()==0 else re.findall(tq,splitList[2])
    fun = None if splitList.__len__()<=3 else splitList[3]
    return attrlist,fun
def evalStr(s,tq,objname):
    # 测试数据
    # s='$$sid.cid.res["topic_id"]["abc"].__len__()'
    # s='$$sid.cid.res["topic_id"]["abc"][0].__len__()'
    # s='$$sid.cid.res["topic_id"]["abc"]'
    # tq=re.compile('\[(.+?)\]')
    # splitList = s.split('.')
    # attrlist = [] if re.findall(tq,splitList[2]).__len__()==0 else re.findall(tq,splitList[2])
    # fun = None if splitList.__len__()<=3 else splitList[3]
    attrlist,fun = getAttrList(s,tq)

    rs = objname
    for i in attrlist:
        rs=rs+'['+i+']'
    if fun!=None:
        rs+='.'+fun
    return rs
def raiseErr(errorType,errormsg):
    return {'status':False,
                   'errorType':errorType,
                   'errormsg':errormsg}
if __name__ == '__main__':
    import json
    # j=json.loads('{')
    # e=AssertMain('{"topic_id":"120"}',('$$sid.cid.res["topic_id"].__len__()',">",'$$sid.cid.["topic_id"]'),{"topic_id":[1,2,3,4,5]})
    e=AssertMain('{"topic_id":{"a":[1,2,3,4,5],"c":"null"}}',[('$$sid.cid.res["topic_id"]["b"]',"==",'null')],{"topic_id":[1,2,3,4,5]}) #
    print e
    # print evalStr('$$sid.cid.res["topic_id"]["b"].__len__()',re.compile('\[(.+?)\]'),'j')
    # test evalStr
    # print evalStr('$$sid.cid.res["topic_id"]["abc"].__len__()',re.compile('\[(.+?)\]'),'j')