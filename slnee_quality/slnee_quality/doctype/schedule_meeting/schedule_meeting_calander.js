// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

frappe.views.calendar["Schedule Meeting"] = {
	field_map: {
		"start": "start",
		"end": "end",
		"id": "name",
		"title": "subject",
		"status": "status"
	},

	get_events_method: "frappe.desk.doctype.event.event.get_events"
}

frappe.views.calendar['Schedule Meeting'] = {
    field_map: {
        start: 'start',
        end: 'end',
        id: 'name',
        title: 'subject',
        status: 'status',
        color: 'color'
    },
    order_by: 'end',
    get_events_method: 'slnee_quality.slnee_quality.doctype.schedule_meeting.schedule_meeting.calendar_view'
}