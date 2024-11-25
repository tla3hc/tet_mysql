import json
from models.modules.normal_function import *
from configs.config_headings import ConfigCategory

class TaskHandler:
    list_attribute = []    
    task_attributes = [
        "task_name", "project", "category", "status", "mon", "tue", "wed", 
        "thu", "fri", "reqs", "estimatedEff", "remainTime", "findings", 
        "startDate", "endDate", "monthEff", "totalEff", "comment"
    ]
    
    def __init__(self):
        pass
    
    def __eq__(self, other) -> bool:
        """
        Compare two TaskHandler objects for equality.

        Args:
            other (TaskHandler): The other TaskHandler object to compare against.

        Returns:
            bool: True if all specified attributes are equal, False otherwise.
            NotImplemented: If the other object is not an instance of TaskHandler.

        Attributes compared:
            - task_name
            - project
            - mon
            - tue
            - wed
            - thu
            - fri
            - reqs
            - findings
            - startDate
            - endDate
            - comment
            - status
        """
        if not isinstance(other, TaskHandler):
            return NotImplemented  # Not comparable with other object types
        attributes = ["task_name", "project", "mon", "tue", "wed", "thu", "fri", "reqs", "findings", "startDate", "endDate", "comment", "status"]
        return all(getattr(self, attr) == getattr(other, attr) for attr in attributes)
                
    def push_obj(self, task_obj, task_name, week):
        self.task_name = task_name
        self.week = week          
        self.project = task_obj['project']
        self.category = task_obj['category']
        self.status = task_obj['status']
        self.mon = task_obj['Mon']
        self.tue = task_obj['Tue']
        self.wed = task_obj['Wed']
        self.thu = task_obj['Thu']
        self.fri = task_obj['Fri']
        self.reqs = task_obj['requirements']
        self.estimatedEff = task_obj['estimatedEffort']
        self.remainTime = task_obj['timeRemaining']
        self.findings = task_obj['findings']
        self.startDate = task_obj['startDate']
        self.endDate = task_obj['endDate']
        self.monthEff = task_obj['effortByMonth']
        self.totalEff = task_obj['totalEffort']
        self.comment = task_obj['comment']
        self.key_id = str(self.task_name) + str(self.project) + str(self.category)
        self.obj_2_list()
        self.cal_estimated_time()
        
    def obj_2_list(self):        
        """
        Converts the object's attributes specified in `self.task_attributes` to a list and assigns it to `self.list_attribute`.

        This method iterates over the attribute names listed in `self.task_attributes`, retrieves their values from the object,
        and stores these values in a list. The resulting list is then assigned to the `self.list_attribute` attribute.

        Returns:
            None
        """
        self.list_attribute = [getattr(self, attr) for attr in self.task_attributes]
    
    def list_2_obj(self, obj_list, week, year):        
        """
        Populates the object's attributes with values from a list and sets additional attributes.

        Args:
            obj_list (list): A list of values to assign to the object's attributes.
            week (int): The week number to be used in the 'week' attribute.
            year (int): The year to be used in the 'week' attribute.

        Sets:
            self.key_id (str): A unique identifier composed of the task name, project, and category.
            self.week (str): A string combining the week and year.
        """
        for attr, value in zip(self.task_attributes, obj_list):
            setattr(self, attr, value)
        self.key_id = f"{self.task_name}{self.project}{self.category}"
        self.week = f"{week}{year}"
                        
    def check_valid(self):
        """
        WTF is this?
        """
        pass
    
    def cal_estimated_time(self):
        configs = ConfigCategory()
        
        # if self.project == "Project B" and self.category not in ['Development', "Common", "N/A", "Project B"]\
        #     and self.task_name not in ["Customer Meeting", "Customer Training"]:
        if self.project == "Project B" and self.category in ["NEW_TS", "NEW_TV", "NEW_TE", "REG_TS", "REG_TV", "REG_TE", "REVIEW"]\
            and self.task_name not in ["Customer Meeting", "Customer Training"]:
            if int(self.reqs) <= 0:
                self.estimatedEff = "Seq-call missing"
            else:
                self.estimatedEff = max(int(self.reqs * 22/60), 4)
                
        elif self.project == "Project C":
            if self.category in configs.time_factor.keys():
                time_factor = configs.time_factor[self.category]
            
                if self.reqs != 0 and self.reqs != 'N/A':
                    self.estimatedEff = self.reqs * time_factor
            else:
                self.estimatedEff = 0
        
    
    
    