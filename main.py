#!/usr/bin/env python3

import asyncio
import json
import os
from typing import Any, Dict, List, Optional
from dotenv import load_dotenv

from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import (
    CallToolRequest,
    CallToolResult,
    ListToolsRequest,
    ListToolsResult,
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
)

from sdp_client import ServiceDeskPlusClient
from config import Config

# Load environment variables
load_dotenv()

# Create MCP server
server = Server("servicedesk-plus")

@server.list_tools()
async def handle_list_tools() -> ListToolsResult:
    """List all available tools"""
    tools = [
        # ==================== TICKET MANAGEMENT ====================
        Tool(
            name="list_tickets",
            description="Get list of tickets from ServiceDesk Plus with optional filters",
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of tickets (default: 50, maximum: 1000)",
                        "default": 50
                    },
                    "status": {
                        "type": "string",
                        "description": "Filter by ticket status",
                        "enum": ["open", "pending", "resolved", "closed", "cancelled", "on_hold"]
                    },
                    "priority": {
                        "type": "string",
                        "description": "Filter by priority",
                        "enum": ["low", "medium", "high", "critical"]
                    },
                    "requester": {
                        "type": "string",
                        "description": "Filter by requester (email or ID)"
                    }
                }
            }
        ),
        Tool(
            name="get_ticket",
            description="Get detailed information about a ticket by ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "ticket_id": {
                        "type": "string",
                        "description": "ID of the ticket to get information"
                    }
                },
                "required": ["ticket_id"]
            }
        ),
        Tool(
            name="create_ticket",
            description="Create a new ticket in ServiceDesk Plus",
            inputSchema={
                "type": "object",
                "properties": {
                    "subject": {
                        "type": "string",
                        "description": "Title of the ticket"
                    },
                    "description": {
                        "type": "string",
                        "description": "Detailed description of the ticket"
                    },
                    "requester": {
                        "type": "string",
                        "description": "Email or ID of the requester"
                    },
                    "priority": {
                        "type": "string",
                        "description": "Priority level",
                        "enum": ["low", "medium", "high", "critical"]
                    },
                    "category": {
                        "type": "string",
                        "description": "Category of the ticket"
                    },
                    "technician": {
                        "type": "string",
                        "description": "ID of the assigned technician"
                    }
                },
                "required": ["subject", "description", "requester"]
            }
        ),
        Tool(
            name="update_ticket",
            description="Update information of a ticket",
            inputSchema={
                "type": "object",
                "properties": {
                    "ticket_id": {
                        "type": "string",
                        "description": "ID of the ticket to update"
                    },
                    "subject": {
                        "type": "string",
                        "description": "New title of the ticket"
                    },
                    "description": {
                        "type": "string",
                        "description": "New description of the ticket"
                    },
                    "status": {
                        "type": "string",
                        "description": "New status",
                        "enum": ["open", "pending", "resolved", "closed", "cancelled", "on_hold"]
                    },
                    "priority": {
                        "type": "string",
                        "description": "New priority level",
                        "enum": ["low", "medium", "high", "critical"]
                    },
                    "technician": {
                        "type": "string",
                        "description": "ID of the new assigned technician"
                    }
                },
                "required": ["ticket_id"]
            }
        ),
        Tool(
            name="delete_ticket",
            description="Delete a ticket",
            inputSchema={
                "type": "object",
                "properties": {
                    "ticket_id": {
                        "type": "string",
                        "description": "ID of the ticket to delete"
                    }
                },
                "required": ["ticket_id"]
            }
        ),
        Tool(
            name="search_tickets",
            description="Search tickets by keyword",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search keyword"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of results (default: 50, maximum: 1000)",
                        "default": 50
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="add_ticket_comment",
            description="Add comment to a ticket",
            inputSchema={
                "type": "object",
                "properties": {
                    "ticket_id": {
                        "type": "string",
                        "description": "ID of the ticket"
                    },
                    "comment": {
                        "type": "string",
                        "description": "Content of the comment"
                    }
                },
                "required": ["ticket_id", "comment"]
            }
        ),
        Tool(
            name="get_ticket_comments",
            description="Get list of comments of a ticket",
            inputSchema={
                "type": "object",
                "properties": {
                    "ticket_id": {
                        "type": "string",
                        "description": "ID of the ticket"
                    }
                },
                "required": ["ticket_id"]
            }
        ),

        # ==================== ADVANCED REQUEST MANAGEMENT ====================

        Tool(
            name="assign_request",
            description="Assign request to technician and group",
            inputSchema={
                "type": "object",
                "properties": {
                    "request_id": {
                        "type": "string",
                        "description": "ID of the request to assign"
                    },
                    "technician_id": {
                        "type": "string",
                        "description": "ID of the technician"
                    },
                    "group_id": {
                        "type": "string",
                        "description": "ID of the group (optional)"
                    }
                },
                "required": ["request_id", "technician_id"]
            }
        ),
        Tool(
            name="reassign_request",
            description="Reassign request to another technician",
            inputSchema={
                "type": "object",
                "properties": {
                    "request_id": {
                        "type": "string",
                        "description": "ID of the request to reassign"
                    },
                    "technician_id": {
                        "type": "string",
                        "description": "ID of the new technician"
                    },
                    "reason": {
                        "type": "string",
                        "description": "Reason for reassignment (optional)"
                    }
                },
                "required": ["request_id", "technician_id"]
            }
        ),
        Tool(
            name="escalate_request",
            description="Escalate request to a higher level",
            inputSchema={
                "type": "object",
                "properties": {
                    "request_id": {
                        "type": "string",
                        "description": "ID of the request to escalate"
                    },
                    "escalation_level": {
                        "type": "string",
                        "description": "Escalation level"
                    },
                    "reason": {
                        "type": "string",
                        "description": "Reason for escalation"
                    }
                },
                "required": ["request_id", "escalation_level", "reason"]
            }
        ),
        Tool(
            name="approve_request",
            description="Approve request",
            inputSchema={
                "type": "object",
                "properties": {
                    "request_id": {
                        "type": "string",
                        "description": "ID of the request to approve"
                    },
                    "approval_comments": {
                        "type": "string",
                        "description": "Approval comments (optional)"
                    }
                },
                "required": ["request_id"]
            }
        ),
        Tool(
            name="reject_request",
            description="Reject request",
            inputSchema={
                "type": "object",
                "properties": {
                    "request_id": {
                        "type": "string",
                        "description": "ID of the request to reject"
                    },
                    "rejection_reason": {
                        "type": "string",
                        "description": "Reason for rejection"
                    },
                    "comments": {
                        "type": "string",
                        "description": "Additional comments (optional)"
                    }
                },
                "required": ["request_id", "rejection_reason"]
            }
        ),
        Tool(
            name="get_request_approvals",
            description="Get approval information of request",
            inputSchema={
                "type": "object",
                "properties": {
                    "request_id": {
                        "type": "string",
                        "description": "ID of the request"
                    }
                },
                "required": ["request_id"]
            }
        ),
        Tool(
            name="get_request_attachments",
            description="Get list of attachments of request",
            inputSchema={
                "type": "object",
                "properties": {
                    "request_id": {
                        "type": "string",
                        "description": "ID of the request"
                    }
                },
                "required": ["request_id"]
            }
        ),
        Tool(
            name="add_request_attachment",
            description="Add attachment to request",
            inputSchema={
                "type": "object",
                "properties": {
                    "request_id": {
                        "type": "string",
                        "description": "ID of the request"
                    },
                    "file_path": {
                        "type": "string",
                        "description": "File path to upload"
                    },
                    "description": {
                        "type": "string",
                        "description": "Description of attachment (optional)"
                    }
                },
                "required": ["request_id", "file_path"]
            }
        ),
        Tool(
            name="delete_request_attachment",
            description="Delete attachment from request",
            inputSchema={
                "type": "object",
                "properties": {
                    "request_id": {
                        "type": "string",
                        "description": "ID of the request"
                    },
                    "attachment_id": {
                        "type": "string",
                        "description": "ID of the attachment to delete"
                    }
                },
                "required": ["request_id", "attachment_id"]
            }
        ),
        Tool(
            name="get_request_history",
            description="Get history/timeline of request",
            inputSchema={
                "type": "object",
                "properties": {
                    "request_id": {
                        "type": "string",
                        "description": "ID of the request"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of records (default: 50, maximum: 1000)",
                        "default": 50
                    }
                },
                "required": ["request_id"]
            }
        ),
        Tool(
            name="get_request_sla_details",
            description="Get SLA information of request",
            inputSchema={
                "type": "object",
                "properties": {
                    "request_id": {
                        "type": "string",
                        "description": "ID of the request"
                    }
                },
                "required": ["request_id"]
            }
        ),
        Tool(
            name="update_request_sla",
            description="Update SLA for request",
            inputSchema={
                "type": "object",
                "properties": {
                    "request_id": {
                        "type": "string",
                        "description": "ID of the request"
                    },
                    "sla_data": {
                        "type": "object",
                        "description": "SLA data to update"
                    }
                },
                "required": ["request_id", "sla_data"]
            }
        ),
        Tool(
            name="get_request_templates",
            description="Get list of available request templates",
            inputSchema={
                "type": "object",
                "properties": {
                    "category": {
                        "type": "string",
                        "description": "Filter by category (optional)"
                    }
                }
            }
        ),
        Tool(
            name="create_request_from_template",
            description="Create request from template",
            inputSchema={
                "type": "object",
                "properties": {
                    "template_id": {
                        "type": "string",
                        "description": "ID of the template"
                    },
                    "request_data": {
                        "type": "object",
                        "description": "Additional request data"
                    }
                },
                "required": ["template_id", "request_data"]
            }
        ),
        Tool(
            name="close_request",
            description="Close request with closure code and resolution",
            inputSchema={
                "type": "object",
                "properties": {
                    "request_id": {
                        "type": "string",
                        "description": "ID of the request to close"
                    },
                    "closure_code": {
                        "type": "string",
                        "description": "Request closure code"
                    },
                    "resolution": {
                        "type": "string",
                        "description": "Resolution description"
                    }
                },
                "required": ["request_id", "closure_code", "resolution"]
            }
        ),
        Tool(
            name="get_closure_codes",
            description="Get list of available closure codes",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="get_request_worklog",
            description="Get worklog entries of request",
            inputSchema={
                "type": "object",
                "properties": {
                    "request_id": {
                        "type": "string",
                        "description": "ID of the request"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of records (default: 50, maximum: 1000)",
                        "default": 50
                    }
                },
                "required": ["request_id"]
            }
        ),
        Tool(
            name="add_worklog_entry",
            description="Add worklog entry to request",
            inputSchema={
                "type": "object",
                "properties": {
                    "request_id": {
                        "type": "string",
                        "description": "ID of the request"
                    },
                    "description": {
                        "type": "string",
                        "description": "Description of the work"
                    },
                    "time_spent": {
                        "type": "string",
                        "description": "Time spent (optional)"
                    },
                    "technician_id": {
                        "type": "string",
                        "description": "ID of the technician (optional)"
                    }
                },
                "required": ["request_id", "description"]
            }
        ),
        Tool(
            name="update_worklog_entry",
            description="Update worklog entry",
            inputSchema={
                "type": "object",
                "properties": {
                    "request_id": {
                        "type": "string",
                        "description": "ID of the request"
                    },
                    "worklog_id": {
                        "type": "string",
                        "description": "ID of the worklog entry"
                    },
                    "update_data": {
                        "type": "object",
                        "description": "Update data"
                    }
                },
                "required": ["request_id", "worklog_id", "update_data"]
            }
        ),
        Tool(
            name="get_request_custom_fields",
            description="Get custom fields of request",
            inputSchema={
                "type": "object",
                "properties": {
                    "request_id": {
                        "type": "string",
                        "description": "ID of the request"
                    }
                },
                "required": ["request_id"]
            }
        ),
        Tool(
            name="update_request_custom_fields",
            description="Update custom fields of request",
            inputSchema={
                "type": "object",
                "properties": {
                    "request_id": {
                        "type": "string",
                        "description": "ID of the request"
                    },
                    "custom_fields": {
                        "type": "object",
                        "description": "Custom fields to update"
                    }
                },
                "required": ["request_id", "custom_fields"]
            }
        ),
        Tool(
            name="get_request_feedback",
            description="Get feedback/survey of request",
            inputSchema={
                "type": "object",
                "properties": {
                    "request_id": {
                        "type": "string",
                        "description": "ID of the request"
                    }
                },
                "required": ["request_id"]
            }
        ),
        Tool(
            name="submit_request_feedback",
            description="Submit feedback for request",
            inputSchema={
                "type": "object",
                "properties": {
                    "request_id": {
                        "type": "string",
                        "description": "ID of the request"
                    },
                    "rating": {
                        "type": "integer",
                        "description": "Rating (1-5)"
                    },
                    "comments": {
                        "type": "string",
                        "description": "Comments (optional)"
                    },
                    "survey_responses": {
                        "type": "object",
                        "description": "Survey responses (optional)"
                    }
                },
                "required": ["request_id", "rating"]
            }
        ),
        Tool(
            name="get_request_notifications",
            description="Get list of notifications sent for request",
            inputSchema={
                "type": "object",
                "properties": {
                    "request_id": {
                        "type": "string",
                        "description": "ID of the request"
                    }
                },
                "required": ["request_id"]
            }
        ),
        Tool(
            name="send_request_notification",
            description="Send notification for request",
            inputSchema={
                "type": "object",
                "properties": {
                    "request_id": {
                        "type": "string",
                        "description": "ID of the request"
                    },
                    "notification_type": {
                        "type": "string",
                        "description": "Type of notification"
                    },
                    "recipients": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of recipient emails"
                    },
                    "custom_message": {
                        "type": "string",
                        "description": "Custom message (optional)"
                    }
                },
                "required": ["request_id", "notification_type", "recipients"]
            }
        ),

        # ==================== USER MANAGEMENT ====================
        Tool(
            name="list_users",
            description="Get list of users from ServiceDesk Plus",
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of users (default: 50, maximum: 1000)",
                        "default": 50
                    }
                }
            }
        ),
        Tool(
            name="get_user",
            description="Get detailed information about a user",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "ID of the user to get information"
                    }
                },
                "required": ["user_id"]
            }
        ),
        Tool(
            name="list_technicians",
            description="Get list of technicians from ServiceDesk Plus",
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of technicians (default: 50, maximum: 1000)",
                        "default": 50
                    }
                }
            }
        ),

        # ==================== CMDB - CONFIGURATION ITEMS ====================
        Tool(
            name="list_configuration_items",
            description="Get list of Configuration Items (CIs) from CMDB",
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of CIs (default: 50, maximum: 1000)",
                        "default": 50
                    },
                    "ci_type": {
                        "type": "string",
                        "description": "Filter by CI type (server, network_device, software, etc.)"
                    },
                    "status": {
                        "type": "string",
                        "description": "Filter by CI status",
                        "enum": ["active", "inactive", "under_maintenance", "retired"]
                    }
                }
            }
        ),
        Tool(
            name="get_configuration_item",
            description="Get detailed information about a Configuration Item",
            inputSchema={
                "type": "object",
                "properties": {
                    "ci_id": {
                        "type": "string",
                        "description": "ID of the Configuration Item"
                    }
                },
                "required": ["ci_id"]
            }
        ),
        Tool(
            name="create_configuration_item",
            description="Create a new Configuration Item in CMDB",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Name of the Configuration Item"
                    },
                    "ci_type": {
                        "type": "string",
                        "description": "CI type (server, network_device, software, etc.)"
                    },
                    "description": {
                        "type": "string",
                        "description": "Detailed description"
                    },
                    "status": {
                        "type": "string",
                        "description": "Status",
                        "enum": ["active", "inactive", "under_maintenance", "retired"]
                    },
                    "location": {
                        "type": "string",
                        "description": "Location"
                    },
                    "owner": {
                        "type": "string",
                        "description": "Owner"
                    }
                },
                "required": ["name", "ci_type"]
            }
        ),
        Tool(
            name="update_configuration_item",
            description="Update Configuration Item information",
            inputSchema={
                "type": "object",
                "properties": {
                    "ci_id": {
                        "type": "string",
                        "description": "ID of the Configuration Item"
                    },
                    "name": {
                        "type": "string",
                        "description": "New name"
                    },
                    "description": {
                        "type": "string",
                        "description": "New description"
                    },
                    "status": {
                        "type": "string",
                        "description": "New status",
                        "enum": ["active", "inactive", "under_maintenance", "retired"]
                    },
                    "location": {
                        "type": "string",
                        "description": "New location"
                    },
                    "owner": {
                        "type": "string",
                        "description": "New owner"
                    }
                },
                "required": ["ci_id"]
            }
        ),
        Tool(
            name="delete_configuration_item",
            description="Delete Configuration Item",
            inputSchema={
                "type": "object",
                "properties": {
                    "ci_id": {
                        "type": "string",
                        "description": "ID of the Configuration Item to delete"
                    }
                },
                "required": ["ci_id"]
            }
        ),
        Tool(
            name="get_ci_types",
            description="Get list of available Configuration Item types",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="get_ci_relationships",
            description="Get list of relationships of a Configuration Item",
            inputSchema={
                "type": "object",
                "properties": {
                    "ci_id": {
                        "type": "string",
                        "description": "ID of the Configuration Item"
                    }
                },
                "required": ["ci_id"]
            }
        ),

        # ==================== ASSET MANAGEMENT ====================
        Tool(
            name="list_assets",
            description="Get list of assets from ServiceDesk Plus with filters",
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of assets (default: 50, maximum: 1000)",
                        "default": 50
                    },
                    "asset_type": {
                        "type": "string",
                        "description": "Filter by asset type"
                    },
                    "status": {
                        "type": "string",
                        "description": "Filter by asset status",
                        "enum": ["in_use", "in_stock", "under_maintenance", "retired", "lost", "stolen"]
                    },
                    "location": {
                        "type": "string",
                        "description": "Filter by location"
                    }
                }
            }
        ),
        Tool(
            name="get_asset",
            description="Get detailed information about an asset",
            inputSchema={
                "type": "object",
                "properties": {
                    "asset_id": {
                        "type": "string",
                        "description": "ID of the asset to get information"
                    }
                },
                "required": ["asset_id"]
            }
        ),
        Tool(
            name="create_asset",
            description="Create a new asset",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Name of the asset"
                    },
                    "asset_type": {
                        "type": "string",
                        "description": "Asset type"
                    },
                    "description": {
                        "type": "string",
                        "description": "Detailed description"
                    },
                    "status": {
                        "type": "string",
                        "description": "Status",
                        "enum": ["in_use", "in_stock", "under_maintenance", "retired", "lost", "stolen"]
                    },
                    "location": {
                        "type": "string",
                        "description": "Location"
                    },
                    "assigned_to": {
                        "type": "string",
                        "description": "Assigned to"
                    },
                    "vendor": {
                        "type": "string",
                        "description": "Vendor"
                    },
                    "model": {
                        "type": "string",
                        "description": "Model"
                    },
                    "serial_number": {
                        "type": "string",
                        "description": "Serial number"
                    }
                },
                "required": ["name", "asset_type"]
            }
        ),
        Tool(
            name="update_asset",
            description="Update asset information",
            inputSchema={
                "type": "object",
                "properties": {
                    "asset_id": {
                        "type": "string",
                        "description": "ID of the asset"
                    },
                    "name": {
                        "type": "string",
                        "description": "New name"
                    },
                    "description": {
                        "type": "string",
                        "description": "New description"
                    },
                    "status": {
                        "type": "string",
                        "description": "New status",
                        "enum": ["in_use", "in_stock", "under_maintenance", "retired", "lost", "stolen"]
                    },
                    "location": {
                        "type": "string",
                        "description": "New location"
                    },
                    "assigned_to": {
                        "type": "string",
                        "description": "New assigned to"
                    }
                },
                "required": ["asset_id"]
            }
        ),
        Tool(
            name="delete_asset",
            description="Delete asset",
            inputSchema={
                "type": "object",
                "properties": {
                    "asset_id": {
                        "type": "string",
                        "description": "ID of the asset to delete"
                    }
                },
                "required": ["asset_id"]
            }
        ),
        Tool(
            name="get_asset_types",
            description="Get list of available asset types",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="get_asset_categories",
            description="Get list of available asset categories",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="get_asset_locations",
            description="Get list of available asset locations",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="get_asset_models",
            description="Get list of available asset models",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="get_asset_vendors",
            description="Get list of available asset vendors",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),

        # ==================== SOFTWARE LICENSE MANAGEMENT ====================
        Tool(
            name="list_software_licenses",
            description="Get list of software licenses",
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of licenses (default: 50, maximum: 1000)",
                        "default": 50
                    },
                    "product": {
                        "type": "string",
                        "description": "Filter by product"
                    },
                    "vendor": {
                        "type": "string",
                        "description": "Filter by vendor"
                    }
                }
            }
        ),
        Tool(
            name="get_software_license",
            description="Get detailed information about a software license",
            inputSchema={
                "type": "object",
                "properties": {
                    "license_id": {
                        "type": "string",
                        "description": "ID of the software license"
                    }
                },
                "required": ["license_id"]
            }
        ),
        Tool(
            name="create_software_license",
            description="Create a new software license",
            inputSchema={
                "type": "object",
                "properties": {
                    "product": {
                        "type": "string",
                        "description": "Product name"
                    },
                    "license_type": {
                        "type": "string",
                        "description": "License type"
                    },
                    "total_licenses": {
                        "type": "integer",
                        "description": "Total number of licenses"
                    },
                    "vendor": {
                        "type": "string",
                        "description": "Vendor"
                    },
                    "purchase_date": {
                        "type": "string",
                        "description": "Purchase date (YYYY-MM-DD)"
                    },
                    "expiry_date": {
                        "type": "string",
                        "description": "Expiry date (YYYY-MM-DD)"
                    },
                    "cost": {
                        "type": "number",
                        "description": "Cost"
                    }
                },
                "required": ["product", "license_type", "total_licenses"]
            }
        ),
        Tool(
            name="update_software_license",
            description="Update software license",
            inputSchema={
                "type": "object",
                "properties": {
                    "license_id": {
                        "type": "string",
                        "description": "ID of the software license"
                    },
                    "product": {
                        "type": "string",
                        "description": "New product name"
                    },
                    "total_licenses": {
                        "type": "integer",
                        "description": "New total number of licenses"
                    },
                    "expiry_date": {
                        "type": "string",
                        "description": "New expiry date (YYYY-MM-DD)"
                    }
                },
                "required": ["license_id"]
            }
        ),
        Tool(
            name="get_software_products",
            description="Get list of available software products",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="get_license_types",
            description="Get list of available license types",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),

        # ==================== CONTRACT MANAGEMENT ====================
        Tool(
            name="list_contracts",
            description="Get list of contracts",
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of contracts (default: 50, maximum: 1000)",
                        "default": 50
                    },
                    "contract_type": {
                        "type": "string",
                        "description": "Filter by contract type"
                    },
                    "status": {
                        "type": "string",
                        "description": "Filter by contract status",
                        "enum": ["active", "expired", "pending", "terminated"]
                    },
                    "vendor": {
                        "type": "string",
                        "description": "Filter by vendor"
                    }
                }
            }
        ),
        Tool(
            name="get_contract",
            description="Get detailed information about a contract",
            inputSchema={
                "type": "object",
                "properties": {
                    "contract_id": {
                        "type": "string",
                        "description": "ID of the contract"
                    }
                },
                "required": ["contract_id"]
            }
        ),
        Tool(
            name="create_contract",
            description="Create a new contract",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Contract name"
                    },
                    "vendor": {
                        "type": "string",
                        "description": "Vendor"
                    },
                    "start_date": {
                        "type": "string",
                        "description": "Start date (YYYY-MM-DD)"
                    },
                    "end_date": {
                        "type": "string",
                        "description": "End date (YYYY-MM-DD)"
                    },
                    "contract_type": {
                        "type": "string",
                        "description": "Contract type"
                    },
                    "value": {
                        "type": "number",
                        "description": "Contract value"
                    },
                    "description": {
                        "type": "string",
                        "description": "Detailed description"
                    }
                },
                "required": ["name", "vendor", "start_date", "end_date"]
            }
        ),
        Tool(
            name="update_contract",
            description="Update contract",
            inputSchema={
                "type": "object",
                "properties": {
                    "contract_id": {
                        "type": "string",
                        "description": "ID of the contract"
                    },
                    "name": {
                        "type": "string",
                        "description": "New name"
                    },
                    "end_date": {
                        "type": "string",
                        "description": "New end date (YYYY-MM-DD)"
                    },
                    "value": {
                        "type": "number",
                        "description": "New value"
                    },
                    "status": {
                        "type": "string",
                        "description": "New status",
                        "enum": ["active", "expired", "pending", "terminated"]
                    }
                },
                "required": ["contract_id"]
            }
        ),
        Tool(
            name="get_contract_types",
            description="Get list of available contract types",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="get_contract_vendors",
            description="Get list of available contract vendors",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),

        # ==================== PURCHASE ORDER MANAGEMENT ====================
        Tool(
            name="list_purchase_orders",
            description="Get list of purchase orders",
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of POs (default: 50, maximum: 1000)",
                        "default": 50
                    },
                    "status": {
                        "type": "string",
                        "description": "Filter by PO status",
                        "enum": ["draft", "pending_approval", "approved", "ordered", "received", "cancelled"]
                    },
                    "vendor": {
                        "type": "string",
                        "description": "Filter by vendor"
                    }
                }
            }
        ),
        Tool(
            name="get_purchase_order",
            description="Get detailed information about a purchase order",
            inputSchema={
                "type": "object",
                "properties": {
                    "po_id": {
                        "type": "string",
                        "description": "ID of the purchase order"
                    }
                },
                "required": ["po_id"]
            }
        ),
        Tool(
            name="create_purchase_order",
            description="Create a new purchase order",
            inputSchema={
                "type": "object",
                "properties": {
                    "vendor": {
                        "type": "string",
                        "description": "Vendor"
                    },
                    "items": {
                        "type": "array",
                        "description": "List of items",
                        "items": {
                            "type": "object",
                            "properties": {
                                "name": {"type": "string"},
                                "quantity": {"type": "integer"},
                                "unit_price": {"type": "number"}
                            }
                        }
                    },
                    "description": {
                        "type": "string",
                        "description": "Description"
                    },
                    "expected_delivery": {
                        "type": "string",
                        "description": "Expected delivery date (YYYY-MM-DD)"
                    }
                },
                "required": ["vendor", "items"]
            }
        ),
        Tool(
            name="update_purchase_order",
            description="Update purchase order",
            inputSchema={
                "type": "object",
                "properties": {
                    "po_id": {
                        "type": "string",
                        "description": "ID of the purchase order"
                    },
                    "status": {
                        "type": "string",
                        "description": "New status",
                        "enum": ["draft", "pending_approval", "approved", "ordered", "received", "cancelled"]
                    },
                    "expected_delivery": {
                        "type": "string",
                        "description": "New expected delivery date (YYYY-MM-DD)"
                    }
                },
                "required": ["po_id"]
            }
        ),
        Tool(
            name="get_po_statuses",
            description="Get list of available PO statuses",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),

        # ==================== VENDOR MANAGEMENT ====================
        Tool(
            name="list_vendors",
            description="Get list of vendors",
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of vendors (default: 50, maximum: 1000)",
                        "default": 50
                    },
                    "vendor_type": {
                        "type": "string",
                        "description": "Filter by vendor type"
                    }
                }
            }
        ),
        Tool(
            name="get_vendor",
            description="Get detailed information about a vendor",
            inputSchema={
                "type": "object",
                "properties": {
                    "vendor_id": {
                        "type": "string",
                        "description": "ID of the vendor"
                    }
                },
                "required": ["vendor_id"]
            }
        ),
        Tool(
            name="create_vendor",
            description="Create a new vendor",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Vendor name"
                    },
                    "email": {
                        "type": "string",
                        "description": "Email"
                    },
                    "phone": {
                        "type": "string",
                        "description": "Phone number"
                    },
                    "address": {
                        "type": "string",
                        "description": "Address"
                    },
                    "vendor_type": {
                        "type": "string",
                        "description": "Vendor type"
                    },
                    "website": {
                        "type": "string",
                        "description": "Website"
                    }
                },
                "required": ["name", "email"]
            }
        ),
        Tool(
            name="update_vendor",
            description="Update vendor",
            inputSchema={
                "type": "object",
                "properties": {
                    "vendor_id": {
                        "type": "string",
                        "description": "ID of the vendor"
                    },
                    "name": {
                        "type": "string",
                        "description": "New name"
                    },
                    "email": {
                        "type": "string",
                        "description": "New email"
                    },
                    "phone": {
                        "type": "string",
                        "description": "New phone number"
                    },
                    "address": {
                        "type": "string",
                        "description": "New address"
                    }
                },
                "required": ["vendor_id"]
            }
        ),
        Tool(
            name="get_vendor_types",
            description="Get list of available vendor types",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),

        # ==================== ADMIN MANAGEMENT - SITES ====================
        Tool(
            name="list_sites",
            description="Get list of sites from ServiceDesk Plus",
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of sites (default: 50, maximum: 1000)",
                        "default": 50
                    },
                    "site_type": {
                        "type": "string",
                        "description": "Filter by site type",
                        "enum": ["headquarters", "branch_office", "data_center", "warehouse", "retail_store", "manufacturing_plant"]
                    },
                    "status": {
                        "type": "string",
                        "description": "Filter by site status"
                    }
                }
            }
        ),
        Tool(
            name="get_site",
            description="Get detailed information about a site",
            inputSchema={
                "type": "object",
                "properties": {
                    "site_id": {
                        "type": "string",
                        "description": "ID of the site to get information"
                    }
                },
                "required": ["site_id"]
            }
        ),
        Tool(
            name="create_site",
            description="Create a new site in ServiceDesk Plus",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Name of the site"
                    },
                    "site_type": {
                        "type": "string",
                        "description": "Site type",
                        "enum": ["headquarters", "branch_office", "data_center", "warehouse", "retail_store", "manufacturing_plant"]
                    },
                    "address": {
                        "type": "string",
                        "description": "Address of the site"
                    },
                    "city": {
                        "type": "string",
                        "description": "City"
                    },
                    "state": {
                        "type": "string",
                        "description": "State/Province"
                    },
                    "country": {
                        "type": "string",
                        "description": "Country"
                    },
                    "zip_code": {
                        "type": "string",
                        "description": "Zip code"
                    },
                    "phone": {
                        "type": "string",
                        "description": "Phone number"
                    },
                    "email": {
                        "type": "string",
                        "description": "Contact email"
                    },
                    "description": {
                        "type": "string",
                        "description": "Detailed description"
                    }
                },
                "required": ["name", "site_type"]
            }
        ),
        Tool(
            name="update_site",
            description="Update information of a site",
            inputSchema={
                "type": "object",
                "properties": {
                    "site_id": {
                        "type": "string",
                        "description": "ID of the site to update"
                    },
                    "name": {
                        "type": "string",
                        "description": "New name of the site"
                    },
                    "site_type": {
                        "type": "string",
                        "description": "New site type",
                        "enum": ["headquarters", "branch_office", "data_center", "warehouse", "retail_store", "manufacturing_plant"]
                    },
                    "address": {
                        "type": "string",
                        "description": "New address"
                    },
                    "city": {
                        "type": "string",
                        "description": "New city"
                    },
                    "state": {
                        "type": "string",
                        "description": "New state/province"
                    },
                    "country": {
                        "type": "string",
                        "description": "New country"
                    },
                    "zip_code": {
                        "type": "string",
                        "description": "New zip code"
                    },
                    "phone": {
                        "type": "string",
                        "description": "New phone number"
                    },
                    "email": {
                        "type": "string",
                        "description": "New contact email"
                    },
                    "description": {
                        "type": "string",
                        "description": "New description"
                    }
                },
                "required": ["site_id"]
            }
        ),
        Tool(
            name="delete_site",
            description="Delete a site",
            inputSchema={
                "type": "object",
                "properties": {
                    "site_id": {
                        "type": "string",
                        "description": "ID of the site to delete"
                    }
                },
                "required": ["site_id"]
            }
        ),
        Tool(
            name="get_site_types",
            description="Get list of available site types",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),

        # ==================== ADMIN MANAGEMENT - USER GROUPS ====================
        Tool(
            name="list_user_groups",
            description="Get list of user groups from ServiceDesk Plus",
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of user groups (default: 50, maximum: 1000)",
                        "default": 50
                    },
                    "group_type": {
                        "type": "string",
                        "description": "Filter by group type",
                        "enum": ["department", "project", "location_based", "role_based", "custom"]
                    },
                    "site_id": {
                        "type": "string",
                        "description": "Filter by site ID"
                    }
                }
            }
        ),
        Tool(
            name="get_user_group",
            description="Get detailed information about a user group",
            inputSchema={
                "type": "object",
                "properties": {
                    "group_id": {
                        "type": "string",
                        "description": "ID of the user group to get information"
                    }
                },
                "required": ["group_id"]
            }
        ),
        Tool(
            name="create_user_group",
            description="Create a new user group in ServiceDesk Plus",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Name of the user group"
                    },
                    "group_type": {
                        "type": "string",
                        "description": "Group type",
                        "enum": ["department", "project", "location_based", "role_based", "custom"]
                    },
                    "description": {
                        "type": "string",
                        "description": "Detailed description"
                    },
                    "site_id": {
                        "type": "string",
                        "description": "ID of the associated site"
                    },
                    "manager": {
                        "type": "string",
                        "description": "ID of the manager"
                    }
                },
                "required": ["name", "group_type"]
            }
        ),
        Tool(
            name="update_user_group",
            description="Update information of a user group",
            inputSchema={
                "type": "object",
                "properties": {
                    "group_id": {
                        "type": "string",
                        "description": "ID of the user group to update"
                    },
                    "name": {
                        "type": "string",
                        "description": "New name of the user group"
                    },
                    "group_type": {
                        "type": "string",
                        "description": "New group type",
                        "enum": ["department", "project", "location_based", "role_based", "custom"]
                    },
                    "description": {
                        "type": "string",
                        "description": "New description"
                    },
                    "site_id": {
                        "type": "string",
                        "description": "New associated site ID"
                    },
                    "manager": {
                        "type": "string",
                        "description": "New manager ID"
                    }
                },
                "required": ["group_id"]
            }
        ),
        Tool(
            name="delete_user_group",
            description="Delete a user group",
            inputSchema={
                "type": "object",
                "properties": {
                    "group_id": {
                        "type": "string",
                        "description": "ID of the user group to delete"
                    }
                },
                "required": ["group_id"]
            }
        ),
        Tool(
            name="get_group_types",
            description="Get list of available user group types",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="get_group_permissions",
            description="Get list of permissions of a user group",
            inputSchema={
                "type": "object",
                "properties": {
                    "group_id": {
                        "type": "string",
                        "description": "ID of the user group"
                    }
                },
                "required": ["group_id"]
            }
        ),
        Tool(
            name="update_group_permissions",
            description="Update permissions for a user group",
            inputSchema={
                "type": "object",
                "properties": {
                    "group_id": {
                        "type": "string",
                        "description": "ID of the user group"
                    },
                    "permissions": {
                        "type": "object",
                        "description": "Object containing permissions with corresponding levels",
                        "additionalProperties": {
                            "type": "string",
                            "enum": ["none", "read", "write", "admin"]
                        }
                    }
                },
                "required": ["group_id", "permissions"]
            }
        ),

        # ==================== ADMIN MANAGEMENT - USERS & TECHNICIANS ====================
        Tool(
            name="list_admin_users",
            description="Get list of users (admin) from ServiceDesk Plus",
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of users (default: 50, maximum: 1000)",
                        "default": 50
                    },
                    "status": {
                        "type": "string",
                        "description": "Filter by user status",
                        "enum": ["active", "inactive", "locked", "pending_activation"]
                    },
                    "role": {
                        "type": "string",
                        "description": "Filter by role",
                        "enum": ["admin", "manager", "technician", "user", "viewer"]
                    },
                    "site_id": {
                        "type": "string",
                        "description": "Filter by site ID"
                    }
                }
            }
        ),
        Tool(
            name="get_admin_user",
            description="Get detailed information about a user (admin)",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "ID of the user to get information"
                    }
                },
                "required": ["user_id"]
            }
        ),
        Tool(
            name="create_admin_user",
            description="Create a new user (admin) in ServiceDesk Plus",
            inputSchema={
                "type": "object",
                "properties": {
                    "username": {
                        "type": "string",
                        "description": "Username"
                    },
                    "email": {
                        "type": "string",
                        "description": "Email of the user"
                    },
                    "first_name": {
                        "type": "string",
                        "description": "First name"
                    },
                    "last_name": {
                        "type": "string",
                        "description": "Last name"
                    },
                    "password": {
                        "type": "string",
                        "description": "Password"
                    },
                    "role": {
                        "type": "string",
                        "description": "Role of the user",
                        "enum": ["admin", "manager", "technician", "user", "viewer"]
                    },
                    "site_id": {
                        "type": "string",
                        "description": "ID of the site"
                    },
                    "department": {
                        "type": "string",
                        "description": "Department"
                    },
                    "phone": {
                        "type": "string",
                        "description": "Phone number"
                    },
                    "status": {
                        "type": "string",
                        "description": "Status",
                        "enum": ["active", "inactive", "locked", "pending_activation"]
                    }
                },
                "required": ["username", "email", "first_name", "last_name"]
            }
        ),
        Tool(
            name="update_admin_user",
            description="Update information of a user (admin)",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "ID of the user to update"
                    },
                    "username": {
                        "type": "string",
                        "description": "New username"
                    },
                    "email": {
                        "type": "string",
                        "description": "New email"
                    },
                    "first_name": {
                        "type": "string",
                        "description": "New first name"
                    },
                    "last_name": {
                        "type": "string",
                        "description": "New last name"
                    },
                    "role": {
                        "type": "string",
                        "description": "New role",
                        "enum": ["admin", "manager", "technician", "user", "viewer"]
                    },
                    "site_id": {
                        "type": "string",
                        "description": "New site ID"
                    },
                    "department": {
                        "type": "string",
                        "description": "New department"
                    },
                    "phone": {
                        "type": "string",
                        "description": "New phone number"
                    },
                    "status": {
                        "type": "string",
                        "description": "New status",
                        "enum": ["active", "inactive", "locked", "pending_activation"]
                    }
                },
                "required": ["user_id"]
            }
        ),
        Tool(
            name="delete_admin_user",
            description="Delete a user (admin)",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "ID of the user to delete"
                    }
                },
                "required": ["user_id"]
            }
        ),
        Tool(
            name="list_admin_technicians",
            description="Get list of technicians (admin) from ServiceDesk Plus",
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of technicians (default: 50, maximum: 1000)",
                        "default": 50
                    },
                    "status": {
                        "type": "string",
                        "description": "Filter by technician status",
                        "enum": ["active", "inactive", "locked", "pending_activation"]
                    },
                    "role": {
                        "type": "string",
                        "description": "Filter by role",
                        "enum": ["admin", "manager", "technician", "user", "viewer"]
                    },
                    "site_id": {
                        "type": "string",
                        "description": "Filter by site ID"
                    }
                }
            }
        ),
        Tool(
            name="get_admin_technician",
            description="Get detailed information about a technician (admin)",
            inputSchema={
                "type": "object",
                "properties": {
                    "technician_id": {
                        "type": "string",
                        "description": "ID of the technician to get information"
                    }
                },
                "required": ["technician_id"]
            }
        ),
        Tool(
            name="create_admin_technician",
            description="Create a new technician (admin) in ServiceDesk Plus",
            inputSchema={
                "type": "object",
                "properties": {
                    "username": {
                        "type": "string",
                        "description": "Username"
                    },
                    "email": {
                        "type": "string",
                        "description": "Email of the technician"
                    },
                    "first_name": {
                        "type": "string",
                        "description": "First name"
                    },
                    "last_name": {
                        "type": "string",
                        "description": "Last name"
                    },
                    "password": {
                        "type": "string",
                        "description": "Password"
                    },
                    "role": {
                        "type": "string",
                        "description": "Role of the technician",
                        "enum": ["admin", "manager", "technician", "user", "viewer"]
                    },
                    "site_id": {
                        "type": "string",
                        "description": "ID of the site"
                    },
                    "department": {
                        "type": "string",
                        "description": "Department"
                    },
                    "phone": {
                        "type": "string",
                        "description": "Phone number"
                    },
                    "status": {
                        "type": "string",
                        "description": "Status",
                        "enum": ["active", "inactive", "locked", "pending_activation"]
                    },
                    "skills": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of skills"
                    },
                    "specializations": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of specializations"
                    }
                },
                "required": ["username", "email", "first_name", "last_name"]
            }
        ),
        Tool(
            name="update_admin_technician",
            description="Update information of a technician (admin)",
            inputSchema={
                "type": "object",
                "properties": {
                    "technician_id": {
                        "type": "string",
                        "description": "ID of the technician to update"
                    },
                    "username": {
                        "type": "string",
                        "description": "New username"
                    },
                    "email": {
                        "type": "string",
                        "description": "New email"
                    },
                    "first_name": {
                        "type": "string",
                        "description": "New first name"
                    },
                    "last_name": {
                        "type": "string",
                        "description": "New last name"
                    },
                    "role": {
                        "type": "string",
                        "description": "New role",
                        "enum": ["admin", "manager", "technician", "user", "viewer"]
                    },
                    "site_id": {
                        "type": "string",
                        "description": "New site ID"
                    },
                    "department": {
                        "type": "string",
                        "description": "New department"
                    },
                    "phone": {
                        "type": "string",
                        "description": "New phone number"
                    },
                    "status": {
                        "type": "string",
                        "description": "New status",
                        "enum": ["active", "inactive", "locked", "pending_activation"]
                    },
                    "skills": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "New list of skills"
                    },
                    "specializations": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "New list of specializations"
                    }
                },
                "required": ["technician_id"]
            }
        ),
        Tool(
            name="delete_admin_technician",
            description="Delete a technician (admin)",
            inputSchema={
                "type": "object",
                "properties": {
                    "technician_id": {
                        "type": "string",
                        "description": "ID of the technician to delete"
                    }
                },
                "required": ["technician_id"]
            }
        ),
        Tool(
            name="get_user_roles",
            description="Get list of available user roles",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="get_technician_roles",
            description="Get list of available technician roles",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="convert_user_to_technician",
            description="Convert user to technician in ServiceDesk Plus",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "ID of the user to convert to technician"
                    },
                    "technician_data": {
                        "type": "object",
                        "description": "Additional data for technician (optional)",
                        "additionalProperties": True
                    },
                    "delete_user_after_conversion": {
                        "type": "boolean",
                        "description": "Whether to delete the user after converting to technician",
                        "default": False
                    }
                },
                "required": ["user_id"]
            }
        ),
        Tool(
            name="activate_admin_user",
            description="Activate user account",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "ID of the user to activate"
                    }
                },
                "required": ["user_id"]
            }
        ),
        Tool(
            name="deactivate_admin_user",
            description="Deactivate user account",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "ID of the user to deactivate"
                    }
                },
                "required": ["user_id"]
            }
        ),
        Tool(
            name="lock_admin_user",
            description="Lock user account",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "ID of the user to lock"
                    }
                },
                "required": ["user_id"]
            }
        ),
        Tool(
            name="unlock_admin_user",
            description="Unlock user account",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "ID of the user to unlock"
                    }
                },
                "required": ["user_id"]
            }
        ),
        Tool(
            name="reset_admin_user_password",
            description="Reset user password",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "ID of the user to reset password"
                    },
                    "new_password": {
                        "type": "string",
                        "description": "New password"
                    }
                },
                "required": ["user_id", "new_password"]
            }
        ),
        Tool(
            name="update_admin_user_profile",
            description="Update user profile information",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "ID of the user to update"
                    },
                    "profile_data": {
                        "type": "object",
                        "description": "Profile data to update",
                        "properties": {
                            "first_name": {"type": "string", "description": "First name"},
                            "last_name": {"type": "string", "description": "Last name"},
                            "email": {"type": "string", "description": "Email"},
                            "phone": {"type": "string", "description": "Phone number"},
                            "department": {"type": "string", "description": "Department"},
                            "job_title": {"type": "string", "description": "Job title"},
                            "employee_id": {"type": "string", "description": "Employee ID"},
                            "location": {"type": "string", "description": "Location"},
                            "manager": {"type": "string", "description": "Manager"},
                            "cost_center": {"type": "string", "description": "Cost center"}
                        }
                    }
                },
                "required": ["user_id", "profile_data"]
            }
        ),
        Tool(
            name="search_admin_users",
            description="Search users by keyword",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search keyword"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of results (default: 50, maximum: 1000)",
                        "default": 50
                    },
                    "search_fields": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Fields to search in (optional)"
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="get_admin_user_groups",
            description="Get list of groups that user belongs to",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "ID of the user"
                    }
                },
                "required": ["user_id"]
            }
        ),
        Tool(
            name="add_admin_user_to_group",
            description="Add user to group",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "ID of the user"
                    },
                    "group_id": {
                        "type": "string",
                        "description": "ID of the group"
                    }
                },
                "required": ["user_id", "group_id"]
            }
        ),
        Tool(
            name="remove_admin_user_from_group",
            description="Remove user from group",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "ID of the user"
                    },
                    "group_id": {
                        "type": "string",
                        "description": "ID of the group"
                    }
                },
                "required": ["user_id", "group_id"]
            }
        ),
        Tool(
            name="bulk_create_admin_users",
            description="Create multiple users at once",
            inputSchema={
                "type": "object",
                "properties": {
                    "users_data": {
                        "type": "array",
                        "description": "List of user data to create",
                        "items": {
                            "type": "object",
                            "properties": {
                                "username": {"type": "string", "description": "Username"},
                                "email": {"type": "string", "description": "Email"},
                                "first_name": {"type": "string", "description": "First name"},
                                "last_name": {"type": "string", "description": "Last name"},
                                "password": {"type": "string", "description": "Password"},
                                "role": {"type": "string", "description": "Role"},
                                "department": {"type": "string", "description": "Department"},
                                "phone": {"type": "string", "description": "Phone number"}
                            },
                            "required": ["username", "email", "first_name", "last_name"]
                        },
                        "minItems": 1,
                        "maxItems": 100
                    }
                },
                "required": ["users_data"]
            }
        ),
        Tool(
            name="get_admin_user_login_history",
            description="Get login history of user",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "ID of the user"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of records (default: 50, maximum: 1000)",
                        "default": 50
                    },
                    "start_date": {
                        "type": "string",
                        "description": "Start date (YYYY-MM-DD)"
                    },
                    "end_date": {
                        "type": "string",
                        "description": "End date (YYYY-MM-DD)"
                    }
                },
                "required": ["user_id"]
            }
        ),
        Tool(
            name="get_admin_user_activity_log",
            description="Get activity log of user",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "ID of the user"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of records (default: 50, maximum: 1000)",
                        "default": 50
                    },
                    "activity_type": {
                        "type": "string",
                        "description": "Activity type to filter"
                    },
                    "start_date": {
                        "type": "string",
                        "description": "Start date (YYYY-MM-DD)"
                    },
                    "end_date": {
                        "type": "string",
                        "description": "End date (YYYY-MM-DD)"
                    }
                },
                "required": ["user_id"]
            }
        ),

        # ==================== ADMIN MANAGEMENT - PERMISSIONS ====================
        Tool(
            name="get_permissions",
            description="Get list of all available permissions",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="get_role_permissions",
            description="Get list of permissions of a role",
            inputSchema={
                "type": "object",
                "properties": {
                    "role_id": {
                        "type": "string",
                        "description": "ID of the role"
                    }
                },
                "required": ["role_id"]
            }
        ),
        Tool(
            name="update_role_permissions",
            description="Update permissions for a role",
            inputSchema={
                "type": "object",
                "properties": {
                    "role_id": {
                        "type": "string",
                        "description": "ID of the role"
                    },
                    "permissions": {
                        "type": "object",
                        "description": "Object containing permissions with corresponding levels",
                        "additionalProperties": {
                            "type": "string",
                            "enum": ["none", "read", "write", "admin"]
                        }
                    }
                },
                "required": ["role_id", "permissions"]
            }
        ),
        Tool(
            name="get_user_permissions",
            description="Get list of permissions of a user",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "ID of the user"
                    }
                },
                "required": ["user_id"]
            }
        ),
        Tool(
            name="update_user_permissions",
            description="Update permissions for a user",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "ID of the user"
                    },
                    "permissions": {
                        "type": "object",
                        "description": "Object containing permissions with corresponding levels",
                        "additionalProperties": {
                            "type": "string",
                            "enum": ["none", "read", "write", "admin"]
                        }
                    }
                },
                "required": ["user_id", "permissions"]
            }
        ),

        # ==================== ADMIN MANAGEMENT - DEPARTMENTS ====================
        Tool(
            name="list_departments",
            description="Get list of departments from ServiceDesk Plus",
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of departments (default: 50, maximum: 1000)",
                        "default": 50
                    },
                    "department_type": {
                        "type": "string",
                        "description": "Filter by department type"
                    },
                    "site_id": {
                        "type": "string",
                        "description": "Filter by site ID"
                    }
                }
            }
        ),
        Tool(
            name="get_department",
            description="Get detailed information about a department",
            inputSchema={
                "type": "object",
                "properties": {
                    "department_id": {
                        "type": "string",
                        "description": "ID of the department to get information"
                    }
                },
                "required": ["department_id"]
            }
        ),
        Tool(
            name="create_department",
            description="Create a new department in ServiceDesk Plus",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Name of the department"
                    },
                    "department_type": {
                        "type": "string",
                        "description": "Department type"
                    },
                    "description": {
                        "type": "string",
                        "description": "Detailed description"
                    },
                    "site_id": {
                        "type": "string",
                        "description": "ID of the associated site"
                    },
                    "manager": {
                        "type": "string",
                        "description": "ID of the manager"
                    }
                },
                "required": ["name", "department_type"]
            }
        ),
        Tool(
            name="update_department",
            description="Update information of a department",
            inputSchema={
                "type": "object",
                "properties": {
                    "department_id": {
                        "type": "string",
                        "description": "ID of the department to update"
                    },
                    "name": {
                        "type": "string",
                        "description": "New name of the department"
                    },
                    "department_type": {
                        "type": "string",
                        "description": "New department type"
                    },
                    "description": {
                        "type": "string",
                        "description": "New description"
                    },
                    "site_id": {
                        "type": "string",
                        "description": "New associated site ID"
                    },
                    "manager": {
                        "type": "string",
                        "description": "New manager ID"
                    }
                },
                "required": ["department_id"]
            }
        ),
        Tool(
            name="delete_department",
            description="Delete a department",
            inputSchema={
                "type": "object",
                "properties": {
                    "department_id": {
                        "type": "string",
                        "description": "ID of the department to delete"
                    }
                },
                "required": ["department_id"]
            }
        ),
        Tool(
            name="get_department_types",
            description="Get list of available department types",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),

        # ==================== ADMIN MANAGEMENT - LOCATIONS ====================
        Tool(
            name="list_locations",
            description="Get list of locations from ServiceDesk Plus",
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of locations (default: 50, maximum: 1000)",
                        "default": 50
                    },
                    "location_type": {
                        "type": "string",
                        "description": "Filter by location type"
                    },
                    "site_id": {
                        "type": "string",
                        "description": "Filter by site ID"
                    }
                }
            }
        ),
        Tool(
            name="get_location",
            description="Get detailed information about a location",
            inputSchema={
                "type": "object",
                "properties": {
                    "location_id": {
                        "type": "string",
                        "description": "ID of the location to get information"
                    }
                },
                "required": ["location_id"]
            }
        ),
        Tool(
            name="create_location",
            description="Create a new location in ServiceDesk Plus",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Name of the location"
                    },
                    "location_type": {
                        "type": "string",
                        "description": "Location type"
                    },
                    "description": {
                        "type": "string",
                        "description": "Detailed description"
                    },
                    "site_id": {
                        "type": "string",
                        "description": "ID of the associated site"
                    },
                    "address": {
                        "type": "string",
                        "description": "Address"
                    },
                    "floor": {
                        "type": "string",
                        "description": "Floor"
                    },
                    "room": {
                        "type": "string",
                        "description": "Room"
                    }
                },
                "required": ["name", "location_type"]
            }
        ),
        Tool(
            name="update_location",
            description="Update information of a location",
            inputSchema={
                "type": "object",
                "properties": {
                    "location_id": {
                        "type": "string",
                        "description": "ID of the location to update"
                    },
                    "name": {
                        "type": "string",
                        "description": "New name of the location"
                    },
                    "location_type": {
                        "type": "string",
                        "description": "New location type"
                    },
                    "description": {
                        "type": "string",
                        "description": "New description"
                    },
                    "site_id": {
                        "type": "string",
                        "description": "New associated site ID"
                    },
                    "address": {
                        "type": "string",
                        "description": "New address"
                    },
                    "floor": {
                        "type": "string",
                        "description": "New floor"
                    },
                    "room": {
                        "type": "string",
                        "description": "New room"
                    }
                },
                "required": ["location_id"]
            }
        ),
        Tool(
            name="delete_location",
            description="Delete a location",
            inputSchema={
                "type": "object",
                "properties": {
                    "location_id": {
                        "type": "string",
                        "description": "ID of the location to delete"
                    }
                },
                "required": ["location_id"]
            }
        ),
        Tool(
            name="get_location_types",
            description="Get list of available location types",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),

        # ==================== ADMIN MANAGEMENT - SYSTEM SETTINGS ====================
        Tool(
            name="get_system_settings",
            description="Get system settings",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="update_system_settings",
            description="Update system settings",
            inputSchema={
                "type": "object",
                "properties": {
                    "settings": {
                        "type": "object",
                        "description": "Object containing system settings to update"
                    }
                },
                "required": ["settings"]
            }
        ),
        Tool(
            name="get_email_settings",
            description="Get email settings",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="update_email_settings",
            description="Update email settings",
            inputSchema={
                "type": "object",
                "properties": {
                    "settings": {
                        "type": "object",
                        "description": "Object containing email settings to update"
                    }
                },
                "required": ["settings"]
            }
        ),
        Tool(
            name="get_notification_settings",
            description="Get notification settings",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="update_notification_settings",
            description="Update notification settings",
            inputSchema={
                "type": "object",
                "properties": {
                    "settings": {
                        "type": "object",
                        "description": "Object containing notification settings to update"
                    }
                },
                "required": ["settings"]
            }
        ),

        # ==================== REFERENCE DATA ====================
        Tool(
            name="get_categories",
            description="Get list of available ticket categories",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="get_priorities",
            description="Get list of available priority levels",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="get_statuses",
            description="Get list of available ticket statuses",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        )
    ]
    return ListToolsResult(tools=tools)

