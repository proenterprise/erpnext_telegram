# -*- coding: utf-8 -*-
# Copyright (c) 2019, Proenterprise Ventures and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
import telegram_send

class SentMessages(Document):
	pass

	"""
		Todo:
		- Add for each sales order item
		- Recreate form, splitting fields
		- Use variables in settings for Bakery,
		- test image types
			- all passed but private files
			- test with msgprint

		Nice
		- Show attached image
	"""

@frappe.whitelist()
def send_message(image, telegram_message="No message"):
	if image:
		image_path = get_absolute_path(image)
		with open(image_path, 'rb') as img:
			telegram_send.send(images=[img], messages=[telegram_message])
	else:
		telegram_send.send(images=None, messages=[telegram_message])

	frappe.msgprint("The order has been sent to the Bakery")

@frappe.whitelist()
def set_order_message(order):
	pass

def get_absolute_path(file_name, is_private=False):
	if(file_name.startswith('/files/')):
		file_name = file_name[7:]
		return frappe.utils.get_bench_path()+ "/sites/" + frappe.utils.get_path('private' if is_private else 'public', 'files', file_name)[2:]
