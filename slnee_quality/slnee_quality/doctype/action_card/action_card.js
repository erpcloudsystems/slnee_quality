// Copyright (c) 2021, erpcloud.systems and contributors
// For license information, please see license.txt

frappe.ui.form.on("Action Card", {
	setup: function(frm) {
		frm.set_query("procedure_repository", function() {
			return {
				filters: [
					["Procedure Repository","docstatus", "=", "1"]
				]
			};
		});
	}
});

frappe.ui.form.on("Action Card", "on_submit", function(frm) {
    frappe.db.set_value("Business Engineering Request",  cur_frm.doc.request, "action_card", cur_frm.doc.name);
});

frappe.ui.form.on("Action Card",{
    setup: function(frm) {
		cur_frm.fields_dict["internal_action_executers"].grid.get_field("employee").get_query = function(doc, cdt, cdn)
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