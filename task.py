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

    def __str__(self):
        rep = "MyClass object\n"
        rep += " date: " + self.date\
               + " title: " + self.title\
               + " time_spent: " + self.time_spent\
               + " notes: " + self.notes
        return rep


