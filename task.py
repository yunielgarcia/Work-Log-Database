
class Task:
    def __init__(self, date, title, time_spent, notes=None):
        self.date = date
        self.title = title
        self.time_spent = time_spent
        self.notes = notes

    def __str__(self):
        rep = "MyClass object\n"
        rep += " date: " + self.date\
               + " title: " + self.title\
               + " time_spent: " + self.time_spent\
               + " notes: " + self.notes
        return rep


