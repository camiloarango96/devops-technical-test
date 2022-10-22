#EKS requiere de 4 subredes, 2 publicas y 2 privadas
#Tienen que haber en varias AZ
resource "aws_subnet" "private-us-east-1a" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.0.0/19"
  availability_zone = "us-east-1a"

  tags = {
    "Name"                            = "private_subnet_us-east-1a" #Solo es un nombre, no es necesario
    "kubernetes.io/role/internal-elb" = 1 #Se usa para que k8s descubra las subredes en donde se usan elb privados
    "kubernetes.io/cluster/flask-cluster"      = "owned"
  }
}

resource "aws_subnet" "private-us-east-1b" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.32.0/19"
  availability_zone = "us-east-1b"

  tags = {
    "Name"                                = "private_subnet_us-east-1b" #Solo es un nombre, no es necesario
    "kubernetes.io/role/internal-elb"     = 1 #Se usa para que k8s descubra las subredes en donde se usan elb privados
    "kubernetes.io/cluster/flask-cluster" = "owned"
  }
}

resource "aws_subnet" "public-us-east-1a" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.64.0/19"
  availability_zone       = "us-east-1a"
  map_public_ip_on_launch = true

  tags = {
    "Name"                                = "public_subnet_us-east-1a" #Solo es un nombre, no es necesario
    "kubernetes.io/role/elb"              = 1 #Indica a k8s crear un elb publico
    "kubernetes.io/cluster/flask-cluster" = "owned"
  }
}

resource "aws_subnet" "public-us-east-1b" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.96.0/19"
  availability_zone       = "us-east-1b"
  map_public_ip_on_launch = true

  tags = {
    "Name"                                = "public_subnet_us-east-1b" #Solo es un nombre, no es necesario
    "kubernetes.io/role/elb"              = 1 #Indica a k8s crear un elb publico
    "kubernetes.io/cluster/flask-cluster" = "owned"
  }
}
