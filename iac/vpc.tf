resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"

  # enable_dns_support = true
  # enable_dns_hostnames = true

  tags = {
    Name = "main"
  }
}


resource "aws_vpc" "rds" {
  cidr_block = "10.0.0.0/16"

  enable_dns_support = true
  enable_dns_hostnames = true

  tags = {
    Name = "rds"
  }
}

resource "aws_subnet" "rds-subnet-a" {
  vpc_id            = aws_vpc.rds.id
  cidr_block        = "10.0.0.0/19"
  availability_zone = "us-east-1a"
}

resource "aws_subnet" "rds-subnet-b" {
  vpc_id            = aws_vpc.rds.id
  cidr_block        = "10.0.32.0/19"
  availability_zone = "us-east-1b"
}

