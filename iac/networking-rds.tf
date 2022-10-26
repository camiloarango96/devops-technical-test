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
  cidr_block        = "10.0.32.0/19"
  availability_zone = "us-east-1a"
}

resource "aws_subnet" "rds-subnet-b" {
  vpc_id            = aws_vpc.rds.id
  cidr_block        = "10.0.64.0/19"
  availability_zone = "us-east-1b"
}

resource "aws_db_subnet_group" "db_subnet_group" {
  name          = "db_subnet_group"
  subnet_ids    = [aws_subnet.rds-subnet-a.id, aws_subnet.rds-subnet-b.id]

  tags = {
    Name = "Grupo de subredes para la db"
  }
}

resource "aws_security_group" "rds_sg" {
  name = "grupo de seguridad para db postgres"
  vpc_id      = aws_vpc.rds.id
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
  
}


resource "aws_internet_gateway" "rds-igw" {
  vpc_id = aws_vpc.rds.id

  tags = {
    Name = "igw"
  }
}

resource "aws_route_table" "rds-public" {
  vpc_id = aws_vpc.rds.id

  route = [
    {
      cidr_block                 = "0.0.0.0/0"
      gateway_id                 = aws_internet_gateway.rds-igw.id
      nat_gateway_id             = ""
      carrier_gateway_id         = ""
      destination_prefix_list_id = ""
      egress_only_gateway_id     = ""
      instance_id                = ""
      ipv6_cidr_block            = ""
      local_gateway_id           = ""
      network_interface_id       = ""
      transit_gateway_id         = ""
      vpc_endpoint_id            = ""
      vpc_peering_connection_id  = ""
    },
  ]

  tags = {
    Name = "public"
  }
}

resource "aws_route_table_association" "rds-subnet-a" {
  subnet_id      = aws_subnet.rds-subnet-a.id
  route_table_id = aws_route_table.rds-public.id
}

resource "aws_route_table_association" "rds-subnet-b" {
  subnet_id      = aws_subnet.rds-subnet-b.id
  route_table_id = aws_route_table.rds-public.id
}