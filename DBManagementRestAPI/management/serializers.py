from rest_framework import serializers 
from management.models import UserProfile
from management.models import Email
 
 
class UserSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = UserProfile
        fields = ('id',
                  'first_name',
                  'last_name',
                  'email_address',
                  'age',
                  'gender',
                  'job_title',
                  'office_location',
                  'mobile_phone',
                  'date_of_bith',
                  'employment_date',
                  'team',
                  'project',
                  'department',
                  'organization',
                  'martial_status',
                  'address',
                  'location',
                  'latitude',
                  'longitude',
                  'hierarchical_superior')


class EmailSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Email
        fields = ('id',
                  'employee',
                  'received_datetime',
                  'sent_datetime',
                  'has_attachments',
                  'subject',
                  'is_read',
                  'is_draft',
                  'from_name',
                  'from_email',
                  'to_recipients',
                  'cc_recipients',
                  'bcc_recipients',
                  'reply_to',
                  'if_forwarded')