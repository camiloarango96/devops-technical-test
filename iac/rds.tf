resource "aws_db_subnet_group" "db_subnet_group" {
  name          = "db_subnet_group"
  subnet_ids    = [aws_subnet.private-us-east-1a.id, aws_subnet.private-us-east-1b.id]

  tags = {
    Name = "Grupo de subredes para la db"
  }
}

resource "aws_db_instance" "postgres" {
  allocated_storage     = 10
  #db_name               = var.db_name
  engine                = "postgresql"
  instance_class        = "db.t3.micro"
  username              = var.db_user
  password              = var.db_password
  skip_final_snapshot   = true

  db_subnet_group_name  = aws_db_subnet_group.db_subnet_group.name
}


