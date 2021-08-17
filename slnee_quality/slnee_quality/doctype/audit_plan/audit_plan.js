// Copyright (c) 2021, erpcloud.systems and contributors
// For license information, please see license.txt

frappe.ui.form.on('Audit Plan',{
    setup: function(frm) {
		cur_frm.fields_dict['actions_card_table'].grid.get_field("action_card").get_query = function(doc, cdt, cdn)
		{
			return {
				filters:  [
					["Action Card","docstatus", "=", 1],
					["Action Card","audit", "=", ""],

				]

			};
		};
	}
});