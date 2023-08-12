import datetime

class Project:

    def __init__(self, name, status='In Planning'):
        self.name = name
        self.status = status
        self.records = []

    def add_record(self, start, end):
        record = Record(start, end)
        self.records.append(record)


class Record:
    """执行记录类"""
    
    def __init__(self, start, end):
        """初始化记录"""
        self.start = start
        self.end = end
        self.duration = end - start # 计算持续时间