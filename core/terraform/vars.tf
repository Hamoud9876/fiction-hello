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
    description = "Password for the master user for RDS DB"
    type = string
    default = "password"
}

variable "db_name_olap" {
    description = "Name of the RDS DB"
    type = string
    default = "db_name"
}

variable "db_user_olap"{
    description = "Master user of the RDS DB"
    type = string
    default = "user"
}

variable "db_password_olap"{
    description = "Password for the master user for RDS DB"
    type = string
    default = "password"
}

variable "region" {
    type = string
    default= "eu-west-2"
}