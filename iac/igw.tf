#Creacion de un internet gateway, que sera necesario para la conexion del cluster con internet

resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "igw"
  }
}