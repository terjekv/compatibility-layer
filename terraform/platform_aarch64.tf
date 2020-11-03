resource "aws_instance" "infra-aarch64" {
  ami                    = data.aws_ami.aarch64.id
  instance_type          = var.instance_aarch64[var.mode]
  vpc_security_group_ids = [aws_security_group.instance.id]
  key_name               = "deployer-key"
  monitoring             = true
  count                  = var.create_aarch64 ? 1 : 0

  root_block_device {
    volume_size = 20
  }

  tags = {
    Name = "eessi-aarch64"
  }
}
