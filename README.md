# AR - TOP 5 - AC&D

Module Odoo de suivi des actions prioritaires avec responsable, echeance, priorite, statut et historique dans le chatter.

## Objectif

Cette documentation explique le perimetre fonctionnel du module, les roles utilisateurs, le workflow, la configuration et les principaux objets techniques.

## Utilisateurs concernes

- Responsable action
- Manager
- Administrateur Odoo

## Workflow metier

1. Creation de action
2. Affectation du responsable
3. Suivi de echeance
4. Detection des retards
5. Marquage comme realisee
6. Archivage ou reouverture

## Fonctionnement operationnel

- Creer une action avec responsable et echeance.
- Definir la priorite.
- Suivre les indicateurs: en retard, aujourd hui, a venir, terminee.
- Marquer action comme realisee.
- Reouvrir une action archivee si necessaire.

## Configuration recommandee

- Configurer les groupes dans security/task_actions_groups.xml.
- Verifier les droits sur task.action.item.
- Adapter les filtres par equipe si necessaire.

## Dependances Odoo

- `base`
- `mail`

## Modeles principaux

- `task.action.item`

## Structure importante du module

- `security/ir.model.access.csv`
- `security/task_actions_groups.xml`
- `views/action_item_views.xml`
- `views/menu.xml`
- `models/__init__.py`
- `models/action_item.py`

## Securite

Les droits sont geres par les fichiers du dossier `security`. Il faut verifier les groupes, les regles enregistrement et les acces CSV apres installation ou modification du module.

## Notifications et suivi

Les modules qui dependent de `mail` utilisent le chatter Odoo pour tracer les changements. Les templates mail presents dans le dossier `data` servent a notifier les acteurs concernes par les transitions.

## Installation

1. Copier le module dans le dossier addons Odoo.
2. Redemarrer le serveur Odoo si necessaire.
3. Mettre a jour la liste des applications.
4. Installer ou mettre a jour le module.
5. Verifier les droits utilisateurs et tester un dossier de bout en bout.

## Maintenance

- Ajouter toute nouvelle etape a la fois dans le modele Python, les vues XML, les droits et les notifications.
- Tester les workflows avec plusieurs roles utilisateurs.
- Mettre a jour les rapports et templates mail quand la procedure interne change.
- Eviter de modifier les donnees de production sans sauvegarde.
- Documenter toute evolution fonctionnelle dans ce README.
