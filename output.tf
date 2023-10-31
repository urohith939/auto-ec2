output "ec2_instance_id" {
  value = aws_instance.instance-1.id
}
output "ec2_instance_public_ip" {
  value = aws_instance.instance-1.public_ip
}
output "ssh_key_file_name" {
  value = local_file.ssh_key.filename
}
output "elastic_ip" {
  value = aws_eip.demo-eip.public_ip
}

output "ssh_key_file_name" {
  value = local_file.ssh_key.filename
}

