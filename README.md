# ServiceDesk Plus MCP Server

MCP (Model Context Protocol) server for integrating with ServiceDesk Plus On-Premise with full CMDB support.

## 🎯 **Features**

### **Ticket Management**
- ✅ Ticket management (create, update, list, delete)
- ✅ Search and filter tickets
- ✅ Manage comments and attachments
- ✅ Workflow automation

### **CMDB (Configuration Management Database)**
- ✅ **Configuration Items (CIs)** - Manage servers, network devices, software
- ✅ **Asset Management** - Manage hardware, software, locations
- ✅ **Software License Management** - Track licenses, compliance
- ✅ **Contract Management** - Vendor contracts, SLA tracking
- ✅ **Purchase Order Management** - Procurement automation
- ✅ **Vendor Management** - Vendor relationships, contacts

### **Admin Management**
- ✅ **Site Management** - Manage sites, locations, branches
- ✅ **User Group Management** - Manage groups, permissions, roles
- ✅ **User & Technician Management** - CRUD operations, role assignment
- ✅ **Permission Management** - Role-based permissions, access control
- ✅ **Department Management** - Organizational structure
- ✅ **Location Management** - Physical locations, rooms, floors
- ✅ **System Settings** - Email, notifications, system configuration

### **User Management**
- ✅ Manage users and technicians
- ✅ Role-based access control
- ✅ User provisioning

### **Advanced Features**
- ✅ Authentication with ServiceDesk Plus API
- ✅ Real-time data synchronization
- ✅ Comprehensive error handling
- ✅ Async/await for high performance
- ✅ Pagination and filtering
- ✅ Search capabilities

## 📦 **Installation**

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Create a `.env` file with your configuration:**
```env
SDP_BASE_URL=https://your-servicedesk-plus-instance.com
SDP_USERNAME=your_username
SDP_PASSWORD=your_password
SDP_API_KEY=your_api_key
```

3. **Run the MCP server:**
```bash
python main.py
```

## ⚙️ **MCP Client Configuration**

### **With Claude Desktop**

Add to your MCP configuration file (`~/.config/claude/desktop-config.json`):

```json
{
  "mcpServers": {
    "servicedesk-plus": {
      "command": "python",
      "args": ["/path/to/servicedeskplus_mcp/main.py"],
      "env": {
        "SDP_BASE_URL": "https://your-instance.com",
        "SDP_USERNAME": "your_username",
        "SDP_PASSWORD": "your_password"
      }
    }
  }
}
```

### **With Cursor**

Add to your MCP configuration file:

```json
{
  "mcpServers": {
    "servicedesk-plus": {
      "command": "python",
      "args": ["/path/to/servicedeskplus_mcp/main.py"]
    }
  }
}
```

## 🛠️ **API Endpoints**

### **Ticket Management (15 tools)**
- `list_tickets` - Get list of tickets with filters
- `get_ticket` - Get detailed ticket information
- `create_ticket` - Create a new ticket
- `update_ticket` - Update a ticket
- `delete_ticket` - Delete a ticket
- `search_tickets` - Search tickets
- `add_ticket_comment` - Add a comment
- `get_ticket_comments` - Get comments

### **CMDB - Configuration Items (7 tools)**
- `list_configuration_items` - Get list of CIs
- `get_configuration_item` - Get CI details
- `create_configuration_item` - Create a new CI
- `update_configuration_item` - Update a CI
- `delete_configuration_item` - Delete a CI
- `get_ci_types` - Get CI types
- `get_ci_relationships` - Get relationships

### **Asset Management (10 tools)**
- `list_assets` - Get list of assets
- `get_asset` - Get asset details
- `create_asset` - Create a new asset
- `update_asset` - Update an asset
- `delete_asset` - Delete an asset
- `get_asset_types` - Get asset types
- `get_asset_categories` - Get asset categories
- `get_asset_locations` - Get asset locations
- `get_asset_models` - Get asset models
- `get_asset_vendors` - Get asset vendors

### **Software License Management (6 tools)**
- `list_software_licenses` - Get list of licenses
- `get_software_license` - Get license details
- `create_software_license` - Create a new license
- `update_software_license` - Update a license
- `get_software_products` - Get software products
- `get_license_types` - Get license types

### **Contract Management (6 tools)**
- `list_contracts` - Get list of contracts
- `get_contract` - Get contract details
- `create_contract` - Create a new contract
- `update_contract` - Update a contract
- `get_contract_types` - Get contract types
- `get_contract_vendors` - Get contract vendors

### **Purchase Order Management (5 tools)**
- `list_purchase_orders` - Get list of POs
- `get_purchase_order` - Get PO details
- `create_purchase_order` - Create a new PO
- `update_purchase_order` - Update a PO
- `get_po_statuses` - Get PO statuses

