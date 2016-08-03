#coding=utf-8
#by hdp 2016.06.29
import datetime
import json
import sqlite3
import threading

class Task():
    '''任务'''  
     
    _name = None
    _beginTime = datetime.datetime
    _endTime = datetime.datetime
    _registerTime = None
    _initData = None
    
    def __init__(self, data):
        self._initData = data
        self._name = data.get('name')
        self.reset()    
    
    def reset(self):
        format = '%Y-%m-%d %H:%M'
        today = str(datetime.date.today())
        b = self._initData.get('beginTime')
        if b == None:
            b = '00:00'
        begin = today+' '+b
        self._beginTime = datetime.datetime.strptime(begin, format)
        e = self._initData.get('endTime')
        if e == None:
            e = '23:59'
        end = today+' '+e
        self._endTime = datetime.datetime.strptime(end, format)    
        self._registerTime = None
    
    def isValid(self):
        now = datetime.datetime.now()
        if now >= self._beginTime and now <= self._endTime:
            return True
        return False
    
    def registerData(self):
        if self._registerTime == None:
            return None
        return {self._name:self._registerTime.strftime('%H:%M')}
    
    def register(self):
        '''签到'''
        if self._registerTime == None and self.isValid():
            self._registerTime = datetime.datetime.now()
            
    def resetRegister(self, time):
        format = '%Y-%m-%d %H:%M'
        today = str(datetime.date.today())
        self._registerTime = datetime.datetime.strptime(today+' '+time, format)
            
    def generateJson(self):
        format = '%H:%M'
        obj = {'name':self._name, 
               'beginTime':str(self._beginTime),
               'endTime':str(self._endTime)}
        if self._registerTime != None:
            obj['registerTime'] = str(self._registerTime)
        
        return obj;
    
class TaskManager():
    '''任务管理'''
    
    _fileName = 'json'
    _dbName = '../data/recorder'
    
    def __init__(self): 
        self.initDatabase()   
        self.initTask()
    
    def initTask(self):
        with open(self._fileName) as file:
            text = file.read()
        data = json.loads(text)
        self._tasks = []
        for d in data:
            self._tasks.append(Task(d))
        self.loadToday()
            
    def initDatabase(self):
        with sqlite3.connect(self._dbName) as conn:
            conn.execute('''CREATE TABLE if not exists recorder (
            DATE TEXT PRIMARY KEY NOT NULL,
            MESSAGE TEXT NOT NULL
            );''')
             
    def save(self):
        registers = []
        for task in self._tasks:
            reg = task.registerData()
            if reg != None:
                registers.append(reg)
        data = json.dumps(registers)        
        today = str(datetime.date.today())      
        
        with sqlite3.connect(self._dbName) as conn:
            cursor = conn.execute('select count(date) from recorder where date=?', (today,))
            count = cursor.fetchone()[0]
            sql = '''insert into recorder (date,message) values (?1, ?2)'''
            if count > 0:
                sql = '''update recorder set message=?2 where date=?1'''
            conn.execute(sql, (today, data))
            conn.commit()
            
    def loadToday(self):
        today = str(datetime.date.today())
        with sqlite3.connect(self._dbName) as conn:
            cursor = conn.execute('''select message from recorder where date=?''', (today,))
            row = cursor.fetchone()
            if row == None:
                return

            datas = json.loads(row[0]);
            for d in datas:
                for name, time in d.items():
                    for task in self._tasks:
                        if name == task._name:
                            task.resetRegister(time)
                      
    def onTimer(self):
        today = datetime.date.today()
        current = datetime.datetime.now()            
        resetTime = datetime(today.year, today.month, today.day, 1)
        if current < resetTime:
            self.reset()       
        
        t = threading.Timer(1800, onTimer)
        t.start()

    def reset(self):
        self._hasSaved = False
        for task in self._tasks:
            task.reset()  
       
    def register(self, name):
        '''签到'''
        if name == None:
            return
        
        for task in self._tasks:
            if(name == task._name):
                task.register()
                self.save()
                
    def generateJson(self):
        datas = []
        for task in self._tasks:
            datas.append(task.generateJson())
        return json.dumps(datas)
    
    def printDatabase(self):
        pass
    





    