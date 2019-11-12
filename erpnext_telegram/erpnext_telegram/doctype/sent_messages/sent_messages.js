// Copyright (c) 2019, Proenterprise Ventures and contributors
// For license information, please see license.txt


var allowed_exts = ["jpg", "png", "jpeg"];

function get_extension(img) {
    return img.split('.').pop().toLowerCase();
}

function show_image_not_supported() {
    msgprint("This image type is not supported.");
    var status = frappe.validated = false;
    return status;
}

frappe.ui.form.on("Sales Order", {
	validate: function(frm) {
        var img = frm.doc.image;

        if ( img && !allowed_exts.includes(get_extension(img)) ){
            show_image_not_supported();
        }
	},

	before_submit: function(frm) {
        var img = frm.doc.image;
        var msg = frm.doc.telegram_message;

        if ( !img || allowed_exts.includes(get_extension(img)) ){ //no image or image with valid extensions

            frappe.call({
                method: "erpnext_telegram.erpnext_telegram.doctype.sent_messages.sent_messages.send_message",
                args: {
                    image: img,
                    telegram_message: msg
                },
                    "callback": function(r){
                    //r.message
                }
            })
        }
        else {
            show_image_not_supported();
        }
	}
})
