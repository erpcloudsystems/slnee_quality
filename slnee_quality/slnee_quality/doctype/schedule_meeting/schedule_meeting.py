from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class ScheduleMeeting(Document):
    pass

@frappe.whitelist()
def calendar_view(start, end):
        if not frappe.has_permission("Shows", "read"):
                raise frappe.PermissionError

        return frappe.db.sql("""select
                timestamp(`date`, start_time) as start,
                timestamp(`date`, end_time) as end,
                name,
                subject as title,
                color,
                status
                
        from `tabSchedule Meeting`
        where `date` between %(start)s and %(end)s""", {
                "start": start,
                "end": end
        }, as_dict=True)