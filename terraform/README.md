# Infrastructure Terraform

Ce dossier contient la configuration Terraform utilisée pour gérer les principales ressources Google Cloud du projet Olist Data Engineering.

## Ressources gérées

- Un bucket Google Cloud Storage utilisé comme Data Lake
- Un dataset BigQuery utilisé pour les données analytiques

Les ressources ayant été initialement créées manuellement dans Google Cloud, elles ont été importées dans le State Terraform afin d’être ensuite gérées comme Infrastructure as Code.

## Structure

```text
terraform/
├── main.tf
├── provider.tf
├── variables.tf
├── terraform.tfvars
├── outputs.tf
└── .terraform.lock.hcl

```

## Commandes principales

Se placer dans le dossier Terraform :

```bash
cd terraform
```

Initialiser le projet Terraform et télécharger le provider Google :

```bash
terraform init
```

Vérifier les changements que Terraform prévoit :

```bash
terraform plan
```

Appliquer les changements après vérification du plan :

```bash
terraform apply
```

Afficher les ressources actuellement enregistrées dans le State :

```bash
terraform state list
```

## Authentification locale

Terraform s’authentifie auprès de Google Cloud avec un Service Account.

La clé JSON n’est jamais stockée dans GitHub. Chaque utilisateur doit utiliser sa propre clé locale et indiquer son chemin avec la variable d’environnement suivante :

```bash
export GOOGLE_APPLICATION_CREDENTIALS="/chemin/vers/service-account.json"
```

Dans mon environnement local, la commande utilisée est :

```bash
export GOOGLE_APPLICATION_CREDENTIALS="$(realpath ../dbt/.keys/dbt-bigquery-sa.json)"
```

Cette variable est valable uniquement dans le terminal courant.

## Reproduire l’infrastructure

Une personne qui clone le dépôt doit :

1. Créer ou utiliser son propre projet Google Cloud.
2. Créer un Service Account avec les permissions nécessaires.
3. Télécharger sa propre clé JSON localement.
4. Définir la variable `GOOGLE_APPLICATION_CREDENTIALS`.
5. Adapter le fichier `terraform.tfvars` avec son propre identifiant de projet.
6. Exécuter :

```bash
terraform init
terraform plan
terraform apply
```

Dans mon cas, le bucket GCS et le dataset BigQuery existaient déjà. Ils ont donc été importés dans le State Terraform avec `terraform import`.

## Ressources actuellement gérées

```text
google_storage_bucket.data_lake
google_bigquery_dataset.analytics
```

## Fichiers non versionnés

Les éléments suivants ne sont jamais envoyés sur GitHub :

```text
.terraform/
terraform.tfstate
terraform.tfstate.*
fichiers JSON de Service Account
```