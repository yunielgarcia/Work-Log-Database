from peewee import *

db = SqliteDatabase('logs.db')


class Task(Model):
    date = CharField(max_length=255)  # will have DD/MM/YYYY format
    title = CharField(max_length=255)
    time_spent = IntegerField()
    notes = TextField(null=True)
    employee_name = CharField(max_length=255)

    class Meta:
        database = db

    def __init__(self, date, title, time_spent, employee_name, notes=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.date = date
        self.title = title
        self.time_spent = time_spent
        self.employee_name = employee_name
        self.notes = notes

    def __eq__(self, other):
        other_dict = {'date': other.date,
                      'title': other.title,
                      'time_spent': other.time_spent,
                      'employee_name': other.employee_name,
                      'notes': other.notes}
        return self.__dict__['__data__'] == other_dict

    def __str__(self):
        rep = "MyClass object\n"
        rep += " date: " + self.date \
               + " title: " + self.title \
               + " time_spent: " + self.time_spent \
               + " notes: " + self.notes
        return rep
