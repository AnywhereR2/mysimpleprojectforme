output "cluster_name" {
  value = google_container_cluster.gke_cluster.name
}

output "endpoint" {
  value = google_container_cluster.gke_cluster.endpoint
}

output "node_pool_name" {
  value = google_container_node_pool.primary_nodes.name
}