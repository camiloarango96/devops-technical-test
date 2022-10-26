#Creacion de de base de datos
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
  db_subnet_group_name  = aws_db_subnet_group.db_subnet_group.id
  vpc_security_group_ids  = [aws_security_group.rds_sg.id]

}