@server.call_tool()
async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> CallToolResult:
    """Handle tool calls"""
    try:
        async with ServiceDeskPlusClient() as client:
            # ==================== TICKET MANAGEMENT ====================
            if name == "list_tickets":
                limit = arguments.get("limit", 50)
                status = arguments.get("status")
                priority = arguments.get("priority")
                requester = arguments.get("requester")
                result = await client.get_tickets(
                    limit=limit,
                    status=status,
                    priority=priority,
                    requester=requester
                )

            elif name == "get_ticket":
                ticket_id = arguments["ticket_id"]
                result = await client.get_ticket(ticket_id)

            elif name == "create_ticket":
                result = await client.create_ticket(arguments)

            elif name == "update_ticket":
                ticket_id = arguments.pop("ticket_id")
                result = await client.update_ticket(ticket_id, arguments)

            elif name == "delete_ticket":
                ticket_id = arguments["ticket_id"]
                result = await client.delete_ticket(ticket_id)

            elif name == "search_tickets":
                query = arguments["query"]
                limit = arguments.get("limit", 50)
                result = await client.search_tickets(query, limit=limit)

            elif name == "add_ticket_comment":
                ticket_id = arguments["ticket_id"]
                comment = arguments["comment"]
                result = await client.add_ticket_comment(ticket_id, comment)

            elif name == "get_ticket_comments":
                ticket_id = arguments["ticket_id"]
                result = await client.get_ticket_comments(ticket_id)

            # ==================== ADVANCED REQUEST MANAGEMENT ====================

            elif name == "assign_request":
                request_id = arguments["request_id"]
                technician_id = arguments["technician_id"]
                group_id = arguments.get("group_id")
                result = await client.assign_request(request_id, technician_id, group_id)

            elif name == "reassign_request":
                request_id = arguments["request_id"]
                technician_id = arguments["technician_id"]
                reason = arguments.get("reason")
                result = await client.reassign_request(request_id, technician_id, reason)

            elif name == "escalate_request":
                request_id = arguments["request_id"]
                escalation_level = arguments["escalation_level"]
                reason = arguments["reason"]
                result = await client.escalate_request(request_id, escalation_level, reason)

            elif name == "approve_request":
                request_id = arguments["request_id"]
                approval_comments = arguments.get("approval_comments")
                result = await client.approve_request(request_id, approval_comments)

            elif name == "reject_request":
                request_id = arguments["request_id"]
                rejection_reason = arguments["rejection_reason"]
                comments = arguments.get("comments")
                result = await client.reject_request(request_id, rejection_reason, comments)

            elif name == "get_request_approvals":
                request_id = arguments["request_id"]
                result = await client.get_request_approvals(request_id)

            elif name == "get_request_attachments":
                request_id = arguments["request_id"]
                result = await client.get_request_attachments(request_id)

            elif name == "add_request_attachment":
                request_id = arguments["request_id"]
                file_path = arguments["file_path"]
                description = arguments.get("description")
                result = await client.add_request_attachment(request_id, file_path, description)

            elif name == "delete_request_attachment":
                request_id = arguments["request_id"]
                attachment_id = arguments["attachment_id"]
                result = await client.delete_request_attachment(request_id, attachment_id)

            elif name == "get_request_history":
                request_id = arguments["request_id"]
                limit = arguments.get("limit", 50)
                result = await client.get_request_history(request_id, limit)

            elif name == "get_request_sla_details":
                request_id = arguments["request_id"]
                result = await client.get_request_sla_details(request_id)

            elif name == "update_request_sla":
                request_id = arguments["request_id"]
                sla_data = arguments["sla_data"]
                result = await client.update_request_sla(request_id, sla_data)

            elif name == "get_request_templates":
                category = arguments.get("category")
                result = await client.get_request_templates(category)

            elif name == "create_request_from_template":
                template_id = arguments["template_id"]
                request_data = arguments["request_data"]
                result = await client.create_request_from_template(template_id, request_data)

            elif name == "close_request":
                request_id = arguments["request_id"]
                closure_code = arguments["closure_code"]
                resolution = arguments["resolution"]
                result = await client.close_request(request_id, closure_code, resolution)

            elif name == "get_closure_codes":
                result = await client.get_closure_codes()

            elif name == "get_request_worklog":
                request_id = arguments["request_id"]
                limit = arguments.get("limit", 50)
                result = await client.get_request_worklog(request_id, limit)

            elif name == "add_worklog_entry":
                request_id = arguments["request_id"]
                description = arguments["description"]
                time_spent = arguments.get("time_spent")
                technician_id = arguments.get("technician_id")
                result = await client.add_worklog_entry(request_id, description, time_spent, technician_id)

            elif name == "update_worklog_entry":
                request_id = arguments["request_id"]
                worklog_id = arguments["worklog_id"]
                update_data = arguments["update_data"]
                result = await client.update_worklog_entry(request_id, worklog_id, update_data)

            elif name == "get_request_custom_fields":
                request_id = arguments["request_id"]
                result = await client.get_request_custom_fields(request_id)

            elif name == "update_request_custom_fields":
                request_id = arguments["request_id"]
                custom_fields = arguments["custom_fields"]
                result = await client.update_request_custom_fields(request_id, custom_fields)

            elif name == "get_request_feedback":
                request_id = arguments["request_id"]
                result = await client.get_request_feedback(request_id)

            elif name == "submit_request_feedback":
                request_id = arguments["request_id"]
                rating = arguments["rating"]
                comments = arguments.get("comments")
                survey_responses = arguments.get("survey_responses")
                result = await client.submit_request_feedback(request_id, rating, comments, survey_responses)

            elif name == "get_request_notifications":
                request_id = arguments["request_id"]
                result = await client.get_request_notifications(request_id)

            elif name == "send_request_notification":
                request_id = arguments["request_id"]
                notification_type = arguments["notification_type"]
                recipients = arguments["recipients"]
                custom_message = arguments.get("custom_message")
                result = await client.send_request_notification(request_id, notification_type, recipients, custom_message)

            # ==================== REFERENCE DATA ====================

            elif name == "get_categories":
                result = await client.get_categories()

            elif name == "get_priorities":
                result = await client.get_priorities()

            elif name == "get_statuses":
                result = await client.get_statuses()

            # ==================== USER MANAGEMENT ====================
            elif name == "list_users":
                limit = arguments.get("limit", 50)
                result = await client.get_users(limit=limit)

            elif name == "get_user":
                user_id = arguments["user_id"]
                result = await client.get_user(user_id)

            elif name == "list_technicians":
                limit = arguments.get("limit", 50)
                result = await client.get_technicians(limit=limit)

            # ==================== CMDB - CONFIGURATION ITEMS ====================
            elif name == "list_configuration_items":
                limit = arguments.get("limit", 50)
                ci_type = arguments.get("ci_type")
                status = arguments.get("status")
                result = await client.get_configuration_items(
                    limit=limit,
                    ci_type=ci_type,
                    status=status
                )

            elif name == "get_configuration_item":
                ci_id = arguments["ci_id"]
                result = await client.get_configuration_item(ci_id)

            elif name == "create_configuration_item":
                result = await client.create_configuration_item(arguments)

            elif name == "update_configuration_item":
                ci_id = arguments.pop("ci_id")
                result = await client.update_configuration_item(ci_id, arguments)

            elif name == "delete_configuration_item":
                ci_id = arguments["ci_id"]
                result = await client.delete_configuration_item(ci_id)

            elif name == "get_ci_types":
                result = await client.get_ci_types()

            elif name == "get_ci_relationships":
                ci_id = arguments["ci_id"]
                result = await client.get_ci_relationships(ci_id)

            # ==================== ASSET MANAGEMENT ====================
            elif name == "list_assets":
                limit = arguments.get("limit", 50)
                asset_type = arguments.get("asset_type")
                status = arguments.get("status")
                location = arguments.get("location")
                result = await client.get_assets(
                    limit=limit,
                    asset_type=asset_type,
                    status=status,
                    location=location
                )

            elif name == "get_asset":
                asset_id = arguments["asset_id"]
                result = await client.get_asset(asset_id)

            elif name == "create_asset":
                result = await client.create_asset(arguments)

            elif name == "update_asset":
                asset_id = arguments.pop("asset_id")
                result = await client.update_asset(asset_id, arguments)

            elif name == "delete_asset":
                asset_id = arguments["asset_id"]
                result = await client.delete_asset(asset_id)

            elif name == "get_asset_types":
                result = await client.get_asset_types()

            elif name == "get_asset_categories":
                result = await client.get_asset_categories()

            elif name == "get_asset_locations":
                result = await client.get_asset_locations()

            elif name == "get_asset_models":
                result = await client.get_asset_models()

            elif name == "get_asset_vendors":
                result = await client.get_asset_vendors()

            # ==================== SOFTWARE LICENSE MANAGEMENT ====================
            elif name == "list_software_licenses":
                limit = arguments.get("limit", 50)
                product = arguments.get("product")
                vendor = arguments.get("vendor")
                result = await client.get_software_licenses(
                    limit=limit,
                    product=product,
                    vendor=vendor
                )

            elif name == "get_software_license":
                license_id = arguments["license_id"]
                result = await client.get_software_license(license_id)

            elif name == "create_software_license":
                result = await client.create_software_license(arguments)

            elif name == "update_software_license":
                license_id = arguments.pop("license_id")
                result = await client.update_software_license(license_id, arguments)

            elif name == "get_software_products":
                result = await client.get_software_products()

            elif name == "get_license_types":
                result = await client.get_license_types()

            # ==================== CONTRACT MANAGEMENT ====================
            elif name == "list_contracts":
                limit = arguments.get("limit", 50)
                contract_type = arguments.get("contract_type")
                status = arguments.get("status")
                vendor = arguments.get("vendor")
                result = await client.get_contracts(
                    limit=limit,
                    contract_type=contract_type,
                    status=status,
                    vendor=vendor
                )

            elif name == "get_contract":
                contract_id = arguments["contract_id"]
                result = await client.get_contract(contract_id)

            elif name == "create_contract":
                result = await client.create_contract(arguments)

            elif name == "update_contract":
                contract_id = arguments.pop("contract_id")
                result = await client.update_contract(contract_id, arguments)

            elif name == "get_contract_types":
                result = await client.get_contract_types()

            elif name == "get_contract_vendors":
                result = await client.get_contract_vendors()

            # ==================== PURCHASE ORDER MANAGEMENT ====================
            elif name == "list_purchase_orders":
                limit = arguments.get("limit", 50)
                status = arguments.get("status")
                vendor = arguments.get("vendor")
                result = await client.get_purchase_orders(
                    limit=limit,
                    status=status,
                    vendor=vendor
                )

            elif name == "get_purchase_order":
                po_id = arguments["po_id"]
                result = await client.get_purchase_order(po_id)

            elif name == "create_purchase_order":
                result = await client.create_purchase_order(arguments)

            elif name == "update_purchase_order":
                po_id = arguments.pop("po_id")
                result = await client.update_purchase_order(po_id, arguments)

            elif name == "get_po_statuses":
                result = await client.get_po_statuses()

            # ==================== VENDOR MANAGEMENT ====================
            elif name == "list_vendors":
                limit = arguments.get("limit", 50)
                vendor_type = arguments.get("vendor_type")
                result = await client.get_vendors(limit=limit, vendor_type=vendor_type)

            elif name == "get_vendor":
                vendor_id = arguments["vendor_id"]
                result = await client.get_vendor(vendor_id)

            elif name == "create_vendor":
                result = await client.create_vendor(arguments)

            elif name == "update_vendor":
                vendor_id = arguments.pop("vendor_id")
                result = await client.update_vendor(vendor_id, arguments)

            elif name == "get_vendor_types":
                result = await client.get_vendor_types()

            # ==================== ADMIN MANAGEMENT - SITES ====================
            elif name == "list_sites":
                limit = arguments.get("limit", 50)
                site_type = arguments.get("site_type")
                status = arguments.get("status")
                result = await client.get_sites(
                    limit=limit,
                    site_type=site_type,
                    status=status
                )

            elif name == "get_site":
                site_id = arguments["site_id"]
                result = await client.get_site(site_id)

            elif name == "create_site":
                result = await client.create_site(arguments)

            elif name == "update_site":
                site_id = arguments.pop("site_id")
                result = await client.update_site(site_id, arguments)

            elif name == "delete_site":
                site_id = arguments["site_id"]
                result = await client.delete_site(site_id)

            elif name == "get_site_types":
                result = await client.get_site_types()

            # ==================== ADMIN MANAGEMENT - USER GROUPS ====================
            elif name == "list_user_groups":
                limit = arguments.get("limit", 50)
                group_type = arguments.get("group_type")
                site_id = arguments.get("site_id")
                result = await client.get_user_groups(
                    limit=limit,
                    group_type=group_type,
                    site_id=site_id
                )

            elif name == "get_user_group":
                group_id = arguments["group_id"]
                result = await client.get_user_group(group_id)

            elif name == "create_user_group":
                result = await client.create_user_group(arguments)

            elif name == "update_user_group":
                group_id = arguments.pop("group_id")
                result = await client.update_user_group(group_id, arguments)

            elif name == "delete_user_group":
                group_id = arguments["group_id"]
                result = await client.delete_user_group(group_id)

            elif name == "get_group_types":
                result = await client.get_group_types()

            elif name == "get_group_permissions":
                group_id = arguments["group_id"]
                result = await client.get_group_permissions(group_id)

            elif name == "update_group_permissions":
                group_id = arguments.pop("group_id")
                result = await client.update_group_permissions(group_id, arguments)

            # ==================== ADMIN MANAGEMENT - USERS & TECHNICIANS ====================
            elif name == "list_admin_users":
                limit = arguments.get("limit", 50)
                status = arguments.get("status")
                role = arguments.get("role")
                site_id = arguments.get("site_id")
                result = await client.get_admin_users(
                    limit=limit,
                    status=status,
                    role=role,
                    site_id=site_id
                )

            elif name == "get_admin_user":
                user_id = arguments["user_id"]
                result = await client.get_admin_user(user_id)

            elif name == "create_admin_user":
                result = await client.create_admin_user(arguments)

            elif name == "update_admin_user":
                user_id = arguments.pop("user_id")
                result = await client.update_admin_user(user_id, arguments)

            elif name == "delete_admin_user":
                user_id = arguments["user_id"]
                result = await client.delete_admin_user(user_id)

            elif name == "list_admin_technicians":
                limit = arguments.get("limit", 50)
                status = arguments.get("status")
                role = arguments.get("role")
                site_id = arguments.get("site_id")
                result = await client.get_admin_technicians(
                    limit=limit,
                    status=status,
                    role=role,
                    site_id=site_id
                )

            elif name == "get_admin_technician":
                technician_id = arguments["technician_id"]
                result = await client.get_admin_technician(technician_id)

            elif name == "create_admin_technician":
                result = await client.create_admin_technician(arguments)

            elif name == "update_admin_technician":
                technician_id = arguments.pop("technician_id")
                result = await client.update_admin_technician(technician_id, arguments)

            elif name == "delete_admin_technician":
                technician_id = arguments["technician_id"]
                result = await client.delete_admin_technician(technician_id)

            elif name == "get_user_roles":
                result = await client.get_user_roles()

            elif name == "get_technician_roles":
                result = await client.get_technician_roles()

            elif name == "convert_user_to_technician":
                user_id = arguments["user_id"]
                technician_data = arguments.get("technician_data")
                delete_user_after_conversion = arguments.get("delete_user_after_conversion", False)
                result = await client.convert_user_to_technician(
                    user_id=user_id,
                    technician_data=technician_data,
                    delete_user_after_conversion=delete_user_after_conversion
                )

            elif name == "activate_admin_user":
                user_id = arguments["user_id"]
                result = await client.activate_admin_user(user_id)

            elif name == "deactivate_admin_user":
                user_id = arguments["user_id"]
                result = await client.deactivate_admin_user(user_id)

            elif name == "lock_admin_user":
                user_id = arguments["user_id"]
                result = await client.lock_admin_user(user_id)

            elif name == "unlock_admin_user":
                user_id = arguments["user_id"]
                result = await client.unlock_admin_user(user_id)

            elif name == "reset_admin_user_password":
                user_id = arguments["user_id"]
                new_password = arguments["new_password"]
                result = await client.reset_admin_user_password(user_id, new_password)

            elif name == "update_admin_user_profile":
                user_id = arguments["user_id"]
                profile_data = arguments["profile_data"]
                result = await client.update_admin_user_profile(user_id, profile_data)

            elif name == "search_admin_users":
                query = arguments["query"]
                limit = arguments.get("limit", 50)
                search_fields = arguments.get("search_fields")
                result = await client.search_admin_users(query, limit=limit, search_fields=search_fields)

            elif name == "get_admin_user_groups":
                user_id = arguments["user_id"]
                result = await client.get_admin_user_groups(user_id)

            elif name == "add_admin_user_to_group":
                user_id = arguments["user_id"]
                group_id = arguments["group_id"]
                result = await client.add_admin_user_to_group(user_id, group_id)

            elif name == "remove_admin_user_from_group":
                user_id = arguments["user_id"]
                group_id = arguments["group_id"]
                result = await client.remove_admin_user_from_group(user_id, group_id)

            elif name == "bulk_create_admin_users":
                users_data = arguments["users_data"]
                result = await client.bulk_create_admin_users(users_data)

            elif name == "get_admin_user_login_history":
                user_id = arguments["user_id"]
                limit = arguments.get("limit", 50)
                start_date = arguments.get("start_date")
                end_date = arguments.get("end_date")
                result = await client.get_admin_user_login_history(
                    user_id, limit=limit, start_date=start_date, end_date=end_date
                )

            elif name == "get_admin_user_activity_log":
                user_id = arguments["user_id"]
                limit = arguments.get("limit", 50)
                activity_type = arguments.get("activity_type")
                start_date = arguments.get("start_date")
                end_date = arguments.get("end_date")
                result = await client.get_admin_user_activity_log(
                    user_id, limit=limit, activity_type=activity_type,
                    start_date=start_date, end_date=end_date
                )

            # ==================== ADMIN MANAGEMENT - PERMISSIONS ====================
            elif name == "get_permissions":
                result = await client.get_permissions()

            elif name == "get_role_permissions":
                role_id = arguments["role_id"]
                result = await client.get_role_permissions(role_id)

            elif name == "update_role_permissions":
                role_id = arguments.pop("role_id")
                result = await client.update_role_permissions(role_id, arguments)

            elif name == "get_user_permissions":
                user_id = arguments["user_id"]
                result = await client.get_user_permissions(user_id)

            elif name == "update_user_permissions":
                user_id = arguments.pop("user_id")
                result = await client.update_user_permissions(user_id, arguments)

            # ==================== ADMIN MANAGEMENT - DEPARTMENTS ====================
            elif name == "list_departments":
                limit = arguments.get("limit", 50)
                department_type = arguments.get("department_type")
                site_id = arguments.get("site_id")
                result = await client.get_departments(
                    limit=limit,
                    department_type=department_type,
                    site_id=site_id
                )

            elif name == "get_department":
                department_id = arguments["department_id"]
                result = await client.get_department(department_id)

            elif name == "create_department":
                result = await client.create_department(arguments)

            elif name == "update_department":
                department_id = arguments.pop("department_id")
                result = await client.update_department(department_id, arguments)

            elif name == "delete_department":
                department_id = arguments["department_id"]
                result = await client.delete_department(department_id)

            elif name == "get_department_types":
                result = await client.get_department_types()

            # ==================== ADMIN MANAGEMENT - LOCATIONS ====================
            elif name == "list_locations":
                limit = arguments.get("limit", 50)
                location_type = arguments.get("location_type")
                site_id = arguments.get("site_id")
                result = await client.get_locations(
                    limit=limit,
                    location_type=location_type,
                    site_id=site_id
                )

            elif name == "get_location":
                location_id = arguments["location_id"]
                result = await client.get_location(location_id)

            elif name == "create_location":
                result = await client.create_location(arguments)

            elif name == "update_location":
                location_id = arguments.pop("location_id")
                result = await client.update_location(location_id, arguments)

            elif name == "delete_location":
                location_id = arguments["location_id"]
                result = await client.delete_location(location_id)

            elif name == "get_location_types":
                result = await client.get_location_types()

            # ==================== ADMIN MANAGEMENT - SYSTEM SETTINGS ====================
            elif name == "get_system_settings":
                result = await client.get_system_settings()

            elif name == "update_system_settings":
                result = await client.update_system_settings(arguments["settings"])

            elif name == "get_email_settings":
                result = await client.get_email_settings()

            elif name == "update_email_settings":
                result = await client.update_email_settings(arguments["settings"])

            elif name == "get_notification_settings":
                result = await client.get_notification_settings()

            elif name == "update_notification_settings":
                result = await client.update_notification_settings(arguments["settings"])

            # ==================== REFERENCE DATA ====================

            elif name == "get_categories":
                result = await client.get_categories()

            elif name == "get_priorities":
                result = await client.get_priorities()

            elif name == "get_statuses":
                result = await client.get_statuses()

            else:
                result = {"error": f"Unknown tool: {name}"}

        return CallToolResult(
            content=[
                TextContent(
                    type="text",
                    text=json.dumps(result, indent=2, ensure_ascii=False)
                )
            ]
        )

    except Exception as e:
        return CallToolResult(
            content=[
                TextContent(
                    type="text",
                    text=json.dumps({"error": str(e)}, indent=2, ensure_ascii=False)
                )
            ]
        )

async def main():
    """Main function to run the MCP server"""
    # Validate configuration
    config_validation = Config.validate_config()
    if not config_validation["valid"]:
        print("Configuration errors:")
        for issue in config_validation["issues"]:
            print(f"  - {issue}")
        return

    # Run the server
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="servicedesk-plus",
                server_version="2.0.0",
                capabilities=server.get_capabilities(
                    notification_options=None,
                    experimental_capabilities=None,
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())
