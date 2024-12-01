module "load_balancer" {
  source              = "Azure/loadbalancer/azurerm"
  version             = "x.x.x" # Replace with the latest version
  resource_group_name = "your-resource-group"
  location            = "eastus"
  frontend_ip_configuration = {
    name                 = "LoadBalancerFrontend"
    subnet_id            = "/subscriptions/xxxx/resourceGroups/xxxx/providers/Microsoft.Network/virtualNetworks/xxxx/subnets/xxxx"
    private_ip_address   = "10.0.0.4"
  }
}

#Using Azure Load Balancer