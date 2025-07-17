
resource "aws_security_group" "allow_internet_traffic" {
  name="allow-internet-traffic"
  description = "allow inbound access to the ec2"
  vpc_id      = data.aws_vpc.default.id

  tags = {
    Name = "ec2_sg"
  }
}

resource "aws_vpc_security_group_ingress_rule" "allow_http_inggress" {
  security_group_id = aws_security_group.allow_internet_traffic.id
  
  cidr_ipv4   = "0.0.0.0/0"
  ip_protocol = "tcp"
  from_port = 8000
  to_port = 8000

}

resource "aws_vpc_security_group_ingress_rule" "allow_ssh_ingress" {
  security_group_id = aws_security_group.allow_internet_traffic.id

  cidr_ipv4   = "0.0.0.0/0"
  ip_protocol = "tcp"
  from_port = 22
  to_port = 22

}

resource "aws_vpc_security_group_egress_rule" "allow_internet_traffic_engress" {
  security_group_id = aws_security_group.allow_internet_traffic.id

  cidr_ipv4   = "0.0.0.0/0"
  ip_protocol = "-1"
}


data "aws_vpc" "default" {
  tags = {
    Name = "Default VPC"
  }
}

data "aws_subnets" "default" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
}

resource "aws_db_subnet_group" "default" {
  name       = "fiction-db-subnet-group"
  subnet_ids = data.aws_subnets.default.ids

  tags = {
    Name = "fiction-db-subnet-group"
  }
}


resource "aws_security_group" "rds_sg" {
  name="allow-rds-traffic"
  description = "allow inbound access to rds"
  vpc_id      = data.aws_vpc.default.id

  tags = {
    Name = "rds_sg"
  }
}

resource "aws_security_group_rule" "allow_ec2_to_rds" {
  type                     = "ingress"
  from_port                = 5432
  to_port                  = 5432
  protocol                 = "tcp"
  security_group_id        = aws_security_group.rds_sg.id
  source_security_group_id = aws_security_group.allow_internet_traffic.id
}

resource "aws_vpc_security_group_egress_rule" "allow_rds_engress" {
  security_group_id = aws_security_group.rds_sg.id

  cidr_ipv4   = "0.0.0.0/0"
  ip_protocol = "-1"
}

