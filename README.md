# Employee_Management_Flask


terraform apply -target=aws_launch_template.main -target=aws_autoscaling_group.main -target=aws_autoscaling_policy.main -target=aws_lb_listener.main -target=aws_lb_target_group.main -target=aws_lb.main -auto-approve


terraform destroy -target=aws_launch_template.main -target=aws_autoscaling_group.main -target=aws_autoscaling_policy.main -target=aws_lb_listener.main -target=aws_lb_target_group.main -target=aws_lb.main -auto-approve


