__author__ = 'Administrator'
class config:
    # p: production
    # t: test
    # d: dev
    env='p'
    host='http://192.168.1.190:3000'
    datapath='d:/codespace/AutoFrame/data/'
    report='d:/codespace/AutoFrame/report/'
def EnvInit(Config=None):
    conf=config()
    return conf