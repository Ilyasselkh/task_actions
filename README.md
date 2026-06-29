# AR - TOP 5 - AC&D

Module Odoo de suivi des actions prioritaires avec responsables, echeances, priorites, sous-actions et historique dans le chatter.

Le module sert a centraliser les actions issues des rituels TOP 5 / AC&D et a donner une vision claire des actions a realiser, en retard, a venir ou terminees.

## Objectif fonctionnel

Assurer le suivi operationnel des actions jusqu'a leur cloture.

Le module permet de :

- creer une action a suivre ;
- affecter un ou plusieurs responsables ;
- definir une echeance ;
- definir une priorite basse, normale ou haute ;
- ajouter une description ;
- rattacher des sous-actions ;
- suivre les indicateurs de delai ;
- marquer une action comme realisee ;
- archiver automatiquement les actions realisees ;
- remettre une action en cours si necessaire ;
- tracer les changements dans le chatter Odoo.

## Roles fonctionnels

### Responsable action

Le responsable action suit l'action qui lui est affectee.

Il peut :

- consulter ses actions ;
- mettre a jour les details ;
- traiter les sous-actions ;
- marquer l'action comme realisee.

### Manager / pilote TOP 5

Le manager suit l'avancement global.

Il peut :

- consulter les actions ouvertes ;
- filtrer par responsable, echeance, priorite ou retard ;
- relancer les actions en retard ;
- verifier les actions archivees.

### Administrateur

L'administrateur gere les droits et la structure du module.

## Etats principaux

Les actions utilisent deux etats :

- `A realiser`
- `Realisee`

Les indicateurs de delai sont calcules automatiquement :

- `En retard`
- `Aujourd'hui`
- `A venir`
- `Terminee`

## Fonctionnement operationnel

1. Creer une action.
2. Renseigner le ou les responsables.
3. Definir l'echeance et la priorite.
4. Ajouter une description si necessaire.
5. Creer des sous-actions lorsque l'action doit etre detaillee.
6. Suivre le statut d'echeance.
7. Marquer l'action comme realisee.
8. Consulter l'action dans les archives si besoin.

## Sous-actions

Une action peut contenir des sous-actions.

Le module bloque les boucles de hierarchie afin qu'une action ne puisse pas devenir sa propre sous-action.

## Securite

Les droits sont definis dans :

- `security/task_actions_groups.xml`
- `security/ir.model.access.csv`

Points a verifier :

- acces aux actions principales ;
- acces aux actions archivees ;
- droits des responsables ;
- droits de creation et modification.

## Modeles principaux

- `task.action.item`
- `task.action.responsible`

## Structure du module

- `security/task_actions_groups.xml`
- `security/ir.model.access.csv`
- `views/action_item_views.xml`
- `views/menu.xml`
- `models/action_item.py`
- `models/action_responsible.py`
- `static/src/scss/task_actions.scss`
- `static/src/js/task_actions.js`

## Installation

1. Copier le module dans le dossier addons Odoo.
2. Redemarrer le serveur Odoo si necessaire.
3. Mettre a jour la liste des applications.
4. Installer le module.
5. Verifier les groupes utilisateurs.
6. Creer une action de test avec responsable et echeance.
7. Tester la cloture et la reouverture.

## Maintenance fonctionnelle

Lorsqu'une regle de suivi change, verifier aussi :

- les champs du modele `task.action.item` ;
- les vues liste, formulaire et archive ;
- les filtres de retard et d'echeance ;
- les droits de securite ;
- ce README.
