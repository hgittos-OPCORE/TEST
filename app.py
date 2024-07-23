# -*- coding: utf-8 -*-
import re
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model
    def _get_default_customer_payment_term(self):
        return self.env['account.payment.term'].search([
            ('line_ids.nb_days', '=', 30),
            ('line_ids.delay_type', '=', 'days_after'),
            ('line_ids.value', '=', 'percent'),
            ('line_ids.value_amount', '=', 100)
        ], limit=1)

    @api.model
    def _get_default_supplier_payment_term(self):
        return self.env['account.payment.term'].search([
            ('line_ids.nb_days', '=', 30),
            ('line_ids.delay_type', '=', 'days_after_end_of_month'),
            ('line_ids.value', '=', 'percent'),
            ('line_ids.value_amount', '=', 100)
        ], limit=1)

    property_payment_term_id = fields.Many2one(
        'account.payment.term',
        default=_get_default_customer_payment_term
    )

    property_supplier_payment_term_id = fields.Many2one(
        'account.payment.term',
        default=_get_default_supplier_payment_term
    )

