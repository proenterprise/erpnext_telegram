# -*- coding: utf-8 -*-
# Copyright (c) 2019, Proenterprise Ventures and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
from datetime import datetime
import frappe
from frappe import _
from frappe.model.document import Document
import telegram_send

"""
    Todo:
    - Add for each sales order item - skipped version - X
    - Use variables in settings for Bakery 
        - Group
        - Bot
        - AUTH KEY
        - 

    Nice
    - Show attached image
"""

@frappe.whitelist()
def send_message(sales_order_name):
    sales_order = frappe.get_doc("Sales Order", sales_order_name)
    image = sales_order.cake_image
    print_image = sales_order.cake_print_image
    telegram_message = format_message(sales_order)

    if image:
        if print_image:
            image_path = get_absolute_path(image)
            print_image_path = get_absolute_path(print_image)
            with open(image_path, 'rb') as img, open(print_image_path, 'rb') as p_img:
                telegram_send.send( images=[img, p_img], 
                                    captions=["Sample cake image", "Print on Cake"],
                                    messages=[telegram_message], 
                                    parse_mode="markdown" )
        else:
            image_path = get_absolute_path(image)
            with open(image_path, 'rb') as img:
                telegram_send.send( images=[img], 
                                    captions=["Sample cake image"],
                                    messages=[telegram_message], 
                                    parse_mode="markdown" )
    else:
        telegram_send.send(images=None, messages=[telegram_message], parse_mode="markdown")

    frappe.msgprint("The order has been sent to the Bakery")

# Format Message
def format_message(sales_order):
    customer_name = sales_order.customer_name
    words = sales_order.words
    customer_address = get_customer_contact(customer_name)
    toppers = ""
    decors = ""
    if (sales_order.toppers): 
        toppers = format_items(sales_order.toppers) or ""
    if (sales_order.decors): 
        toppers = format_items(sales_order.decors) or ""

    order_no = str(sales_order.name)
    print(order_no)

    full_msg =  " *CAKE ORDER*: " + order_no

    if (customer_address):
        full_msg = (full_msg + " \n\n *Customer*: " + customer_name + customer_address +
                    "\n *Delivery Date:* " + str(sales_order.delivery_date.strftime("%d/%m/%Y")) +
                    " - " + str(sales_order.delivery_time)[:5] +
                    "\n *Delivery Type:* " + (str(sales_order.delivery_type) or "") )

    if (sales_order.grand_total):
        full_msg = (full_msg +
                    "\n \n *Order* \n  Cake: " + sales_order.cake_description +
                    "\n  Qty: " + str(sales_order.total_qty) +
                    "\n  Price: " + str(sales_order.grand_total) +
                    "\n\n *Tiers*" + format_tiers(sales_order.cake_tiers) +
                    "\n\n Toppers: " + toppers +
                    "\n Decor: " + decors )

    if (words):
        full_msg = full_msg + "\n\n *Writting on cake*: \n" + words

    

    return full_msg

def format_items(items):
    items = items.split(",")
    value = ""
    count = 0

    for item in items:
        if (count < 1) :
            value = value + (str(item) or "")
        else:
            value = value + ( (", " + str(item)) or "" )
        
        count = 1

    return value

def format_tiers(cake_tiers):
    num = 1
    tiers = ""

    for cake_tier in cake_tiers:
        check = lambda x : "" if (x == None or x == "No Filling") else ", " + x
        check_filling = lambda f : "" if f == None else (". No Filling" if (f == "No Filling" and cake_tier.layer_2 !="") else ". Filling: " + f )
        check_note = lambda x : "" if (x == None or x == "") else ". Note: " + x

        tiers = ( tiers + "\n  " + str(num) + ". Layers: " +
                    str(cake_tier.layer_1) +
                    str(check(cake_tier.layer_2)) +
                    str(check(cake_tier.layer_3)) +
                    str(check(cake_tier.layer_4)) +
                    str(check_filling(cake_tier.filling)) +
                    str(check_note(cake_tier.layer_notes)) )
        num += 1

    return tiers

def get_customer_contact(customer_name):
    customer = frappe.get_doc("Customer", customer_name)
    print(customer)
    address = frappe.get_doc("Address", customer_name + "-Billing")

    customer_address = ""

    if (customer.customer_type):
        customer_address = customer_address + " (" + customer.customer_type + ")" 
    
    if(address.address_line1):
        customer_address = customer_address + "\n *Address*: " + address.address_line1 +", "+ (address.city or "")

    if (customer.mobile_no):
        customer_address = customer_address + "\n *Mobile*: " + customer.mobile_no

    return customer_address
    #sales_order = frappe.get_doc("Contact", sales_order_name)

def get_absolute_path(file_name, is_private=False):
	if(file_name.startswith('/files/')):
		file_name = file_name[7:]
		return frappe.utils.get_bench_path()+ "/sites/" + frappe.utils.get_path('private' if is_private else 'public', 'files', file_name)[2:]
