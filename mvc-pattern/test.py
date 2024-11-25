import calendar 
from datetime import datetime as dt

class Test():
    dict_leo = {"Mon":1, "Tue":2, "Wed":3, "Thu":4, "Fri":5}
    
    def test_01(self):
        month = 4
        year = 2024        
        month_len = calendar.monthrange(2024, month)[1]
        first_day = dt(year, month, 1)
        last_day = dt(year, month, month_len)
        
        first_week_day = first_day.strftime("%a")
        last_week_day = last_day.strftime("%a")
        
        start_week = first_day.strftime("%W")
        end_week = last_day.strftime("%W")
        
        print(first_day)        
        print(first_week_day)
        print(start_week)
        
        print(last_day)        
        print(last_week_day)
        print(end_week)
        
        self.get_first_effort(first_week_day)
        self.get_last_effort(last_week_day)
        
        pass
    
    def get_first_effort(self, start):
        date_list = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
        anchor = date_list.index(start)
        new_list = date_list[anchor:len(date_list)]
        sum = 0
        for i in new_list:
            sum += self.dict_leo[i]
        print(new_list)
        print(sum)

    def get_last_effort(self, end):
        date_list = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']        
        anchor = date_list.index(end)
        new_list = date_list[0:anchor+1]
        sum = 0
        for i in new_list:
            sum += self.dict_leo[i]
        print(new_list)
        print(sum)
    
Test().test_01()