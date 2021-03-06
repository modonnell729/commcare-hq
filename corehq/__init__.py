from corehq.apps.domain.models import Domain
from corehq.apps.hqadmin.reports import AdminUserReport, AdminAppReport
from corehq.apps.reports.standard import (monitoring, inspect, export,
    deployments, sms, ivr)
import corehq.apps.receiverwrapper.reports as receiverwrapper
import phonelog.reports as phonelog
from corehq.apps.reports.commtrack import psi_prototype
from corehq.apps.reports.commtrack import standard as commtrack_reports
from corehq.apps.reports.commtrack import maps as commtrack_maps
import hashlib
from dimagi.utils.modules import to_function
import logging

from django.utils.translation import ugettext_noop as _

def REPORTS(project):
    from corehq.apps.reports.standard.cases.basic import CaseListReport
    from corehq.apps.reports.standard.cases.careplan import make_careplan_reports
    from corehq.apps.reports.standard.maps import DemoMapReport, DemoMapReport2, DemoMapCaseList

    reports = [
        (_("Monitor Workers"), (
            monitoring.WorkerActivityReport,
            monitoring.DailyFormStatsReport,
            monitoring.SubmissionsByFormReport,
            monitoring.FormCompletionTimeReport,
            monitoring.CaseActivityReport,
            monitoring.FormCompletionVsSubmissionTrendsReport,
            monitoring.WorkerActivityTimes,
        )),
        (_("Inspect Data"), (
            inspect.SubmitHistory, CaseListReport,
        )),
        (_("Manage Deployments"), (
            deployments.ApplicationStatusReport,
            receiverwrapper.SubmissionErrorReport,
            phonelog.FormErrorReport,
            phonelog.DeviceLogDetailsReport
        )),
        (_("Demos for Previewers"), (
            DemoMapReport, DemoMapReport2, DemoMapCaseList,
        )),
    ]
    
    if project.commtrack_enabled:
        reports.insert(0, (_("Commtrack"), (
            commtrack_reports.ReportingRatesReport,
            commtrack_reports.CurrentStockStatusReport,
            commtrack_reports.AggregateStockStatusReport,
            commtrack_reports.RequisitionReport,
            psi_prototype.VisitReport,
            psi_prototype.SalesAndConsumptionReport,
            psi_prototype.CumulativeSalesAndConsumptionReport,
            psi_prototype.StockOutReport,
            psi_prototype.StockReportExport,
            commtrack_maps.StockStatusMapReport,
            commtrack_maps.ReportingStatusMapReport,
        )))

    if project.has_careplan:
        from corehq.apps.app_manager.models import CareplanConfig
        config = CareplanConfig.for_domain(project.name)
        if config:
            cp_reports = tuple(make_careplan_reports(config))
            reports.insert(0, (_("Care Plans"), cp_reports))

    messaging_reports = (
        sms.MessagesReport,
        sms.MessageLogReport,
        ivr.CallLogReport,
        ivr.ExpectedCallbackReport,
    )

    messaging_reports += getattr(Domain.get_module_by_name(project.name), 'MESSAGING_REPORTS', ())

    messaging = (lambda project, user: (
        _("Logs") if project.commtrack_enabled else _("Messaging")), messaging_reports)

    if project.commconnect_enabled:
        reports.insert(0, messaging)
    else:
        reports.append(messaging)

    reports.extend(dynamic_reports(project))

    return reports
    
def dynamic_reports(project):
    """include any reports that can be configured/customized with static parameters for this domain"""
    for reportset in project.dynamic_reports:
        yield (reportset.section_title, filter(None, (make_dynamic_report(report, [reportset.section_title]) for report in reportset.reports)))

