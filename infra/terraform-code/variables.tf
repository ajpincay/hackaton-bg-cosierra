variable "solutionName" {
  type        = string
  description = "Use to add resources to a group"
  default     = "Hackaton-BG-Cosierra"
}

variable "env" {
  type    = string
  default = "PROD"
}

variable "db-username" {
  type      = string
  default   = "dbadmin"
  sensitive = true
}

variable "db-password" {
  type      = string
  default   = "P4$$w0rD"
  sensitive = true
}