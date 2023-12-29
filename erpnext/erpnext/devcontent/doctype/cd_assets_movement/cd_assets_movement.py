# Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document

class CDAssetsMovement(Document):
	def before_submit(self):
		self.validate_borrowed_employee()
		self.validate_condition_asset()
		self.validate_employee_transfer()

	def on_update_after_submit(self):
		#loop borrow asset list
		for borrow_asset in self.borrow_asset_list:
			condition = frappe.db.get_value("CD Asset", borrow_asset.asset_name, "condition") #Get condition asset
			custodian_desk = frappe.db.get_value('CD Room', {'room': 'Custodian Desk'}, ['room']) #Get custodian desk

			if condition == "Broken":
				return
			elif condition == "In Maintenance":
				return
			else:
				frappe.db.set_value('CD Asset', borrow_asset.asset_name, 'custodian', borrow_asset.to_employee)
				frappe.db.set_value('CD Asset', borrow_asset.asset_name, 'status', 'Borrowed')			
				frappe.db.set_value('CD Asset', borrow_asset.asset_name, 'custodian_location', custodian_desk)

	def validate_condition_asset(self):
		for borrow_asset in self.borrow_asset_list:
			condition = frappe.db.get_value("CD Asset", borrow_asset.asset_name, "condition")
			if condition == "Broken":
				frappe.throw(_("The asset : {0} cannot be borrowed, because current asset condition is {1}").format(frappe.bold(borrow_asset.asset_name), frappe.bold(condition)))
			elif condition == "In Maintenance":
				frappe.throw(_("The asset : {0} cannot be borrowed, because current asset condition is {1}").format(frappe.bold(borrow_asset.asset_name), frappe.bold(condition)))
		
		for borrow_asset in self.borrow_asset_list:
			condition = frappe.db.get_value("CD Asset", borrow_asset.asset_name, "condition")
			if condition == "Broken":
				frappe.throw(_("The asset : {0} cannot be borrowed, because current asset condition is {1}").format(frappe.bold(borrow_asset.asset_name), frappe.bold(condition)))
			elif condition == "In Maintenance":
				frappe.throw(_("The asset : {0} cannot be borrowed, because current asset condition is {1}").format(frappe.bold(borrow_asset.asset_name), frappe.bold(condition)))

	def validate_borrowed_employee(self):
		for d in self.borrow_asset_list:
			if d.to_employee:
				current_custodian = frappe.db.get_value("CD Asset", d.asset_name, "custodian")
				current_employee = frappe.db.get_value("Employee", current_custodian, "employee_name")

				if current_custodian != None and current_custodian != d.to_employee:
					frappe.throw(_("The asset : {0} has been borrowed by the custodian : {1}").format(frappe.bold(d.asset_name),frappe.bold(current_employee)))
				else:
					custodianDesk = frappe.db.get_value('CD Room', {'room': 'Custodian Desk'}, ['room'])
					frappe.db.set_value('CD Asset', d.asset_name, {
						'custodian': d.to_employee,
						'status': 'Borrowed',
						'custodian_location': custodianDesk
					})

	def validate_employee_transfer(self):
		for d in self.transfer_asset_list:
			if d.from_employee_transfer:
				current_custodian = frappe.db.get_value("CD Asset", d.asset_transfer, "custodian")
				current_employee = frappe.db.get_value("Employee", d.from_employee_transfer, "employee_name")
				belongs_to_employee = frappe.db.get_value("Employee", current_custodian, "employee_name")

				if current_custodian != None and current_custodian != d.from_employee_transfer:
					frappe.throw(_("The asset : {0} does not belong to the custodian : {1}, it belongs to {2}").format(frappe.bold(d.asset_transfer),frappe.bold(current_employee),frappe.bold(belongs_to_employee)))
				else:
					frappe.db.set_value('CD Asset', d.asset_transfer,{
						'custodian': d.to_employee_transfer,
						'status': 'Borrowed'
					})
		
	@frappe.whitelist()
	def get_linked_doc(self):
		for borrow_asset in self.borrow_asset_list:
			name_asset 		= frappe.db.get_value("CD Asset", borrow_asset.asset_name, "name")
			condition 		= frappe.db.get_value("CD Asset", borrow_asset.asset_name, "condition")
			status 			= frappe.db.get_value("CD Asset", borrow_asset.asset_name, "status")
			asset_name 		= frappe.db.get_value("CD Asset", borrow_asset.asset_name, "asset_name")
			location_asset 	= frappe.db.get_value("CD Asset", borrow_asset.asset_name, "room")
			redirect 		= '<a href="http://192.168.101.36:10001/app/cd-asset-store">CD Asset Store</a>'

			if condition == 'Broken' and status == 'Borrowed':
				frappe.msgprint(
					msg=_('The Asset Name : {0}, Currently Its Update From CD Asset Parent, Cause Condition From Asset : {1}, Is : {2}. Please Return Asset To Store Location {3} From Asset Store {4}').format(frappe.bold(name_asset), frappe.bold(asset_name), frappe.bold(condition), frappe.bold(location_asset), frappe.bold(redirect)),
					title='Announcement',
					indicator='blue',
				)
				frappe.db.set_value('CD Asset', name_asset, {
					'custodian': None,
					'custodian_location': None,
					'status': 'Stored'
				})
				frappe.db.delete('CD Asset Borrow', {'asset_name': name_asset})