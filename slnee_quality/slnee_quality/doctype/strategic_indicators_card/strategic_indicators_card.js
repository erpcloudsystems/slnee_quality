// Copyright (c) 2021, erpcloud.systems and contributors
// For license information, please see license.txt

frappe.ui.form.on('Strategic Indicators Card', {
	// refresh: function(frm) {

	// }
});

frappe.ui.form.on("Strategic Indicators Card","strategic_plan", function(frm){
    cur_frm.clear_table("strategic_goals_table");
    if(frm.doc.strategic_plan){
        frappe.model.with_doc("Strategic Plan", frm.doc.strategic_plan, function() {
        var tabletransfer= frappe.model.get_doc("Strategic Plan", frm.doc.strategic_plan);

			$.each(tabletransfer.strategic_goals_table, function(d, row){
            d = frm.add_child("strategic_goals_table");
            d.goal_name = row.goal_name;
            d.goal_code = row.goal_code;
            d.goal_description = row.goal_description;
            cur_frm.refresh_field("strategic_goals_table");
			});
    });
    }
});
frappe.ui.form.on("Strategic Indicators Card","validate", function(){
        if (cur_frm.doc.strategic_goals_table.length != 1){
            frappe.throw("Please Select Only One Strategic Goal");
        }
});