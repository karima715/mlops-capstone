terraform {
  required_version = ">= 1.6.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# -------- Variables (easy to tweak) --------
variable "aws_region" {
  description = "AWS region to deploy into"
  type        = string
  default     = "ap-south-1"
}

variable "instance_type" {
  description = "EC2 instance size"
  type        = string
  default     = "t3.micro"
}

variable "docker_image" {
  description = "Docker image to run"
  type        = string
  default     = "karimaji143/mlops-capstone:latest"
}

variable "open_cidr" {
  description = "CIDR allowed to reach the API (0.0.0.0/0 = public)"
  type        = string
  default     = "0.0.0.0/0"
}

# -------- Provider --------
provider "aws" {
  region = var.aws_region
}

# -------- Networking (Security Group) --------
resource "aws_security_group" "api_sg" {
  name        = "mlops-capstone-sg"
  description = "Allow SSH (22, optional) and API (8000)"

  # SSH (optional; leave if you might need to debug)
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.open_cidr]
  }

  # FastAPI
  ingress {
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = [var.open_cidr]
  }

  # Outbound (anywhere)
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# -------- Find latest Ubuntu 22.04 LTS --------
data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"] # Canonical

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }
}

# -------- EC2 Instance --------
resource "aws_instance" "api" {
  ami                         = data.aws_ami.ubuntu.id
  instance_type               = var.instance_type
  vpc_security_group_ids      = [aws_security_group.api_sg.id]
  associate_public_ip_address = true

  # Optional: if you created an EC2 Key Pair and want SSH, set key_name here
  # key_name = "your-ec2-keypair-name"

  user_data = <<-EOF
              #!/bin/bash
              set -e

              # Update and install Docker
              apt-get update -y
              apt-get install -y docker.io
              systemctl enable docker
              systemctl start docker
              usermod -aG docker ubuntu || true

              # Pull your public image and run the API
              IMAGE="${var.docker_image}"
              docker pull "docker.io/${var.docker_image}"

              # Stop previous container if exists
              if [ "$(docker ps -aq -f name=mlops-capstone)" ]; then
                docker rm -f mlops-capstone || true
              fi

              # Run container on port 8000, restart if VM reboots
              docker run -d --restart unless-stopped \
                --name mlops-capstone \
                -p 8000:8000 \
                "docker.io/${var.docker_image}"
              EOF

  tags = { Name = "mlops-capstone-api" }
}

# -------- Useful Outputs --------
output "public_ip" {
  value       = aws_instance.api.public_ip
  description = "Public IP of the API server"
}

output "api_url" {
  value       = "http://${aws_instance.api.public_ip}:8000"
  description = "HTTP URL to reach FastAPI root"
}
