__author__ = 'Administrator'
import httplib2
import urllib
def request(case,config,logger):
    logger.debug(case.url,case.method,case.param)
    return _request(logger,config,url=case.url,method=case.method,headers=None,body=case.param)
def _request(logger,config,method="POST",headers=None,body=None,url=None):
    http=httplib2.Http()
    if headers is not None:
        if type(headers)==type({}) :
            if headers.keys().count('content-type')>0:
                pass
            else:
                headers['content-type']='application/x-www-form-urlencoded'
        else:
            headers={'content-type':'application/x-www-form-urlencoded'}
    else:
        headers={'content-type':'application/x-www-form-urlencoded'}
    if url==None:
        return
    if body is not None:
        body_encode=urllib.urlencode(body)
    else:
        body_encode=None
    try:
        r,c=http.request(config.host+url,method=method,headers=headers,body=body_encode)
        return r,c
    except Exception,e:
        logger.error( 'Httpclient error!')
        return "httpclient error:",e


# class HC(httplib2):
#     headers={'content-type':'application/x-www-form-urlencoded'}
#     def __init__(self):
#         self.http=httplib2.Http()
#     def getResponse(self,url,method=None,headers=None,body=None):
#         if method==None:
#             method='POST'
#         if headers==None:
#             headers = self.headers
#         try:
#             if body!=None:
#                 r,c=self.http.request(url,method=method,headers=headers,body=urllib.urlencode(body))
#             else:
#                 r,c=self.http.request(url,method=method,headers=headers)
#             return r,c
#         except Exception,e:
#             return
