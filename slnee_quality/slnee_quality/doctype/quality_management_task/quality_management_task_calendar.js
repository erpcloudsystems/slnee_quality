// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

frappe.views.calendar['Quality Management Task'] = {
    field_map: {
        start: 'start',
        end: 'end',
        id: 'name',
        title: 'subject',
        status: 'status',
        color: 'color'
    },
    order_by: 'start_date',
    get_events_method: 'slnee_quality.slnee_quality.doctype.quality_management_task.quality_management_task.calendar_view'
}