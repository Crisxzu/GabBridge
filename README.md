# GabBridge

GabBride est un projet **Django** qui a été réalisé pour répondre au test technique de Bridge.<br/>
L'énoncé était le suivant :


>Concevoir un système de GAB simulé pour permettre aux utilisateurs
d’accéder à leur compte bancaire, de consulter leur solde, d’effectuer des retraits et
des dépôts, et de visualiser un historique de leurs transactions. Le système devra
inclure une authentification simulée via un numéro de carte et un code PIN.

La base de données utilisée est **PostgreSQL**.<br/>
**Boostrap 5** a été utilisée pour le frontend.

Si jamais, vous souhaitez le tester en live, il est accessible à ce lien : https://gabbridge.dazu.fr/ <br/>
Pour s'authentifier, voici les identifants de test : <br/>
Numéro de compte : 0744980859 <br/>
PIN : 9230

## Structure du projet

```
gab/
├── bridge/                 # Application principale
│   ├── models/            # Modèles de données
│   ├── templates/         # Templates HTML
│   ├── static/            # Fichiers statiques
│   └── views/             # Vues
├── gab/                   # Configuration du projet
└── manage.py
```


## Prérequis

- Python 3.10
- PostgreSQL
- pip

## Installation

- Cloner le repo

```bash
git clone https://github.com/Crisxzu/GabBridge.git
```

- Créer l'environnement virtuel

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

- Installer les dépendances

```bash
pip install -r requirements.txt
```

- Lancer le projet

```bash
python manage.py runserver
```

## Configuration

- Modifier les variables dans `.env`

```bash
cp .env.example .env
```

- Lancer les migrations

```bash
python manage.py migrate
```

- Créer le super utilisateur

```bash
python manage.py createsuperuser
```

N'oubliez pas de consulter le fichier `gab/settings.py` pour adapter le projet en fonction de vos besoins.
Par exemple, modifier les hôtes autorisés et l'hôte de confiance pour le CRSF.

## Fonctionnement

Avec le compte super utilisateur, vous pouvez accéder au panel d'administration à `/admin`.<br/>
Afin de créer des clients et des comptes bancaires. <br/>
Attention, une distinction est à faire entre les utilisateurs staff et les utilisateurs classiques (les clients).<br/>
Les clients n'ont pas accés au panel d'administration.<br/>
Les utilisateurs staff n'ont pas de compte bancaire.<br/>

Pour accéder à votre compte bancaire, vous devez utiliser votre numéro de compte(12 chiffres) et votre code PIN(4 chiffres).

## Sécurité

- Hashage des PINS
- Sessions limités à 5 min si aucune action
- Validation des entrées

