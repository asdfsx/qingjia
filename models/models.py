# -*- coding: utf-8 -*-

from odoo import models, fields, api

# class qingjia(models.Model):
#     _name = 'qingjia.qingjia'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100

class Qingjd(models.Model):
    _name = 'qingjia.qingjd'
    name = fields.Many2one('res.users', string="申请人", required=True)
    manager = fields.Many2one('res.users', string="主管", required=True)
    beginning = fields.Date(string="开始日期", required=True, default=fields.Datetime.now())
    ending = fields.Date(string="结束日期", required=True)
    reason = fields.Text(string="请假事由", required=True)
    accept_reason = fields.Text(string="同意理由", default="同意")

    current_name = fields.Many2one('hr.employee', string="当前登录人", compute="_get_current_name")
    is_manager = fields.Boolean(compute="_get_is_manager")

    state = fields.Selection([('draft','草稿'),
                              ('confirmed','待审批'),
                              ('accepted','批准'),
                              ('rejected','拒绝'),],
                              string='状态', default='draft', readonly=True)

    @api.model
    def _get_default_name(self):
        uid = self.env.uid
        res = self.env['resource.resource'].search([('user_id', '=', uid)]) 
        name = res.name
        employee = self.env['hr.employee'].search([('name_related','=',name)])
        return employee

    @api.model
    def _get_default_manager(self):
        uid = self.env.uid
        res = self.env['resource.resource'].search([('user_id', '=', uid)])
        name = res.name
        employee = self.env['hr.employee'].search([('name_related','=',name)])
        return employee.parent_id
    

    defaults = {'name':_get_default_name,'manager':_get_default_manager,}

    def _get_is_manager(self):
        if self.current_name == self.manager:
            self.is_manager = True
        else:
            self.is_manager = False

    def _get_current_name(self):
        uid = self.env.uid
        res = self.env['resource.resource'].search([('user_id', '=', uid)])
        self.current_name = res
        #name = res.name
        #employee = self.env['hr.employee'].search([('name_related','=',name)])
        #self.current_name = employee

    def draft(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        self.write(cr, uid, ids, {'state':'draft'}, context=context)
        return True

    def confirm(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        self.write(cr, uid, ids, {'state':'confirm'}, context=context)
        return True

    def accept(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        self.write(cr, uid, ids, {'state':'accept'}, context=context)
        return True

    def reject(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        self.write(cr, uid, ids, {'state':'reject'}, context=context)
        return True
