# -*- coding: utf-8 -*-
from odoo import http, fields, _
from odoo.http import request
from odoo.exceptions import AccessError, MissingError
from odoo.addons.portal.controllers.mail import _message_post_helper
from odoo.osv import expression
from odoo.addons.portal.controllers.portal import CustomerPortal, get_records_pager


class CustomSales(CustomerPortal):

    @http.route(['/my/orders/<int:order_id>/edit'], type='http', auth="public", website=True)
    def custom_portal_order_page(self, order_id, report_type=None, access_token=None, message=False, download=False, **kw):
        try:
            order_sudo = self._document_check_access('sale.order', order_id, access_token=access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')

        if report_type in ('html', 'pdf', 'text'):
            return self._show_report(model=order_sudo, report_type=report_type, report_ref='sale.action_report_saleorder', download=download)

        # use sudo to allow accessing/viewing orders for public user
        # only if he knows the private token
        now = fields.Date.today()

        # Log only once a day
        if order_sudo and request.session.get('view_quote_%s' % order_sudo.id) != now and request.env.user.share and access_token:
            request.session['view_quote_%s' % order_sudo.id] = now
            body = _('Quotation viewed by customer')
            _message_post_helper(res_model='sale.order', res_id=order_sudo.id, message=body, token=order_sudo.access_token, message_type='notification', subtype="mail.mt_note", partner_ids=order_sudo.user_id.sudo().partner_id.ids)

        values = {
            'sale_order': order_sudo,
            'message': message,
            'token': access_token,
            'return_url': '/shop/payment/validate',
            'bootstrap_formatting': True,
            'partner_id': order_sudo.partner_id.id,
            'report_type': 'html',
        }

        if order_sudo.has_to_be_paid():
            domain = expression.AND([
                ['&', ('website_published', '=', True), ('company_id', '=', order_sudo.company_id.id)],
                ['|', ('specific_countries', '=', False), ('country_ids', 'in', [order_sudo.partner_id.country_id.id])]
            ])
            acquirers = request.env['payment.acquirer'].sudo().search(domain)

            values['acquirers'] = acquirers.filtered(lambda acq: (acq.payment_flow == 'form' and acq.view_template_id) or
                                                     (acq.payment_flow == 's2s' and acq.registration_view_template_id))
            values['pms'] = request.env['payment.token'].search(
                [('partner_id', '=', order_sudo.partner_id.id),
                ('acquirer_id', 'in', acquirers.filtered(lambda acq: acq.payment_flow == 's2s').ids)])

        if order_sudo.state in ('draft', 'sent', 'cancel'):
            history = request.session.get('my_quotations_history', [])
        else:
            history = request.session.get('my_orders_history', [])
        values.update(get_records_pager(history, order_sudo))

        request.session['order-id'] = order_id
        request.session['rm-orderline'] = list()
        request.session['ed-orderline'] = list()

        return request.render('custom_sales.custom_sale_order_portal_template', values)

    @http.route(['/getProducts'], auth='user', type='http')
    def get_products(self, **params):
        values = {'products': request.env['product.product'].search([('product_tmpl_id.name', 'ilike', params.get('query'))])}
        return request.render('custom_sales.my_sale_order_portal_products', values)

    @http.route(['/addOLtoRM'], methods=['POST'], auth='user', type='json')
    def add_ol_to_rm(self, **params):
        tmp = [value for value in request.session.get('rm-orderline')]
        tmp.append(params.get('olId'))
        request.session['rm-orderline'] = tmp
        return {'success': True}

    @http.route(['/addOLtoED'], methods=['POST'], auth='user')
    def add_ol_to_ed(self, **params):
        tmp = {'old-product': params.get('oldId'), 'new-product': {'quantity': params.get('quantity'), 'id': params.get('newId')}}
        request.session['ed-orderline'].append(tmp)

    @http.route(['/acepted-edit'], methods=['POST'], auth='user')
    def accept_edit(self, **params):
        """
        Rido, esta funcion es la que se va a ejecutar cuando aceptes guardar los cambios, fijate que no paso
        ningun parametro pq lo cambiado debera estar en session, en las listas rm-orderline y ed-orderline,
        esta funcion deberia devolver un valor Booleano, para saber si se ejecuto todo bien.
        :param params:
        :return:
        """
        return {'success': True}
