# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class AddressAuxMassEdit(models.TransientModel):
    _inherit = 'clv.address_aux.mass_edit'

    verification_marker_ids = fields.Many2many(
        comodel_name='clv.verification.marker',
        relation='clv_address_aux_mass_edit_verification_marker_rel',
        column1='address_aux_id',
        column2='verification_marker_id',
        string='Verification Markers'
    )
    verification_marker_ids_selection = fields.Selection(
        [('add', 'Add'),
         ('remove_m2m', 'Remove'),
         ('set', 'Set'),
         ], string='Verification Markers:', default=False, readonly=False, required=False
    )

    address_aux_verification_exec = fields.Boolean(
        string='Address (Aux) Verification Execute'
    )

    # @api.multi
    def do_address_aux_mass_edit(self):
        self.ensure_one()

        super().do_address_aux_mass_edit()

        for address_aux in self.address_aux_ids:

            _logger.info(u'%s %s', '>>>>>', address_aux.name)

            if self.verification_marker_ids_selection == 'add':
                m2m_list = []
                for verification_marker_id in self.verification_marker_ids:
                    m2m_list.append((4, verification_marker_id.id))
                _logger.info(u'%s %s', '>>>>>>>>>>', m2m_list)
                address_aux.verification_marker_ids = m2m_list
            if self.verification_marker_ids_selection == 'remove_m2m':
                m2m_list = []
                for verification_marker_id in self.verification_marker_ids:
                    m2m_list.append((3, verification_marker_id.id))
                _logger.info(u'%s %s', '>>>>>>>>>>', m2m_list)
                address_aux.verification_marker_ids = m2m_list
            if self.verification_marker_ids_selection == 'set':
                m2m_list = []
                for verification_marker_id in address_aux.verification_marker_ids:
                    m2m_list.append((3, verification_marker_id.id))
                _logger.info(u'%s %s', '>>>>>>>>>>', m2m_list)
                address_aux.verification_marker_ids = m2m_list
                m2m_list = []
                for verification_marker_id in self.verification_marker_ids:
                    m2m_list.append((4, verification_marker_id.id))
                _logger.info(u'%s %s', '>>>>>>>>>>', m2m_list)
                address_aux.verification_marker_ids = m2m_list

            if self.address_aux_verification_exec:
                address_aux.address_aux_verification_exec()

        return True