### **Vendor Management (5 tools)**
- `list_vendors` - Get list of vendors
- `get_vendor` - Get vendor details
- `create_vendor` - Create a new vendor
- `update_vendor` - Update a vendor
- `get_vendor_types` - Get vendor types

### **Admin Management - Sites (6 tools)**
- `list_sites` - Get list of sites
- `get_site` - Get site details
- `create_site` - Create a new site
- `update_site` - Update a site
- `delete_site` - Delete a site
- `get_site_types` - Get site types

### **Admin Management - User Groups (8 tools)**
- `list_user_groups` - Get list of user groups
- `get_user_group` - Get user group details
- `create_user_group` - Create a new user group
- `update_user_group` - Update a user group
- `delete_user_group` - Delete a user group
- `get_group_types` - Get group types
- `get_group_permissions` - Get group permissions
- `update_group_permissions` - Update group permissions

### **Admin Management - Users & Technicians (12 tools)**
- `list_admin_users` - Get list of admin users
- `get_admin_user` - Get admin user details
- `create_admin_user` - Create a new admin user
- `update_admin_user` - Update an admin user
- `delete_admin_user` - Delete an admin user
- `list_admin_technicians` - Get list of admin technicians
- `get_admin_technician` - Get admin technician details
- `create_admin_technician` - Create a new admin technician
- `update_admin_technician` - Update an admin technician
- `delete_admin_technician` - Delete an admin technician
- `get_user_roles` - Get user roles
- `get_technician_roles` - Get technician roles

### **Admin Management - Permissions (5 tools)**
- `get_permissions` - Get list of permissions
- `get_role_permissions` - Get role permissions
- `update_role_permissions` - Update role permissions
- `get_user_permissions` - Get user permissions
- `update_user_permissions` - Update user permissions

### **Admin Management - Departments (6 tools)**
- `list_departments` - Get list of departments
- `get_department` - Get department details
- `create_department` - Create a new department
- `update_department` - Update a department
- `delete_department` - Delete a department
- `get_department_types` - Get department types

### **Admin Management - Locations (6 tools)**
- `list_locations` - Get list of locations
- `get_location` - Get location details
- `create_location` - Create a new location
- `update_location` - Update a location
- `delete_location` - Delete a location
- `get_location_types` - Get location types

### **Admin Management - System Settings (6 tools)**
- `get_system_settings` - Get system settings
- `update_system_settings` - Update system settings
- `get_email_settings` - Get email settings
- `update_email_settings` - Update email settings
- `get_notification_settings` - Get notification settings
- `update_notification_settings` - Update notification settings

### **User Management (3 tools)**
- `list_users` - Get list of users
- `get_user` - Get user information
- `list_technicians` - Get list of technicians

### **Reference Data (3 tools)**
- `get_categories` - Get ticket categories
- `get_priorities` - Get priority levels
- `get_statuses` - Get ticket statuses

## 🎯 **Usage Examples**

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

### **Admin Management:**
```
"Create a new site 'Branch Office Hanoi' of type branch_office"
"Create user group 'IT Support Team' and assign permissions"
"Create admin user 'john.doe' with role technician"
"Update permissions for role 'manager'"
"Create department 'Software Development'"
"Get list of all locations in site 'Headquarters'"
"Update email settings for ticket notifications"
```

## 📊 **Highlights**

- **🔄 Async/await** - High performance with async operations
- **🛡️ Error handling** - Comprehensive error handling
- **🔐 Authentication** - Supports Basic Auth and API Key
- **📄 Pagination** - Efficiently handle large datasets
- **🔍 Filtering** - Flexible filters for all endpoints
- **📝 Validation** - Input data validation
- **📊 Logging** - Detailed logging for debugging
- **⚙️ Configuration** - Flexible configuration management

## 🚀 **Benefits**

1. **Centralized Management** - Centrally manage your entire IT infrastructure
2. **Compliance Tracking** - Track compliance with licenses and contracts
3. **Asset Lifecycle** - Manage the full lifecycle of assets
4. **Vendor Management** - Efficiently manage vendor relationships
5. **Procurement Automation** - Automate the procurement process
6. **Reporting & Analytics** - CMDB data reporting and analytics
7. **AI Integration** - Integrate AI to automate tasks

## 📚 **Documentation**

- [📖 Detailed Usage Guide](USAGE.md)
- [🏗️ CMDB Features](CMDB_FEATURES.md)
- [🧪 Test Connection](test_connection.py)

## 🔧 **Troubleshooting**

Run the test script to check connectivity:
```bash
python test_connection.py
```

Check logs for debugging:
```bash
python main.py --verbose
```

---

**Version:** 2.0.0
**Total Tools:** 100+ tools
**CMDB Support:** ✅ Full Support
**Admin Management:** ✅ Full Support
**License:** MIT
