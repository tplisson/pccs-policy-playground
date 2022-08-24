resource "azurerm_resource_group" "rga" {
  name     = "example-resources"
  location = "Canada East"
  tags = {
    yor_trace = "cd1a42ee-3bd1-4112-bc5d-5e0c93ce9f3d"
  }
}

resource "azurerm_route_table" "rt" {
  name                = "acceptanceTestRouteTable1"
  location            = azurerm_resource_group.rga.location
  resource_group_name = azurerm_resource_group.rga.name
  tags = {
    yor_trace = "ca8ae044-bd37-43a5-96f6-b233b8c56a4d"
  }
}

resource "azurerm_route" "route1" {
  name                = "route1"
  resource_group_name = azurerm_resource_group.rga.name
  route_table_name    = azurerm_route_table.rt.name
  address_prefix      = "0.0.0.0/0"
  next_hop_type       = "vnetlocal"
}

resource "azurerm_route" "route2" {
  name                = "route2"
  resource_group_name = azurerm_resource_group.rga.name
  route_table_name    = azurerm_route_table.rt.name
  address_prefix      = "10.1.0.0/16"
  next_hop_type       = "Internet"
}

resource "azurerm_route" "route3" {
  name                = "route3"
  resource_group_name = azurerm_resource_group.rga.name
  route_table_name    = azurerm_route_table.rt.name
  address_prefix      = "0.0.0.0/0"
  next_hop_type       = "Internet"
}