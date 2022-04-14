

resource "azurerm_resource_group" "rg" {
  name     = "example-resources"
  location = "Canada Central"
}

# This NSG is NOT associated with a network watchter flow log
resource "azurerm_network_security_group" "bad" {
  name                = "good-nsg-with-watcher-flow-log"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
}

# This NSG is associated with a network watchter flow log
resource "azurerm_network_security_group" "good" {
  name                = "good-nsg-with-watcher-flow-log"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
}

# This Resource Group is located in an approved location
resource "azurerm_network_watcher_flow_log" "good" {
  network_watcher_name = azurerm_network_watcher.watcher.name
  resource_group_name  = azurerm_resource_group.rg.name
  name                 = "good-nsg-watcher-flow-log"

  network_security_group_id = azurerm_network_security_group.good.id
  storage_account_id        = azurerm_storage_account.sa.id
  enabled                   = true

  retention_policy {
    enabled = true
    days    = 7
  }

  traffic_analytics {
    enabled               = true
    workspace_id          = azurerm_log_analytics_workspace.test.workspace_id
    workspace_region      = azurerm_log_analytics_workspace.test.location
    workspace_resource_id = azurerm_log_analytics_workspace.test.id
    interval_in_minutes   = 10
  }
}

resource "azurerm_network_watcher" "watcher" {
  name                = "network-watcher-flow-log"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
}

resource "azurerm_storage_account" "sa" {
  name                = "storage-account"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location

  account_tier              = "Standard"
  account_kind              = "StorageV2"
  account_replication_type  = "LRS"
  enable_https_traffic_only = true
}

resource "azurerm_log_analytics_workspace" "ws" {
  name                = "analytics-workspace"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  sku                 = "PerGB2018"
}

