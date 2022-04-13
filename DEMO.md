# Demo: PCCS Custom Build Policy via API

## Agenda
1. Overview of demo setup
2. Listing existing Policies via the API
3. Writing / updating a custom policy
4. Using checkov to test locally 
5. Publishing a new Policy via the API
6. Viewing policy violations in the PCCS UI
7. Updating existing Policies via the API
8. Deleting existing Policies via the API


## 1. Overview of Demo Setup 
```
.
├── DEMO.md
├── README.md
├── pccs
│   ├── actions
...
│   │   └── policy_actions.py
│   ├── common
...
│   │   ├── auth.py
│   │   └── utils.py
│   └── main.py
├── policies
│   └── azure
│       ├── CUST_LOCATIONS.yml
│       ├── CUST_NSG_ASSOC.yml
│       ├── DEMO_NSG_POLICY.yml
└── terraform
    └── azure
        ├── nsg.tf
        ├── rg.tf
        ├── route.tf
        └── vn.tf
```
  
    
Our new custom policy for the demo: **`policies/azure/`**

Sample Terraform IaC folder: **`terraform/azure/`**

Sample Terraform IaC repo: **`https://github.com/tplisson/tom-github-tf-azure`**

Python script to list / publish / update / delete custom policies via the API:
**`https://github.com/kartikp10/pccs-policy-playground`**  

```commandline
$ python pccs/main.py -h
usage: Manage PCCS policies [-h] [--auth AUTH] [--list] [--publish PUBLISH]
                            [--delete DELETE] [--update UPDATE] [--verbose]
                            [--policy-id POLICY_ID]

optional arguments:
  -h, --help            show this help message and exit
  --auth AUTH           String with credentials and API endpoint -
                        "https://api.prismacloud.io::<your-access-key>::<your-
                        secret-key>"
  --list, -l            List custom policies
  --publish PUBLISH, -p PUBLISH
                        Publish policy from file
  --delete DELETE, -d DELETE
                        Delete policy by ID
  --update UPDATE, -u UPDATE
                        Update policy by ID from file
  --verbose, -v         Print verbose response
  --policy-id POLICY_ID, -id POLICY_ID
                        Get policy by ID
```


## 2. Listing existing Policies via the API

Listing existing policies
```commandline
python pccs/main.py --list
python pccs/main.py -l 
```
Getting details for all existing policies
```commandline
python pccs/main.py -l -v
```

Getting details about an existing policies
```commandline
python pccs/main.py -id <Policy_ID>
```

## 3. Writing / updating a custom policy

Writing / updating a policy
`policies/azure/DEMO_NSG_POLICY.yaml`

```yaml
---
metadata:
  name: "DEMO-NSG: Ensure subnet is associated with NSG"  
  #id: "DEMO_NSG_POLICY"
  guidelines: |
    Every subnet should be associated with NSG for controlling access to 
    resources within the subnet.
  category: "networking"
  severity: "high"
scope:
  provider: "azure" 
definition:
  and:
  - cond_type: "connection"
    resource_types:
    - "azurerm_subnet_network_security_group_association"
    connected_resource_types: 
    - "azurerm_subnet"
    - "azurerm_network_security_group"
    operator: "exists"
  - cond_type: "filter"
    attribute: "resource_type"
    value:
    - "azurerm_subnet"
    operator: "within"
```

Sample Terraform IaC file to be scanned
`terraform/azure/nsg.tf`  


## 4. Using checkov to test locally 
```commandline
export PC_ACCESS_KEY=<KEY>
export PC_SECRET_KEY=<SECRET>
export PRISMA_API_URL=https://api2.prismacloud.io
```

```commandline
checkov -h
```

```commandline
checkov -f <tf_file> -c <policy_id> —external-checks-dir <path-to-external-yaml-policies>
checkov -d <tf_directory> -c <policy_id> —external-checks-dir <path-to-external-yaml-policies>
```

Scanning `nsg.tf` file for new policy
```commandline
checkov -f terraform/azure/nsg.tf -c DEMO_NSG_POLICY.yaml --external-checks-dir policies/azure/
```

Scanning entire directory for one policy
```
checkov -d terraform/azure/ --external-checks-dir policies/azure/ -c DEMO_NSG_POLICY.yaml
```

Scanning entire directory for all policies
```
checkov -d terraform/azure/ --external-checks-dir policies/azure/
```


## 5. Publishing a new Policy via the API
Publishing our new policy
```commandline
python pccs/main.py --publish <Policy_ID>
python pccs/main.py -p <Policy_ID>
```
```commandline
python pccs/main.py -p policies/azure/DEMO_NSG_POLICY.yml 
```

> 💡 *Note: Before publishing your custom policy, make sure to remove any policy ID as these are automatically assigned by Prisma Cloud Code Security*

## 6. Viewing policy violations in the PCCS UI

Prisma Cloud Code Security
https://app2.prismacloud.io/projects/projects?types=Errors&repository=tplisson%2Ftom-github-tf-azure&branch=main



GitHub repositories
https://github.com/tplisson/pccs-policy-playground/terraform/azure/  
https://github.com/tplisson/tom-github-tf-azure/terraform/azure/  

- Create a pull request in GitHub
- View Prisma Cloud checks in GitHub
- Open Prisma Cloud console to view more details

## 7. API: Updating an existing Policy (by ID)
Updating an existing Policy using its ID
```commandline
python pccs/main.py -u <Policy_ID>
python pccs/main.py --update <Policy_ID>
```
Verifying
```commandline
python pccs/main.py -id <Policy_ID>
```

## 8. API: Deleting an existing Policy (by ID)
Deleting an existing Policy using its ID
```commandline
python pccs/main.py -d <Policy_ID>
python pccs/main.py --delete <Policy_ID>
```
Verifying
```commandline
python pccs/main.py -id <Policy_ID>
python pccs/main.py --list
```

---
## Links & references

#### GitHub repositories
https://github.com/tplisson/pccs-policy-playground  
https://github.com/tplisson/tom-github-tf-azure  

#### Prisma Cloud Code Security
https://app2.prismacloud.io/projects/projects?types=Errors&repository=tplisson%2Ftom-github-tf-azure&branch=main  

#### Bridgecrew Standalone
https://www.bridgecrew.cloud/policies/create  

#### Bridgecrew Docs
Bridgecrew custom polcies
https://docs.bridgecrew.io/docs/yaml-format-for-custom-policies#policy-definition-component---specification  

#### Bridgecrew API
Save new policy
https://docs.bridgecrew.io/reference/savepolicy  

#### Checkov
https://www.checkov.io/

Checkov custom polcies  
https://github.com/bridgecrewio/checkov/tree/master/docs/3.Custom%20Policies

#### Terraform Provider
Azure Terraform Provider
https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs

