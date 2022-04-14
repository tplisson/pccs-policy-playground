# This Resource Group is associated with a "CanNotDelete" lock
resource "azurerm_resource_group" "good" {
  name     = "resource-group-locked-cannot-delete"
  location = "Canada Central"
}

resource "azurerm_management_lock" "good" {
  name       = "resource-group-level"
  scope      = azurerm_resource_group.good.id
  lock_level = "CanNotDelete"
  notes      = "This Resource Group is cannot be deleted"
}

# This Resource Group has no lock associated at all
resource "azurerm_resource_group" "bad" {
  name     = "resource-group-no-lock"
  location = "Canada Central"
}

# This Resource Group is associated with a "ReadOnly" lock
resource "azurerm_resource_group" "notsollbad" {
  name     = "resource-group-locked-read-only"
  location = "Canada Central"
}

resource "azurerm_management_lock" "notsobad" {
  name       = "resource-group-level"
  scope      = azurerm_resource_group.notsobad.id
  lock_level = "ReadOnly"
  notes      = "This Resource Group is Read-Only"
}