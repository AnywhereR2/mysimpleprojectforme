variable "project_id" {
  description = "GCP project ID"
  type        = string
}

variable "region" {
  description = "GCP region"
  type        = string
  default     = "us-east4"
}

variable "zone" {
  description = "GCP zone"
  type        = string
  default     = "us-east4-a"
}

variable "cluster_name" {
  description = "Name of the GKE cluster"
  type        = string
}

variable "machine_type" {
  description = "Type of GCE VM instances"
  type        = string
  default     = "e2-medium"
}

variable "disk_size" {
  description = "Size of boot disk (GB)"
  type        = number
  default     = 20
}

variable "min_node" {
  description = "Minimum number of nodes in the pool"
  type        = number
  default     = 1
}

variable "max_node" {
  description = "Maximum number of nodes in the pool"
  type        = number
  default     = 1
}
