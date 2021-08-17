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
from frappe.model.document import Document

class AuditPlan(Document):
	@frappe.whitelist()
	def on_submit(self):
		self.update_action_card()

	def on_cancel(self):
		self.update_action_card_on_cancel()

	@frappe.whitelist()
	def update_action_card(self):
		for x in self.actions_card_table:
			frappe.db.sql("""update `tabAction Card` set audit=%s where name=%s """, (x.status, x.action_card))

	def update_action_card_on_cancel(self):
		for x in self.actions_card_table:
			frappe.db.sql("""update `tabAction Card` set audit=%s where name=%s """, ("", x.action_card))

pass