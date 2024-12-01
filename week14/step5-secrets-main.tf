data "azurerm_key_vault_secret" "example" {
  name         = "secret example"
  key_vault_id = "/subscriptions/xxxx/resourceGroups/xxxx/providers/Microsoft.KeyVault/vaults/your-vault-name"
}

output "secret_value" {
  value = data.azurerm_key_vault_secret.example.value
}

#Using azurerm_key_vault_secret
