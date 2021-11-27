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
            "label": _("Strategic Indicators Card"),
            "fieldname": "strategic_indicators_card",
            "fieldtype": "Link",
            "options": "Strategic Indicators Card",
            "width": 200
        },
        {
            "label": _("Goal Name"),
            "fieldname": "goal_name",
            "fieldtype": "Data",
            "width": 250
        },
        {
            "label": _("Strategic Plan"),
            "fieldname": "strategic_plan",
            "fieldtype": "Link",
            "options": "Strategic Plan",
            "width": 120
        },
        {
            "label": _("Strategic Plan Name"),
            "fieldname": "strategic_plan_name",
            "fieldtype": "Data",
            "width": 250
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
            "fieldtype": "Link",
            "options": "Program",
            "width": 120
        },
        {
            "label": _("Plan Progress"),
            "fieldname": "progress",
            "fieldtype": "Percent",
            "width": 140
        },
        {
            "label": _("Count Of Stages"),
            "fieldname": "count_of_phase_stages",
            "fieldtype": "Data",
            "width": 150
        },
        {
            "label": _("Count Of Missions"),
            "fieldname": "count_of_missions",
            "fieldtype": "Data",
            "width": 150
        },
        {
            "label": _("Count Of Completed Missions"),
            "fieldname": "count_of_completed_missions",
            "fieldtype": "Data",
            "width": 200
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
        conditions += " and `tabStrategic Plan`.strategic_plan =%(strategic_plan)s"
    item_results = frappe.db.sql("""
                select distinct
                        `tabOperational Plan`.name as name,
						(select count(stage_name) from `tabStages Table`  where `tabStages Table`.parent = `tabOperational Plan`.name {conditions} ) as count_of_phase_stages,
						(select (goal_name) from `tabStrategic Goals`  where `tabStrategic Goals`.parent = `tabStrategic Indicators Card`.name {conditions} ) as goal_name,
						(select count(`tabOperational Plan`.name) from `tabOperational Plan` join `tabStrategic Indicators Card` join `tabStrategic Plan` where `tabOperational Plan`.strategic_plan = `tabStrategic Indicators Card`.strategic_plan and `tabOperational Plan`.strategic_plan = `tabStrategic Indicators Card`.strategic_plan ) as no_of_operational_plan,
						(select `tabStrategic Indicators Card`.name from `tabStrategic Indicators Card`  where `tabOperational Plan`.strategic_plan = `tabStrategic Indicators Card`.strategic_plan) as strategic_indicators_card,
						(select count(stage) from `tabMissions Table`  where `tabMissions Table`.parent = `tabOperational Plan`.name {conditions} ) as count_of_missions,
						(select count(stage) from `tabMissions Table`  where `tabMissions Table`.parent = `tabOperational Plan`.name and `tabMissions Table`.status = "Completed"  {conditions} ) as count_of_completed_missions,												
                        `tabOperational Plan`.plan_name as plan_name,                    
                        `tabOperational Plan`.program as program,
                        `tabOperational Plan`.strategic_plan as strategic_plan,                        
                        `tabOperational Plan`.strategic_plan_name as strategic_plan_name,                        
                        `tabOperational Plan`.progress as progress

                from
                `tabOperational Plan` join `tabStages Table` join `tabStrategic Indicators Card`
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
                'strategic_plan': item_dict.strategic_plan,
                'stage_name': item_dict.stage_name,
                'count_of_phase_stages': item_dict.count_of_phase_stages,
                'stage_progress': item_dict.stage_progress,
                'progress': item_dict.progress,
                'message': item_dict.message,
                'count_of_missions': item_dict.count_of_missions,
                'strategic_indicators_card': item_dict.strategic_indicators_card,
                'no_of_operational_plan': item_dict.no_of_operational_plan,
                'strategic_plan_name': item_dict.strategic_plan_name,
                'count_of_completed_missions': item_dict.count_of_completed_missions,
                'goal_name': item_dict.goal_name
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
