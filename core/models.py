from django.db import models

# Create your models here.


class Calendar_users(models.Model):
    first_name = models.CharField(max_length = 20)
    last_name = models.CharField(max_length = 20)
    date_of_account_creation = models.DateField(null=False, blank=False)
    username = models.CharField(max_length=50, null=False, blank=False, unique=True)
    password = models.CharField(max_length=50, null=False, blank=False, unique=True)
    email = models.EmailField(null = False, blank = False)






status_choices=[
    ('Confirmed', 'Confirmed'),
    ('Tentative', 'Tentative'),
    ('Cancelled', 'Cancelled'),
]



# condition_choices=[
#     ('Active', 'Active'),
#     ('Deleted', 'Deleted'),
#     ('Suspended', 'Suspended'),
# ]




recurrence=[
    ('Standard_recurrence', 'Standard_recurrence'),
    ('Interval_patterns', 'Interval_patterns'),
    ('Weekday_selection', 'Weekday_selection'),
    ('Relative_date_patterns', 'Relative_date_patterns'),
]



class Events_on_Calendar(models.Model):
    event_name = models.CharField(null=False, blank=False, max_length=50)
    event_description = models.CharField(null=True, blank=True, max_length=300)
    date_of_creation = models.DateTimeField(null=False, blank=False)
    status = models.CharField(choices=status_choices, max_length=9)
    created_by = models.ForeignKey(Calendar_users, on_delete=models.PROTECT, null=False, blank=False)
    recurrence = models.BooleanField(default=False, null=False, blank=False)
    due_date = models.DateField(null=True, blank=True)



class Recurring_Events(models.Model):
    Event = models.ForeignKey(Events_on_Calendar, on_delete=models.CASCADE, null=False, blank=False)
    recurrence_type = models.CharField(choices=recurrence, max_length=22)
    recurring_time = models.JSONField(null=False, blank=False)