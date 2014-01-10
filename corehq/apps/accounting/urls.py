from django.conf.urls.defaults import *
from corehq import AccountingAdminInterfaceDispatcher
from corehq.apps.accounting.dispatcher import SubscriptionAdminInterfaceDispatcher
from corehq.apps.accounting.views import ManageBillingAccountView, EditSubscriptionView, NewBillingAccountView


urlpatterns = patterns('corehq.apps.accounting.views',
    url(r'^view_billing_accounts/$', 'view_billing_accounts', name='view_billing_accounts'),
    url(r'^accounting_default/$', 'accounting_default', name='accounting_default'),
    url(r'^accounts/(\d+)/', ManageBillingAccountView.as_view(), name='manage_billing_account'),
    url(r'^accounts/new/', NewBillingAccountView.as_view()),
    url(r'^subscriptions/(\d+)/', EditSubscriptionView.as_view()),
    url(AccountingAdminInterfaceDispatcher.pattern(), AccountingAdminInterfaceDispatcher.as_view(),
        name=AccountingAdminInterfaceDispatcher.name()),
    url(SubscriptionAdminInterfaceDispatcher.pattern(), SubscriptionAdminInterfaceDispatcher.as_view(),
        name=SubscriptionAdminInterfaceDispatcher.name()),
)
