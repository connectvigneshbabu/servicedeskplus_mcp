# CMDB Features - ServiceDesk Plus MCP Server

## 🎯 **CMDB Overview**

The MCP server has been extended to fully support CMDB (Configuration Management Database) functions in ServiceDesk Plus, including:

## 📋 **Supported CMDB Modules**

### 1. **Configuration Items (CIs) Management**
- ✅ `list_configuration_items` - Get list of CIs with filters
- ✅ `get_configuration_item` - Get CI details
- ✅ `create_configuration_item` - Create a new CI
- ✅ `update_configuration_item` - Update a CI
- ✅ `delete_configuration_item` - Delete a CI
- ✅ `get_ci_types` - Get list of CI types
- ✅ `get_ci_relationships` - Get CI relationships

**Usage Examples:**
```
"Create a new Configuration Item for web server named 'WEB-SRV-001', type 'server', status 'active'"
"Get list of 20 Configuration Items of type 'network_device' with status 'active'"
"Update CI WEB-SRV-001 with status 'under_maintenance'"
```

### 2. **Asset Management**
- ✅ `list_assets` - Get list of assets with filters
- ✅ `get_asset` - Get asset details
- ✅ `create_asset` - Create a new asset
- ✅ `update_asset` - Update an asset
- ✅ `delete_asset` - Delete an asset
- ✅ `get_asset_types` - Get list of asset types
- ✅ `get_asset_categories` - Get asset categories
- ✅ `get_asset_locations` - Get asset locations
- ✅ `get_asset_models` - Get asset models
- ✅ `get_asset_vendors` - Get asset vendors

**Usage Examples:**
```
"Create new asset named 'LAPTOP-001', type 'laptop', status 'in_use', assigned to 'john.doe@company.com'"
"Get list of assets with status 'under_maintenance' and location 'IT Department'"
"Update asset LAPTOP-001 with status 'retired'"
```

### 3. **Software License Management**
- ✅ `list_software_licenses` - Get list of software licenses
- ✅ `get_software_license` - Get license details
- ✅ `create_software_license` - Create a new license
- ✅ `update_software_license` - Update a license
- ✅ `get_software_products` - Get list of software products
- ✅ `get_license_types` - Get license types

**Usage Examples:**
```
"Create new software license for 'Microsoft Office 365' with 100 licenses, vendor 'Microsoft'"
"Get list of licenses from vendor 'Adobe' for product 'Photoshop'"
"Update Office 365 license with new license count of 150"
```

### 4. **Contract Management**
- ✅ `list_contracts` - Get list of contracts
- ✅ `get_contract` - Get contract details
- ✅ `create_contract` - Create a new contract
- ✅ `update_contract` - Update a contract
- ✅ `get_contract_types` - Get contract types
- ✅ `get_contract_vendors` - Get contract vendors

**Usage Examples:**
```
"Create new contract with vendor 'Dell', starting '2024-01-01', ending '2024-12-31'"
"Get list of contracts with status 'active' and vendor 'Microsoft'"
"Update Dell contract with new end date '2025-12-31'"
```

### 5. **Purchase Order Management**
- ✅ `list_purchase_orders` - Get list of purchase orders
- ✅ `get_purchase_order` - Get purchase order details
- ✅ `create_purchase_order` - Create a new purchase order
- ✅ `update_purchase_order` - Update a purchase order
- ✅ `get_po_statuses` - Get purchase order statuses

**Usage Examples:**
```
"Create new purchase order with vendor 'HP' for 10 laptops"
"Get list of purchase orders with status 'pending_approval'"
"Update PO HP-001 with status 'approved'"
```

### 6. **Vendor Management**
- ✅ `list_vendors` - Get list of vendors
- ✅ `get_vendor` - Get vendor details
- ✅ `create_vendor` - Create a new vendor
- ✅ `update_vendor` - Update a vendor
- ✅ `get_vendor_types` - Get vendor types

**Usage Examples:**
```
"Create new vendor 'Dell Technologies' with email 'contact@dell.com'"
"Get detailed information about vendor 'Microsoft'"
"Update Dell vendor with new phone number"
```

## 🔧 **Statuses and Data Types**

### **Asset Statuses:**
- `in_use` - Currently in use
- `in_stock` - In stock
- `under_maintenance` - Under maintenance
- `retired` - Retired
- `lost` - Lost
- `stolen` - Stolen

### **CI Statuses:**
- `active` - Active
- `inactive` - Inactive
- `under_maintenance` - Under maintenance
- `retired` - Retired

### **Contract Statuses:**
- `active` - Active
- `expired` - Expired
- `pending` - Pending
- `terminated` - Terminated

### **Purchase Order Statuses:**
- `draft` - Draft
- `pending_approval` - Pending approval
- `approved` - Approved
- `ordered` - Ordered
- `received` - Received
- `cancelled` - Cancelled

## 🎯 **Real-World Usage Examples**

### **Infrastructure Management:**
```
"Create a Configuration Item for new database server 'DB-SRV-001'"
"Get list of all active network devices"
"Create an asset for a new switch and assign it to the data center"
```

### **Software Management:**
```
"Create a software license for Adobe Creative Suite with 50 licenses"
"Check remaining license count for Microsoft Office"
"Update Adobe license with a new expiry date"
```

### **Contract Management:**
```
"Create a maintenance contract with vendor Dell for 3 years"
"Get list of contracts expiring within the next 30 days"
"Update Microsoft contract with new value"
```

### **Procurement Management:**
```
"Create a purchase order for 20 monitors from vendor HP"
"Check status of purchase order PO-2024-001"
"Update PO with a new delivery date"
```

## 🔍 **Search and Reporting**

All tools support:
- **Pagination** - Limit the number of results
- **Filtering** - Filter by various criteria
- **Search** - Search by keyword
- **Sorting** - Sort results

## 📊 **AI Integration**

The MCP server enables AI assistants to:
- **Automatically create** CIs, assets, licenses, contracts
- **Track** the status and lifecycle of items
- **Report** on inventory and compliance
- **Manage** relationships between items
- **Optimize** procurement and vendor management

## 🚀 **Benefits**

1. **Centralized Management** - Centrally manage all configuration items
2. **Compliance Tracking** - Track compliance with licenses and contracts
3. **Asset Lifecycle** - Manage the full lifecycle of assets
4. **Vendor Management** - Efficiently manage vendor relationships
5. **Procurement Automation** - Automate the procurement process
6. **Reporting & Analytics** - CMDB data reporting and analytics

With these CMDB functions, the MCP server provides a complete solution to manage your entire IT infrastructure through an AI assistant!
