#security group that allows lemabda to access the private RDS
resource "aws_security_group" "lambda_sg" {
  name="lambda-sg"
  description = "giving access to private rds"
  vpc_id      = data.terraform_remote_state.backend.outputs.vpc_id

  tags = {
    Name = "private_access"
  }
}

resource "aws_security_group_rule" "lambda_to_rds_egress" {
  type              = "egress"
  from_port         = 5432
  to_port           = 5432
  protocol          = "tcp"
  security_group_id = aws_security_group.lambda_sg.id
  cidr_blocks       = [data.terraform_remote_state.backend.outputs.private1_subnet_cidr,
                       data.terraform_remote_state.backend.outputs.private2_subnet_cidr]
}

resource "aws_security_group_rule" "lambda_sg_egress_all" {
  type                     = "egress"
  from_port                = 0
  to_port                  = 0
  protocol                 = "-1"
  security_group_id        = aws_security_group.lambda_sg.id
  cidr_blocks              = ["0.0.0.0/0"]
}