from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ActionItem(models.Model):
    _name = "task.action.item"
    _description = "Action à suivre"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "state asc, deadline asc, priority desc, id desc"

    name = fields.Char(string="Action", required=True, tracking=True)
    user_id = fields.Many2one("res.users", string="Responsable historique", index=True)
    user_ids = fields.Many2many(
        "res.users",
        "task_action_item_res_users_rel",
        "action_id",
        "user_id",
        string="Responsables",
        default=lambda self: self.env.user,
        required=True,
        tracking=True,
    )
    deadline = fields.Date(string="Échéance", tracking=True)

    primary_user_id = fields.Many2one(
        "res.users",
        string="Responsable principal",
        compute="_compute_primary_user_id",
        store=True,
        index=True,
    )

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
    parent_id = fields.Many2one(
        "task.action.item",
        string="Action parente",
        index=True,
        tracking=True,
        ondelete="cascade",
    )
    child_ids = fields.One2many(
        "task.action.item",
        "parent_id",
        string="Sous-actions",
    )
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

    def init(self):
        self.env.cr.execute(
            """
            INSERT INTO task_action_item_res_users_rel (action_id, user_id)
            SELECT id, user_id
              FROM task_action_item
             WHERE user_id IS NOT NULL
            ON CONFLICT DO NOTHING
            """
        )

    @api.depends("user_ids")
    def _compute_primary_user_id(self):
        for rec in self:
            rec.primary_user_id = rec.user_ids[:1]

    @api.constrains("parent_id")
    def _check_parent_id(self):
        for rec in self:
            parent = rec.parent_id
            while parent:
                if parent == rec:
                    raise ValidationError(_("Une action ne peut pas être sa propre sous-action."))
                parent = parent.parent_id

    @api.depends("deadline", "state")
    def _compute_deadline_indicators(self):
        today = fields.Date.today()
        for rec in self:
            if not rec.deadline:
                rec.remaining_days = 0
                rec.is_overdue = False
                rec.deadline_status = "done" if rec.state == "done" else "upcoming"
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
            rec.message_post(body=_("Action réalisée et archivée par %s.") % self.env.user.name)
        return self.env.ref("task_actions.action_task_action_item_archive").read()[0]

    def action_mark_done_inline(self):
        self.write({"state": "done"})
        for rec in self:
            rec.message_post(body=_("Sous-action réalisée par %s.") % self.env.user.name)
        return True

    def action_mark_todo(self):
        self.write({"state": "todo", "active": True})
        for rec in self:
            rec.message_post(body=_("Action remise en cours par %s.") % self.env.user.name)
        return self.env.ref("task_actions.action_task_action_item").read()[0]
