# ServiceDesk Plus MCP Server - Usage Guide

## Installation and Configuration

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file from the `env.example` file:

```bash
cp env.example .env
```

Edit the `.env` file with your actual details:

```env
SDP_BASE_URL=https://your-servicedesk-plus-instance.com
SDP_USERNAME=your_username
SDP_PASSWORD=your_password
SDP_API_KEY=your_api_key_here
```

### 3. Test the Connection

Run the test script to verify the connection:

```bash
python test_connection.py
```

## MCP Client Configuration

### With Claude Desktop

Add to your MCP configuration file (usually at `~/.config/claude/desktop-config.json`):

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

### With Cursor

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

## Available Tools

### Ticket Management

#### `list_tickets`
Get list of tickets with optional filters.

**Parameters:**
- `limit` (optional): Maximum number of tickets (default: 50, maximum: 1000)
- `status` (optional): Filter by status (open, pending, resolved, closed, cancelled, on_hold)
- `priority` (optional): Filter by priority (low, medium, high, critical)
- `requester` (optional): Filter by requester

**Example:**
```
Get 10 tickets with status "open" and priority "high"
```

#### `get_ticket`
Get detailed information about a ticket.

**Parameters:**
- `ticket_id` (required): ID of the ticket

**Example:**
```
Get detailed information about ticket with ID "TKT-001"
```

#### `create_ticket`
Create a new ticket.

**Parameters:**
- `subject` (required): Ticket subject
- `description` (required): Detailed description
- `requester` (required): Requester email or ID
- `priority` (optional): Priority level
- `category` (optional): Category
- `technician` (optional): Assigned technician ID

**Example:**
```
Create a new ticket with subject "Printer not working", description "HP LaserJet cannot print", requester "user@company.com", priority "medium"
```

#### `update_ticket`
Update ticket information.

**Parameters:**
- `ticket_id` (required): ID of the ticket
- `subject` (optional): New subject
- `description` (optional): New description
- `status` (optional): New status
- `priority` (optional): New priority
- `technician` (optional): New technician ID

**Example:**
```
Update ticket TKT-001 with status "resolved" and priority "low"
```

#### `delete_ticket`
Delete a ticket.

**Parameters:**
- `ticket_id` (required): ID of the ticket

### User Management

#### `list_users`
Get list of users.

**Parameters:**
- `limit` (optional): Maximum number of users

#### `get_user`
Get detailed information about a user.

**Parameters:**
- `user_id` (required): ID of the user

### Asset Management

#### `list_assets`
Get list of assets.

**Parameters:**
- `limit` (optional): Maximum number of assets

#### `get_asset`
Get detailed information about an asset.

**Parameters:**
- `asset_id` (required): ID of the asset

### Technician Management

#### `list_technicians`
Get list of technicians.

**Parameters:**
- `limit` (optional): Maximum number of technicians

### Search and Reference

#### `search_tickets`
Search tickets by keyword.

**Parameters:**
- `query` (required): Search keyword
- `limit` (optional): Maximum number of results

#### `get_categories`
Get list of available categories.

#### `get_priorities`
Get list of available priority levels.

#### `get_statuses`
Get list of available statuses.

### Comment Management

#### `add_ticket_comment`
Add a comment to a ticket.

**Parameters:**
- `ticket_id` (required): ID of the ticket
- `comment` (required): Comment content

#### `get_ticket_comments`
Get list of comments for a ticket.

**Parameters:**
- `ticket_id` (required): ID of the ticket

## Admin Management

### Site Management

#### `list_sites`
Get list of sites with filters.

**Parameters:**
- `limit` (optional): Maximum number of sites (default: 50)
- `site_type` (optional): Filter by site type (headquarters, branch_office, data_center, warehouse, retail_store, manufacturing_plant)
- `status` (optional): Filter by site status

**Example:**
```
Get list of 10 sites of type "branch_office"
```

#### `get_site`
Get detailed information about a site.

**Parameters:**
- `site_id` (required): ID of the site

#### `create_site`
Create a new site.

**Parameters:**
- `name` (required): Site name
- `site_type` (required): Site type
- `address` (optional): Address
- `city` (optional): City
- `state` (optional): State/Province
- `country` (optional): Country
- `zip_code` (optional): Zip code
- `phone` (optional): Phone number
- `email` (optional): Contact email
- `description` (optional): Description

**Example:**
```
Create new site "Branch Office Hanoi" of type "branch_office", address "123 Nguyen Trai, Hanoi, Vietnam"
```

#### `update_site`
Update site information.

**Parameters:**
- `site_id` (required): ID of the site
- `name` (optional): New name
- `site_type` (optional): New site type
- `address` (optional): New address
- `city` (optional): New city
- `state` (optional): New state/province
- `country` (optional): New country
- `zip_code` (optional): New zip code
- `phone` (optional): New phone number
- `email` (optional): New contact email
- `description` (optional): New description

#### `delete_site`
Delete a site.

**Parameters:**
- `site_id` (required): ID of the site

