resource "aws_db_instance" "default" {
  allocated_storage    = 10
  db_name              = var.db_name
  engine               = "postgres"
  engine_version       = "15.7"
  instance_class       = "db.t3.micro"
  username             = var.db_user
  password             = var.db_password
  vpc_security_group_ids  = [aws_security_group.rds_sg.id]
  db_subnet_group_name = aws_db_subnet_group.default.name
  publicly_accessible = false
  skip_final_snapshot  = true

  tags ={
    Name="fiction-hello-db"
  }
}
