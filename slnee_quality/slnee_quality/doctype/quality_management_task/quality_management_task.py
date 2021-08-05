from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class QualityManagementTask(Document):
	pass

@frappe.whitelist()
def calendar_view(start, end):
	if not frappe.has_permission("Shows", "read"):
		raise frappe.PermissionError

	return frappe.db.sql("""select
                timestamp(`start_date`) as start,
            	timestamp(`start_date`) as end,
                name,
                subject
                
        from `tabQuality Management Task`
        where `start_date` between %(start)s and %(end)s""", {
		"start": start,
		"end": end
	}, as_dict=True)
