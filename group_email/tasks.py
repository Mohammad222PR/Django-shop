# from celery import shared_task
# from group_email.models import GroupEmail, GroupEmailStatus
# from django.core.mail import EmailMessage
# from django.utils import timezone

# @shared_task
# def send_group_emails():
#     group_email_objs = GroupEmail.objects.filter(status=GroupEmailStatus.draft.value)
#     current_time = timezone.now()

#     for email_obj in group_email_objs:
#         if email_obj.published_date == current_time:
#             email = EmailMessage(
#                 subject=email_obj.subject,
#                 body=email_obj.content,
#                 from_email=email_obj.from_email,
#                 to=email_obj.to_email,
#             )
#             email.send()
#         else:
#             pass
