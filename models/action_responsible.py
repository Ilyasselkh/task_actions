from odoo import api, fields, models, tools


class ActionResponsible(models.Model):
    _name = "task.action.responsible"
    _description = "Action par responsable"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _auto = False
    _order = "state asc, deadline asc, priority desc, action_id desc"

    action_id = fields.Many2one("task.action.item", string="Action", readonly=True)
    name = fields.Char(string="Action")
    user_id = fields.Many2one("res.users", string="Responsable", readonly=True)
    user_ids = fields.Many2many(
        "res.users",
        string="Tous les responsables",
        related="action_id.user_ids",
        readonly=False,
    )
    deadline = fields.Date(string="Echeance")
    remaining_days = fields.Integer(string="Jours restants", readonly=True)
    deadline_status = fields.Selection(
        [
            ("overdue", "En retard"),
            ("today", "Aujourd'hui"),
            ("upcoming", "A venir"),
            ("done", "Terminee"),
        ],
        string="Situation",
        readonly=True,
    )
    priority = fields.Selection(
        [("0", "Basse"), ("1", "Normale"), ("2", "Haute")],
        string="Priorite",
        default="1",
    )
    state = fields.Selection(
        [
            ("todo", "A realiser"),
            ("done", "Realisee"),
        ],
        string="Statut",
        readonly=True,
    )
    is_overdue = fields.Boolean(string="En retard", readonly=True)
    active = fields.Boolean(string="Actif", readonly=True)
    parent_id = fields.Many2one("task.action.item", string="Action parente")
    child_ids = fields.One2many(
        "task.action.item",
        "parent_id",
        string="Sous-actions",
        related="action_id.child_ids",
        readonly=False,
    )
    child_summary = fields.Text(string="Sous-actions", compute="_compute_child_summary")
    description = fields.Text(string="Details")

    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute(
            """
            CREATE OR REPLACE VIEW task_action_responsible AS (
                SELECT
                    row_number() OVER (ORDER BY action.id, rel.user_id)::integer AS id,
                    action.id AS action_id,
                    action.name AS name,
                    rel.user_id AS user_id,
                    action.deadline AS deadline,
                    action.remaining_days AS remaining_days,
                    action.deadline_status AS deadline_status,
                    action.priority AS priority,
                    action.state AS state,
                    action.is_overdue AS is_overdue,
                    action.active AS active,
                    action.parent_id AS parent_id,
                    action.description AS description
                FROM task_action_item_res_users_rel rel
                JOIN task_action_item action ON action.id = rel.action_id
                WHERE action.parent_id IS NULL
            )
            """
        )

    @api.depends("action_id.child_ids.name")
    def _compute_child_summary(self):
        for rec in self:
            rec.child_summary = "\n".join(rec.action_id.child_ids.mapped("name"))

    @api.model_create_multi
    def create(self, vals_list):
        records = self.browse()
        Action = self.env["task.action.item"]
        for vals in vals_list:
            child_commands = vals.pop("child_ids", False)
            action_vals = {
                key: vals[key]
                for key in ("name", "deadline", "priority", "description")
                if key in vals
            }
            if vals.get("user_ids"):
                action_vals["user_ids"] = vals["user_ids"]
            elif vals.get("user_id"):
                action_vals["user_ids"] = [(6, 0, [vals["user_id"]])]

            action = Action.create(action_vals)
            if child_commands:
                action.write({"child_ids": child_commands})
            self.env.flush_all()
            records |= self.search([("action_id", "=", action.id)], limit=1)
        return records

    def write(self, vals):
        action_vals = {
            key: vals[key]
            for key in ("name", "deadline", "priority", "parent_id", "description", "user_ids")
            if key in vals
        }
        if action_vals:
            self.mapped("action_id").write(action_vals)
        return True

    def action_open_action(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": self.action_id.display_name,
            "res_model": "task.action.item",
            "res_id": self.action_id.id,
            "view_mode": "form",
            "target": "current",
        }
