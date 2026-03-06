from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, date, timedelta

# Create your models here.


class Tasks(models.Model):
    task_id = models.AutoField(primary_key=True)
    #users = models.ManyToManyField(User)
    
    taskname = models.TextField()
    description = models.TextField(blank=True, null=True)
    deadline = models.DateField(blank=True, null=True)
    schedule_type = models.TextField(default="daily") #daily, weekly, monthly, quarterly, yearly, period
    interval = models.SmallIntegerField(blank=True, null=True)
    previous = models.DateTimeField(default=datetime.now())

    def next_deadline(self):
        today = date.today()
        if self.schedule_type == "daily":
            self.deadline = today + timedelta(days=1)
        elif self.schedule_type == "weekly":
            gap = ((int(self.interval) + 7) - today.weekday())%7
            self.deadline = today + timedelta(days=gap)
        elif self.schedule_type == "monthly":
            if today.day >= self.interval:
                if today.month == 12:
                    today.year += 1
                month = today.month + 1
            else:
                month = today.month
            self.deadline = date(today.year, month, self.interval)
        elif self.schedule_type == "quarterly": #due start of quarter
            ordinal_day = today.toordinal()
            ordinal_reference = date(today.year, 1, 1).toordinal()-1
            julian_day = ordinal_day - ordinal_reference
            if julian_day < 91:
                self.deadline = date.fromordinal(91+ordinal_reference)
            elif julian_day < 182:
                self.deadline = date.fromordinal(182+ordinal_reference)
            elif julian_day < 273:
                self.deadline = date.fromordinal(273+ordinal_reference)
            else:
                self.deadline = date((today.year+1), 1, 1)
        return self.deadline



class Logs(models.Model):
    log_id = models.AutoField(primary_key=True)
    task = models.ForeignKey(Tasks, models.CASCADE)

    data = models.JSONField(blank=True, null=True)
    delay = models.IntegerField(blank=True, null=True)
    timestamp = models.DateField()
    notes = models.TextField(blank=True, null=True)



