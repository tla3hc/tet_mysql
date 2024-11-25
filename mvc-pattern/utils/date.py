import datetime

# Define a class for handling date-related operations
class Date:
    # Class variable to hold the class name
    m_class_name = 'Date'

    # Constructor method that initializes the Date object
    def __init__(self):
        # Get the current date and time and store it in the current_time attribute
        self.current_time = datetime.datetime.now()

    # Method to get the current week number
    def get_current_week(self):
        # Calculate the ISO week number using the isocalendar() method of the current_time
        iso_week_number = self.current_time.isocalendar()[1]
        
        # Format the current week information as a string and return it
        return f"{iso_week_number}"

    # Method to get the current year
    def get_current_year(self):
        # Retrieve the year component from the current_time and return it as a string
        return f"{self.current_time.year}"
    
    def get_week_number(self):
        self.last_day_of_year = datetime.date(self.current_time.year, 12, 31)
        return (int(self.last_day_of_year.strftime("%U")) + 1)

    @staticmethod
    def get_date(day, week, year):
        week = int(week)
        year = int(year)
        # Convert the day name to a numeric representation (0 = Monday, 6 = Sunday)
        days_of_week = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
        day_index = days_of_week.index(day)

        # Calculate the date for the given week, year, and day
        start_date = datetime.datetime(year, 1, 1)
        week_start = start_date + datetime.timedelta(days=(week - 1) * 7 + day_index)
        
        # Format the output as "day/month" (e.g., "Mon 03/10" for Monday in week 10)
        formatted_date = week_start.strftime("%a %d/%m")
        return formatted_date