#### `get_site_types`
Get list of available site types.

### User Group Management

#### `list_user_groups`
Get list of user groups.

**Parameters:**
- `limit` (optional): Maximum number of groups
- `group_type` (optional): Filter by group type (department, project, location_based, role_based, custom)
- `site_id` (optional): Filter by site ID

#### `get_user_group`
Get detailed information about a user group.

**Parameters:**
- `group_id` (required): ID of the user group

#### `create_user_group`
Create a new user group.

**Parameters:**
- `name` (required): Group name
- `group_type` (required): Group type
- `description` (optional): Description
- `site_id` (optional): Associated site ID
- `manager` (optional): Manager ID

**Example:**
```
Create user group "IT Support Team" of type "department", description "IT support team"
```

#### `update_user_group`
Update user group information.

**Parameters:**
- `group_id` (required): ID of the user group
- `name` (optional): New name
- `group_type` (optional): New group type
- `description` (optional): New description
- `site_id` (optional): New associated site ID
- `manager` (optional): New manager ID

#### `delete_user_group`
Delete a user group.

**Parameters:**
- `group_id` (required): ID of the user group

#### `get_group_types`
Get list of available group types.

#### `get_group_permissions`
Get permissions for a user group.

**Parameters:**
- `group_id` (required): ID of the user group

#### `update_group_permissions`
Update permissions for a user group.

**Parameters:**
- `group_id` (required): ID of the user group
- `permissions` (required): Object containing permissions with corresponding levels (none, read, write, admin)

**Example:**
```
Update permissions for group "IT Support" with "read" for tickets and "write" for assets
```

### User & Technician Management (Admin)

#### `list_admin_users`
Get list of admin users.

**Parameters:**
- `limit` (optional): Maximum number of users
- `status` (optional): Filter by status (active, inactive, locked, pending_activation)
- `role` (optional): Filter by role (admin, manager, technician, user, viewer)
- `site_id` (optional): Filter by site ID

#### `get_admin_user`
Get detailed information about an admin user.

**Parameters:**
- `user_id` (required): ID of the user

#### `create_admin_user`
Create a new admin user.

**Parameters:**
- `username` (required): Username
- `email` (required): Email
- `first_name` (required): First name
- `last_name` (required): Last name
- `password` (optional): Password
- `role` (optional): Role (admin, manager, technician, user, viewer)
- `site_id` (optional): Site ID
- `department` (optional): Department
- `phone` (optional): Phone number
- `status` (optional): Status (active, inactive, locked, pending_activation)

**Example:**
```
Create admin user "john.doe" with email "john.doe@company.com", role "technician", assigned to site "Headquarters"
```

#### `update_admin_user`
Update admin user information.

**Parameters:**
- `user_id` (required): ID of the user
- `username` (optional): New username
- `email` (optional): New email
- `first_name` (optional): New first name
- `last_name` (optional): New last name
- `role` (optional): New role
- `site_id` (optional): New site ID
- `department` (optional): New department
- `phone` (optional): New phone number
- `status` (optional): New status

#### `delete_admin_user`
Delete an admin user.

**Parameters:**
- `user_id` (required): ID of the user

#### `list_admin_technicians`
Get list of admin technicians.

**Parameters:**
- `limit` (optional): Maximum number of technicians
- `status` (optional): Filter by status
- `role` (optional): Filter by role
- `site_id` (optional): Filter by site ID

#### `get_admin_technician`
Get detailed information about an admin technician.

**Parameters:**
- `technician_id` (required): ID of the technician

#### `create_admin_technician`
Create a new admin technician.

**Parameters:**
- `username` (required): Username
- `email` (required): Email
- `first_name` (required): First name
- `last_name` (required): Last name
- `password` (optional): Password
- `role` (optional): Role
- `site_id` (optional): Site ID
- `department` (optional): Department
- `phone` (optional): Phone number
- `status` (optional): Status
- `skills` (optional): List of skills
- `specializations` (optional): List of specializations

**Example:**
```
Create technician "jane.smith" with skills "network, security" and specializations "firewall"
```

#### `update_admin_technician`
Update admin technician information.

**Parameters:**
- `technician_id` (required): ID of the technician
- `username` (optional): New username
- `email` (optional): New email
- `first_name` (optional): New first name
- `last_name` (optional): New last name
- `role` (optional): New role
- `site_id` (optional): New site ID
- `department` (optional): New department
- `phone` (optional): New phone number
- `status` (optional): New status
- `skills` (optional): New list of skills
- `specializations` (optional): New list of specializations

#### `delete_admin_technician`
Delete an admin technician.

**Parameters:**
- `technician_id` (required): ID of the technician

#### `get_user_roles`
Get list of available user roles.

#### `get_technician_roles`
Get list of available technician roles.

### Permission Management

#### `get_permissions`
Get list of all available permissions.

#### `get_role_permissions`
Get permissions for a role.

**Parameters:**
- `role_id` (required): ID of the role

