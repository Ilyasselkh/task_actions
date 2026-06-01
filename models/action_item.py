from odoo import api, fields, models, _


class ActionItem(models.Model):
    _name = "task.action.item"
    _description = "Action à suivre"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "state asc, deadline asc, priority desc, id desc"

    name = fields.Char(string="Action", required=True, tracking=True)
    user_id = fields.Many2one(
        "res.users",
        string="Responsable",
        default=lambda self: self.env.user,
        required=True,
        tracking=True,
    )
    deadline = fields.Date(string="Échéance", required=True, tracking=True)

    state = fields.Selection(
        [
            ("todo", "À réaliser"),
            ("done", "Réalisée"),
        ],
        string="Statut",
        default="todo",
        required=True,
        tracking=True,
    )

    priority = fields.Selection(
        [("0", "Basse"), ("1", "Normale"), ("2", "Haute")],
        string="Priorité",
        default="1",
        tracking=True,
    )

    description = fields.Text(string="Détails")
    is_overdue = fields.Boolean(string="En retard", compute="_compute_deadline_indicators", store=True)
    remaining_days = fields.Integer(string="Jours restants", compute="_compute_deadline_indicators", store=True)
    deadline_status = fields.Selection(
        [
            ("overdue", "En retard"),
            ("today", "Aujourd'hui"),
            ("upcoming", "À venir"),
            ("done", "Terminée"),
        ],
        string="Situation",
        compute="_compute_deadline_indicators",
        store=True,
    )
    active = fields.Boolean(default=True)

    @api.depends("deadline", "state")
    def _compute_deadline_indicators(self):
        today = fields.Date.today()
        for rec in self:
            if not rec.deadline:
                rec.remaining_days = 0
                rec.is_overdue = False
                rec.deadline_status = "upcoming"
                continue

            delta = (rec.deadline - today).days
            rec.remaining_days = delta
            rec.is_overdue = rec.state == "todo" and delta < 0

            if rec.state == "done":
                rec.deadline_status = "done"
            elif delta < 0:
                rec.deadline_status = "overdue"
            elif delta == 0:
                rec.deadline_status = "today"
            else:
                rec.deadline_status = "upcoming"

    def action_mark_done(self):
        self.write({"state": "done", "active": False})
        for rec in self:
            rec.message_post(body=_("Action marquée comme réalisée et archivée."))
        return self.env.ref("task_actions.action_task_action_item_archive").read()[0]

    def action_mark_todo(self):
        self.write({"state": "todo", "active": True})
        for rec in self:
            rec.message_post(body=_("Action remise en cours."))
        return self.env.ref("task_actions.action_task_action_item").read()[0]
