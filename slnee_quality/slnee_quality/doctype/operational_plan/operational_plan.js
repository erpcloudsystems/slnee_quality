// Copyright (c) 2021, erpcloud.systems and contributors
// For license information, please see license.txt

frappe.ui.form.on("Operational Plan", {
	setup: function(frm) {
		frm.set_query("program", function() {
			return {
				filters: [
					["Strategic Plan Program","workflow_state", "in", "Approved"],
					["Strategic Plan Program","docstatus", "in", "1"]
				]
			};
		});
	}
});


frappe.ui.form.on('Operational Plan',{
        setup: function(frm) {
    		cur_frm.fields_dict['missions_table'].grid.get_field("stage").get_query = function(doc, cdt, cdn)
    		{
    			return {
    				filters:  [
    					["Stages Table","parent", "in", cur_frm.doc.name]
    				]

    					};
    		};
    	}
    });

frappe.ui.form.on("Operational Plan", {
    refresh: (frm, cdt, cdn) => {
        if(frm.doc.workflow_state == "Approved" && frm.doc.end_date <= get_today()){
            frm.add_custom_button("End Plan", () => {
                if (frm.doc.end_date > get_today()) {
                    frappe.throw("لا يمكن إنهاء الخطة قبل تاريخ إنتهائها");
                }
                else {
                cur_frm.set_value("workflow_state", "Completed");
                cur_frm.save('Update');
                }

            }).addClass("btn-primary").css({'color':'white'});
        }
    }
});

frappe.ui.form.on("Operational Plan","program", function(frm){
    cur_frm.clear_table("actions_table");
    if(frm.doc.program){
        frappe.model.with_doc("Strategic Plan Program", frm.doc.program, function() {
        var tabletransfer= frappe.model.get_doc("Strategic Plan Program", frm.doc.program);
			$.each(tabletransfer.actions_table, function(d, row){
            d = frm.add_child("actions_table");
            d.sub_goal = row.sub_goal;
            d.sub_goal_code = row.sub_goal_code;
            d.sub_goal_name = row.sub_goal_name;
            d.sub_goal = row.sub_goal_description;
            d.action_code = row.action_code;
            d.action_name = row.action_name;
            d.action_description = row.action_description;
            cur_frm.refresh_field("actions_table");
			});
    });
    }
});

frappe.ui.form.on("Operational Plan",{
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