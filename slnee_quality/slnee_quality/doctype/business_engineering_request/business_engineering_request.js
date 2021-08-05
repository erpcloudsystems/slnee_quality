// Copyright (c) 2021, erpcloud.systems and contributors
// For license information, please see license.txt

frappe.ui.form.on("Business Engineering Request","operational_plan", function(frm){
    cur_frm.clear_table("stages_table");
    if(frm.doc.operational_plan){
        frappe.model.with_doc("Operational Plan", frm.doc.operational_plan, function() {
        var tabletransfer= frappe.model.get_doc("Operational Plan", frm.doc.operational_plan);
			$.each(tabletransfer.stages_table, function(d, row){
            d = frm.add_child("stages_table");
            d.stage_name = row.stage_name;
            d.stage_progress = row.stage_progress;
            d.expected_start_date = row.expected_start_date;
            d.expected_end_date = row.expected_end_date;
            d.roles = row.roles;
            d.procedure_requirements = row.procedure_requirements;
            d.operational_responsibilites = row.operational_responsibilites;
            d.duration = row.duration;
            cur_frm.refresh_field("stages_table");
			});
    });
    }
});

frappe.ui.form.on("Business Engineering Request", {
	refresh: function(frm, cdt, cdn) {
	   if(frm.doc.workflow_state == "Plan Approved" && frm.doc.request_type == "Action Documentation Request" && !frm.doc.action_card){
    		frm.add_custom_button(__("Issue Action Card"), function() {
    		    var child = locals[cdt][cdn];
    			frappe.route_options = {
    			    "request":frm.doc.name,
    			    "action_owner": frm.doc.applicant
    			};
    			frappe.new_doc("Action Card");
    		},
    		).addClass("btn-primary").css({'color':'white'});
	    }
	}
});

frappe.ui.form.on("Business Engineering Request", {
	refresh: function(frm, cdt, cdn) {
	   if(frm.doc.workflow_state == "Plan Approved" && frm.doc.request_type == "Action Improvement Request" && !frm.doc.improvement_card){
    		frm.add_custom_button(__("Issue Improvement Card"), function() {
    		    var child = locals[cdt][cdn];
    			frappe.route_options = {
    			    "request":frm.doc.name
    			};
    			frappe.new_doc("Improvement Card");
    		},
    		).addClass("btn-primary").css({'color':'white'});
	    }
	}
});
