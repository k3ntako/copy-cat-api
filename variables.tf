variable "RDS_USERNAME" {
  description = "Database administrator username"
  type        = string
  sensitive   = true
}

variable "RDS_PASSWORD" {
  description = "Database administrator password"
  type        = string
  sensitive   = true
}

variable "RDS_PORT" {
  description = "Database administrator username"
  type        = number
  sensitive   = true
}

variable "RDS_DB_NAME" {
  description = "Database administrator password"
  type        = string
  sensitive   = true
}