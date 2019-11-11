# -*- coding: utf-8 -*-
# Copyright (c) 2019, Proenterprise Ventures and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
# import frappe
from frappe.model.document import Document
import telegram_send

class SentMessages(Document):

	message = "hello from python"

@frappe.whitelist()
def send_message(message):
	if message:
		telegram-send message
	else:
		msg.print("Nothing to be sent")

def get_order_message():
	pass

send_message(message)