def make_dynamic_report(report_config, keyprefix):
    """create a report class the descends from a generic report class but has specific parameters set"""
    # a unique key to distinguish this particular configuration of the generic report
    report_key = keyprefix + [report_config.report, report_config.name]
    slug = hashlib.sha1(':'.join(report_key)).hexdigest()[:12]
    kwargs = dict(report_config.kwargs)
    kwargs.update({
            'name': report_config.name,
            'slug': slug,
        })
    if report_config.previewers_only:
        # note this is a classmethod that will be injected into the dynamic class below
        @classmethod
        def show_in_navigation(cls, domain=None, project=None, user=None):
            return user and user.is_previewer()
        kwargs['show_in_navigation'] = show_in_navigation

    try:
        metaclass = to_function(report_config.report, failhard=True)
    except StandardError:
        logging.error('dynamic report config for [%s] is invalid' % report_config.report)
        return None

    # dynamically create a report class
    return type('DynamicReport%s' % slug, (metaclass,), kwargs)



from corehq.apps.data_interfaces.interfaces import CaseReassignmentInterface
from corehq.apps.importer.base import ImportCases

DATA_INTERFACES = (
    (_("Export Data"), (
        export.ExcelExportReport,
        export.CaseExportReport,
        export.DeidExportReport,
    )),
)

EDIT_DATA_INTERFACES = (
    (_('Edit Data'), (
        CaseReassignmentInterface,
        ImportCases
    )),
)


from corehq.apps.adm.reports.supervisor import SupervisorReportsADMSection

ADM_SECTIONS = (
    (_('Supervisor Report'), (
        SupervisorReportsADMSection,
    )),
)

from corehq.apps.adm.admin import columns, reports

ADM_ADMIN_INTERFACES = (
    (_("ADM Default Columns"), (
        columns.ReducedADMColumnInterface,
        columns.DaysSinceADMColumnInterface,
        columns.ConfigurableADMColumnInterface
    )),
    (_("ADM Default Reports"), (
        reports.ADMReportAdminInterface,
    ))
)

from corehq.apps.indicators.admin import document_indicators, couch_indicators, dynamic_indicators

INDICATOR_ADMIN_INTERFACES = (
    (_("Form Based Indicators"), (
        document_indicators.FormLabelIndicatorDefinitionAdminInterface,
        document_indicators.FormAliasIndicatorDefinitionAdminInterface,
        document_indicators.CaseDataInFormAdminInterface,
    )),
    (_("Case Based Indicators"), (
        document_indicators.FormDataInCaseAdminInterface,
    )),
    (_("Dynamic Indicators"), (
        dynamic_indicators.CombinedIndicatorAdminInterface,
    )),
    (_("Couch Based Indicators"), (
        couch_indicators.CouchIndicatorAdminInterface,
        couch_indicators.CountUniqueCouchIndicatorAdminInterface,
        couch_indicators.MedianCouchIndicatorAdminInterface,
        couch_indicators.SumLastEmittedCouchIndicatorAdminInterface,
    )),
)

from corehq.apps.announcements.interface import (
    ManageGlobalHQAnnouncementsInterface,
    ManageReportAnnouncementsInterface)

ANNOUNCEMENTS_ADMIN_INTERFACES = (
    (_("Manage Announcements"), (
        ManageGlobalHQAnnouncementsInterface,
        ManageReportAnnouncementsInterface
    )),
)

from corehq.apps.appstore.interfaces import CommCareExchangeAdvanced

APPSTORE_INTERFACES = (
    (_('App Store'), (
        CommCareExchangeAdvanced,
    )),
)

from corehq.apps.reports.standard.domains import OrgDomainStatsReport, AdminDomainStatsReport

BASIC_REPORTS = (
    (_('Project Stats'), (
        OrgDomainStatsReport,
    )),
)

ADMIN_REPORTS = (
    (_('Domain Stats'), (
        AdminDomainStatsReport,
        AdminUserReport,
        AdminAppReport,
    )),
)

from corehq.apps.hqwebapp.models import *

TABS = (
    ProjectInfoTab,
    ReportsTab,
    ProjectDataTab,
    CommTrackSetupTab,
    ProjectUsersTab,
    ApplicationsTab,
    CloudcareTab,
    MessagingTab,
    ExchangeTab,
    OrgReportTab,
    OrgSettingsTab, # separate menu?
    AdminTab,
)
