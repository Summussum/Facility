from datetime import date


def get_task_groups(task_data):
    daily = task_data.filter(schedule_type="daily", status="active").exclude(previous__date = date.today()).order_by('deadline')
    weekly = task_data.filter(schedule_type="weekly", status="active").order_by('deadline')
    monthly = task_data.filter(schedule_type="monthly", status="active").order_by('deadline')
    quarterly = task_data.filter(schedule_type="quarterly", status="active").order_by('deadline')
    yearly = task_data.filter(schedule_type="yearly", status="active").order_by('deadline')
    custom = task_data.filter(schedule_type="custom", status="active").order_by('deadline')
    overdue = task_data.filter(deadline__lte=date.today(), status="active").exclude(schedule_type="daily").order_by('deadline')
    upcoming = task_data.filter(deadline__gte = date.today(), status="active").exclude(schedule_type="daily").order_by('deadline')
    today = task_data.filter(previous__date = date.today())
    paused = task_data.filter(status="paused")
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