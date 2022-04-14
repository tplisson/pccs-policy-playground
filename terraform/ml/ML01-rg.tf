# This Resource Group is located in an approved location
resource "azurerm_resource_group" "good" {
  name     = "resource-group-in-good-location"
  location = "Canada Central"
}

# This Resource Group is not located in an approved location
resource "azurerm_resource_group" "bad" {
  name     = "resource-group-in-bad-location"
  location = "West Europe" 
}
