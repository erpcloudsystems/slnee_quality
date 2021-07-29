# Copyright (c) 2021, erpcloud.systems and contributors
# For license information, please see license.txt

# import frappe
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
# import frappe


class Mission(Document):
	def validate(self):
		self.update_mission_table()
		self.update_stage_table()
		self.update_percent_complete()

	def update_mission_table(self):
		q1 = frappe.db.sql("""update `tabMissions Table` set status = %s where
						name=%s """, (self.status,self.mission_t))
		return q1

	def update_stage_table(self):
		stage = frappe.db.sql("""select stage from `tabMissions Table` where name=%s """, self.mission_t)[0][0]

		missions_counts = frappe.db.count('Missions Table', dict(stage=stage))



		completed_missions = frappe.db.sql("""select count(name) from `tabMissions Table` where
				stage=%s and status = 'Completed' """, stage)[0][0]

		completed_percent = flt((flt(completed_missions,2)/flt(missions_counts,2))*100,2)

		q2 = frappe.db.sql("""update `tabStages Table` set stage_progress = %s where
								name=%s """, (completed_percent, stage))
		return q2




	def update_percent_complete(self):
		parent = frappe.db.sql("""select parent from `tabMissions Table` where name=%s """, self.mission_t)[0][0]

		count_stage = frappe.db.count('Stages Table', dict(parent=parent))
		total_progress = frappe.db.sql("""select sum(stage_progress) from `tabStages Table` where
				parent=%s """, parent)[0][0]

		total = flt(total_progress / count_stage, 2)

		q3 = frappe.db.sql("""update `tabOperational Plan` set progress = %s where
								name=%s """, (total, parent))
		return q3


	pass
