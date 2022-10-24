resource "aws_db_subnet_group" "db_subnet_group" {
  name          = "db_subnet_group"
  subnet_ids    = ["subnet-0d4c3635d34fab244", "subnet-06d0fd201c19e248f"]

  tags = {
    Name = "Grupo de subredes para la db"
  }
}

resource "aws_db_instance" "postgres" {
  allocated_storage     = 10
  #db_name               = "clients"
  engine                = "postgres"
  instance_class        = "db.t3.micro"
  username              = var.db_user
  password              = var.db_password
  skip_final_snapshot   = true
  publicly_accessible   = true

  db_subnet_group_name  = aws_db_subnet_group.db_subnet_group.name
}