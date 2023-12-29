// Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('CD Assets Movement', {
	refresh: function(frm){
		frm.call('get_linked_doc').then(r => {
			if (r.message){
				let linked_doc = r.message
			}
		})
	},
});