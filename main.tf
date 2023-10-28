terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }

  required_version = ">= 1.2.0"
}

provider "aws" {
  region = "ap-south-2"
}

data "aws_subnet" "instance_subnet" {
  id = var.subnet_id
}

resource "aws_instance" "instance-1" {
  ami           = "ami-0caaf932a5d8ef491"
  instance_type = var.instance_type
  subnet_id     = var.subnet_id
  vpc_security_group_ids = var.security_group_ids
    user_data = <<-EOF
   #!/bin/bash
   sudo yum update
   curl -fsSL https://rpm.nodesource.com/setup_16.x | sudo bash -
   sudo yum update
   sudo yum install -y nodejs
   node -v
   npm -v
   sudo npm install -g npm@latest
  EOF
  
  tags = {
    Name = var.instance_name
  }
  key_name = aws_key_pair.key_pair.key_name
}

resource "tls_private_key" "private_key" {
  algorithm = "RSA"
  rsa_bits  = 4096
}

resource "aws_key_pair" "key_pair" {
  key_name   = "${var.instance_name}-keypair"  # Name for the AWS Key Pair
  public_key = tls_private_key.private_key.public_key_openssh
}


resource "aws_eip" "demo-eip" {
  instance = aws_instance.instance-1.id
  vpc      = true
}
resource "aws_ebs_volume" "example" {
  availability_zone = data.aws_subnet.instance_subnet.availability_zone
  size             = var.ebs_size            # Adjust the size in GB as needed
  type             = "gp2"          # Adjust the volume type as needed
    tags = {
    Name = "${var.instance_name}-ebs"
  }
  
}


resource "aws_volume_attachment" "example" {
  device_name = "/dev/xvdf"       # Adjust the device name as needed
  volume_id   = aws_ebs_volume.example.id
  instance_id = aws_instance.instance-1.id
}

resource "local_file" "ssh_key" {
  filename = "${aws_key_pair.key_pair.key_name}.pem"
  content  = tls_private_key.private_key.private_key_pem
}
