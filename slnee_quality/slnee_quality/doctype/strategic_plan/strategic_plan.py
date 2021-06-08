# Copyright (c) 2021, erpcloud.systems and contributors
# For license information, please see license.txt

# import frappe
from __future__ import unicode_literals
import frappe

from frappe.utils import getdate, nowdate
from frappe import _
from frappe.model.document import Document
from frappe.utils import cstr, get_datetime, formatdate

class StrategicPlan(Document):
	def validate(self):
		self.validate_duplicate_record()
	def validate_duplicate_record(self):
		res = frappe.db.sql("""
			select name from `tabStrategic Plan`
			where workflow_state NOT IN ("Approved","Rejected","Completed") 
				and name != %s
				and docstatus != 2
		""", (self.name))
		if res:
			frappe.throw(_("You Can't Create A New Strategic Plan While Another Plan Is Still In Progress").format(
				frappe.bold(self.name)))
	#pass
