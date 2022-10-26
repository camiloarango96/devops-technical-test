resource "aws_db_subnet_group" "db_subnet_group" {
  name          = "db_subnet_group"
  subnet_ids    = [aws_subnet.rds-subnet.id]

  tags = {
    Name = "Grupo de subredes para la db"
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
  
}

resource "aws_db_instance" "postgres" {
  allocated_storage     = 10
  #db_name               = var.db_name
  engine                = "postgres"
  instance_class        = "db.t3.micro"
  username              = var.db_user
  password              = var.db_password
  skip_final_snapshot   = true
  port                  = 5432
  publicly_accessible   = true
  db_subnet_group_name = aws_db_subnet_group.db_subnet_group.id

}


