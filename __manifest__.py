{
    "name": "AR - TOP 5 - AC&D",
    "version": "1.0.0",
    "category": "Productivity",
    "summary": "Plan d'actions professionnel avec responsables, échéances et suivi",
    "depends": ["base", "mail"],
    "data": [
        "security/task_actions_groups.xml",
        "security/ir.model.access.csv",
        "views/action_item_views.xml",
        "views/menu.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "task_actions/static/src/scss/task_actions.scss",
            "task_actions/static/src/js/task_actions.js",
        ],
    },
    "application": True,
    "license": "LGPL-3",
}
