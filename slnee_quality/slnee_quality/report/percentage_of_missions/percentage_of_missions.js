// Copyright (c) 2016, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["percentage of missions"] = {
	"filters": [
		{
			"fieldname": "from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default": frappe.defaults.get_user_default("year_start_date"),
			"reqd": 1
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": frappe.defaults.get_user_default("year_end_date"),
			"reqd": 1
		},
		{
			"fieldname": "name",
			"label": __("Operational Plan"),
			"fieldtype": "Link",
			"options": "Operational Plan",
			"reqd": 1
		},
		{
			"fieldname": "name",
			"label": __("Strategic Plan"),
			"fieldtype": "Link",
			"options": "Strategic Plan",
			"reqd": 1
		},
	]
}


