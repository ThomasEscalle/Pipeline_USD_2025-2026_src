# USD Asset Resolver

## Introduction

Le **USD Asset Resolver** est un système de résolution d'assets personnalisé pour Pixar's Universal Scene Description (USD). Il permet de résoudre des chemins d'assets via des URIs personnalisées, facilitant la gestion et l'accès aux ressources dans un pipeline de production 3D.

## Qu'est-ce qu'un Asset Resolver USD ?

Un Asset Resolver USD est un composant pluggable du système USD qui définit comment les références d'assets (textures, géométries, scènes, etc.) sont résolues en chemins de fichiers réels sur le système de fichiers. Au lieu d'utiliser des chemins absolus ou relatifs traditionnels, un Asset Resolver permet d'utiliser des URIs personnalisées qui peuvent être traduites en chemins système.

### Avantages clés

- **Portabilité** : Les scènes USD peuvent référencer des assets via des URIs logiques plutôt que des chemins absolus
- **Flexibilité** : Permet de réorganiser la structure de fichiers sans casser les références
- **Pipeline integration** : Facilite l'intégration avec des systèmes de gestion d'assets
- **Version management** : Gestion automatique des versions d'assets
- **Performance** : Mise en cache des résolutions pour améliorer les performances

## Pourquoi est-ce utile ?

Dans un pipeline de production 3D, les assets sont souvent :

1. **Distribués** sur plusieurs serveurs ou emplacements
2. **Versionnés** avec des systèmes de numérotation complexes
3. **Organisés** selon des conventions de nommage spécifiques
4. **Partagés** entre plusieurs projets et équipes

L'Asset Resolver permet de :

- Abstraire la complexité de l'organisation des fichiers
- Automatiser la résolution vers la dernière version
- Centraliser la configuration des chemins de projets
- Simplifier les références dans les scènes USD

## Structure des URIs

Ce système utilise des URIs avec le schéma `bp://` suivant cette structure :

```text
bp://<project>/?<parameters>
```

### Schéma de l'URI

| Composant | Description | Obligatoire | Exemple |
|-----------|-------------|-------------|---------|
| `bp://` | Schéma URI identifiant le resolver | ✅ Oui | `bp://` |
| `<project>` | Nom du projet | ✅ Oui | `MyProject` |
| `?` | Séparateur de paramètres | ✅ Oui | `?` |
| `<parameters>` | Paramètres de requête | ✅ Oui | `type=asset&name=character` |

## Paramètres de requête

### Paramètres généraux

| Paramètre | Alias | Description | Obligatoire | Valeur par défaut | Exemple |
|-----------|--------|-------------|-------------|-------------------|---------|
| `type` | `t` | Type d'asset | ✅ Oui | `Asset` | `type=chars` |
| `name` | `n` | Nom de l'asset | ✅ Oui (pour assets) | - | `name=hero_character` |
| `product` | `p` | Type de produit/export | ❌ Non | `USD_Asset` | `product=USD_Asset` |
| `version` | `v` | Version spécifique | ❌ Non | `latest` | `version=v001` |

### Paramètres pour les Plans (Shots)

| Paramètre | Alias | Description | Obligatoire | Exemple |
|-----------|--------|-------------|-------------|---------|
| `seq` | `s`, `sequence`, `seqs` | Nom de la séquence | ✅ Oui | `seq=sq010` |
| `shot` | `sh`, `sht`, `shots`, `shts` | Nom du shot | ❌ Non | `shot=sh010` |

## Types d'assets supportés

### Assets

| Type | Alias | Description | Dossier cible |
|------|-------|-------------|---------------|
| `chars` | `c`, `char` | Personnages | `01_Assets/Chars/` |
| `props` | `p`, `prop` | Props/Objets | `01_Assets/Props/` |
| `enviros` | `e`, `env`, `envs` | Environnements | `01_Assets/Enviros/` |
| `items` | `i`, `item` | Items/Éléments | `01_Assets/Items/` |
| `modules` | `m`, `module` | Modules | `01_Assets/Modules/` |
| `asset` | `a`, `assets` | Asset générique | `01_Assets/` |

### Shots

| Type | Alias | Description | Dossier cible |
|------|-------|-------------|---------------|
| `shot` | `s`, `shots` | Plan/Shot | `02_Shots/` |

