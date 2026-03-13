from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, date, timedelta
from calendar import monthrange
import logging

# Create your models here.
logger = logging.getLogger(__name__)

class Tasks(models.Model):
    task_id = models.AutoField(primary_key=True)
    #users = models.ManyToManyField(User)
    
    taskname = models.TextField()
    description = models.TextField(blank=True, null=True)
    deadline = models.DateField(blank=True, null=True)
    schedule_type = models.TextField(default="daily") #daily, weekly, monthly, quarterly, yearly, period, single
    interval = models.IntegerField(blank=True, null=True)
    previous = models.DateTimeField(blank=True, null=True)

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
        elif self.schedule_type == "yearly":
            today = date.today()
            deadline = date(self.deadline.year, self.deadline.month, self.deadline.day)
            if deadline < today:
                month_range = monthrange(today.year+1, self.deadline.month)[1]
                if self.deadline.day > month_range:
                    self.deadline.day = month_range
                self.deadline = date(today.year+1, self.deadline.month, self.deadline.day)
            else:
                month_range = monthrange(today.year, self.deadline.month)[1]
                if self.deadline.day > month_range:
                    self.deadline.day = month_range
                self.deadline = date(today.year, self.deadline.month, self.deadline.day)
        return self.deadline
    
    def bump(self):
        self.next_deadline()
        if self.schedule_type == "daily":
            self.deadline = self.deadline + timedelta(days=1)
        elif self.schedule_type == "weekly":
            self.deadline = self.deadline + timedelta(days=7)
        elif self.schedule_type == "monthly":
            if self.deadline.month == 12:
                self.deadline = date(self.deadline.year+1, 1, self.interval)
            else:
                self.deadline = date(self.deadline.year, self.deadline.month+1, self.interval)
        elif self.schedule_type == "quarterly":
            today = date.today()
            ordinal_day = today.toordinal()
            ordinal_reference = date(today.year, 1, 1).toordinal()-1
            julian_day = ordinal_day - ordinal_reference
            if julian_day < 91:
                self.deadline = date.fromordinal(182+ordinal_reference)
            elif julian_day < 182:
                self.deadline = date.fromordinal(273+ordinal_reference)
            elif julian_day < 273:
                self.deadline = date((today.year+1), 1, 1)
            else:
                self.deadline = date.fromordinal(365+91+ordinal_reference)
        elif self.schedule_type == "yearly":
            today = date.today()
            deadline = date(self.deadline.year, self.deadline.month, self.deadline.day)
            if deadline < today:
                month_range = monthrange(today.year+2, self.deadline.month)[1]
                if self.deadline.day > month_range:
                    self.deadline.day = month_range
                self.deadline = date(today.year+2, self.deadline.month, self.deadline.day)
            else:
                month_range = monthrange(today.year+1, self.deadline.month)[1]
                if self.deadline.day > month_range:
                    self.deadline.day = month_range
                self.deadline = date(today.year+1, self.deadline.month, self.deadline.day)
        return self.deadline


class Logs(models.Model):
    log_id = models.AutoField(primary_key=True)
    task = models.ForeignKey(Tasks, models.CASCADE)

    data = models.JSONField(blank=True, null=True)
    delay = models.IntegerField(blank=True, null=True)
    timestamp = models.DateField()
    notes = models.TextField(blank=True, null=True)



