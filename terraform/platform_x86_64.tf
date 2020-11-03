resource "aws_instance" "infra-x86_64" {
  ami                    = data.aws_ami.x86_64.id
  instance_type          = var.instance_x86_64[var.mode]
  vpc_security_group_ids = [aws_security_group.instance.id]
  key_name               = "deployer-key"
  monitoring             = true
  count                  = var.create_x86_64 ? 1 : 0

  root_block_device {
    volume_size = 20
  }

  tags = {
    Name = "eessi-x86_64"
  }
}
