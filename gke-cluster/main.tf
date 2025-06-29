provider "google" {
  project = var.project_id
  region  = var.region
  zone    = var.zone
}

resource "google_compute_network" "vpc_network" {
  name                    = "gke-vpc"
  auto_create_subnetworks = false
}

resource "google_compute_subnetwork" "subnet" {
  name          = "gke-subnet"
  ip_cidr_range = "10.0.0.0/16"
  region        = var.region
  network       = google_compute_network.vpc_network.id
}

resource "google_container_cluster" "gke_cluster" {
  name     = var.cluster_name
  location = var.zone

  enable_shielded_nodes    = true
  remove_default_node_pool = true
  initial_node_count       = 1

  release_channel {
    channel = "STABLE"
  }

  addons_config {
    http_load_balancing {
      disabled = false
    }
  }

  networking_mode = "VPC_NATIVE"
  ip_allocation_policy {
    cluster_ipv4_cidr_block  = "/16"
    services_ipv4_cidr_block = "/22"
  }

  timeouts {
    create = "20m"
    update = "20m"
  }

  lifecycle {
    ignore_changes = [node_pool]
  }
}

resource "google_container_node_pool" "primary_nodes" {
  name       = "${var.cluster_name}-pool"
  location   = var.zone
  cluster    = google_container_cluster.gke_cluster.name
  node_count = 1

  management {
    auto_repair  = true
    auto_upgrade = true
  }

  autoscaling {
    min_node_count = var.min_node
    max_node_count = var.max_node
  }

  timeouts {
    create = "20m"
    update = "20m"
  }

  node_config {
    preemptible     = true
    machine_type    = var.machine_type
    disk_size_gb    = var.disk_size

    oauth_scopes = [
      "https://www.googleapis.com/auth/compute",
      "https://www.googleapis.com/auth/cloud-platform",
      "https://www.googleapis.com/auth/devstorage.read_only",
      "https://www.googleapis.com/auth/logging.write",
      "https://www.googleapis.com/auth/monitoring",
    ]
  }
}
