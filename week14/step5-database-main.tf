module "sql_database" {
  source              = "Azure/terraform-azurerm-sql/azurerm"
  version             = "x.x.x" # Replace with the latest version
  resource_group_name = "The name of your resource group"
  location            = "eastus"
  sql_server_name     = "The name of your SQL server"
  sql_administrator_login          = "adminuser"
  sql_administrator_login_password = "Password123!"
}

#Using Azure SQL Module