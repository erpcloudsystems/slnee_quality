frappe.ui.form.on("Improvement Card", "on_submit", function(frm) {
    frappe.db.set_value("Business Engineering Request",  cur_frm.doc.request, "improvement_card", cur_frm.doc.name);
});