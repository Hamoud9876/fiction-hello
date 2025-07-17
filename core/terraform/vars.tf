variable "db_name" {
    description = "Name of the RDS DB"
    type = string
    default = "db_name"
}

variable "db_user"{
    description = "Master user of the RDS DB"
    type = string
    default = "user"
}

variable "db_password"{
    description = "Passeord for the master user for RDS DB"
    type = string
    default = "password"
}

variable "region" {
    type = string
    default= "eu-west-2"
}