"""
ServiceDesk Plus API Client
"""

import aiohttp
import asyncio
from typing import Dict, Any, List, Optional
from config import Config

class ServiceDeskPlusClient:
    """Client for interacting with ServiceDesk Plus API"""
    
    def __init__(self):
        self.base_url = Config.SDP_BASE_URL.rstrip('/')
        self.username = Config.SDP_USERNAME
        self.password = Config.SDP_PASSWORD
        self.api_key = Config.SDP_API_KEY
        self.session: Optional[aiohttp.ClientSession] = None
        self._auth_valid = False
        
    async def __aenter__(self):
        """Async context manager entry"""
        await self.authenticate()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.close()
        
    async def close(self):
        """Close the HTTP session"""
        if self.session:
            await self.session.close()
            self.session = None
            
    async def authenticate(self) -> bool:
        """Authenticate with ServiceDesk Plus"""
        if not self.session:
            timeout = aiohttp.ClientTimeout(total=Config.REQUEST_TIMEOUT)
            self.session = aiohttp.ClientSession(timeout=timeout)
            
        # Check if already authenticated
        if self._auth_valid:
            return True
            
        # Validate configuration
        config_validation = Config.validate_config()
        if not config_validation["valid"]:
            raise ValueError(f"Configuration issues: {config_validation['issues']}")
            
        # Test connection with authentication
        try:
            auth = aiohttp.BasicAuth(self.username, self.password)
            headers = Config.get_auth_headers()
            
            async with self.session.get(
                f"{self.base_url}{Config.API_ENDPOINTS['tickets']}",
                auth=auth,
                headers=headers,
                params={"limit": 1}
            ) as response:
                if response.status == 200:
                    self._auth_valid = True
                    return True
                else:
                    print(f"Authentication failed: {response.status} - {await response.text()}")
                    return False
                    
        except Exception as e:
            print(f"Authentication error: {e}")
            return False
            
    async def _make_request(
        self, 
        method: str, 
        endpoint: str, 
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make HTTP request to ServiceDesk Plus API"""
        if not await self.authenticate():
            raise Exception("Authentication failed")
            
        url = f"{self.base_url}{endpoint}"
        auth = aiohttp.BasicAuth(self.username, self.password)
        headers = Config.get_auth_headers()
        
        try:
            async with self.session.request(
                method=method,
                url=url,
                auth=auth,
                headers=headers,
                params=params,
                data=data,
                json=json_data
            ) as response:
                if response.status in [200, 201]:
                    return await response.json()
                else:
                    error_text = await response.text()
                    raise Exception(f"API request failed: {response.status} - {error_text}")
                    
        except Exception as e:
            raise Exception(f"Request failed: {e}")
            
    # ==================== TICKET MANAGEMENT ====================
    
    async def get_tickets(
        self, 
        limit: int = Config.DEFAULT_LIMIT,
        status: Optional[str] = None,
        priority: Optional[str] = None,
        requester: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get list of tickets with optional filtering"""
        params = {"limit": min(limit, Config.MAX_LIMIT)}
        
        if status:
            params["status"] = status
        if priority:
            params["priority"] = priority
        if requester:
            params["requester"] = requester
            
        return await self._make_request(
            "GET",
            Config.API_ENDPOINTS["tickets"],
            params=params
        )
        
    async def get_ticket(self, ticket_id: str) -> Dict[str, Any]:
        """Get specific ticket details"""
        return await self._make_request(
            "GET",
            f"{Config.API_ENDPOINTS['tickets']}/{ticket_id}"
        )
        
    async def create_ticket(self, ticket_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new ticket"""
        # Validate required fields
        required_fields = ["subject", "description", "requester"]
        for field in required_fields:
            if field not in ticket_data:
                raise ValueError(f"Required field '{field}' is missing")
                
        return await self._make_request(
            "POST",
            Config.API_ENDPOINTS["tickets"],
            json_data=ticket_data
        )
        
    async def update_ticket(self, ticket_id: str, update_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing ticket"""
        return await self._make_request(
            "PUT",
            f"{Config.API_ENDPOINTS['tickets']}/{ticket_id}",
            json_data=update_data
        )
        
    async def delete_ticket(self, ticket_id: str) -> Dict[str, Any]:
        """Delete a ticket"""
        return await self._make_request(
            "DELETE",
            f"{Config.API_ENDPOINTS['tickets']}/{ticket_id}"
        )
        
    async def search_tickets(self, query: str, limit: int = Config.DEFAULT_LIMIT) -> Dict[str, Any]:
        """Search tickets by query"""
        params = {
            "query": query,
            "limit": min(limit, Config.MAX_LIMIT)
        }
        return await self._make_request(
            "GET",
            f"{Config.API_ENDPOINTS['tickets']}/search",
            params=params
        )
        
    async def add_ticket_comment(self, ticket_id: str, comment: str) -> Dict[str, Any]:
        """Add a comment to a ticket"""
        comment_data = {"comment": comment}
        return await self._make_request(
            "POST",
            f"{Config.API_ENDPOINTS['tickets']}/{ticket_id}/comments",
            json_data=comment_data
        )
        
    async def get_ticket_comments(self, ticket_id: str) -> Dict[str, Any]:
        """Get comments for a ticket"""
        return await self._make_request(
            "GET",
            f"{Config.API_ENDPOINTS['tickets']}/{ticket_id}/comments"
        )
        
    # ==================== USER MANAGEMENT ====================
    
    async def get_users(self, limit: int = Config.DEFAULT_LIMIT) -> Dict[str, Any]:
        """Get list of users"""
        params = {"limit": min(limit, Config.MAX_LIMIT)}
        return await self._make_request(
            "GET",
            Config.API_ENDPOINTS["users"],
            params=params
        )
        
    async def get_user(self, user_id: str) -> Dict[str, Any]:
        """Get specific user details"""
        return await self._make_request(
            "GET",
            f"{Config.API_ENDPOINTS['users']}/{user_id}"
        )
        
    async def get_technicians(self, limit: int = Config.DEFAULT_LIMIT) -> Dict[str, Any]:
        """Get list of technicians"""
        params = {"limit": min(limit, Config.MAX_LIMIT)}
        return await self._make_request(
            "GET",
            Config.API_ENDPOINTS["technicians"],
            params=params
        )
        
    # ==================== ADMIN MANAGEMENT - SITES ====================
    
    async def get_sites(
        self, 
        limit: int = Config.DEFAULT_LIMIT,
        site_type: Optional[str] = None,
        status: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get list of sites"""
        params = {"limit": min(limit, Config.MAX_LIMIT)}
        
        if site_type:
            params["site_type"] = site_type
        if status:
            params["status"] = status
            
        return await self._make_request(
            "GET",
            Config.API_ENDPOINTS["sites"],
            params=params
        )
        
    async def get_site(self, site_id: str) -> Dict[str, Any]:
        """Get specific site details"""
        return await self._make_request(
            "GET",
            f"{Config.API_ENDPOINTS['sites']}/{site_id}"
        )
        
    async def create_site(self, site_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new site"""
        required_fields = ["name", "site_type"]
        for field in required_fields:
            if field not in site_data:
                raise ValueError(f"Required field '{field}' is missing")
                
        return await self._make_request(
            "POST",
            Config.API_ENDPOINTS["sites"],
            json_data=site_data
        )
        
    async def update_site(self, site_id: str, update_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing site"""
        return await self._make_request(
            "PUT",
            f"{Config.API_ENDPOINTS['sites']}/{site_id}",
            json_data=update_data
        )
        
    async def delete_site(self, site_id: str) -> Dict[str, Any]:
        """Delete a site"""
        return await self._make_request(
            "DELETE",
            f"{Config.API_ENDPOINTS['sites']}/{site_id}"
        )
        
    async def get_site_types(self) -> Dict[str, Any]:
        """Get list of site types"""
        return await self._make_request(
            "GET",
            Config.API_ENDPOINTS["site_types"]
        )
        
    # ==================== ADMIN MANAGEMENT - USER GROUPS ====================
    
    async def get_user_groups(
        self, 
        limit: int = Config.DEFAULT_LIMIT,
        group_type: Optional[str] = None,
        site_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get list of user groups"""
        params = {"limit": min(limit, Config.MAX_LIMIT)}
        
        if group_type:
            params["group_type"] = group_type
        if site_id:
            params["site_id"] = site_id
            
        return await self._make_request(
            "GET",
            Config.API_ENDPOINTS["user_groups"],
            params=params
        )
        
    async def get_user_group(self, group_id: str) -> Dict[str, Any]:
        """Get specific user group details"""
        return await self._make_request(
            "GET",
            f"{Config.API_ENDPOINTS['user_groups']}/{group_id}"
        )
        
    async def create_user_group(self, group_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new user group"""
        required_fields = ["name", "group_type"]
        for field in required_fields:
            if field not in group_data:
                raise ValueError(f"Required field '{field}' is missing")
                
        return await self._make_request(
            "POST",
            Config.API_ENDPOINTS["user_groups"],
            json_data=group_data
        )
        
    async def update_user_group(self, group_id: str, update_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing user group"""
        return await self._make_request(
            "PUT",
            f"{Config.API_ENDPOINTS['user_groups']}/{group_id}",
            json_data=update_data
        )
        
    async def delete_user_group(self, group_id: str) -> Dict[str, Any]:
        """Delete a user group"""
        return await self._make_request(
            "DELETE",
            f"{Config.API_ENDPOINTS['user_groups']}/{group_id}"
        )
        
    async def get_group_types(self) -> Dict[str, Any]:
        """Get list of group types"""
        return await self._make_request(
            "GET",
            Config.API_ENDPOINTS["group_types"]
        )
        
    async def get_group_permissions(self, group_id: str) -> Dict[str, Any]:
        """Get permissions for a user group"""
        return await self._make_request(
            "GET",
            f"{Config.API_ENDPOINTS['group_permissions']}?group_id={group_id}"
        )
        
    async def update_group_permissions(self, group_id: str, permissions: Dict[str, Any]) -> Dict[str, Any]:
        """Update permissions for a user group"""
        return await self._make_request(
            "PUT",
            f"{Config.API_ENDPOINTS['group_permissions']}/{group_id}",
            json_data=permissions
        )
        
    # ==================== ADMIN MANAGEMENT - USERS & TECHNICIANS ====================
    
    async def get_admin_users(
        self, 
        limit: int = Config.DEFAULT_LIMIT,
        status: Optional[str] = None,
        role: Optional[str] = None,
        site_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get list of users (admin)"""
        params = {"limit": min(limit, Config.MAX_LIMIT)}
        
        if status:
            params["status"] = status
        if role:
            params["role"] = role
        if site_id:
            params["site_id"] = site_id
            
        return await self._make_request(
            "GET",
            Config.API_ENDPOINTS["admin_users"],
            params=params
        )
        
    async def get_admin_user(self, user_id: str) -> Dict[str, Any]:
        """Get specific user details (admin)"""
        return await self._make_request(
            "GET",
            f"{Config.API_ENDPOINTS['admin_users']}/{user_id}"
        )
        
    async def create_admin_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new user (admin)"""
        required_fields = ["username", "email", "first_name", "last_name"]
        for field in required_fields:
            if field not in user_data:
                raise ValueError(f"Required field '{field}' is missing")
                
        return await self._make_request(
            "POST",
            Config.API_ENDPOINTS["admin_users"],
            json_data=user_data
        )
        
    async def update_admin_user(self, user_id: str, update_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing user (admin)"""
        return await self._make_request(
            "PUT",
            f"{Config.API_ENDPOINTS['admin_users']}/{user_id}",
            json_data=update_data
        )
        
    async def delete_admin_user(self, user_id: str) -> Dict[str, Any]:
        """Delete a user (admin)"""
        return await self._make_request(
            "DELETE",
            f"{Config.API_ENDPOINTS['admin_users']}/{user_id}"
        )
        
    async def get_admin_technicians(
        self, 
        limit: int = Config.DEFAULT_LIMIT,
        status: Optional[str] = None,
        role: Optional[str] = None,
        site_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get list of technicians (admin)"""
        params = {"limit": min(limit, Config.MAX_LIMIT)}
        
        if status:
            params["status"] = status
        if role:
            params["role"] = role
        if site_id:
            params["site_id"] = site_id
            
        return await self._make_request(
            "GET",
            Config.API_ENDPOINTS["admin_technicians"],
            params=params
        )
        
    async def get_admin_technician(self, technician_id: str) -> Dict[str, Any]:
        """Get specific technician details (admin)"""
        return await self._make_request(
            "GET",
            f"{Config.API_ENDPOINTS['admin_technicians']}/{technician_id}"
        )
        
    async def create_admin_technician(self, technician_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new technician (admin)"""
        required_fields = ["username", "email", "first_name", "last_name"]
        for field in required_fields:
            if field not in technician_data:
                raise ValueError(f"Required field '{field}' is missing")
                
        return await self._make_request(
            "POST",
            Config.API_ENDPOINTS["admin_technicians"],
            json_data=technician_data
        )
        
    async def update_admin_technician(self, technician_id: str, update_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing technician (admin)"""
        return await self._make_request(
            "PUT",
            f"{Config.API_ENDPOINTS['admin_technicians']}/{technician_id}",
            json_data=update_data
        )
        
    async def delete_admin_technician(self, technician_id: str) -> Dict[str, Any]:
        """Delete a technician (admin)"""
        return await self._make_request(
            "DELETE",
            f"{Config.API_ENDPOINTS['admin_technicians']}/{technician_id}"
        )
        
    async def get_user_roles(self) -> Dict[str, Any]:
        """Get list of user roles"""
        return await self._make_request(
            "GET",
            Config.API_ENDPOINTS["user_roles"]
        )
        
    async def get_technician_roles(self) -> Dict[str, Any]:
        """Get list of technician roles"""
        return await self._make_request(
            "GET",
            Config.API_ENDPOINTS["technician_roles"]
        )
        
    # ==================== ADMIN MANAGEMENT - PERMISSIONS ====================
    
    async def get_permissions(self) -> Dict[str, Any]:
        """Get list of all permissions"""
        return await self._make_request(
            "GET",
            Config.API_ENDPOINTS["permissions"]
        )
        
    async def get_role_permissions(self, role_id: str) -> Dict[str, Any]:
        """Get permissions for a specific role"""
        return await self._make_request(
            "GET",
            f"{Config.API_ENDPOINTS['role_permissions']}?role_id={role_id}"
        )
        
    async def update_role_permissions(self, role_id: str, permissions: Dict[str, Any]) -> Dict[str, Any]:
        """Update permissions for a specific role"""
        return await self._make_request(
            "PUT",
            f"{Config.API_ENDPOINTS['role_permissions']}/{role_id}",
            json_data=permissions
        )
        
    async def get_user_permissions(self, user_id: str) -> Dict[str, Any]:
        """Get permissions for a specific user"""
        return await self._make_request(
            "GET",
            f"{Config.API_ENDPOINTS['user_permissions']}?user_id={user_id}"
        )
        
    async def update_user_permissions(self, user_id: str, permissions: Dict[str, Any]) -> Dict[str, Any]:
        """Update permissions for a specific user"""
        return await self._make_request(
            "PUT",
            f"{Config.API_ENDPOINTS['user_permissions']}/{user_id}",
            json_data=permissions
        )
        
    # ==================== ADMIN MANAGEMENT - DEPARTMENTS ====================
    
    async def get_departments(
        self, 
        limit: int = Config.DEFAULT_LIMIT,
        department_type: Optional[str] = None,
        site_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get list of departments"""
        params = {"limit": min(limit, Config.MAX_LIMIT)}
        
        if department_type:
            params["department_type"] = department_type
        if site_id:
            params["site_id"] = site_id
            
        return await self._make_request(
            "GET",
            Config.API_ENDPOINTS["departments"],
            params=params
        )
        
    async def get_department(self, department_id: str) -> Dict[str, Any]:
        """Get specific department details"""
        return await self._make_request(
            "GET",
            f"{Config.API_ENDPOINTS['departments']}/{department_id}"
        )
        
    async def create_department(self, department_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new department"""
        required_fields = ["name", "department_type"]
        for field in required_fields:
            if field not in department_data:
                raise ValueError(f"Required field '{field}' is missing")
                
        return await self._make_request(
            "POST",
            Config.API_ENDPOINTS["departments"],
            json_data=department_data
        )
        
    async def update_department(self, department_id: str, update_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing department"""
        return await self._make_request(
            "PUT",
            f"{Config.API_ENDPOINTS['departments']}/{department_id}",
            json_data=update_data
        )
        
    async def delete_department(self, department_id: str) -> Dict[str, Any]:
        """Delete a department"""
        return await self._make_request(
            "DELETE",
            f"{Config.API_ENDPOINTS['departments']}/{department_id}"
        )
        
    async def get_department_types(self) -> Dict[str, Any]:
        """Get list of department types"""
        return await self._make_request(
            "GET",
            Config.API_ENDPOINTS["department_types"]
        )
        
    # ==================== ADMIN MANAGEMENT - LOCATIONS ====================
    
    async def get_locations(
        self, 
        limit: int = Config.DEFAULT_LIMIT,
        location_type: Optional[str] = None,
        site_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get list of locations"""
        params = {"limit": min(limit, Config.MAX_LIMIT)}
        
        if location_type:
            params["location_type"] = location_type
        if site_id:
            params["site_id"] = site_id
            
        return await self._make_request(
            "GET",
            Config.API_ENDPOINTS["locations"],
            params=params
        )
        
    async def get_location(self, location_id: str) -> Dict[str, Any]:
        """Get specific location details"""
        return await self._make_request(
            "GET",
            f"{Config.API_ENDPOINTS['locations']}/{location_id}"
        )
        
    async def create_location(self, location_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new location"""
        required_fields = ["name", "location_type"]
        for field in required_fields:
            if field not in location_data:
                raise ValueError(f"Required field '{field}' is missing")
                
        return await self._make_request(
            "POST",
            Config.API_ENDPOINTS["locations"],
            json_data=location_data
        )
        
    async def update_location(self, location_id: str, update_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing location"""
        return await self._make_request(
            "PUT",
            f"{Config.API_ENDPOINTS['locations']}/{location_id}",
            json_data=update_data
        )
        
    async def delete_location(self, location_id: str) -> Dict[str, Any]:
        """Delete a location"""
        return await self._make_request(
            "DELETE",
            f"{Config.API_ENDPOINTS['locations']}/{location_id}"
        )
        
    async def get_location_types(self) -> Dict[str, Any]:
        """Get list of location types"""
        return await self._make_request(
            "GET",
            Config.API_ENDPOINTS["location_types"]
        )
        
    # ==================== ADMIN MANAGEMENT - SYSTEM SETTINGS ====================
    
    async def get_system_settings(self) -> Dict[str, Any]:
        """Get system settings"""
        return await self._make_request(
            "GET",
            Config.API_ENDPOINTS["system_settings"]
        )
        
    async def update_system_settings(self, settings_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update system settings"""
        return await self._make_request(
            "PUT",
            Config.API_ENDPOINTS["system_settings"],
            json_data=settings_data
        )
        
    async def get_email_settings(self) -> Dict[str, Any]:
        """Get email settings"""
        return await self._make_request(
            "GET",
            Config.API_ENDPOINTS["email_settings"]
        )
        
    async def update_email_settings(self, settings_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update email settings"""
        return await self._make_request(
            "PUT",
            Config.API_ENDPOINTS["email_settings"],
            json_data=settings_data
        )
        
    async def get_notification_settings(self) -> Dict[str, Any]:
        """Get notification settings"""
        return await self._make_request(
            "GET",
            Config.API_ENDPOINTS["notification_settings"]
        )
        
    async def update_notification_settings(self, settings_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update notification settings"""
        return await self._make_request(
            "PUT",
            Config.API_ENDPOINTS["notification_settings"],
            json_data=settings_data
        )
        
    # ==================== CMDB - CONFIGURATION ITEMS ====================
    
    async def get_configuration_items(
        self, 
        limit: int = Config.DEFAULT_LIMIT,
        ci_type: Optional[str] = None,
        status: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get list of configuration items"""
        params = {"limit": min(limit, Config.MAX_LIMIT)}
        
        if ci_type:
            params["ci_type"] = ci_type
        if status:
            params["status"] = status
            
        return await self._make_request(
            "GET",
            Config.API_ENDPOINTS["configuration_items"],
            params=params
        )
        
    async def get_configuration_item(self, ci_id: str) -> Dict[str, Any]:
        """Get specific configuration item details"""
        return await self._make_request(
            "GET",
            f"{Config.API_ENDPOINTS['configuration_items']}/{ci_id}"
        )
        
    async def create_configuration_item(self, ci_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new configuration item"""
        required_fields = ["name", "ci_type"]
        for field in required_fields:
            if field not in ci_data:
                raise ValueError(f"Required field '{field}' is missing")
                
        return await self._make_request(
            "POST",
            Config.API_ENDPOINTS["configuration_items"],
            json_data=ci_data
        )
        
    async def update_configuration_item(self, ci_id: str, update_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing configuration item"""
        return await self._make_request(
            "PUT",
            f"{Config.API_ENDPOINTS['configuration_items']}/{ci_id}",
            json_data=update_data
        )
        
    async def delete_configuration_item(self, ci_id: str) -> Dict[str, Any]:
        """Delete a configuration item"""
        return await self._make_request(
            "DELETE",
            f"{Config.API_ENDPOINTS['configuration_items']}/{ci_id}"
        )
        
    async def get_ci_types(self) -> Dict[str, Any]:
        """Get list of CI types"""
        return await self._make_request(
            "GET",
            Config.API_ENDPOINTS["ci_types"]
        )
        
    async def get_ci_relationships(self, ci_id: str) -> Dict[str, Any]:
        """Get relationships for a configuration item"""
        return await self._make_request(
            "GET",
            f"{Config.API_ENDPOINTS['ci_relationships']}?ci_id={ci_id}"
        )
        
    # ==================== ASSET MANAGEMENT ====================
    
    async def get_assets(
        self, 
        limit: int = Config.DEFAULT_LIMIT,
        asset_type: Optional[str] = None,
        status: Optional[str] = None,
        location: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get list of assets with optional filtering"""
        params = {"limit": min(limit, Config.MAX_LIMIT)}
        
        if asset_type:
            params["asset_type"] = asset_type
        if status:
            params["status"] = status
        if location:
            params["location"] = location
            
        return await self._make_request(
            "GET",
            Config.API_ENDPOINTS["assets"],
            params=params
        )
        
    async def get_asset(self, asset_id: str) -> Dict[str, Any]:
        """Get specific asset details"""
        return await self._make_request(
            "GET",
            f"{Config.API_ENDPOINTS['assets']}/{asset_id}"
        )
        
    async def create_asset(self, asset_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new asset"""
        required_fields = ["name", "asset_type"]
        for field in required_fields:
            if field not in asset_data:
                raise ValueError(f"Required field '{field}' is missing")
                
        return await self._make_request(
            "POST",
            Config.API_ENDPOINTS["assets"],
            json_data=asset_data
        )
        
    async def update_asset(self, asset_id: str, update_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing asset"""
        return await self._make_request(
            "PUT",
            f"{Config.API_ENDPOINTS['assets']}/{asset_id}",
            json_data=update_data
        )
        
    async def delete_asset(self, asset_id: str) -> Dict[str, Any]:
        """Delete an asset"""
        return await self._make_request(
            "DELETE",
            f"{Config.API_ENDPOINTS['assets']}/{asset_id}"
        )
        
    async def get_asset_types(self) -> Dict[str, Any]:
        """Get list of asset types"""
        return await self._make_request(
            "GET",
            Config.API_ENDPOINTS["asset_types"]
        )
        
    async def get_asset_categories(self) -> Dict[str, Any]:
        """Get list of asset categories"""
        return await self._make_request(
            "GET",
            Config.API_ENDPOINTS["asset_categories"]
        )
        
    async def get_asset_locations(self) -> Dict[str, Any]:
        """Get list of asset locations"""
        return await self._make_request(
            "GET",
            Config.API_ENDPOINTS["asset_locations"]
        )
        
    async def get_asset_models(self) -> Dict[str, Any]:
        """Get list of asset models"""
        return await self._make_request(
            "GET",
            Config.API_ENDPOINTS["asset_models"]
        )
        
    async def get_asset_vendors(self) -> Dict[str, Any]:
        """Get list of asset vendors"""
        return await self._make_request(
            "GET",
            Config.API_ENDPOINTS["asset_vendors"]
        )
        
    # ==================== SOFTWARE LICENSE MANAGEMENT ====================
    
    async def get_software_licenses(
        self, 
        limit: int = Config.DEFAULT_LIMIT,
        product: Optional[str] = None,
        vendor: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get list of software licenses"""
        params = {"limit": min(limit, Config.MAX_LIMIT)}
        
        if product:
            params["product"] = product
        if vendor:
            params["vendor"] = vendor
            
        return await self._make_request(
            "GET",
            Config.API_ENDPOINTS["software_licenses"],
            params=params
        )
        
    async def get_software_license(self, license_id: str) -> Dict[str, Any]:
        """Get specific software license details"""
        return await self._make_request(
            "GET",
            f"{Config.API_ENDPOINTS['software_licenses']}/{license_id}"
        )
        
    async def create_software_license(self, license_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new software license"""
        required_fields = ["product", "license_type", "total_licenses"]
        for field in required_fields:
            if field not in license_data:
                raise ValueError(f"Required field '{field}' is missing")
                
        return await self._make_request(
            "POST",
            Config.API_ENDPOINTS["software_licenses"],
            json_data=license_data
        )
        
    async def update_software_license(self, license_id: str, update_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing software license"""
        return await self._make_request(
            "PUT",
            f"{Config.API_ENDPOINTS['software_licenses']}/{license_id}",
            json_data=update_data
        )
        
    async def get_software_products(self) -> Dict[str, Any]:
        """Get list of software products"""
        return await self._make_request(
            "GET",
            Config.API_ENDPOINTS["software_products"]
        )
        
    async def get_license_types(self) -> Dict[str, Any]:
        """Get list of license types"""
        return await self._make_request(
            "GET",
            Config.API_ENDPOINTS["license_types"]
        )
        
    # ==================== CONTRACT MANAGEMENT ====================
    
    async def get_contracts(
        self, 
        limit: int = Config.DEFAULT_LIMIT,
        contract_type: Optional[str] = None,
        status: Optional[str] = None,
        vendor: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get list of contracts"""
        params = {"limit": min(limit, Config.MAX_LIMIT)}
        
        if contract_type:
            params["contract_type"] = contract_type
        if status:
            params["status"] = status
        if vendor:
            params["vendor"] = vendor
            
        return await self._make_request(
            "GET",
            Config.API_ENDPOINTS["contracts"],
            params=params
        )
        
    async def get_contract(self, contract_id: str) -> Dict[str, Any]:
        """Get specific contract details"""
        return await self._make_request(
            "GET",
            f"{Config.API_ENDPOINTS['contracts']}/{contract_id}"
        )
        
    async def create_contract(self, contract_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new contract"""
        required_fields = ["name", "vendor", "start_date", "end_date"]
        for field in required_fields:
            if field not in contract_data:
                raise ValueError(f"Required field '{field}' is missing")
                
        return await self._make_request(
            "POST",
            Config.API_ENDPOINTS["contracts"],
            json_data=contract_data
        )
        
    async def update_contract(self, contract_id: str, update_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing contract"""
        return await self._make_request(
            "PUT",
            f"{Config.API_ENDPOINTS['contracts']}/{contract_id}",
            json_data=update_data
        )
        
    async def get_contract_types(self) -> Dict[str, Any]:
        """Get list of contract types"""
        return await self._make_request(
            "GET",
            Config.API_ENDPOINTS["contract_types"]
        )
        
    async def get_contract_vendors(self) -> Dict[str, Any]:
        """Get list of contract vendors"""
        return await self._make_request(
            "GET",
            Config.API_ENDPOINTS["contract_vendors"]
        )
        
    # ==================== PURCHASE ORDER MANAGEMENT ====================
    
    async def get_purchase_orders(
        self, 
        limit: int = Config.DEFAULT_LIMIT,
        status: Optional[str] = None,
        vendor: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get list of purchase orders"""
        params = {"limit": min(limit, Config.MAX_LIMIT)}
        
        if status:
            params["status"] = status
        if vendor:
            params["vendor"] = vendor
            
        return await self._make_request(
            "GET",
            Config.API_ENDPOINTS["purchase_orders"],
            params=params
        )
        
    async def get_purchase_order(self, po_id: str) -> Dict[str, Any]:
        """Get specific purchase order details"""
        return await self._make_request(
            "GET",
            f"{Config.API_ENDPOINTS['purchase_orders']}/{po_id}"
        )
        
    async def create_purchase_order(self, po_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new purchase order"""
        required_fields = ["vendor", "items"]
        for field in required_fields:
            if field not in po_data:
                raise ValueError(f"Required field '{field}' is missing")
                
        return await self._make_request(
            "POST",
            Config.API_ENDPOINTS["purchase_orders"],
            json_data=po_data
        )
        
    async def update_purchase_order(self, po_id: str, update_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing purchase order"""
        return await self._make_request(
            "PUT",
            f"{Config.API_ENDPOINTS['purchase_orders']}/{po_id}",
            json_data=update_data
        )
        
    async def get_po_statuses(self) -> Dict[str, Any]:
        """Get list of purchase order statuses"""
        return await self._make_request(
            "GET",
            Config.API_ENDPOINTS["po_statuses"]
        )
        
    # ==================== VENDOR MANAGEMENT ====================
    
    async def get_vendors(
        self, 
        limit: int = Config.DEFAULT_LIMIT,
        vendor_type: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get list of vendors"""
        params = {"limit": min(limit, Config.MAX_LIMIT)}
        
        if vendor_type:
            params["vendor_type"] = vendor_type
            
        return await self._make_request(
            "GET",
            Config.API_ENDPOINTS["vendors"],
            params=params
        )
        
    async def get_vendor(self, vendor_id: str) -> Dict[str, Any]:
        """Get specific vendor details"""
        return await self._make_request(
            "GET",
            f"{Config.API_ENDPOINTS['vendors']}/{vendor_id}"
        )
        
    async def create_vendor(self, vendor_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new vendor"""
        required_fields = ["name", "email"]
        for field in required_fields:
            if field not in vendor_data:
                raise ValueError(f"Required field '{field}' is missing")
                
        return await self._make_request(
            "POST",
            Config.API_ENDPOINTS["vendors"],
            json_data=vendor_data
        )
        
    async def update_vendor(self, vendor_id: str, update_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing vendor"""
        return await self._make_request(
            "PUT",
            f"{Config.API_ENDPOINTS['vendors']}/{vendor_id}",
            json_data=update_data
        )
        
    async def get_vendor_types(self) -> Dict[str, Any]:
        """Get list of vendor types"""
        return await self._make_request(
            "GET",
            Config.API_ENDPOINTS["vendor_types"]
        )
        
    # ==================== REFERENCE DATA ====================
    
    async def get_categories(self) -> Dict[str, Any]:
        """Get list of ticket categories"""
        return await self._make_request(
            "GET",
            Config.API_ENDPOINTS["categories"]
        )
        
    async def get_priorities(self) -> Dict[str, Any]:
        """Get list of ticket priorities"""
        return await self._make_request(
            "GET",
            Config.API_ENDPOINTS["priorities"]
        )
        
    async def get_statuses(self) -> Dict[str, Any]:
        """Get list of ticket statuses"""
        return await self._make_request(
            "GET",
            Config.API_ENDPOINTS["statuses"]
        ) 