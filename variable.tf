# Define variables
variable "instance_type" {
  description = "The instance type for the EC2 instance"
  type        = string
  default     = "t2.micro"
}

variable "subnet_id" {
  description = "The ID of the subnet in which to launch the EC2 instance"
  type        = string
  default     = "subnet-065b7cadf0caddbbd"
}

variable "security_group_ids" {
  description = "List of security group IDs for the EC2 instance"
  type        = list(string)
  default     = ["sg-06d1e104433f82fc6"]
}

variable "instance_name" {
  description = "The name of the EC2 instance"
  type        = string
  default     = "BOM_BOM"
}

variable "ebs_size" {
  type = number
  default = 8
  
}

# Add more variables as needed
