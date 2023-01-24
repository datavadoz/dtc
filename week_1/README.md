# Week 1

## Overview
There are 3 main components:
- Postgres: Relational database.
- Pgadmin: UI for ease of Postgres manipulation.
- Worker: ETL should be performed here.

## Prerequisite
Docker with compose plugin (current testing version: 20.10.17).

## Instruction
Build and bring system up:
```
mkdir -p pgadmin
sudo chown -R 5050:5050 pgadmin
docker compose build
docker compose up -d
```

## Homework - Docker & SQL
### Question 1: Which tag has the following text? - Write the image ID to the file
```
$ docker build --help | grep "Write the image ID to the file"
      --iidfile string          Write the image ID to the file
```
**Answer**: --iidfile string

### Question 2: How many python packages/modules are installed in python:3.9 image?
```
$ docker run -it python:3.9 pip list
Package    Version
---------- -------
pip        22.0.4
setuptools 58.1.0
wheel      0.38.4
WARNING: You are using pip version 22.0.4; however, version 22.3.1 is available.
You should consider upgrading via the '/usr/local/bin/python -m pip install --upgrade pip' command.
```
**Answer**: 3

### Question 3: How many taxi trips were totally made on January 15?
**Answer**: 20530
```
SELECT COUNT(*)
FROM green_taxi
WHERE lpep_pickup_datetime::date = '2019-01-15'
	AND lpep_dropoff_datetime::date = '2019-01-15'
```

### Question 4: Which was the day with the largest trip distance? Use the pick up time for your calculations.
**Answer**: 2019-01-15
```
SELECT lpep_pickup_datetime::date
FROM green_taxi
GROUP BY lpep_pickup_datetime::date
ORDER BY MAX(trip_distance) DESC
LIMIT 1
```

### Question 5: In 2019-01-01 how many trips had 2 and 3 passengers?
**Answer**: 2: 1282 ; 3: 254
```
SELECT passenger_count, COUNT(*)
FROM green_taxi
WHERE lpep_pickup_datetime::date = '2019-01-01'
	AND (passenger_count = 2 OR passenger_count = 3)
GROUP BY passenger_count
```

### Question 6: For the passengers picked up in the Astoria Zone which was the drop off zone that had the largest tip? We want the name of the zone, not the id.
**Answer**: Long Island City/Queens Plaza
```
SELECT "Zone"
FROM taxi_zone_lookup
WHERE "LocationID" = (
	SELECT "DOLocationID"
	FROM green_taxi
	WHERE "PULocationID" = (
		SELECT "LocationID"
		FROM taxi_zone_lookup
		WHERE "Zone" = 'Astoria'
	)
	GROUP BY "DOLocationID"
	ORDER BY MAX(tip_amount) DESC
	LIMIT 1
)
```

## Homework - Terraform
There are some required steps:

0. Install Terrform.
1. Install Google Cloud SDK.
2. Create GCP (Google Clould Platform) account. Then, add credit card into it :)
3. Create a new GCP project (ex: dtc-de).
4. Create a service account (ex: dtc-de-user) with **Viewer** role on new created project. Then, generate and store private JSON key on that created service account securely.
5. Enable following additional roles for created service account: BigQuery Admin, Storage Admin, Storage Object Admin.
6. Enable following APIs:
	- IAM Service Account Credentials API
	- Identity and Access Management (IAM) API
7. Login GCP via CLI:
```
export GOOGLE_APPLICATION_CREDENTIALS="<path_to_private_json_key_from_step_4>"
gcloud auth application-default login
```
8. Terraform show:
```
cd terraform
# Initialize state file (.tfstate)
terraform init

# Check changes to new infra plan
terraform plan -var="project=<your-gcp-project-id>"

# Create new infra
terraform apply -var="project=<your-gcp-project-id>"

# Delete infra after your work, to avoid costs on any running services
terraform destroy
```

For more detail, refer to this [Youtube tutorial](https://www.youtube.com/watch?v=Hajwnmj0xfQ&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=11) and [Terraform HW](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/week_1_basics_n_setup/1_terraform_gcp/terraform).

### Question: After updating the `main.tf` and `variables.tf` files, perform `terraform apply` and paste the output of this command.
**Answer**:
```
$ terraform apply -var="project=dtc-de-375513"  # dtc-de-375513 is the project ID

Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
  + create

Terraform will perform the following actions:

  # google_bigquery_dataset.dataset will be created
  + resource "google_bigquery_dataset" "dataset" {
      + creation_time              = (known after apply)
      + dataset_id                 = "trips_data_all"
      + delete_contents_on_destroy = false
      + etag                       = (known after apply)
      + id                         = (known after apply)
      + labels                     = (known after apply)
      + last_modified_time         = (known after apply)
      + location                   = "northamerica-northeast1"
      + project                    = "dtc-de-375513"
      + self_link                  = (known after apply)

      + access {
          + domain         = (known after apply)
          + group_by_email = (known after apply)
          + role           = (known after apply)
          + special_group  = (known after apply)
          + user_by_email  = (known after apply)

          + dataset {
              + target_types = (known after apply)

              + dataset {
                  + dataset_id = (known after apply)
                  + project_id = (known after apply)
                }
            }

          + routine {
              + dataset_id = (known after apply)
              + project_id = (known after apply)
              + routine_id = (known after apply)
            }

          + view {
              + dataset_id = (known after apply)
              + project_id = (known after apply)
              + table_id   = (known after apply)
            }
        }
    }

  # google_storage_bucket.data-lake-bucket will be created
  + resource "google_storage_bucket" "data-lake-bucket" {
      + force_destroy               = true
      + id                          = (known after apply)
      + location                    = "NORTHAMERICA-NORTHEAST1"
      + name                        = "dtc_data_lake_dtc-de-375513"
      + project                     = (known after apply)
      + public_access_prevention    = (known after apply)
      + self_link                   = (known after apply)
      + storage_class               = "STANDARD"
      + uniform_bucket_level_access = true
      + url                         = (known after apply)

      + lifecycle_rule {
          + action {
              + type = "Delete"
            }

          + condition {
              + age                   = 30
              + matches_prefix        = []
              + matches_storage_class = []
              + matches_suffix        = []
              + with_state            = (known after apply)
            }
        }

      + versioning {
          + enabled = true
        }

      + website {
          + main_page_suffix = (known after apply)
          + not_found_page   = (known after apply)
        }
    }

Plan: 2 to add, 0 to change, 0 to destroy.

Do you want to perform these actions?
  Terraform will perform the actions described above.
  Only 'yes' will be accepted to approve.

  Enter a value: yes

google_bigquery_dataset.dataset: Creating...
google_storage_bucket.data-lake-bucket: Creating...
google_bigquery_dataset.dataset: Creation complete after 2s [id=projects/dtc-de-375513/datasets/trips_data_all]
google_storage_bucket.data-lake-bucket: Creation complete after 5s [id=dtc_data_lake_dtc-de-375513]

Apply complete! Resources: 2 added, 0 changed, 0 destroyed.
```
