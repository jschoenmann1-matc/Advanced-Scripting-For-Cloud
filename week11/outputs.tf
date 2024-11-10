#Author: Jordan Sexton-Schoenmann

#General Description: This script defines output variables in Terraform which will display instance ID and public IP of the EC2 instance when complete.

#Comment: This outputs the ID of the EC2 instance.

output "instance_id" {
  description = "ID of the EC2 instance"
  value       = aws_instance.app_server.id
}

#Comment: This outputs the public IP address of the EC2 instance.

output "instance_public_ip" {
  description = "Public IP address of the EC2 instance"
  value       = aws_instance.app_server.public_ip
}