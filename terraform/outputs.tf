output "vpc_id" {
  description = "ID of the VPC"
  value       = aws_vpc.main.id
}

output "alb_dns_name" {
  description = "DNS name of the Application Load Balancer"
  value       = aws_lb.main.dns_name
}

output "application_url" {
  description = "URL to access the application"
  value       = "http://${aws_lb.main.dns_name}"
}

output "app_version" {
  description = "Version of the application deployed"
  value       = var.app_version
}

output "deployment_timestamp" {
  description = "Timestamp of the latest deployment"
  value       = timestamp()
}

output "db_host" {
  description = "Host of the database server"
  value       = aws_instance.mariadb.private_ip
}

output "asg_name" {
  description = "Name of the Auto Scaling Group"
  value       = aws_autoscaling_group.main.name
}