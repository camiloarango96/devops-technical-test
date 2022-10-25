resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"

  # enable_dns_support = true
  # enable_dns_hostnames = true

  tags = {
    Name = "main"
  }
}

resource "aws_security_group" "rds_sg" {

  ingress = {
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
  
}

resource "aws_vpc" "rds" {
  cidr_block = "10.0.0.0/16"

  enable_dns_support = true
  enable_dns_hostnames = true
  default_security_group_id = aws_security_group.rds_sg.id

  tags = {
    Name = "main"
  }
}