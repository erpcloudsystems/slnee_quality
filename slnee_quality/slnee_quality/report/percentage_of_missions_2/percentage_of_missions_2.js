// Copyright (c) 2016, erpcloud.systems and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Percentage Of Missions 2"] = {
	"filters": [
        {
            "fieldname": "name",
            "label": __("Operational Plan"),
            "fieldtype": "Link",
            "options" : "Operational Plan",
        },
        {
            "fieldname": "strategic_plan",
            "label": __("Strategic Plan"),
            "fieldtype": "Link",
            "options" : "Strategic Plan"
        }
	]
}
