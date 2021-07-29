// Copyright (c) 2021, erpcloud.systems and contributors
// For license information, please see license.txt

cur_frm.add_fetch('meeting',  'subject',  'meeting_subject');
cur_frm.add_fetch('meeting',  'location',  'meeting_location');
cur_frm.add_fetch('meeting',  'date',  'meeting_date');
cur_frm.add_fetch('meeting',  'start_time',  'start_time');
cur_frm.add_fetch('meeting',  'end_time',  'end_time');

frappe.ui.form.on("Meeting Record", {
	setup: function(frm) {
		frm.set_query("meeting", function() {
			return {
				filters: [
					["Schedule Meeting","workflow_state", "in", "Approved"]
				]
			};
		});
	}
});

frappe.ui.form.on("Meeting Record","meeting", function(frm){
    cur_frm.clear_table("attendance");
    if(frm.doc.meeting){
        frappe.model.with_doc("Schedule Meeting", frm.doc.meeting, function() {
        var tabletransfer= frappe.model.get_doc("Schedule Meeting", frm.doc.meeting);
			$.each(tabletransfer.departments, function(d, row){
            d = frm.add_child("attendance");
            d.name1 = row.employee_name;
            cur_frm.refresh_field("attendance");
			});
    });
    }
});
