# AR - TOP 5 - AC&D


> Documentation du module de plan d?actions avec responsables, ?ch?ances et suivi.


## Vue d?ensemble

Ce module fournit une application l?g?re de pilotage des actions prioritaires. Il est con?u pour suivre les actions ouvertes, les responsables, les ?ch?ances, les priorit?s et les retards. Le chatter conserve l?historique, ce qui permet de garder une trace des d?cisions et des cl?tures.

## Utilisateurs concern?s

- Responsable action : ex?cute et met ? jour son action.
- Manager : suit les actions ouvertes, en retard ou cl?tur?es.
- Administrateur : g?re les droits d?acc?s.

## Workflow m?tier

1. Cr?ation de l?action
2. Affectation d?un responsable
3. Suivi de l??ch?ance
4. Marquage comme r?alis?e
5. Archivage automatique
6. R?ouverture possible

## Fonctionnement op?rationnel

- Cr?er une action avec un responsable et une ?ch?ance.
- Classer la priorit? : basse, normale ou haute.
- Surveiller les indicateurs : en retard, aujourd?hui, ? venir ou termin?e.
- Cliquer sur le bouton de cl?ture pour marquer l?action comme r?alis?e.
- Consulter les actions archiv?es si besoin de r?ouverture.

## Configuration recommand?e

- Configurer les groupes dans security/task_actions_groups.xml.
- V?rifier les acc?s au mod?le task.action.item.
- Adapter les vues si des filtres par ?quipe ou service sont n?cessaires.

## D?pendances Odoo

- `base`
- `mail`

## Mod?les techniques

- `task.action.item` : Action à suivre (`models/action_item.py`)

## ?tats d?tect?s dans le code

- `models/action_item.py` : `todo` (À réaliser), `done` (Réalisée)

## Actions serveur principales

- `action_mark_done` (`models/action_item.py`)
- `action_mark_todo` (`models/action_item.py`)

## Fichiers charg?s par le manifest

- `security/task_actions_groups.xml`
- `security/ir.model.access.csv`
- `views/action_item_views.xml`
- `views/menu.xml`

## S?curit? et droits

Le module s?appuie sur les fichiers suivants pour d?finir les groupes, r?gles d?enregistrement et droits d?acc?s :

- `security/ir.model.access.csv`
- `security/task_actions_groups.xml`

## Assets et interface

- `static/src/js/task_actions.js`
- `static/src/scss/task_actions.scss`

## Bonnes pratiques d?utilisation

- V?rifier que chaque utilisateur Odoo est li? au bon employ? lorsque le module d?pend de `hr.employee`.
- Tester le workflow avec un dossier de test avant utilisation en production.
- Contr?ler les groupes de s?curit? apr?s installation afin que seuls les bons r?les voient les boutons de validation.
- Garder les templates e-mail et rapports align?s avec les proc?dures internes.
- Sauvegarder la base avant toute modification structurelle du module.

## Maintenance

- Les ?volutions fonctionnelles doivent ?tre ajout?es dans les mod?les Python, les vues XML et les r?gles de s?curit? correspondantes.
- Apr?s modification des vues, mettre ? jour le module depuis Odoo ou red?marrer le serveur selon le type de changement.
- Apr?s modification des assets, vider le cache navigateur et recompiler les assets si n?cessaire.
- Toute nouvelle ?tape de workflow doit ?tre accompagn?e des droits, boutons, notifications et filtres correspondants.
