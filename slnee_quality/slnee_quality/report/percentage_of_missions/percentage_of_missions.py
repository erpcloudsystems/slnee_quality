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
            "fieldname": "strategic_plan",
            "fieldtype": "Link",
            "options": "Strategic Plan",
            "width": 120
        },
        {
            "label": _("Operational Plan"),
            "fieldname": "name",
            "fieldtype": "Link",
            "options": "Operational Plan",
            "width": 130
        },
        {
            "label": _("Plan Name"),
            "fieldname": "plan_name",
            "fieldtype": "Data",
            "width": 200
        },
        {
            "label": _("Program"),
            "fieldname": _("program"),
            "fieldtype": "Data",
            "width": 120
        },
        {
            "label": _("Posting Date"),
            "fieldname": "posting_date",
            "fieldtype": "Date",
            "width": 120
        },
        {
            "label": _("Plan Progress"),
            "fieldname": "progress",
            "fieldtype": "Percent",
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
            "label": _("Stage Name"),
            "fieldname": "stage_name",
            "fieldtype": "Data",
            "width": 120
        },
        {
            "label": _("Stage Progress"),
            "fieldname": "stage_progress",
            "fieldtype": "Percent",
            "width": 120
        }
    ]


def get_data(filters, columns):
    item_price_qty_data = []
    item_price_qty_data = get_item_price_qty_data(filters)
    return item_price_qty_data


def get_item_price_qty_data(filters):
    conditions = ""
    if filters.get("name"):
        conditions += " and `tabOperational Plan`.name =%(name)s"
    if filters.get("strategic_plan"):
        conditions += " and `tabOperational Plan`.strategic_plan =%(strategic_plan)s"
    if filters.get("from_date"):
        conditions += " and `tabOperational Plan`.posting_date>=%(from_date)s"
    if filters.get("to_date"):
        conditions += " and `tabOperational Plan`.posting_date<=%(to_date)s"
    item_results = frappe.db.sql("""
                select
                        `tabOperational Plan`.name as name,
                        `tabOperational Plan`.plan_name as plan_name,                    
                        `tabOperational Plan`.program as program,
                        `tabOperational Plan`.strategic_plan as strategic_plan,
                        `tabOperational Plan`.posting_date as posting_date,
                        `tabOperational Plan`.start_date as start_date,
                        `tabOperational Plan`.end_date as end_date,
                        `tabOperational Plan`.progress as progress,
                        `tabStages Table`.stage_name as stage_name,
                        `tabStages Table`.stage_progress as stage_progress
                                                                           
                from
                `tabOperational Plan` join `tabStages Table`
                where
                `tabOperational Plan`.docstatus != 2
                and `tabStages Table`.parent = `tabOperational Plan`.name
                {conditions}
                order by `tabOperational Plan`.name desc


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
                'program': item_dict.program,
                'posting_date': item_dict.posting_date,
                'strategic_plan': _(item_dict.strategic_plan),
                'start_date': item_dict.start_date,
                'end_date': item_dict.end_date,
                'stage_name': item_dict.stage_name,
                'no_of_missions': item_dict.no_of_missions,
                'stage_progress': item_dict.stage_progress,
                'progress': item_dict.progress,
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
