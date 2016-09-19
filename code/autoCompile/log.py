#coding=utf-8
#hdp 2016.09.19

class Log():
    '''日志类，用于记录自动编译时的输出信息'''
    
    def __init__(self):
        self._datas = []
    
    def send(self, message):
        self._datas.insert(0, message)
        self._datas = self._datas[0:10]
    
    def receive(self):
        message = ''
        for d in self._datas:
            message = message+'<p>'+d+'</p>'
            
        return message
    
    def clear(self):
        self._datas.clear()
