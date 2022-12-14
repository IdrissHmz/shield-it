from django.db import models

# Create your models here.
class UserProfile(models.Model):
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)
    email_address = models.EmailField(max_length=254)
    age = models.IntegerField()
    gender= models.CharField(max_length=1,null=True,default='M')
    job_title = models.CharField(max_length=50, blank=True)
    office_location = models.CharField(max_length=256)
    mobile_phone = models.CharField(max_length=10)
    date_of_bith = models.DateTimeField()
    employment_date = models.DateTimeField()
    team = models.CharField(max_length=256)
    project = models.CharField(max_length=256)
    department = models.CharField(max_length=256)
    organization = models.CharField(max_length=256)
    martial_status = models.CharField(max_length=10, default='single', null=True)
    address = models.CharField(max_length=256)
    location = models.CharField(max_length=256)
    latitude = models.FloatField(blank=True, null=True, verbose_name=("Latitude"))
    longitude= models.FloatField(blank=True, null=True, verbose_name=("Longitude"))
    hierarchical_superior = models.ForeignKey('self', null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    
    # portfolio_site = models.URLField(blank=True)
    # profile_pic = models.ImageField(upload_to='profile_pics',blank=True)
    
    def __str__(self):
        return self.user.username

class Email(models.Model):
    text = models.TextField()
    employee =  models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    received_datetime = models.DateTimeField()
    sent_datetime = models.DateTimeField()
    has_attachments = models.BooleanField()
    subject = models.CharField(max_length=256)
    is_read = models.BooleanField()
    is_draft = models.BooleanField()
    #from_id = models.ForeignKey(UserProfile, null=True, on_delete=models.CASCADE)
    from_name = models.CharField(max_length=256)
    from_email = models.EmailField(max_length=254)
    # the fields json below will have the following format for example: {to_recipients:[emain@adress.com, ...]} 
    to_recipients = models.JSONField()
    cc_recipients = models.JSONField()
    bcc_recipients = models.JSONField()
    reply_to = models.JSONField()
    if_forwarded = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
