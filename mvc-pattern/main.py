# from views.main_window import MainWindow
# from controllers.main_controller import MainController
from models.modules.log import Logger

logger = Logger()

# from models.modules.mysql_migration_utils.add_employee import AddEmployee
# AddEmployee().add()

from models.modules.mysql_migration_utils.add_project import AddProject
AddProject().add()

# main_ctrler = MainController()
# main_ctrler.view.mainloop()


