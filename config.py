"""
Configuration file for ServiceDesk Plus MCP Server
"""

import os
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for ServiceDesk Plus MCP Server"""
    
    # ServiceDesk Plus API Configuration
    SDP_BASE_URL = os.getenv("SDP_BASE_URL", "")
    SDP_USERNAME = os.getenv("SDP_USERNAME", "")
    SDP_PASSWORD = os.getenv("SDP_PASSWORD", "")
    SDP_API_KEY = os.getenv("SDP_API_KEY", "")
    
    # API Endpoints
    API_ENDPOINTS = {
        # Ticket Management
        "tickets": "/api/v3/tickets",
        "users": "/api/v3/users",
        "technicians": "/api/v3/technicians",
        "categories": "/api/v3/categories",
        "priorities": "/api/v3/priorities",
        "statuses": "/api/v3/statuses",
        
        # CMDB - Configuration Items
        "configuration_items": "/api/v3/cmdb/ci",
        "ci_types": "/api/v3/cmdb/ci_types",
        "ci_relationships": "/api/v3/cmdb/ci_relationships",
        
        # Asset Management
        "assets": "/api/v3/assets",
        "asset_types": "/api/v3/asset_types",
        "asset_categories": "/api/v3/asset_categories",
        "asset_locations": "/api/v3/asset_locations",
        "asset_models": "/api/v3/asset_models",
        "asset_vendors": "/api/v3/asset_vendors",
        
        # Software License Management
        "software_licenses": "/api/v3/software_licenses",
        "software_products": "/api/v3/software_products",
        "license_types": "/api/v3/license_types",
        
        # Contract Management
        "contracts": "/api/v3/contracts",
        "contract_types": "/api/v3/contract_types",
        "contract_vendors": "/api/v3/contract_vendors",
        
        # Purchase Order Management
        "purchase_orders": "/api/v3/purchase_orders",
        "po_statuses": "/api/v3/po_statuses",
        
        # Vendor Management
        "vendors": "/api/v3/vendors",
        "vendor_types": "/api/v3/vendor_types",
        
        # Admin Management - Sites
        "sites": "/api/v3/admin/sites",
        "site_types": "/api/v3/admin/site_types",
        
        # Admin Management - User Groups
        "user_groups": "/api/v3/admin/user_groups",
        "group_types": "/api/v3/admin/group_types",
        "group_permissions": "/api/v3/admin/group_permissions",
        
        # Admin Management - Users & Technicians
        "admin_users": "/api/v3/admin/users",
        "admin_technicians": "/api/v3/admin/technicians",
        "user_roles": "/api/v3/admin/user_roles",
        "technician_roles": "/api/v3/admin/technician_roles",
        
        # Admin Management - Permissions
        "permissions": "/api/v3/admin/permissions",
        "role_permissions": "/api/v3/admin/role_permissions",
        "user_permissions": "/api/v3/admin/user_permissions",
        
        # Admin Management - Departments
        "departments": "/api/v3/admin/departments",
        "department_types": "/api/v3/admin/department_types",
        
        # Admin Management - Locations
        "locations": "/api/v3/admin/locations",
        "location_types": "/api/v3/admin/location_types",
        
        # Admin Management - System Settings
        "system_settings": "/api/v3/admin/system_settings",
        "email_settings": "/api/v3/admin/email_settings",
        "notification_settings": "/api/v3/admin/notification_settings",
        
        # Discovery
        "discovery": "/api/v3/discovery",
        "discovery_profiles": "/api/v3/discovery_profiles",
        
        # Reports
        "reports": "/api/v3/reports",
        "cmdb_reports": "/api/v3/cmdb/reports"
    }
    
    # Ticket Statuses
    TICKET_STATUSES = [
        "open",
        "pending",
        "resolved",
        "closed",
        "cancelled",
        "on_hold"
    ]
    
    # Ticket Priorities
    TICKET_PRIORITIES = [
        "low",
        "medium",
        "high",
        "critical"
    ]
    
    # Asset Statuses
    ASSET_STATUSES = [
        "in_use",
        "in_stock",
        "under_maintenance",
        "retired",
        "lost",
        "stolen"
    ]
    
    # CI Statuses
    CI_STATUSES = [
        "active",
        "inactive",
        "under_maintenance",
        "retired"
    ]
    
    # Contract Statuses
    CONTRACT_STATUSES = [
        "active",
        "expired",
        "pending",
        "terminated"
    ]
    
    # Purchase Order Statuses
    PO_STATUSES = [
        "draft",
        "pending_approval",
        "approved",
        "ordered",
        "received",
        "cancelled"
    ]
    
    # User Statuses
    USER_STATUSES = [
        "active",
        "inactive",
        "locked",
        "pending_activation"
    ]
    
    # User Roles
    USER_ROLES = [
        "admin",
        "manager",
        "technician",
        "user",
        "viewer"
    ]
    
    # Site Types
    SITE_TYPES = [
        "headquarters",
        "branch_office",
        "data_center",
        "warehouse",
        "retail_store",
        "manufacturing_plant"
    ]
    
    # Group Types
    GROUP_TYPES = [
        "department",
        "project",
        "location_based",
        "role_based",
        "custom"
    ]
    
    # Permission Levels
    PERMISSION_LEVELS = [
        "none",
        "read",
        "write",
        "admin"
    ]
    
    # Default pagination
    DEFAULT_LIMIT = 50
    MAX_LIMIT = 1000
    
    # Request timeout (seconds)
    REQUEST_TIMEOUT = 30
    
    @classmethod
    def validate_config(cls) -> Dict[str, Any]:
        """Validate configuration and return any issues"""
        issues = []
        
        if not cls.SDP_BASE_URL:
            issues.append("SDP_BASE_URL is not set")
        
        if not cls.SDP_USERNAME:
            issues.append("SDP_USERNAME is not set")
        
        if not cls.SDP_PASSWORD:
            issues.append("SDP_PASSWORD is not set")
        
        return {
            "valid": len(issues) == 0,
            "issues": issues
        }
    
    @classmethod
    def get_auth_headers(cls) -> Dict[str, str]:
        """Get authentication headers for API requests"""
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        if cls.SDP_API_KEY:
            headers["X-API-Key"] = cls.SDP_API_KEY
        
        return headers 