from datetime import date


def get_task_groups(task_data):
    daily = task_data.filter(schedule_type="daily", deadline__isnull=False).exclude(previous__date = date.today()).order_by('deadline')
    weekly = task_data.filter(schedule_type="weekly", deadline__isnull=False).order_by('deadline')
    monthly = task_data.filter(schedule_type="monthly", deadline__isnull=False).order_by('deadline')
    quarterly = task_data.filter(schedule_type="quarterly", deadline__isnull=False).order_by('deadline')
    yearly = task_data.filter(schedule_type="yearly", deadline__isnull=False).order_by('deadline')
    custom = task_data.filter(schedule_type="custom", deadline__isnull=False).order_by('deadline')
    overdue = task_data.filter(deadline__lt=date.today(), deadline__isnull=False).exclude(schedule_type="daily").order_by('deadline')
    upcoming = task_data.filter(deadline__gte = date.today(), deadline__isnull=False).exclude(schedule_type="daily").order_by('deadline')
    today = task_data.filter(previous__date = date.today())
    paused = task_data.filter(deadline__isnull=True)
    task_groups = {
        "daily": daily,
        "weekly": weekly,
        "monthly": monthly,
        "quarterly": quarterly,
        "yearly": yearly,
        "custom": custom,
        "overdue": overdue,
        "upcoming": upcoming,
        "today": today,
        "paused": paused
    }
    return task_groups