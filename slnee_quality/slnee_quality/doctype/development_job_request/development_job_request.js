frappe.ui.form.on("Development Job Request", "after_save", function(frm)
{
 cur_frm.set_value("request_number",cur_frm.doc.name);	
    

});