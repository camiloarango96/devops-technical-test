#Credenciales con las que se creara la base de datos
#Estas son inyectadas por secrets de github
variable "db_user" {
    type        = string
    sensitive   = true
}

variable "db_password" {
    type        = string
    sensitive   = true
}

