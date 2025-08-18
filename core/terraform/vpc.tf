#custom VPN
resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
  enable_dns_support = true
  enable_dns_hostnames = true
  tags = { Name = "custom-vpc" }
}

#public1 subnet for the EC2
resource "aws_subnet" "public1" {
  vpc_id = aws_vpc.main.id
  cidr_block = "10.0.1.0/24"
  map_public_ip_on_launch = true
  availability_zone = "eu-west-2a"
  tags = { Name = "public1-subnet" }
}

#public2 subnet for the EC2
resource "aws_subnet" "public2" {
  vpc_id = aws_vpc.main.id
  cidr_block = "10.0.2.0/24"
  map_public_ip_on_launch = true
  availability_zone = "eu-west-2b"
  tags = { Name = "public2-subnet" }
}

#private1 subnet for the for core DB
resource "aws_subnet" "private1" {
  vpc_id = aws_vpc.main.id
  cidr_block = "10.0.3.0/24"
  map_public_ip_on_launch = false
  availability_zone = "eu-west-2a"
  tags = { Name = "private1-subnet" }
}

#private2 subnet for the for core DB
resource "aws_subnet" "private2" {
  vpc_id = aws_vpc.main.id
  cidr_block = "10.0.4.0/24"
  map_public_ip_on_launch = false
  availability_zone = "eu-west-2b"
  tags = { Name = "private2-subnet" }
}

#internet gateway to allow internet access to 
resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.main.id
  tags = { Name = "main-igw" }
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id
  }
}

resource "aws_vpc_dhcp_options" "default" {
  domain_name         = "ec2.internal"
  domain_name_servers = ["AmazonProvidedDNS"]
  
  tags = { Name = "default-dhcp-options" }
}

resource "aws_vpc_dhcp_options_association" "vpc" {
  vpc_id          = aws_vpc.main.id
  dhcp_options_id = aws_vpc_dhcp_options.default.id
}

resource "aws_route_table_association" "public1" {
  subnet_id = aws_subnet.public1.id
  route_table_id = aws_route_table.public.id
}

resource "aws_route_table_association" "public2" {
  subnet_id      = aws_subnet.public2.id
  route_table_id = aws_route_table.public.id
}

resource "aws_nat_gateway" "nat" {
  allocation_id = aws_eip.nat.id
  subnet_id     = aws_subnet.public1.id
}

resource "aws_eip" "nat" {
  domain = "vpc"
  tags = {
    Name = "nat-eip"
  }
}

resource "aws_route_table" "private" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.nat.id
  }
}

resource "aws_route_table_association" "private1" {
  subnet_id      = aws_subnet.private1.id
  route_table_id = aws_route_table.private.id
}

resource "aws_route_table_association" "private2" {
  subnet_id      = aws_subnet.private2.id
  route_table_id = aws_route_table.private.id
}


resource "aws_security_group" "allow_internet_traffic" {
  name="allow-internet-traffic"
  description = "allow inbound access to the ec2"
  vpc_id      = aws_vpc.main.id

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


resource "aws_security_group" "rds_sg" {
  name="allow-rds-traffic"
  description = "allow inbound access to rds"
  vpc_id      = aws_vpc.main.id

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

resource "aws_db_subnet_group" "private" {
  name       = "my-db-subnet-group-private"
  subnet_ids = [aws_subnet.private1.id, aws_subnet.private2.id] 

  tags = {
    Name = "My db Subnet Group"
  }
}


resource "aws_security_group" "rds_sg_olap" {
  name="allow-rds-traffic-olap"
  description = "allow exterenal access to rds"
  vpc_id      = aws_vpc.main.id

  tags = {
    Name = "rds_sg-olap"
  }
}

resource "aws_db_subnet_group" "public" {
  name       = "my-db-subnet-group"
  subnet_ids = [aws_subnet.public1.id, aws_subnet.public2.id] 

  tags = {
    Name = "My db Subnet Group"
  }
}


resource "aws_security_group_rule" "allow_lambda_ingress" {
  type                     = "ingress"
  from_port                = 0
  to_port                  = 0
  protocol                 = "-1"
  security_group_id        = aws_security_group.rds_sg.id
  source_security_group_id = data.terraform_remote_state.etl.outputs.lambda_sg_id
}