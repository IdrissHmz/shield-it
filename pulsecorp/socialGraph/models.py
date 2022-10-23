from django.db import models
from django.contrib.auth.models import User

class Country(models.Model):
    country = models.CharField(max_length=50)

class State(models.Model):
    state = models.CharField(max_length=50)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

class City(models.Model):
    city = models.CharField(max_length=50)
    state = models.ForeignKey(State, on_delete=models.CASCADE)

class Organization(models.Model):
    name = models.CharField(max_length=42)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Department(models.Model):
    name = models.CharField(max_length=42)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Medium(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class ContentType(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class UserProfileInfo(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)
    portfolio_site = models.URLField(blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics',blank=True)
    job_title = models.CharField(max_length=50, blank=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.username

    def get_user_with_slack_key(key):
        try:
            user = UserMedium.objects.filter(user_key=key,medium=Medium.objects.get(name='slack')).values_list('user_id',flat=True)
            if user:
                return User.objects.get(pk=user[0])
            else:
                return None
        except UserProfileInfo.DoesNotExist:
            return None
        # return User.objects.get(pk=UserMedium.objects.filter(user_key=key,medium=Medium.objects.get(name='slack')).values_list('user_id',flat=True)[0])

    def get_user_with_jira_key(key):
        try:
            user = UserMedium.objects.filter(user_key=key,medium=Medium.objects.get(name='jira')).values_list('user_id',flat=True)
            if user:
                return User.objects.get(pk=user[0])
            else:
                return None
        except UserProfileInfo.DoesNotExist:
            return None

    def get_user_with_ms_key(key):
        try:
            user = UserMedium.objects.filter(user_key=key,medium=Medium.objects.get(name='microsoft')).values_list('user_id',flat=True)
            if user:
                return User.objects.get(pk=user[0])
            else:
                return None
        except UserProfileInfo.DoesNotExist:
            return None

class UserMedium(models.Model):
    user_key = models.CharField(max_length=64)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    medium = models.ForeignKey(Medium, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class MSEmail(models.Model):
    subject = models.TextField(blank=True)
    body = models.TextField(blank=True)
    email_datetime = models.DateTimeField(auto_now_add=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    importance = models.CharField(choices=[('Low', 'Low'), ('Normal','Normal'), ('High','High')], max_length=10, default='Normal')
    size = models.IntegerField(default=0)
    delta_time_for_each_msg = models.IntegerField(blank=True, default=0)
    to_boss = models.BooleanField(default=False)
    to_team = models.BooleanField(default=False)
    is_work_related = models.BooleanField(default=False)
    ai_predicted_topic = models.CharField(max_length=50, blank=True)
    ai_predicted_sentiment = models.CharField(max_length=50, blank=True)
    ai_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject

class MSEmailRecipient(models.Model):
    recipient_type = models.CharField(choices=[
        ('to', 'To'),
        ('cc', 'CC'),
        ('bcc', 'BCC'),
    ], max_length=20)
    email = models.ForeignKey(MSEmail, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    from_boss = models.BooleanField(default=False)
    from_team = models.BooleanField(default=False)
    delta_time_for_each_msg = models.IntegerField(blank=True, default=0)
    is_work_related = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class MSEmailAttachment(models.Model):
    attachment = models.CharField(max_length=100)
    email = models.ForeignKey(MSEmail, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

class MSTeam(models.Model):
    ms_id = models.CharField(max_length=100)
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class UserMSTeam(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ms_team = models.ForeignKey(MSTeam, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

class MSTeamChannel(models.Model):
    ms_id = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    description = models.TextField()
    ms_team = models.ForeignKey(MSTeam, on_delete=models.CASCADE)
    # creator = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class MSTeamChannelMember(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ms_team_channel = models.ForeignKey(MSTeamChannel, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

class MSTeamMessageType(models.Model):
    message_type = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message_type

class MSTeamMessage(models.Model):
    ms_message_id = models.CharField(max_length=50)
    text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ms_team = models.ForeignKey(MSTeam, on_delete=models.CASCADE)
    ms_team_channel = models.ForeignKey(MSTeamChannel, on_delete=models.CASCADE)
    ms_team_message_type = models.ForeignKey(MSTeamMessageType, on_delete=models.CASCADE)
    # reply_to = models.ForeignKey(MSTeamMessage, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    ms_team_message_datetime = models.DateTimeField(auto_now_add=True)
    size = models.IntegerField(default=0)
    delta_time_for_each_msg = models.IntegerField(blank=True, default=0)
    to_boss = models.BooleanField(default=False)
    to_team = models.BooleanField(default=False)
    is_work_related = models.BooleanField(default=False)
    ai_predicted_topic = models.CharField(max_length=50, blank=True)
    ai_predicted_sentiment = models.CharField(max_length=50, blank=True)
    ai_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

class MSTeamMessageRecipient(models.Model):
    recipient_type = models.CharField(choices=[
        ('cm', 'Channel Message'),
        ('dm', 'Direct Message'),
    ], max_length=20)
    ms_team_message = models.ForeignKey(MSTeamMessage, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    from_boss = models.BooleanField(default=False)
    from_team = models.BooleanField(default=False)
    delta_time_for_each_msg = models.IntegerField(blank=True, default=0)
    is_work_related = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class MSTeamMessageAttachment(models.Model):
    attachment = models.CharField(max_length=100)
    ms_team_message = models.ForeignKey(MSTeamMessage, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

class MSCalendar(models.Model):
    subject = models.TextField(blank=True)
    body = models.TextField(blank=True)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE)
    start = models.DateTimeField(auto_now_add=True)
    end = models.DateTimeField(auto_now_add=True)
    # location = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject

class MSCalendarAttendees(models.Model):
    attendee = models.ForeignKey(User, on_delete=models.CASCADE)
    ms_calendar = models.ForeignKey(MSCalendar, on_delete=models.CASCADE)
    response = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.attendee.username

class SlackTeam(models.Model):
    slack_team_id = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_slack_team_with_key(key):
        return SlackTeam.objects.get(slack_team_id=key)

class slackUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    slack_team = models.ForeignKey(SlackTeam, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

class SlackChannel(models.Model):
    name = models.CharField(max_length=50)
    slack_channel_id = models.CharField(max_length=50)
    slack_team = models.ForeignKey(SlackTeam, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    slack_channel_datetime = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_slack_channel_with_key(key):
        return SlackChannel.objects.get(slack_channel_id=key)

class SlackChannelDescription(models.Model):
    slack_channel_description = models.CharField(choices=[
        ('topic', 'Topic'),
        ('purpose', 'Purpose'),
    ], max_length=100)
    text = models.TextField()
    slack_channel = models.ForeignKey(SlackChannel, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

class SlackChannelMember(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    slack_channel = models.ForeignKey(SlackChannel, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

class SlackMessageType(models.Model):
    message_type = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

class SlackMessage(models.Model):
    slack_message_id = models.CharField(max_length=50)
    text = models.TextField()
    slack_message_datetime = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    slack_team = models.ForeignKey(SlackTeam, on_delete=models.CASCADE)
    slack_channel = models.ForeignKey(SlackChannel, on_delete=models.CASCADE)
    # slack_message_type = models.ForeignKey(SlackMessageType, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    # reply_to = models.ForeignKey(SlackMessage, on_delete=models.CASCADE)
    size = models.IntegerField(default=0)
    delta_time_for_each_msg = models.IntegerField(blank=True, default=0)
    to_boss = models.BooleanField(default=False)
    to_team = models.BooleanField(default=False)
    is_work_related = models.BooleanField(default=False)
    ai_predicted_topic = models.CharField(max_length=50, blank=True)
    ai_predicted_sentiment = models.CharField(max_length=50, blank=True)
    ai_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

class SlackMessageRecipient(models.Model):
    recipient_type = models.CharField(choices=[
        ('cm', 'Channel Message'),
        ('dm', 'Direct Message'),
    ], max_length=20)
    slack_message = models.ForeignKey(SlackMessage, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    from_boss = models.BooleanField(default=False)
    from_team = models.BooleanField(default=False)
    delta_time_for_each_msg = models.IntegerField(blank=True, default=0)
    is_work_related = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class SlackMessageAttachment(models.Model):
    slack_message = models.ForeignKey(SlackMessage, on_delete=models.CASCADE)
    attachment = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

class JiraProject(models.Model):
    name = models.CharField(max_length=50)
    Key = models.CharField(max_length=50)
    jira_id = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class JiraIssue(models.Model):
    assignee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assignee')
    timeSpent = models.CharField(max_length=50)
    createDate = models.DateTimeField(auto_now_add=True)
    dueDate = models.DateTimeField(auto_now_add=True)
    resolutionDate = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50)
    reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reporter')
    name = models.CharField(max_length=50)
    summary = models.TextField()
    description = models.TextField(blank=True, null=True)
    jira_project = models.ForeignKey(JiraProject, on_delete=models.CASCADE)
    is_on_time = models.BooleanField(default=None, null=True, blank=True)

    def __str__(self):
        return self.name

class JiraProjectUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    jira_project = models.ForeignKey(JiraProject, on_delete=models.CASCADE)

class EmailSummary(models.Model):
    sender = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='sender')
    email = models.ForeignKey(MSEmail, on_delete=models.DO_NOTHING, related_name='email')
    recipient_type = models.CharField(max_length=10)
    total_recipients = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'email_summary'

class SlackmsgSummary(models.Model):
    slack_message = models.ForeignKey(SlackMessage, on_delete=models.DO_NOTHING, related_name='message')
    sender = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='slack_msg_sender')
    total_recipients = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'slack_msg_summary'

class MSTeammsgSummary(models.Model):
    msteam_message = models.ForeignKey(MSTeamMessage, on_delete=models.DO_NOTHING, related_name='message')
    sender = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='msteam_msg_sender')
    total_recipients = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'msteam_msg_summary'

class TaskSummary(models.Model):
    department = models.ForeignKey(Department, on_delete=models.DO_NOTHING, related_name='department')
    assignee = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='task_assignee')
    total_task = models.IntegerField()
    # Jira_project = models.ForeignKey(JiraProject, on_delete=models.DO_NOTHING, related_name='jira_project')
    status = models.CharField(max_length=50)
    class Meta:
        managed = False
        db_table = 'task_summary'

class KPI(models.Model):
    KPI_name = models.CharField(choices=[
        ('collaboration', 'Collaboration'),
        ('productivity', 'Productivity'),
        ('communication', 'Communication'),
        ('burnout', 'Burnout'),
        ('selfish_worker', 'Selfish Worker'),
        ('motivation', 'Motivation  (Toxicity Level)'),
        ('moral', 'Moral'),
        ('collective_intelligence', 'Collective Intelligence'),
    ], max_length=50)
    KPI_value = models.FloatField()
    Kpi_avg = models.FloatField()
    KPI_max_value = models.FloatField()
    Kpi_min_value = models.FloatField()
    Kpi_percentage = models.FloatField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

class KPISummary(models.Model):
    KPI_name = models.CharField(max_length=50)
    vgood = models.IntegerField()
    good = models.IntegerField()
    neutral = models.IntegerField()
    bad = models.IntegerField()
    vbad = models.IntegerField()
    class Meta:
        managed = False
        db_table = 'kpi_summary'


class person(models.Model):
    name = models.CharField(max_length=42)
    email = models.EmailField(max_length=75)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class communication(models.Model):
    medium = models.ForeignKey(Medium, on_delete=models.CASCADE)
    source = models.ForeignKey(person, on_delete=models.CASCADE, related_name='source')
    target = models.ForeignKey(person, on_delete=models.CASCADE, related_name='target')
    subject = models.TextField()
    body = models.TextField()
    date = models.DateTimeField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)