// Copyright (c) 2019, Proenterprise Ventures and contributors
// For license information, please see license.txt

frappe.ui.form.on('Sent Messages', {
	 refresh: function(frm) {
     frappe.call({
       "method": "erpnext_telegram.erpnext_telegram.doctype.sent_messages.sent_messages.send_message",
       "callback": function(r){
         //r.message
       }
     })
   }
});
