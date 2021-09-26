frappe.ui.form.on("Organizational creation and restructuring", "after_save", function(frm)
{
 cur_frm.set_value("request_number",cur_frm.doc.name);	
    

});