from datetime import date


def get_task_groups(task_data):
    daily = task_data.filter(schedule_type="daily").order_by('deadline')
    weekly = task_data.filter(schedule_type="weekly").order_by('deadline')
    monthly = task_data.filter(schedule_type="monthly").order_by('deadline')
    quarterly = task_data.filter(schedule_type="quarterly").order_by('deadline')
    yearly = task_data.filter(schedule_type="yearly").order_by('deadline')
    custom = task_data.filter(schedule_type="custom").order_by('deadline')
    overdue = task_data.filter(deadline__lt=date.today()).exclude(schedule_type="daily").order_by('deadline')
    upcoming = task_data.filter(deadline__gte = date.today()).exclude(schedule_type="daily").order_by('deadline')
    task_groups = {
        "daily": daily,
        "weekly": weekly,
        "monthly": monthly,
        "quarterly": quarterly,
        "yearly": yearly,
        "custom": custom,
        "overdue": overdue,
        "upcoming": upcoming
    }
    return task_groups