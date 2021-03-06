from django.conf.urls.defaults import *
from corehq.apps.reminders.models import REMINDER_TYPE_ONE_TIME
from corehq.apps.reminders.views import (
    CreateScheduledReminderView,
    EditScheduledReminderView,
    RemindersListView,
    CreateComplexScheduledReminderView,
    KeywordsListView,
)

urlpatterns = patterns('corehq.apps.reminders.views',
    url(r'^$', 'default', name='reminders_default'),
    url(r'^all/$', 'list_reminders', name='list_reminders'),
    url(r'^list/$', RemindersListView.as_view(), name=RemindersListView.urlname),
    url(r'^add_fixed/$', 'add_reminder', name='add_reminder'),
    url(r'^edit_fixed/(?P<handler_id>[\w-]+)/$', 'add_reminder', name='edit_reminder'),
    url(r'^delete/(?P<handler_id>[\w-]+)/$', 'delete_reminder', name='delete_reminder'),
    url(r'^scheduled/', 'scheduled_reminders', name='scheduled_reminders'),
    url(r'^add_complex/', 'add_complex_reminder_schedule', name='add_complex_reminder_schedule'),
    url(r'^edit_complex/(?P<handler_id>[\w-]+)/$', 'add_complex_reminder_schedule', name='edit_complex'),
    url(r'^schedule/complex/$',
        CreateComplexScheduledReminderView.as_view(), name=CreateComplexScheduledReminderView.urlname),
    url(r'^schedule/(?P<handler_id>[\w-]+)/$',
        EditScheduledReminderView.as_view(), name=EditScheduledReminderView.urlname),
    url(r'^schedule/$',
        CreateScheduledReminderView.as_view(), name=CreateScheduledReminderView.urlname),
    url(r'^keywords/$', 'manage_keywords', name='manage_keywords'),
    url(r'^keywords_new/$', KeywordsListView.as_view(), name=KeywordsListView.urlname),
    url(r'^keywords/add/$', 'add_keyword', name='add_keyword'),
    url(r'^keywords/edit/(?P<keyword_id>[\w-]+)/$', 'add_keyword', name='edit_keyword'),
    url(r'^delete_keyword/(?P<keyword_id>[\w-]+)/$', 'delete_keyword', name='delete_keyword'),
    url(r'^survey_list/$', 'survey_list', name='survey_list'),
    url(r'^add_survey/$', 'add_survey', name='add_survey'),
    url(r'^edit_survey/(?P<survey_id>[\w-]+)/$', 'add_survey', name='edit_survey'),
    url(r'^add_sample/$', 'add_sample', name='add_sample'),
    url(r'^edit_sample/(?P<sample_id>[\w-]+)/$', 'add_sample', name='edit_sample'),
    url(r'^sample_list/$', 'sample_list', name='sample_list'),
    url(r'^edit_contact/(?P<sample_id>[\w-]+)/(?P<case_id>[\w-]+)/$', 'edit_contact', name='edit_contact'),
    url(r'^reminders_in_error/$', 'reminders_in_error', name='reminders_in_error'),
    url(r'^one_time_reminders/$', 'list_reminders', name='one_time_reminders', kwargs={"reminder_type" : REMINDER_TYPE_ONE_TIME}),
    url(r'^one_time_reminders/add/$', 'add_one_time_reminder', name='add_one_time_reminder'),
    url(r'^one_time_reminders/edit/(?P<handler_id>[\w-]+)/$', 'add_one_time_reminder', name='edit_one_time_reminder'),
    url(r'^one_time_reminders/copy/(?P<handler_id>[\w-]+)/$', 'copy_one_time_reminder', name='copy_one_time_reminder'),
)
