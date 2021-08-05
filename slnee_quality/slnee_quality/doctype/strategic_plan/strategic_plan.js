frappe.ui.form.on("Strategic Plan", {
    refresh: (frm, cdt, cdn) => {
        if(frm.doc.workflow_state == "Approved" && frm.doc.end_date <= get_today()){
            frm.add_custom_button("End Plan", () => {
                if (frm.doc.end_date > get_today()) {
                    frappe.throw("You Cannot Close The Plan Before The End Date");
                }
                else {
                cur_frm.set_value("workflow_state", "Completed");
                cur_frm.save('Update');
                }
     
            }).addClass("btn-primary").css({'color':'white'});
        }    
    }
});