frappe.ui.form.on("Request to raise work quality", "after_save", function(frm)
{
 cur_frm.set_value("request_number",cur_frm.doc.name);	
    

});