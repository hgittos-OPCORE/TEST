# -*- coding: utf-8 -*-
import re
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class ResPartner(models.Model):
    _inherit = 'res.partner'

    siret = fields.Char(string="SIRET")
    kbis = fields.Binary(string="KBIs")
    nda = fields.Binary(string="NDA")
    info_message = fields.Html(string='Information', compute='_compute_info_message', readonly=True)
    

    @api.depends('is_company', 'country_id', 'vat', 'siret', 'kbis', 'street', 'zip', 'country_id', 'phone', 'email', 'company_registry', 'bank_ids', 'nda')
    def _compute_info_message(self):
        france = self.env['res.country'].search([('name', '=', 'France')], limit=1)
        eu_group = self.env['res.country.group'].search([('name', '=', 'European Union')], limit=1)
        for contact in self:
            if contact.is_company:
                base_message = """
                <div style="background-color: #e6f3ff; padding: 15px; border-radius: 5px;">
                <p>The following fields are mandatory to switch to "Submitted" status:</p>
                <ul>
                """
                fields_to_check = []
                if eu_group and contact.country_id in eu_group.country_ids:
                    fields_to_check.append(('VAT (Tax ID)', contact.vat))
                if france and contact.country_id == france:
                    fields_to_check.extend([
                        ('Siret', contact.siret),
                        ('KBIs', contact.kbis)
                    ])
                fields_to_check.extend([
                    ('Address', contact.street),
                    ('Zip', contact.zip),
                    ('Country', contact.country_id),
                    ('Phone', contact.phone),
                    ('Email', contact.email),
                    ('Company ID', contact.company_registry),
                    ('RIB', contact.bank_ids),
                    ('NDA', contact.nda)
                ])
                for field_name, field_value in fields_to_check:
                    if not field_value:
                        base_message += f"<li>{field_name}</li>"
                base_message += """
                </ul>
                </div>
                """
                contact.info_message = base_message
            else:
                contact.info_message = False