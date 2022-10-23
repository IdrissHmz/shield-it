# Generated by Django 3.0.5 on 2020-06-05 12:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='ContentType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=42)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='JiraProject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('Key', models.CharField(max_length=50)),
                ('jira_id', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Medium',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='MSCalendar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.TextField(blank=True)),
                ('body', models.TextField(blank=True)),
                ('start', models.DateTimeField(auto_now_add=True)),
                ('end', models.DateTimeField(auto_now_add=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('organizer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MSEmail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.TextField(blank=True)),
                ('body', models.TextField(blank=True)),
                ('email_datetime', models.DateTimeField(auto_now_add=True)),
                ('ai_predicted_topic', models.CharField(max_length=50)),
                ('ai_predicted_sentiment', models.CharField(max_length=50)),
                ('ai_status', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MSTeam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ms_id', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='MSTeamChannel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ms_id', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('ms_team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='socialGraph.MSTeam')),
            ],
        ),
        migrations.CreateModel(
            name='MSTeamMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ms_message_id', models.CharField(max_length=50)),
                ('text', models.TextField()),
                ('ms_team_message_datetime', models.DateTimeField(auto_now_add=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='socialGraph.ContentType')),
                ('ms_team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='socialGraph.MSTeam')),
                ('ms_team_channel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='socialGraph.MSTeamChannel')),
            ],
        ),
        migrations.CreateModel(
            name='MSTeamMessageType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message_type', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=42)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='socialGraph.City')),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='socialGraph.Country')),
            ],
        ),
        migrations.CreateModel(
            name='SlackChannel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('slack_channel_id', models.CharField(max_length=50)),
                ('slack_channel_datetime', models.DateTimeField(auto_now_add=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SlackMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slack_message_id', models.CharField(max_length=50)),
                ('text', models.TextField()),
                ('slack_message_datetime', models.DateTimeField(auto_now_add=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='socialGraph.ContentType')),
                ('slack_channel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='socialGraph.SlackChannel')),
            ],
        ),
        migrations.CreateModel(
            name='SlackMessageType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message_type', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='SlackTeam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slack_team_id', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfileInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('portfolio_site', models.URLField(blank=True)),
                ('profile_pic', models.ImageField(blank=True, upload_to='profile_pics')),
                ('job_title', models.CharField(blank=True, max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='socialGraph.Department')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='socialGraph.Organization')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserMSTeam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('ms_team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='socialGraph.MSTeam')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserMedium',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_key', models.CharField(max_length=64)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('medium', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='socialGraph.Medium')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.CharField(max_length=50)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='socialGraph.Country')),
            ],
        ),
        migrations.CreateModel(
            name='slackUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('slack_team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='socialGraph.SlackTeam')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SlackMessageAttachment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attachment', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('slack_message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='socialGraph.SlackMessage')),
            ],
        ),
        migrations.AddField(
            model_name='slackmessage',
            name='slack_team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='socialGraph.SlackTeam'),
        ),
        migrations.AddField(
            model_name='slackmessage',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='SlackChannelMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('slack_channel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='socialGraph.SlackChannel')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SlackChannelDescription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slack_channel_description', models.CharField(choices=[('topic', 'Topic'), ('purpose', 'Purpose')], max_length=100)),
                ('text', models.TextField()),
                ('status', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('slack_channel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='socialGraph.SlackChannel')),
            ],
        ),
        migrations.AddField(
            model_name='slackchannel',
            name='slack_team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='socialGraph.SlackTeam'),
        ),
        migrations.CreateModel(
            name='person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=42)),
                ('email', models.EmailField(max_length=75)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='socialGraph.Department')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='socialGraph.Organization')),
            ],
        ),
        migrations.AddField(
            model_name='organization',
            name='state',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='socialGraph.State'),
        ),
        migrations.CreateModel(
            name='MSTeamMessageAttachment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attachment', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('ms_team_message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='socialGraph.MSTeamMessage')),
            ],
        ),
        migrations.AddField(
            model_name='msteammessage',
            name='ms_team_message_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='socialGraph.MSTeamMessageType'),
        ),
        migrations.AddField(
            model_name='msteammessage',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='MSEmailRecipient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipient_type', models.CharField(choices=[('to', 'To'), ('cc', 'CC'), ('bcc', 'BCC')], max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('email', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='socialGraph.MSEmail')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MSEmailAttachment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attachment', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('email', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='socialGraph.MSEmail')),
            ],
        ),
        migrations.CreateModel(
            name='MSCalendarAttendees',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('response', models.CharField(blank=True, max_length=50)),
                ('attendee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('ms_calendar', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='socialGraph.MSCalendar')),
            ],
        ),
        migrations.CreateModel(
            name='JiraProjectUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jira_project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='socialGraph.JiraProject')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='JiraIssue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timeSpent', models.CharField(max_length=50)),
                ('createDate', models.DateTimeField(auto_now_add=True)),
                ('dueDate', models.DateTimeField(auto_now_add=True)),
                ('resolutionDate', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=50)),
                ('summary', models.TextField()),
                ('description', models.TextField(blank=True, null=True)),
                ('assignee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assignee', to=settings.AUTH_USER_MODEL)),
                ('reporter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reporter', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='communication',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.TextField()),
                ('body', models.TextField()),
                ('date', models.DateTimeField(blank=True, null=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('medium', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='socialGraph.Medium')),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='source', to='socialGraph.person')),
                ('target', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='target', to='socialGraph.person')),
            ],
        ),
        migrations.AddField(
            model_name='city',
            name='state',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='socialGraph.State'),
        ),
    ]
