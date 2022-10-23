# Generated by Django 3.0.5 on 2020-06-18 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socialGraph', '0007_emailsummary'),
    ]

    operations = [
        migrations.CreateModel(
            name='SlackmsgSummary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_recipients', models.IntegerField()),
            ],
            options={
                'db_table': 'slack_msg_summary',
                'managed': False,
            },
        ),
        migrations.AddField(
            model_name='slackmessage',
            name='ai_predicted_sentiment',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='slackmessage',
            name='ai_predicted_topic',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='slackmessage',
            name='ai_status',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='slackmessage',
            name='delta_time_for_each_msg',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AddField(
            model_name='slackmessage',
            name='is_work_related',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='slackmessage',
            name='size',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='slackmessage',
            name='to_boss',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='slackmessage',
            name='to_team',
            field=models.BooleanField(default=False),
        ),
    ]
