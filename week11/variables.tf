#Author: Jordan Sexton-Schoenmann

#General Description: This defines a variable for the Terraform configuration. The instance_name sets the name tag for the EC2 instance and allows for easier identification in AWS.

#Comment: This defines a variable for the EC2 instance name tag.

variable "instance_name" {
  description = "Value of the Name tag for the EC2 instance"
  type        = string
  default     = "JordanInstance"
}