# AR - TOP 5 - AC&D

Module Odoo de suivi des actions prioritaires avec responsable, échéance, priorité et statut.

## Objectif

Ce module centralise les actions à réaliser dans un tableau de pilotage simple. Chaque action est affectée à un utilisateur, possède une échéance, une priorité et un état d'avancement. Le module utilise le chatter Odoo pour conserver l'historique des changements et les échanges autour de l'action.

## Dépendances

- `base`
- `mail`

## Modèle principal

- `task.action.item` : action à suivre.

Champs principaux :

- `name` : intitulé de l'action.
- `user_id` : responsable.
- `deadline` : date limite.
- `priority` : basse, normale ou haute.
- `state` : `todo` ou `done`.
- `description` : détails de l'action.
- `remaining_days`, `is_overdue`, `deadline_status` : indicateurs calculés selon l'échéance.

## Fonctionnement

1. L'utilisateur crée une action et renseigne le responsable, la date limite, la priorité et les détails.
2. Le module calcule automatiquement la situation de l'échéance : à venir, aujourd'hui, en retard ou terminée.
3. Une action peut être marquée comme réalisée avec `action_mark_done`; elle passe à `done` et devient inactive.
4. Une action archivée peut être remise en cours avec `action_mark_todo`.
5. Les changements importants sont tracés dans le chatter grâce à `mail.thread`.

## Vues et menus

Le module fournit des vues de liste, formulaire et recherche pour piloter les actions par statut, responsable, priorité et échéance.

## Sécurité

Les groupes et droits d'accès sont définis dans :

- `security/task_actions_groups.xml`
- `security/ir.model.access.csv`

## Assets

Des fichiers SCSS et JavaScript améliorent l'affichage backend :

- `static/src/scss/task_actions.scss`
- `static/src/js/task_actions.js`

