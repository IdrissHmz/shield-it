from django.contrib import admin
from socialGraph.models import *
# Register your models here.

class organizationAdmin(admin.ModelAdmin):
    list_display = ("name",)

class departmentAdmin(admin.ModelAdmin):
    list_display = ("name",)

class mediumAdmin(admin.ModelAdmin):
    list_display = ("name",)


class KPIAdmin(admin.ModelAdmin):
    list_display = ("user", "KPI_name", "KPI_value", "Kpi_avg", "KPI_max_value", "Kpi_min_value", "Kpi_percentage")

class KPISummaryAdmin(admin.ModelAdmin):
    list_display = ("KPI_name", "vgood", "good", "neutral", "bad", "vbad")
    list_display_links = None

class EmailSummaryAdmin(admin.ModelAdmin):
    list_display = ("sender","email", "recipient_type", "total_recipients")
    list_display_links = None

class SlackmsgSummaryAdmin(admin.ModelAdmin):
    list_display = ("sender","slack_message", "total_recipients")
    list_display_links = None


class MSTeammsgSummaryAdmin(admin.ModelAdmin):
    list_display = ("sender","msteam_message", "total_recipients")
    list_display_links = None

class TaskSummaryAdmin(admin.ModelAdmin):
    list_display = ("department", 'total_task', 'assignee', 'status')
    list_display_links = None

    # def has_add_permission(self, request, obj=None):
    #     return False

    # def has_change_permission(self, request, obj=None):
    #     return False

    # def has_delete_permission(self, request, obj=None):
    #     return False

# class personAdmin(admin.ModelAdmin):
#     list_display = ("name", "email", "organization", "department")

# class communicationAdmin(admin.ModelAdmin):
#     list_display = ("source", "target", "medium", "date", "subject")

admin.site.site_header = 'Pulsecorp'
admin.site.register(Organization, organizationAdmin)
admin.site.register(Department, departmentAdmin)
admin.site.register(Medium, mediumAdmin)
admin.site.register(UserProfileInfo)
admin.site.register(SlackTeam)
admin.site.register(SlackChannel)
admin.site.register(SlackChannelMember)
admin.site.register(MSEmail)
admin.site.register(MSEmailRecipient)
admin.site.register(SlackMessage)
admin.site.register(SlackMessageRecipient)
admin.site.register(MSTeam)
admin.site.register(MSTeamChannel)
admin.site.register(MSTeamChannelMember)
admin.site.register(MSTeamMessage)
admin.site.register(MSTeamMessageType)
admin.site.register(MSTeamMessageRecipient)
admin.site.register(MSCalendar)
admin.site.register(MSCalendarAttendees)
admin.site.register(JiraProject)
admin.site.register(JiraIssue)
admin.site.register(Country)
admin.site.register(State)
admin.site.register(City)
admin.site.register(ContentType)
admin.site.register(UserMedium)
admin.site.register(EmailSummary, EmailSummaryAdmin)
admin.site.register(SlackmsgSummary, SlackmsgSummaryAdmin)
admin.site.register(MSTeammsgSummary, MSTeammsgSummaryAdmin)
admin.site.register(TaskSummary, TaskSummaryAdmin)
admin.site.register(KPI, KPIAdmin)
admin.site.register(KPISummary, KPISummaryAdmin)