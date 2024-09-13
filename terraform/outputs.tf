# output "instance_public_ip" {
#   description = "Public IP address of the EC2 instance"
#   value       = aws_instance.main.public_ip
# }

# output "instance_public_dns" {
#   description = "Public DNS of the EC2 instance"
#   value       = aws_instance.main.public_dns
# }

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

output "alb_instance_ips_command" {
  description = "AWS CLI command to get public IPs of instances behind the ALB"
  value       = <<EOT
ASG_NAME=$(aws autoscaling describe-auto-scaling-groups --query 'AutoScalingGroups[?contains(AutoScalingGroupName, "${var.project_name}")].AutoScalingGroupName' --output text) && \
INSTANCE_IDS=$(aws autoscaling describe-auto-scaling-groups --auto-scaling-group-name "$ASG_NAME" --query 'AutoScalingGroups[].Instances[].InstanceId' --output text) && \
aws ec2 describe-instances --instance-ids $INSTANCE_IDS --query 'Reservations[].Instances[].PublicIpAddress' --output text
EOT
}