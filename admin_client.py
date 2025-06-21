"""
Admin Management Client for ServiceDesk Plus MCP Server
"""

import aiohttp
from typing import Dict, Any, Optional
from config import Config

class AdminManagementClient:
    """Client for Admin Management functions"""
    
    def __init__(self, session: aiohttp.ClientSession, base_url: str, auth):
        self.session = session
        self.base_url = base_url
        self.auth = auth
        self.headers = Config.get_auth_headers()
        
    async def _make_request(
        self, 
        method: str, 
        endpoint: str, 
        params: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make HTTP request to ServiceDesk Plus API"""
        url = f"{self.base_url}{endpoint}"
        
        try:
            async with self.session.request(
                method=method,
                url=url,
                auth=self.auth,
                headers=self.headers,
                params=params,
                json=json_data
            ) as response:
                if response.status in [200, 201]:
                    return await response.json()
                else:
                    error_text = await response.text()
                    raise Exception(f"API request failed: {response.status} - {error_text}")
                    
        except Exception as e:
            raise Exception(f"Request failed: {e}")
            
    # ==================== SITE MANAGEMENT ====================
    
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
        
    # ==================== USER GROUP MANAGEMENT ====================
    
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
        
    # ==================== USER & TECHNICIAN MANAGEMENT ====================
    
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
        
    # ==================== PERMISSION MANAGEMENT ====================
    
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
        
    # ==================== DEPARTMENT MANAGEMENT ====================
    
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
        
    # ==================== LOCATION MANAGEMENT ====================
    
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
        
    # ==================== SYSTEM SETTINGS ====================
    
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