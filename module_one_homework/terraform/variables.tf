variable "credentials" {
  description = "My Credentials"
  default     = "./keys/my_secret_key.json"
  #ex: if you have a directory where this file is called keys with your service account json file
  #saved there as my-creds.json you could use default = "./keys/my-creds.json"
}

variable "project" {
  description = "Project"
  default     = "poised-kiln-485113-k4"
}

variable "region" {
  description = "Region"
  #Update the below to your desired region
  default = "europe-west2"
}

variable "location" {
  description = "Project Location"
  #Update the below to your desired location
  default = "europe-west2"
}

variable "bq_dataset_name" {
  description = "My BigQuery Dataset Name"
  # Changed hyphens to underscores
  default = "dez_module_one_fc_demo_dataset"
}

variable "gcs_bucket_name" {
  description = "My Storage Bucket Name"
  #Update the below to a unique bucket name
  default = "dez_module_one_fc_demo_terra_bucket"
}

variable "gcs_storage_class" {
  description = "Bucket Storage Class"
  default     = "STANDARD"
}