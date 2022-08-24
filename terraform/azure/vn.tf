resource "azurerm_resource_group" "rgb" {
  name     = "example-resources"
  location = "Central US"
  tags = {
    yor_trace = "98c8e684-7115-4a0a-96ab-6d0cd0cc2b03"
  }
}

resource "azurerm_network_security_group" "nsg" {
  name                = "example-security-group"
  location            = azurerm_resource_group.rgb.location
  resource_group_name = azurerm_resource_group.rgb.name
  tags = {
    yor_trace = "5b6d86fa-5e27-47b5-b08c-cd68731d90f8"
  }
}

resource "azurerm_virtual_network" "vn1" {
  name                = "example-network-1"
  location            = azurerm_resource_group.rgb.location
  resource_group_name = azurerm_resource_group.rgb.name
  address_space       = ["10.1.0.0/16"]
  dns_servers         = ["10.1.0.4", "10.1.0.5"]

  subnet {
    name           = "subnet1"
    address_prefix = "10.1.1.0/24"
  }

  subnet {
    name           = "subnet2"
    address_prefix = "10.1.2.0/24"
    security_group = azurerm_network_security_group.nsg.id
  }

  tags = {
    environment = "Production"
    yor_trace   = "a264982c-a5df-4117-9e13-576250b2fa66"
  }
}

resource "azurerm_virtual_network" "vn2" {
  name                = "example-network-2"
  location            = azurerm_resource_group.rgb.location
  resource_group_name = azurerm_resource_group.rgb.name
  address_space       = ["10.2.0.0/16"]
  dns_servers         = ["10.2.0.4", "10.2.0.5"]

  tags = {
    environment = "Production"
    yor_trace   = "96674cca-1246-40ab-8058-c27c6304afd3"
  }
}


resource "azurerm_virtual_network" "vn3" {
  name                = "example-network-3"
  location            = azurerm_resource_group.rgb.location
  resource_group_name = azurerm_resource_group.rgb.name
  address_space       = ["10.3.0.0/16"]
  dns_servers         = ["10.3.0.4", "10.3.0.5"]

  subnet {
    name           = "subnet3"
    address_prefix = "10.3.3.0/24"
    security_group = azurerm_network_security_group.nsg.id
  }

  tags = {
    environment = "Production"
    yor_trace   = "a046dd00-7bb3-4494-b235-acf43cf79975"
  }
}

resource "azurerm_network_security_rule" "rule1" {
  name                        = "rule11"
  priority                    = 100
  direction                   = "Outbound"
  access                      = "Allow"
  protocol                    = "Tcp"
  source_port_range           = "*"
  destination_port_range      = "https"
  source_address_prefix       = "*"
  destination_address_prefix  = "*"
  resource_group_name         = azurerm_resource_group.rgb.name
  network_security_group_name = azurerm_network_security_group.nsg.name
}

resource "azurerm_network_security_rule" "rule2" {
  name                        = "rule12"
  priority                    = 100
  direction                   = "Outbound"
  access                      = "Deny"
  protocol                    = "Tcp"
  source_port_range           = "*"
  destination_port_range      = "https"
  source_address_prefix       = "*"
  destination_address_prefix  = "*"
  resource_group_name         = azurerm_resource_group.rgb.name
  network_security_group_name = azurerm_network_security_group.nsg.name
}

resource "azurerm_network_security_rule" "rule3" {
  name                        = "rule13"
  priority                    = 100
  direction                   = "Outbound"
  access                      = "Allow"
  protocol                    = "Tcp"
  source_port_range           = "*"
  destination_port_range      = "https"
  source_address_prefix       = "1.1.1.1/32"
  destination_address_prefix  = "2.2.2.2/32"
  resource_group_name         = azurerm_resource_group.rgb.name
  network_security_group_name = azurerm_network_security_group.nsg.name
}

