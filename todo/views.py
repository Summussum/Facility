from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from render_block import render_block_to_string
from todo.models import User, Tasks, Logs
from todo.utility import get_task_groups
from datetime import datetime, date, timedelta
import logging

# Create your views here.
logger = logging.getLogger(__name__)


def home(request):
    task_data = Tasks.objects #.filter(user=request.user)
    task_groups = get_task_groups(task_data)
    response = render(request, "dashboard.html", context={"task_groups": task_groups})
    return response

def schedule_type_select(request):
    schedule_type = request.POST.get("schedule_type")
    html = render_block_to_string("partials.html", schedule_type, context={"range": range(1,29,1)})
    return HttpResponse(html)


def create_task(request):
    logging.debug("create_task started")
    task = Tasks(
        taskname = request.POST.get("taskname"),
        description = request.POST.get("description"),
        deadline = date.today(),
        schedule_type = request.POST.get("schedule_type"),
        interval = int(request.POST.get("interval"))
        )
    logging.debug("task initialized")
    task.next_deadline()
    task.save()
    html = render_block_to_string("partials.html", "new_task_form", context={"task": task})
    return HttpResponse(html)

def log_task(request, task_id):
    task = Tasks.objects.get(task_id=task_id).first()
    new_log = Logs(
        task = task,
        timestamp = datetime.now(),
        delay = task.interval,
        data = serializers.serialize('json', task)
    )
    new_log.save()
    task.deadline = task.next_deadline()
    task.previous = datetime.now()
    task.save()