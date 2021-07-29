// Copyright (c) 2021, erpcloud.systems and contributors
// For license information, please see license.txt

frappe.ui.form.on('Procedure Repository',  'classification',  function(frm) {
    if (cur_frm.doc.classification == "Administrative (A)") {
        cur_frm.set_value('naming_series', 'A-');
    }
    if (cur_frm.doc.classification == "Essential (E)") {
        cur_frm.set_value('naming_series', 'E-');
    }
    if (cur_frm.doc.classification == "Supportive (S)") {
        cur_frm.set_value('naming_series', 'S-');
    }
});