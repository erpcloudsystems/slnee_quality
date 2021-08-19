// Copyright (c) 2021, erpcloud.systems and contributors
// For license information, please see license.txt

frappe.ui.form.on("Strategic Plan Program", {
	setup: function(frm) {
		frm.set_query("strategic_plan", function() {
			return {
				filters: [
					["Strategic Plan","workflow_state", "in", "Approved"],
					["Strategic Plan","docstatus", "in", "1"]
				]
			};
		});
	}
});

frappe.ui.form.on("Strategic Plan Program","strategic_plan", function(frm){
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

//frappe.ui.form.on('Strategic Plan Program',{
//        setup: function(frm) {
//    		cur_frm.fields_dict['sub_goals_table'].grid.get_field("main_goal").get_query = function(doc, cdt, cdn)
//    		{
//    			return {
//    				filters:  [
//    					["Strategic Goals","parent", "in", cur_frm.doc.strategic_plan]
//    				]
//
//    					};
//    		};
//    	}
//    });

frappe.ui.form.on('Strategic Plan Program',{
        setup: function(frm) {
    		cur_frm.fields_dict['actions_table'].grid.get_field("sub_goal").get_query = function(doc, cdt, cdn)
    		{
    			return {
    				filters:  [
    					["Sub Goals","parent", "in", cur_frm.doc.name]
    				]

    					};
    		};
    	}
    });

//frappe.ui.form.on("Strategic Plan Program","validate", function(){
//        if (cur_frm.doc.strategic_goals_table.length > 1){
//            frappe.throw("Please Select Only One Strategic Goal");
//        }
//});

frappe.ui.form.on("Strategic Plan Program",{
    setup: function(frm) {
		cur_frm.fields_dict["internal_beneficiaries"].grid.get_field("employee").get_query = function(doc, cdt, cdn)
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

frappe.ui.form.on("Strategic Plan Program",{
    setup: function(frm) {
		cur_frm.fields_dict["internal_direct_relationship_holders"].grid.get_field("employee").get_query = function(doc, cdt, cdn)
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