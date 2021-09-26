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

class StrategicPlanProgram(Document):
	def validate(self):
		if self.workflow_state == "Approved":
			self.create_actions()

	def create_actions(self):
		for action in self.actions_table:
			self.action_details(action)

	def action_details(self, action):
			return frappe.get_doc(dict(
			doctype="Strategic Actions",
			linked_program =self.name,
			program_number=self.program_number,
			program_name=self.program_name,
			strategic_plan=self.strategic_plan,
			action_name=action.action_name,
			action_code=action.action_code,
			action_description=action.action_description,
			action_owner=action.action_owner,
			start_date=action.start_date,
			target_stakeholders=action.target_stakeholders,
			end_date=action.end_date
		)).insert()

	pass
