# from celery import shared_task
# from django_celery_beat.models import PeriodicTask


# @shared_task
# def clean_up_completed_tasks():
#     tasks = PeriodicTask.objects.filter(enabled=False)
#     for task in tasks:
#         task.delete()
#     print("clean up completed tasks completed")