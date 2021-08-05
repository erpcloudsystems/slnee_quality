# Copyright (c) 2021, erpcloud.systems and contributors
# For license information, please see license.txt
from __future__ import unicode_literals
import frappe
from frappe import _
from six import iteritems
from email_reply_parser import EmailReplyParser
from frappe.utils import (flt, getdate, get_url, now,
	nowtime, get_time, today, get_datetime, add_days)
from erpnext.controllers.queries import get_filters_cond
from frappe.desk.reportview import get_match_cond
from erpnext.hr.doctype.daily_work_summary.daily_work_summary import get_users_email
from erpnext.hr.doctype.holiday_list.holiday_list import is_holiday
from frappe.model.document import Document
from erpnext.education.doctype.student_attendance.student_attendance import get_holiday_list
# import frappe
from frappe.model.document import Document

class OperationalPlan(Document):
	def validate(self):
		if self.workflow_state == "Approved":
			self.create_missions()

	def on_update_after_submit(self):
		if self.workflow_state == "Approved":
			self.create_missions()

	def create_missions(self):
		for mission in self.missions_table:
			if not mission.mission_no:
				self.mission_details(mission)

	def mission_details(self, mission):
		doc = frappe.get_doc(dict(
		doctype='Mission',
		stage=mission.stage_name,
		operational_plan=self.name,
		mission_t= mission.name,
		status= mission.status,
		subject= mission.subject,
		start_date= mission.start_date,
		mission_weight=mission.mission_weight,
		unit_of_execution_duration= mission.unit_of_execution_duration,
		duration= mission.duration,
		description= mission.description
		))
		doc.insert()
		frappe.db.set_value('Missions Table', mission.name, 'mission_no', doc.name)
		self.reload()


	pass


@frappe.whitelist()
def calendar_view(start, end):
	if not frappe.has_permission("Shows", "read"):
		raise frappe.PermissionError

	return frappe.db.sql("""select
                timestamp(`start_date`) as start,
                timestamp(`end_date`) as end,
                name,
                CONCAT_WS(' - ',name,plan_name) as subject,
                workflow_state as status

        from `tabOperational Plan`
        where `posting_date` between %(start)s and %(end)s""", {
		"start": start,
		"end": end
	}, as_dict=True)