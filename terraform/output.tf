output "public_dns_x86_64" {
  value       = aws_instance.infra-x86_64.*.public_dns
}

output "public_dns_aarch64" {
  value       = aws_instance.infra-aarch64.*.public_dns
}

