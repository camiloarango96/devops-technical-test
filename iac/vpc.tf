resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"

  # enable_dns_support = true
  # enable_dns_hostnames = true

  tags = {
    Name = "main"
  }
}

resource "aws_security_group" "rds_sg" {
  name = "grupo de seguridad para db postgres"
  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  vpc_id      = aws_vpc.rds.id
  
}

resource "aws_vpc" "rds" {
  cidr_block = "10.0.0.0/16"

  enable_dns_support = true
  enable_dns_hostnames = true

  tags = {
    Name = "rds"
  }
}

resource "aws_subnet" "rds-subnet" {
  vpc_id            = aws_vpc.rds.id
  cidr_block        = "10.0.0.0/19"
  availability_zone = "us-east-1a"
}