## Structure de projet

Le resolver attend une structure de projet standardisée :

```text
<PROJECT_ROOT>/
├── 03_Production/
│   ├── 01_Assets/
│   │   ├── Chars/
│   │   │   └── <asset_name>/
│   │   │       └── Export/
│   │   │           ├── USD_Asset/
│   │   │           │   └── asset.usda
│   │   │           └── <product>/
│   │   │               ├── v001/
│   │   │               ├── v002/
│   │   │               └── latest -> v002/
│   │   ├── Props/
│   │   ├── Enviros/
│   │   ├── Items/
│   │   └── Modules/
│   └── 02_Shots/
│       └── <sequence>/
│           └── <shot>/
│               └── Export/
│                   └── <product>/
│                       ├── v001/
│                       ├── v002/
│                       └── latest -> v002/
```

## Configuration

La configuration des projets se fait via le fichier `projects.json` :

```json
{
    "projects": [
        {
            "name": "MyProject",
            "root": "/path/to/project/root"
        },
        {
            "name": "AnotherProject", 
            "root": "/path/to/another/project"
        }
    ]
}
```

## Exemples d'URIs

### Assets de base

```bash
# Récupérer un personnage (dernière version)
bp://MyProject/?type=chars&name=hero_character

# Version spécifique d'un prop
bp://MyProject/?type=props&name=magic_sword&version=v003

# Environnement avec produit spécifique
bp://MyProject/?type=enviros&name=forest_temple&product=USD_Geo&version=latest
```

### Shots

```bash
# Shot spécifique avec produit
bp://MyProject/?type=shot&seq=sq010&shot=sh020&product=USD_Layout

# Shot master d'une séquence
bp://MyProject/?type=shot&seq=sq010&product=USD_Master

# Avec version spécifique
bp://MyProject/?type=shot&seq=sq010&shot=sh020&product=USD_Animation&version=v005
```

### Syntaxe raccourcie avec alias

```bash
# Utilisation des alias pour une syntaxe plus courte
bp://MyProject/?t=c&n=hero_character&v=latest
bp://MyProject/?t=p&n=magic_sword&p=USD_Asset
bp://MyProject/?t=s&s=sq010&sh=sh020&p=USD_Layout
```

### Cas d'usage avancés

```bash
# Asset générique dans le dossier racine Assets
bp://MyProject/?type=asset&name=shared_library

# Module réutilisable
bp://MyProject/?type=modules&name=building_kit&product=USD_Variants

# Item spécialisé
bp://MyProject/?type=items&name=fx_explosion&version=v010
```

## Comportement de résolution

1. **Validation de l'URI** : Vérification du schéma `bp://` et de la présence du projet
2. **Résolution du projet** : Mapping du nom de projet vers le chemin racine via `projects.json`
3. **Construction du chemin** : Assemblage du chemin basé sur le type d'asset
4. **Recherche d'asset** : Localisation du dossier d'asset (insensible à la casse)
5. **Résolution de version** :
   - `latest` → dernière version disponible (triée numériquement)
   - Version spécifique → dossier exact
   - Fallback vers la dernière version si la version demandée n'existe pas
6. **Sélection de fichier** : Premier fichier USD trouvé (`.usd`, `.usda`, `.usdc`, `.usdz`)
7. **Mise en cache** : Stockage du résultat pour les accès futurs

## Notes techniques

- **Performance** : Le système met en cache les résolutions pour éviter les accès disque répétés
- **Logging** : Logging détaillé pour le debugging des résolutions
- **Robustesse** : Gestion des erreurs avec fallback et messages informatifs
- **Flexibilité** : Support de multiples aliases pour faciliter l'utilisation
- **Compatibilité** : Chemins normalisés pour la compatibilité cross-platform

---

!!! tip "Conseil"
    Utilisez toujours `version=latest` en production pour récupérer automatiquement la dernière version approuvée d'un asset.

!!! warning "Attention"
    Assurez-vous que la structure de dossiers respecte la convention attendue par le resolver pour un fonctionnement optimal.

!!! info "Information"
    Le resolver peut rechercher des assets avec une recherche insensible à la casse jusqu'à 3 niveaux de profondeur dans l'arborescence.
