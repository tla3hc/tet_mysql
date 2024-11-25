from models.modules.normal_function import *
import pandas

class ExcelRecordHandler():
    def __init__(self, name) -> None:
        self.name = name
        self.project = ''
        self.task_name = ''
        self.status = ''
        self.month_effort = 0
                    
    def obj_2_dict(self):
        self.dict = {
            'Name': self.name,
            'Project': self.project,
            'Task Name': self.task_name,
            'Status': self.status,
            'Effort By Month': self.month_effort            
        }
    
    