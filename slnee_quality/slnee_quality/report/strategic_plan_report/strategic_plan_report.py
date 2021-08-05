# Copyright (c) 2013, erpcloud.systems and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _


def execute(filters=None):
    columns, data = [], []
    columns = get_columns()
    data = get_data(filters, columns)
    return columns, data


def get_columns():
    return [
        {
            "label": _("Strategic Plan"),
            "fieldname": "name",
            "fieldtype": "Link",
            "options": "Strategic Plan",
            "width": 120
        },
        {
            "label": _("Plan Name"),
            "fieldname": "plan_name",
            "fieldtype": "Data",
            "width": 300
        },
        {
            "label": _("Plan Description"),
            "fieldname": _("plan_description"),
            "fieldtype": "Data",
            "width": 300
        },
        {
            "label": _("Posting Date"),
            "fieldname": "posting_date",
            "fieldtype": "Date",
            "width": 120
        },
        {
            "label": _("Workflow State"),
            "fieldname": "workflow_state",
            "fieldtype": "Data",
            "width": 140
        },
        {
            "label": _("Start Date"),
            "fieldname": "start_date",
            "fieldtype": "Date",
            "width": 120
        },
		{
			"label": _("End Date"),
			"fieldname": "end_date",
			"fieldtype": "Date",
			"width": 120
		},
        {
            "label": _("Vision"),
            "fieldname": "vision",
            "fieldtype": "Data",
            "width": 300
        },
        {
            "label": _("Message"),
            "fieldname": "message",
            "fieldtype": "Data",
            "width": 300
        },
        {
            "label": _("Values"),
            "fieldname": "values",
            "fieldtype": "Data",
            "width": 300
        },
        {
            "label": _("Main Goals"),
            "fieldname": "main_goals",
            "fieldtype": "Data",
            "width": 300
        }
    ]


def get_data(filters, columns):
    item_price_qty_data = []
    item_price_qty_data = get_item_price_qty_data(filters)
    return item_price_qty_data


def get_item_price_qty_data(filters):
    conditions = ""
    if filters.get("from_date"):
        conditions += " and `tabStrategic Plan`.posting_date>=%(from_date)s"
    if filters.get("to_date"):
        conditions += " and `tabStrategic Plan`.posting_date<=%(to_date)s"
    item_results = frappe.db.sql("""
                select
                        `tabStrategic Plan`.name as name,
                        `tabStrategic Plan`.plan_name as plan_name,
                        `tabStrategic Plan`.plan_description as plan_description,
                        `tabStrategic Plan`.posting_date as posting_date,
                        `tabStrategic Plan`.workflow_state as workflow_state,
                        `tabStrategic Plan`.start_date as start_date,
                        `tabStrategic Plan`.end_date as end_date,
                        `tabStrategic Plan`.vision as vision,
                        `tabStrategic Plan`.message as message,
                        `tabStrategic Plan`.values as x,
                        (SELECT GROUP_CONCAT('<li>',`tabStrategic Goals`.goal_name order by idx separator '</li>')
                        FROM `tabStrategic Goals`
                        WHERE `tabStrategic Goals`.parent = `tabStrategic Plan`.name) as main_goals
                from
                `tabStrategic Plan`
                where
                `tabStrategic Plan`.docstatus != 2
                {conditions}
                order by `tabStrategic Plan`.name desc


                """.format(conditions=conditions), filters, as_dict=1)

    # price_list_names = list(set([item.price_list_name for item in item_results]))

    # buying_price_map = get_price_map(price_list_names, buying=1)
    # selling_price_map = get_price_map(price_list_names, selling=1)

    result = []
    if item_results:
        for item_dict in item_results:
            data = {
                'name': item_dict.name,
                'plan_name': item_dict.plan_name,
                'plan_description': item_dict.plan_description,
                'posting_date': item_dict.posting_date,
                'workflow_state': _(item_dict.workflow_state),
                'start_date': item_dict.start_date,
                'end_date': item_dict.end_date,
                'vision': item_dict.vision,
                'message': item_dict.message,
                'values': item_dict.x,
                'main_goals': item_dict.main_goals,
            }
            result.append(data)

    return result


def get_price_map(price_list_names, buying=0, selling=0):
    price_map = {}

    if not price_list_names:
        return price_map

    rate_key = "Buying Rate" if buying else "Selling Rate"
    price_list_key = "Buying Price List" if buying else "Selling Price List"

    filters = {"name": ("in", price_list_names)}
    if buying:
        filters["buying"] = 1
    else:
        filters["selling"] = 1

    pricing_details = frappe.get_all("Item Price",
                                     fields=["name", "price_list", "price_list_rate"], filters=filters)

    for d in pricing_details:
        name = d["name"]
        price_map[name] = {
            price_list_key: d["price_list"],
            rate_key: d["price_list_rate"]
        }

    return price_map
