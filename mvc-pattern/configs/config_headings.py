class ConfigListBox:
    m_class_name = 'List Box Configuration'
    project_List = ['All', 'Common', 'Project A', 'Project B', 'Project C', 'Project LabVIEW','Project CANoe', 'Project Sound2Light', 'Project Unassigned']
    show_Task = ['All', 'On Going','In Review', 'Done', 'Cancel']
    version = "1.1.3"
    
class ConfigTable:
    m_class_name = 'Table Configuration'
    headings = ['Task description', 'Project','Category','Status','Monday','Tuesday','Wednesday','Thursday','Friday','No.Reqs','estEffort','timeRemaining','Review Finding','Start Date','End Date','Effort by month','Total Actual Effort','Comment']
    row_color = ''
    column_color = ''

class ConfigCategory:
    projectC = ['Undefine', 'SWC', 'Cariad Ticket','ASW1', 'ASW2', 'ASW9', 'ASW14', 'ASW15', 'Unit Testing', 'Technical Review'] 
    time_factor = {
        'Undefine' : 24,
        'SWC' : 0,
        'Cariad Ticket' : 20,        
        'ASW2' : 0.35,
        'ASW9' : 0.39,
        'Unit Testing' : 3        
    }    