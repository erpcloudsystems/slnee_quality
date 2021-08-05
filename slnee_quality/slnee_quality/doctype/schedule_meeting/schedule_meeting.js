// Copyright (c) 2021, erpcloud.systems and contributors
// For license information, please see license.txt

frappe.ui.form.on("Schedule Meeting", {
	setup: function(frm) {
		frm.set_query("operational_plan", function() {
			return {
				filters: [
					["Operational Plan","workflow_state", "in", ["Pending Approval","Entering Data ...","Modification Requested","Planning Manager Approved"]]
				]
			};
		});
	}
});

frappe.ui.form.on("Schedule Meeting",{
    setup: function(frm) {
		cur_frm.fields_dict["departments"].grid.get_field("employee").get_query = function(doc, cdt, cdn)
		{
		    var d = locals[cdt][cdn];
			return {
				filters:  [
					["Employee","department","in", d.department],
				]

					};
		};
	}
});
