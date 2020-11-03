variable "aws_region" {
  default = "eu-west-1"
}

variable "mode" {
  type = string

  validation {
    condition = var.mode == "test" || var.mode == "build"
    error_message = "Set TF_VAR_mode to either 'test' or 'build'."
  }
}

variable "ssh" {
  type = map

  default = {
    port = 22
    user = "ec2-user"
  }
}

variable "keys" {
  type = map

  default = {
    private = "~/.ssh/id_rsa.terraform"
    public  = "~/.ssh/id_rsa.terraform.pub"
  }
}

variable "create_x86_64" {
  default = false
}

variable "create_aarch64" {
  default = false
}

variable "instance_aarch64" {
  type = map

  default = {
    test = "t4g.micro"
    build = "c6g.xlarge"
#    prod = "c6g.4xlarge"
  }
}

variable "instance_x86_64" {
  type = map

  default = {
    test = "t2.micro"
    build = "c5.xlarge"
#    prod = "c5.4xlarge"
  }
}
