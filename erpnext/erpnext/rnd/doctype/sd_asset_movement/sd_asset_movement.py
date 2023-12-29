# Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import logging
import frappe
from frappe import _
from frappe.model.document import Document

class SDAssetMovement(Document):
	def before_save(self) : 
		self.validate_asset()

	def validate_asset(self):
		logging.warning(self.purpose)
		# has_missing = []
		# for d in self.transfer_asset_list:
			# status = frappe.db.get_value("SD Assets", d.assets, ["status"])
			# if self.purpose == "Transfer" and status in ("Missing", "In Maintenance"):
			# 	frappe.throw(_("{0} is {1}. {2} asset cannot be transferred").format(frappe.bold((" , ").join(has_missing)),frappe.bold(status),frappe.bold(status)))

