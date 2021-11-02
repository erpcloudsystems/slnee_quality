// Copyright (c) 2016, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["percentage of missions"] = {
	"filters": [
		{
			"fieldname": "name",
			"label": __("Operational Plan"),
			"fieldtype": "Link",
			"options": "Operational Plan",
			"reqd": 0
		},
		{
			"fieldname": "name",
			"label": __("Strategic Plan"),
			"fieldtype": "Link",
			"options": "Strategic Plan",
			"reqd": 0
		}

	]
}


