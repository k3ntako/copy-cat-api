output "rds_hostname" {
  value = aws_db_instance.copy_cat_prod.address
}