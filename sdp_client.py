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

    # ==================== ADVANCED REQUEST MANAGEMENT ====================

    async def assign_request(self, request_id: str, technician_id: str, group_id: Optional[str] = None) -> Dict[str, Any]:
        """Assign request to a technician and/or group"""
        assignment_data = {"technician_id": technician_id}
        if group_id:
            assignment_data["group_id"] = group_id

        return await self._make_request(
            "PUT",
            f"{Config.API_ENDPOINTS['tickets']}/{request_id}/assign",
            json_data=assignment_data
        )

    async def reassign_request(self, request_id: str, technician_id: str, reason: Optional[str] = None) -> Dict[str, Any]:
        """Reassign request to another technician"""
        reassign_data = {"technician_id": technician_id}
        if reason:
            reassign_data["reason"] = reason

        return await self._make_request(
            "PUT",
            f"{Config.API_ENDPOINTS['tickets']}/{request_id}/reassign",
            json_data=reassign_data
        )

    async def escalate_request(self, request_id: str, escalation_level: str, reason: str) -> Dict[str, Any]:
        """Escalate a request"""
        escalation_data = {
            "escalation_level": escalation_level,
            "reason": reason
        }

        return await self._make_request(
            "PUT",
            f"{Config.API_ENDPOINTS['tickets']}/{request_id}/escalate",
            json_data=escalation_data
        )

    async def approve_request(self, request_id: str, approval_comments: Optional[str] = None) -> Dict[str, Any]:
        """Approve a request"""
        approval_data = {"action": "approve"}
        if approval_comments:
            approval_data["comments"] = approval_comments

        return await self._make_request(
            "PUT",
            f"{Config.API_ENDPOINTS['tickets']}/{request_id}/approval",
            json_data=approval_data
        )

    async def reject_request(self, request_id: str, rejection_reason: str, comments: Optional[str] = None) -> Dict[str, Any]:
        """Reject a request"""
        rejection_data = {
            "action": "reject",
            "reason": rejection_reason
        }
        if comments:
            rejection_data["comments"] = comments

        return await self._make_request(
            "PUT",
            f"{Config.API_ENDPOINTS['tickets']}/{request_id}/approval",
            json_data=rejection_data
        )

    async def get_request_approvals(self, request_id: str) -> Dict[str, Any]:
        """Get approval details for a request"""
        return await self._make_request(
            "GET",
            f"{Config.API_ENDPOINTS['tickets']}/{request_id}/approvals"
        )

    async def get_request_attachments(self, request_id: str) -> Dict[str, Any]:
        """Get attachments for a request"""
        return await self._make_request(
            "GET",
            f"{Config.API_ENDPOINTS['tickets']}/{request_id}/attachments"
        )

    async def add_request_attachment(self, request_id: str, file_path: str, description: Optional[str] = None) -> Dict[str, Any]:
        """Add attachment to a request"""
        import aiofiles

        async with aiofiles.open(file_path, 'rb') as f:
            file_content = await f.read()

        files = {'file': file_content}
        data = {}
        if description:
            data['description'] = description

        return await self._make_request(
            "POST",
            f"{Config.API_ENDPOINTS['tickets']}/{request_id}/attachments",
            data=data,
            files=files
        )

    async def delete_request_attachment(self, request_id: str, attachment_id: str) -> Dict[str, Any]:
        """Delete attachment from a request"""
        return await self._make_request(
            "DELETE",
            f"{Config.API_ENDPOINTS['tickets']}/{request_id}/attachments/{attachment_id}"
        )

    async def get_request_history(self, request_id: str, limit: int = 50) -> Dict[str, Any]:
        """Get request history/timeline"""
        params = {"limit": min(limit, 1000)}
        return await self._make_request(
            "GET",
            f"{Config.API_ENDPOINTS['tickets']}/{request_id}/history",
            params=params
        )

    async def get_request_sla_details(self, request_id: str) -> Dict[str, Any]:
        """Get SLA details for a request"""
        return await self._make_request(
            "GET",
            f"{Config.API_ENDPOINTS['tickets']}/{request_id}/sla"
        )

    async def update_request_sla(self, request_id: str, sla_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update SLA for a request"""
        return await self._make_request(
            "PUT",
            f"{Config.API_ENDPOINTS['tickets']}/{request_id}/sla",
            json_data=sla_data
        )

    async def get_request_templates(self, category: Optional[str] = None) -> Dict[str, Any]:
        """Get available request templates"""
        params = {}
        if category:
            params["category"] = category

        return await self._make_request(
            "GET",
            f"{Config.API_ENDPOINTS['tickets']}/templates",
            params=params
        )

    async def create_request_from_template(self, template_id: str, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create request from template"""
        return await self._make_request(
            "POST",
            f"{Config.API_ENDPOINTS['tickets']}/templates/{template_id}/create",
            json_data=request_data
        )

    async def close_request(self, request_id: str, closure_code: str, resolution: str) -> Dict[str, Any]:
        """Close a request with closure code and resolution"""
        closure_data = {
            "status": "closed",
            "closure_code": closure_code,
            "resolution": resolution
        }

        return await self._make_request(
            "PUT",
            f"{Config.API_ENDPOINTS['tickets']}/{request_id}/close",
            json_data=closure_data
        )

    async def get_closure_codes(self) -> Dict[str, Any]:
        """Get available closure codes"""
        return await self._make_request(
            "GET",
            f"{Config.API_ENDPOINTS['tickets']}/closure_codes"
        )

    async def get_request_worklog(self, request_id: str, limit: int = 50) -> Dict[str, Any]:
        """Get worklog entries for a request"""
        params = {"limit": min(limit, 1000)}
        return await self._make_request(
            "GET",
            f"{Config.API_ENDPOINTS['tickets']}/{request_id}/worklog",
            params=params
        )

    async def add_worklog_entry(
        self,
        request_id: str,
        description: str,
        time_spent: Optional[str] = None,
        technician_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Add worklog entry to a request"""
        worklog_data = {"description": description}
        if time_spent:
            worklog_data["time_spent"] = time_spent
        if technician_id:
            worklog_data["technician_id"] = technician_id

        return await self._make_request(
            "POST",
            f"{Config.API_ENDPOINTS['tickets']}/{request_id}/worklog",
            json_data=worklog_data
        )

    async def update_worklog_entry(self, request_id: str, worklog_id: str, update_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update worklog entry"""
        return await self._make_request(
            "PUT",
            f"{Config.API_ENDPOINTS['tickets']}/{request_id}/worklog/{worklog_id}",
            json_data=update_data
        )

    async def get_request_custom_fields(self, request_id: str) -> Dict[str, Any]:
        """Get custom fields for a request"""
        return await self._make_request(
            "GET",
            f"{Config.API_ENDPOINTS['tickets']}/{request_id}/custom_fields"
        )

    async def update_request_custom_fields(self, request_id: str, custom_fields: Dict[str, Any]) -> Dict[str, Any]:
        """Update custom fields for a request"""
        return await self._make_request(
            "PUT",
            f"{Config.API_ENDPOINTS['tickets']}/{request_id}/custom_fields",
            json_data=custom_fields
        )

    async def get_request_feedback(self, request_id: str) -> Dict[str, Any]:
        """Get feedback/survey for a request"""
        return await self._make_request(
            "GET",
            f"{Config.API_ENDPOINTS['tickets']}/{request_id}/feedback"
        )

    async def submit_request_feedback(
        self,
        request_id: str,
        rating: int,
        comments: Optional[str] = None,
        survey_responses: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Submit feedback for a request"""
        feedback_data = {"rating": rating}
        if comments:
            feedback_data["comments"] = comments
        if survey_responses:
            feedback_data["survey_responses"] = survey_responses

        return await self._make_request(
            "POST",
            f"{Config.API_ENDPOINTS['tickets']}/{request_id}/feedback",
            json_data=feedback_data
        )

    async def get_request_notifications(self, request_id: str) -> Dict[str, Any]:
        """Get notifications sent for a request"""
        return await self._make_request(
            "GET",
            f"{Config.API_ENDPOINTS['tickets']}/{request_id}/notifications"
        )

    async def send_request_notification(
        self,
        request_id: str,
        notification_type: str,
        recipients: List[str],
        custom_message: Optional[str] = None
    ) -> Dict[str, Any]:
        """Send notification for a request"""
        notification_data = {
            "type": notification_type,
            "recipients": recipients
        }
        if custom_message:
            notification_data["message"] = custom_message

        return await self._make_request(
            "POST",
            f"{Config.API_ENDPOINTS['tickets']}/{request_id}/notifications",
            json_data=notification_data
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

    async def convert_user_to_technician(
        self,
        user_id: str,
        technician_data: Optional[Dict[str, Any]] = None,
        delete_user_after_conversion: bool = False
    ) -> Dict[str, Any]:
        """Convert a user to technician

        Args:
            user_id: ID of the user to convert
            technician_data: Additional data for technician creation (optional)
            delete_user_after_conversion: Whether to delete the user after conversion

        Returns:
            Dict containing technician creation result and optional user deletion result
        """
        # Get user details first
        user_details = await self.get_admin_user(user_id)

        if "error" in user_details:
            raise Exception(f"Failed to get user details: {user_details['error']}")

        # Prepare technician data from user data
        tech_data = {
            "username": user_details.get("username", user_details.get("email", "")),
            "email": user_details.get("email", ""),
            "first_name": user_details.get("first_name", ""),
            "last_name": user_details.get("last_name", ""),
            "phone": user_details.get("phone", ""),
            "department": user_details.get("department", ""),
            "site_id": user_details.get("site_id", ""),
            "status": user_details.get("status", "active"),
            "role": "technician"
        }

        # Merge with additional technician data if provided
        if technician_data:
            tech_data.update(technician_data)

        # Create technician
        technician_result = await self.create_admin_technician(tech_data)

        if "error" in technician_result:
            raise Exception(f"Failed to create technician: {technician_result['error']}")

        result = {
            "technician_created": technician_result,
            "user_converted": user_id
        }

        # Optionally delete the user after successful technician creation
        if delete_user_after_conversion:
            delete_result = await self.delete_admin_user(user_id)
            result["user_deleted"] = delete_result

        return result

    async def activate_admin_user(self, user_id: str) -> Dict[str, Any]:
        """Activate a user account"""
        return await self.update_admin_user(user_id, {"status": "active"})

    async def deactivate_admin_user(self, user_id: str) -> Dict[str, Any]:
        """Deactivate a user account"""
        return await self.update_admin_user(user_id, {"status": "inactive"})

    async def lock_admin_user(self, user_id: str) -> Dict[str, Any]:
        """Lock a user account"""
        return await self.update_admin_user(user_id, {"status": "locked"})

    async def unlock_admin_user(self, user_id: str) -> Dict[str, Any]:
        """Unlock a user account"""
        return await self.update_admin_user(user_id, {"status": "active"})

    async def reset_admin_user_password(self, user_id: str, new_password: str) -> Dict[str, Any]:
        """Reset user password"""
        return await self.update_admin_user(user_id, {"password": new_password})

    async def change_admin_user_password(
        self,
        user_id: str,
        current_password: str,
        new_password: str
    ) -> Dict[str, Any]:
        """Change user password (requires current password)"""
        update_data = {
            "current_password": current_password,
            "password": new_password
        }
        return await self.update_admin_user(user_id, update_data)

    async def update_admin_user_profile(self, user_id: str, profile_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update user profile information"""
        # Validate profile fields
        valid_fields = [
            "first_name", "last_name", "email", "phone", "department",
            "job_title", "employee_id", "location", "manager", "cost_center"
        ]

        filtered_data = {k: v for k, v in profile_data.items() if k in valid_fields}
        if not filtered_data:
            raise ValueError("No valid profile fields provided")

        return await self.update_admin_user(user_id, filtered_data)

    async def search_admin_users(
        self,
        query: str,
        limit: int = Config.DEFAULT_LIMIT,
        search_fields: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Search users by query"""
        params = {
            "query": query,
            "limit": min(limit, Config.MAX_LIMIT)
        }

        if search_fields:
            params["search_fields"] = ",".join(search_fields)

        return await self._make_request(
            "GET",
            f"{Config.API_ENDPOINTS['admin_users']}/search",
            params=params
        )

    async def get_admin_user_groups(self, user_id: str) -> Dict[str, Any]:
        """Get groups that a user belongs to"""
        return await self._make_request(
            "GET",
            f"{Config.API_ENDPOINTS['admin_users']}/{user_id}/groups"
        )

    async def add_admin_user_to_group(self, user_id: str, group_id: str) -> Dict[str, Any]:
        """Add user to a group"""
        group_data = {"group_id": group_id}
        return await self._make_request(
            "POST",
            f"{Config.API_ENDPOINTS['admin_users']}/{user_id}/groups",
            json_data=group_data
        )

    async def remove_admin_user_from_group(self, user_id: str, group_id: str) -> Dict[str, Any]:
        """Remove user from a group"""
        return await self._make_request(
            "DELETE",
            f"{Config.API_ENDPOINTS['admin_users']}/{user_id}/groups/{group_id}"
        )

    async def bulk_create_admin_users(self, users_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create multiple users at once"""
        if not users_data or len(users_data) > 100:
            raise ValueError("Users data must contain 1-100 user records")

        # Validate each user record
        for i, user_data in enumerate(users_data):
            required_fields = ["username", "email", "first_name", "last_name"]
            missing_fields = [field for field in required_fields if field not in user_data]
            if missing_fields:
                raise ValueError(f"User {i+1}: Missing required fields: {missing_fields}")

        return await self._make_request(
            "POST",
            f"{Config.API_ENDPOINTS['admin_users']}/bulk",
            json_data={"users": users_data}
        )

    async def bulk_update_admin_users(self, updates_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Update multiple users at once"""
        if not updates_data or len(updates_data) > 100:
            raise ValueError("Updates data must contain 1-100 user update records")

        # Validate each update record has user_id
        for i, update_data in enumerate(updates_data):
            if "user_id" not in update_data:
                raise ValueError(f"Update {i+1}: Missing user_id field")

        return await self._make_request(
            "PUT",
            f"{Config.API_ENDPOINTS['admin_users']}/bulk",
            json_data={"updates": updates_data}
        )

    async def get_admin_user_login_history(
        self,
        user_id: str,
        limit: int = 50,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get user login history"""
        params = {"limit": min(limit, 1000)}

        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date

        return await self._make_request(
            "GET",
            f"{Config.API_ENDPOINTS['admin_users']}/{user_id}/login_history",
            params=params
        )

    async def get_admin_user_activity_log(
        self,
        user_id: str,
        limit: int = 50,
        activity_type: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get user activity log"""
        params = {"limit": min(limit, 1000)}

        if activity_type:
            params["activity_type"] = activity_type
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date

        return await self._make_request(
            "GET",
            f"{Config.API_ENDPOINTS['admin_users']}/{user_id}/activity_log",
            params=params
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
