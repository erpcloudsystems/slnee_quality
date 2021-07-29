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
		for x in self.missions_table:
			if self.workflow_state == "Approved" and not x.mission_created:
				self.create_missions()
				x.mission_created = 1

	def on_update_after_submit(self):
		for x in self.missions_table:
			if self.workflow_state == "Approved" and not x.mission_created:
				self.create_missions()
				x.mission_created = 1

	def create_missions(self):
		for mission in self.missions_table:
			self.mission_details(mission)

	def mission_details(self, mission):
			return frappe.get_doc(dict(
			doctype='Mission',
			stage=mission.stage_name,
			operational_plan=self.name,
			mission_t= mission.name,
			status= mission.status,
			subject= mission.subject,
			start_date= mission.start_date,
			duration= mission.duration,
			description= mission.description
		)).insert()


	pass
