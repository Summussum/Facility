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
    logging.error("create_task started")
    if request.POST.get("deadline"):
        deadline = date.fromisoformat(request.POST.get("deadline"))
        logger.error(f"{type(deadline)}, {deadline}")
    else:
        deadline = date.today()
    task = Tasks(
        taskname = request.POST.get("taskname"),
        description = request.POST.get("description"),
        deadline = deadline,
        schedule_type = request.POST.get("schedule_type"),
        interval = int(request.POST.get("interval"))
        )
    logging.error("task initialized")
    if request.POST.get("deadline"):
        task.interval = task.deadline.toordinal()
    task.next_deadline()
    task.save()
    table = "upcoming"
    if task.schedule_type == "daily":
        table = "daily"
    html = render_block_to_string("partials.html", "new_task_form", context={"task": task, "table": table})
    return HttpResponse(html)


def log_task(request, task_id):
    timestamp = datetime.now()
    task = Tasks.objects.get(task_id=task_id)
    new_log = Logs(
        task = task,
        timestamp = timestamp,
        delay = task.interval,
        data = task.get_task_dict()
    )
    new_log.save()
    task.previous = timestamp
    if task.schedule_type == "single":
        task.status = "archived"
        task.save()
        response = home(request)
        return response
    
    task.deadline = task.next_deadline()
    task.save()
    response = home(request)
    return response


def bump_task(request, task_id):
    task = Tasks.objects.get(task_id=task_id)
    task.deadline = task.bump()
    logger.debug(f"{{task_id}}")
    task.save()
    response = home(request)
    return response


def pause_task(request, task_id):
    task = Tasks.objects.get(task_id=task_id)
    if task.status == "paused":
        if task.schedule_type == "yearly" or task.schedule_type == "single":
            task.deadline = date.fromordinal(task.interval)
            task.status = "active"
        task.next_deadline()
    else:
        if task.schedule_type == "yearly" or task.schedule_type == "single":
            task.interval = date.toordinal(task.deadline)
        task.status = "paused"
    task.save()
    response = home(request)
    return response