#### `update_role_permissions`
Update permissions for a role.

**Parameters:**
- `role_id` (required): ID of the role
- `permissions` (required): Object containing permissions with corresponding levels

#### `get_user_permissions`
Get permissions for a user.

**Parameters:**
- `user_id` (required): ID of the user

#### `update_user_permissions`
Update permissions for a user.

**Parameters:**
- `user_id` (required): ID of the user
- `permissions` (required): Object containing permissions with corresponding levels

### Department Management

#### `list_departments`
Get list of departments.

**Parameters:**
- `limit` (optional): Maximum number of departments
- `department_type` (optional): Filter by department type
- `site_id` (optional): Filter by site ID

#### `get_department`
Get detailed information about a department.

**Parameters:**
- `department_id` (required): ID of the department

#### `create_department`
Create a new department.

**Parameters:**
- `name` (required): Department name
- `department_type` (required): Department type
- `description` (optional): Description
- `site_id` (optional): Associated site ID
- `manager` (optional): Manager ID

#### `update_department`
Update department information.

**Parameters:**
- `department_id` (required): ID of the department
- `name` (optional): New name
- `department_type` (optional): New department type
- `description` (optional): New description
- `site_id` (optional): New associated site ID
- `manager` (optional): New manager ID

#### `delete_department`
Delete a department.

**Parameters:**
- `department_id` (required): ID of the department

#### `get_department_types`
Get list of available department types.

### Location Management

#### `list_locations`
Get list of locations.

**Parameters:**
- `limit` (optional): Maximum number of locations
- `location_type` (optional): Filter by location type
- `site_id` (optional): Filter by site ID

#### `get_location`
Get detailed information about a location.

**Parameters:**
- `location_id` (required): ID of the location

#### `create_location`
Create a new location.

**Parameters:**
- `name` (required): Location name
- `location_type` (required): Location type
- `description` (optional): Description
- `site_id` (optional): Associated site ID
- `address` (optional): Address
- `floor` (optional): Floor
- `room` (optional): Room

#### `update_location`
Update location information.

**Parameters:**
- `location_id` (required): ID of the location
- `name` (optional): New name
- `location_type` (optional): New location type
- `description` (optional): New description
- `site_id` (optional): New associated site ID
- `address` (optional): New address
- `floor` (optional): New floor
- `room` (optional): New room

#### `delete_location`
Delete a location.

**Parameters:**
- `location_id` (required): ID of the location

#### `get_location_types`
Get list of available location types.

### System Settings Management

#### `get_system_settings`
Get current system settings.

#### `update_system_settings`
Update system settings.

**Parameters:**
- `settings` (required): Object containing system settings to update

#### `get_email_settings`
Get current email settings.

#### `update_email_settings`
Update email settings.

**Parameters:**
- `settings` (required): Object containing email settings to update

#### `get_notification_settings`
Get current notification settings.

#### `update_notification_settings`
Update notification settings.

**Parameters:**
- `settings` (required): Object containing notification settings to update

## Real-World Usage Examples

### Infrastructure Management
```
"Create new site 'Data Center Singapore' of type data_center"
"Create location 'Server Room A' in site 'Data Center Singapore'"
"Create department 'Infrastructure Team' and assign manager"
"Create user group 'Network Admins' with appropriate permissions"
```

### User Management
```
"Create admin user 'john.doe' with role technician"
"Assign user 'john.doe' to department 'IT Support'"
"Update permissions for role 'manager'"
"Create technician 'jane.smith' with skills 'network, security'"
```

### Permission Management
```
"Get list of all available permissions"
"Assign 'admin' permission for tickets to role 'manager'"
"Update permissions for user 'john.doe'"
"Check permissions for group 'IT Support'"
```

### System Management
```
"Get current system settings"
"Update email settings to send ticket notifications"
"Configure notification settings for high priority tickets"
"Check email settings for automated reports"
```

## Troubleshooting

### Common Errors

1. **Authentication Error**
   - Check username/password in the .env file
   - Ensure the API key is valid (if used)

2. **Connection Error**
   - Check the URL in SDP_BASE_URL
   - Ensure the ServiceDesk Plus instance is running

3. **Permission Error**
   - Check user permissions in ServiceDesk Plus
   - Ensure the user has admin rights for admin operations

4. **Validation Error**
   - Check required fields in the request
   - Ensure data format is correct

### Debug

Run test connection to verify:
```bash
python test_connection.py
```

Check detailed logs:
```bash
python main.py --verbose
```

## Best Practices

1. **Security**
   - Always use the principle of least privilege
   - Regularly audit permissions and access rights
   - Log all admin activities

2. **Performance**
   - Use pagination for large lists
   - Cache frequently used data
   - Use batch operations when possible

3. **Maintenance**
   - Regularly backup admin configurations
   - Review and clean up unused users/groups
   - Monitor system performance

4. **Documentation**
   - Document all custom workflows
   - Maintain user role matrix
   - Keep site/department hierarchy updated
