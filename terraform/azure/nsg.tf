resource "azurerm_resource_group" "rg" {
  name     = "example-resources"
  location = "Canada Central"
}

# resource "azurerm_virtual_network" "vn1" {
#   name                = "example-network"
#   address_space       = ["10.1.0.0/16"]
#   location            = azurerm_resource_group.rg.location
#   resource_group_name = azurerm_resource_group.rg.name
# }

# resource "azurerm_subnet" "subnet-vn1-good" {
#   name                 = "subnet-vn1-good"
#   resource_group_name  = azurerm_resource_group.rg.name
#   virtual_network_name = azurerm_virtual_network.vn.name
#   address_prefixes     = ["10.1.1.0/24"]
# }

# resource "azurerm_subnet_network_security_group_association" "subnet-vn1-assoc" {
#   subnet_id                 = azurerm_subnet.subnet-vn1-good.id
#   network_security_group_id = azurerm_network_security_group.nsg.id
# }

# # This subnet 
# resource "azurerm_subnet" "subnet-vn1-bad" {
#   name                 = "frontend"
#   resource_group_name  = azurerm_resource_group.rg.name
#   virtual_network_name = azurerm_virtual_network.vn.name
#   address_prefixes     = ["10.1.2.0/24"]
# }

resource "azurerm_virtual_network" "vn2" {
  name                = "example-network"
  address_space       = ["10.2.0.0/16"]
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name

  subnet {
    name           = "subnet-vn2-bad"
    address_prefix = "10.2.1.0/24"
    security_group = azurerm_network_security_group.nsg.id
  }

  subnet {
    name           = "subnet-vn2-good"
    address_prefix = "10.2.2.0/24"
    security_group = azurerm_network_security_group.nsg.id
  }

  tags = {
    environment = "Production"
  }
}


resource "azurerm_network_security_group" "nsg" {
  name                = "example-nsg"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name

  security_rule {
    name                       = "test123"
    priority                   = 100
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "*"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }
}



# resource "azurerm_subnet" "notsobad" {
#   name                 = "frontend"
#   resource_group_name  = azurerm_resource_group.rg.name
#   virtual_network_name = azurerm_virtual_network.vn.name
#   address_prefixes     = ["10.1.3.0/24"]
# }

# resource "azurerm_subnet_network_security_group_association" "nsgb" {
#   subnet_id                 = azurerm_subnet.notsobad.id
#   network_security_group_id = azurerm_network_security_group.nsg.id
# }