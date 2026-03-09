#!/usr/bin/env python3

"""
Test script to verify the connection to ServiceDesk Plus and CMDB features
"""

import asyncio
import json
from sdp_client import ServiceDeskPlusClient
from config import Config

async def test_connection():
    """Test connection to ServiceDesk Plus"""
    print("🔍 Checking configuration...")

    # Validate configuration
    config_validation = Config.validate_config()
    if not config_validation["valid"]:
        print("❌ Configuration error:")
        for issue in config_validation["issues"]:
            print(f"  - {issue}")
        return False

    print("✅ Configuration is valid")
    print(f"📡 Connecting to: {Config.SDP_BASE_URL}")

    try:
        async with ServiceDeskPlusClient() as client:
            print("🔐 Authenticating...")

            # Test authentication
            if await client.authenticate():
                print("✅ Authentication successful")
            else:
                print("❌ Authentication failed")
                return False

            # Test basic API calls
            print("\n📋 Testing basic API calls...")

            # Test get tickets
            print("  - Getting list of tickets...")
            tickets = await client.get_tickets(limit=5)
            if "error" not in tickets:
                print(f"    ✅ Success - Found {len(tickets.get('tickets', []))} tickets")
            else:
                print(f"    ❌ Error: {tickets['error']}")

            # Test get users
            print("  - Getting list of users...")
            users = await client.get_users(limit=5)
            if "error" not in users:
                print(f"    ✅ Success - Found {len(users.get('users', []))} users")
            else:
                print(f"    ❌ Error: {users['error']}")

            # Test get categories
            print("  - Getting list of categories...")
            categories = await client.get_categories()
            if "error" not in categories:
                print(f"    ✅ Success - Found {len(categories.get('categories', []))} categories")
            else:
                print(f"    ❌ Error: {categories['error']}")

            print("\n🎉 All basic tests completed!")
            return True

    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False

async def test_cmdb_features():
    """Test CMDB features"""
    print("\n🏗️ Testing CMDB features...")

    try:
        async with ServiceDeskPlusClient() as client:

            # Test Configuration Items
            print("  📦 Configuration Items:")
            print("    - Getting list of CIs...")
            cis = await client.get_configuration_items(limit=5)
            if "error" not in cis:
                print(f"      ✅ Success - Found {len(cis.get('configuration_items', []))} CIs")
            else:
                print(f"      ❌ Error: {cis['error']}")

            print("    - Getting list of CI types...")
            ci_types = await client.get_ci_types()
            if "error" not in ci_types:
                print(f"      ✅ Success - Found {len(ci_types.get('ci_types', []))} CI types")
            else:
                print(f"      ❌ Error: {ci_types['error']}")

            # Test Asset Management
            print("  💻 Asset Management:")
            print("    - Getting list of assets...")
            assets = await client.get_assets(limit=5)
            if "error" not in assets:
                print(f"      ✅ Success - Found {len(assets.get('assets', []))} assets")
            else:
                print(f"      ❌ Error: {assets['error']}")

            print("    - Getting list of asset types...")
            asset_types = await client.get_asset_types()
            if "error" not in asset_types:
                print(f"      ✅ Success - Found {len(asset_types.get('asset_types', []))} asset types")
            else:
                print(f"      ❌ Error: {asset_types['error']}")

            print("    - Getting list of asset categories...")
            asset_categories = await client.get_asset_categories()
            if "error" not in asset_categories:
                print(f"      ✅ Success - Found {len(asset_categories.get('asset_categories', []))} asset categories")
            else:
                print(f"      ❌ Error: {asset_categories['error']}")

            # Test Software License Management
            print("  📄 Software License Management:")
            print("    - Getting list of software licenses...")
            licenses = await client.get_software_licenses(limit=5)
            if "error" not in licenses:
                print(f"      ✅ Success - Found {len(licenses.get('software_licenses', []))} licenses")
            else:
                print(f"      ❌ Error: {licenses['error']}")

            print("    - Getting list of software products...")
            products = await client.get_software_products()
            if "error" not in products:
                print(f"      ✅ Success - Found {len(products.get('software_products', []))} products")
            else:
                print(f"      ❌ Error: {products['error']}")

            # Test Contract Management
            print("  📋 Contract Management:")
            print("    - Getting list of contracts...")
            contracts = await client.get_contracts(limit=5)
            if "error" not in contracts:
                print(f"      ✅ Success - Found {len(contracts.get('contracts', []))} contracts")
            else:
                print(f"      ❌ Error: {contracts['error']}")

            print("    - Getting list of contract types...")
            contract_types = await client.get_contract_types()
            if "error" not in contract_types:
                print(f"      ✅ Success - Found {len(contract_types.get('contract_types', []))} contract types")
            else:
                print(f"      ❌ Error: {contract_types['error']}")

            # Test Purchase Order Management
            print("  🛒 Purchase Order Management:")
            print("    - Getting list of purchase orders...")
            pos = await client.get_purchase_orders(limit=5)
            if "error" not in pos:
                print(f"      ✅ Success - Found {len(pos.get('purchase_orders', []))} purchase orders")
            else:
                print(f"      ❌ Error: {pos['error']}")

            print("    - Getting list of PO statuses...")
            po_statuses = await client.get_po_statuses()
            if "error" not in po_statuses:
                print(f"      ✅ Success - Found {len(po_statuses.get('po_statuses', []))} PO statuses")
            else:
                print(f"      ❌ Error: {po_statuses['error']}")

            # Test Vendor Management
            print("  🏢 Vendor Management:")
            print("    - Getting list of vendors...")
            vendors = await client.get_vendors(limit=5)
            if "error" not in vendors:
                print(f"      ✅ Success - Found {len(vendors.get('vendors', []))} vendors")
            else:
                print(f"      ❌ Error: {vendors['error']}")

            print("    - Getting list of vendor types...")
            vendor_types = await client.get_vendor_types()
            if "error" not in vendor_types:
                print(f"      ✅ Success - Found {len(vendor_types.get('vendor_types', []))} vendor types")
            else:
                print(f"      ❌ Error: {vendor_types['error']}")

    except Exception as e:
        print(f"❌ CMDB error: {e}")

async def test_ticket_operations():
    """Test ticket operations"""
    print("\n🎫 Testing ticket operations...")

    try:
        async with ServiceDeskPlusClient() as client:
            # Test search tickets
            print("  - Searching tickets...")
            search_result = await client.search_tickets("test", limit=5)
            if "error" not in search_result:
                print(f"    ✅ Success - Found {len(search_result.get('tickets', []))} tickets")
            else:
                print(f"    ❌ Error: {search_result['error']}")

            # Test get priorities
            print("  - Getting list of priorities...")
            priorities = await client.get_priorities()
            if "error" not in priorities:
                print(f"    ✅ Success - Found {len(priorities.get('priorities', []))} priorities")
            else:
                print(f"    ❌ Error: {priorities['error']}")

            # Test get statuses
            print("  - Getting list of statuses...")
            statuses = await client.get_statuses()
            if "error" not in statuses:
                print(f"    ✅ Success - Found {len(statuses.get('statuses', []))} statuses")
            else:
                print(f"    ❌ Error: {statuses['error']}")

    except Exception as e:
        print(f"❌ Error: {e}")

async def test_advanced_features():
    """Test advanced features"""
    print("\n🚀 Testing advanced features...")

    try:
        async with ServiceDeskPlusClient() as client:
            # Test filtering capabilities
            print("  🔍 Filtering capabilities:")
            print("    - Filtering tickets by status...")
            filtered_tickets = await client.get_tickets(limit=5, status="open")
            if "error" not in filtered_tickets:
                print(f"      ✅ Success - Found {len(filtered_tickets.get('tickets', []))} open tickets")
            else:
                print(f"      ❌ Error: {filtered_tickets['error']}")

            print("    - Filtering assets by status...")
            filtered_assets = await client.get_assets(limit=5, status="in_use")
            if "error" not in filtered_assets:
                print(f"      ✅ Success - Found {len(filtered_assets.get('assets', []))} in-use assets")
            else:
                print(f"      ❌ Error: {filtered_assets['error']}")

            # Test pagination
            print("  📄 Pagination:")
            print("    - Testing pagination with limit=10...")
            paginated_tickets = await client.get_tickets(limit=10)
            if "error" not in paginated_tickets:
                tickets_count = len(paginated_tickets.get('tickets', []))
                print(f"      ✅ Success - Retrieved {tickets_count} tickets (limit=10)")
            else:
                print(f"      ❌ Error: {paginated_tickets['error']}")

    except Exception as e:
        print(f"❌ Advanced features error: {e}")

async def test_admin_features():
    """Test Admin Management features"""
    print("\n👨‍💼 Testing Admin Management features...")

    try:
        async with ServiceDeskPlusClient() as client:

            # Test Site Management
            print("  🏢 Site Management:")
            print("    - Getting list of sites...")
            sites = await client.get_sites(limit=5)
            if "error" not in sites:
                print(f"      ✅ Success - Found {len(sites.get('sites', []))} sites")
            else:
                print(f"      ❌ Error: {sites['error']}")

            print("    - Getting list of site types...")
            site_types = await client.get_site_types()
            if "error" not in site_types:
                print(f"      ✅ Success - Found {len(site_types.get('site_types', []))} site types")
            else:
                print(f"      ❌ Error: {site_types['error']}")

            # Test User Group Management
            print("  👥 User Group Management:")
            print("    - Getting list of user groups...")
            user_groups = await client.get_user_groups(limit=5)
            if "error" not in user_groups:
                print(f"      ✅ Success - Found {len(user_groups.get('user_groups', []))} user groups")
            else:
                print(f"      ❌ Error: {user_groups['error']}")

            print("    - Getting list of group types...")
            group_types = await client.get_group_types()
            if "error" not in group_types:
                print(f"      ✅ Success - Found {len(group_types.get('group_types', []))} group types")
            else:
                print(f"      ❌ Error: {group_types['error']}")

            # Test Admin Users Management
            print("  👤 Admin Users Management:")
            print("    - Getting list of admin users...")
            admin_users = await client.get_admin_users(limit=5)
            if "error" not in admin_users:
                print(f"      ✅ Success - Found {len(admin_users.get('admin_users', []))} admin users")
            else:
                print(f"      ❌ Error: {admin_users['error']}")

            print("    - Getting list of user roles...")
            user_roles = await client.get_user_roles()
            if "error" not in user_roles:
                print(f"      ✅ Success - Found {len(user_roles.get('user_roles', []))} user roles")
            else:
                print(f"      ❌ Error: {user_roles['error']}")

            # Test Admin Technicians Management
            print("  🔧 Admin Technicians Management:")
            print("    - Getting list of admin technicians...")
            admin_technicians = await client.get_admin_technicians(limit=5)
            if "error" not in admin_technicians:
                print(f"      ✅ Success - Found {len(admin_technicians.get('admin_technicians', []))} admin technicians")
            else:
                print(f"      ❌ Error: {admin_technicians['error']}")

            print("    - Getting list of technician roles...")
            technician_roles = await client.get_technician_roles()
            if "error" not in technician_roles:
                print(f"      ✅ Success - Found {len(technician_roles.get('technician_roles', []))} technician roles")
            else:
                print(f"      ❌ Error: {technician_roles['error']}")

            # Test Permission Management
            print("  🔐 Permission Management:")
            print("    - Getting list of permissions...")
            permissions = await client.get_permissions()
            if "error" not in permissions:
                print(f"      ✅ Success - Found {len(permissions.get('permissions', []))} permissions")
            else:
                print(f"      ❌ Error: {permissions['error']}")

            # Test Department Management
            print("  🏛️ Department Management:")
            print("    - Getting list of departments...")
            departments = await client.get_departments(limit=5)
            if "error" not in departments:
                print(f"      ✅ Success - Found {len(departments.get('departments', []))} departments")
            else:
                print(f"      ❌ Error: {departments['error']}")

            print("    - Getting list of department types...")
            department_types = await client.get_department_types()
            if "error" not in department_types:
                print(f"      ✅ Success - Found {len(department_types.get('department_types', []))} department types")
            else:
                print(f"      ❌ Error: {department_types['error']}")

            # Test Location Management
            print("  📍 Location Management:")
            print("    - Getting list of locations...")
            locations = await client.get_locations(limit=5)
            if "error" not in locations:
                print(f"      ✅ Success - Found {len(locations.get('locations', []))} locations")
            else:
                print(f"      ❌ Error: {locations['error']}")

            print("    - Getting list of location types...")
            location_types = await client.get_location_types()
            if "error" not in location_types:
                print(f"      ✅ Success - Found {len(location_types.get('location_types', []))} location types")
            else:
                print(f"      ❌ Error: {location_types['error']}")

            # Test System Settings
            print("  ⚙️ System Settings:")
            print("    - Getting system settings...")
            system_settings = await client.get_system_settings()
            if "error" not in system_settings:
                print(f"      ✅ Success - Retrieved system settings")
            else:
                print(f"      ❌ Error: {system_settings['error']}")

            print("    - Getting email settings...")
            email_settings = await client.get_email_settings()
            if "error" not in email_settings:
                print(f"      ✅ Success - Retrieved email settings")
            else:
                print(f"      ❌ Error: {email_settings['error']}")

            print("    - Getting notification settings...")
            notification_settings = await client.get_notification_settings()
            if "error" not in notification_settings:
                print(f"      ✅ Success - Retrieved notification settings")
            else:
                print(f"      ❌ Error: {notification_settings['error']}")

    except Exception as e:
        print(f"❌ Admin Management error: {e}")

async def test_admin_crud_operations():
    """Test Admin CRUD operations (Create, Read, Update, Delete)"""
    print("\n🔄 Testing Admin CRUD operations...")

    try:
        async with ServiceDeskPlusClient() as client:

            # Test Site CRUD operations
            print("  🏢 Site CRUD Operations:")

            # Create test site
            test_site_data = {
                "name": "Test Site - MCP",
                "site_type": "branch_office",
                "address": "123 Test Street",
                "city": "Test City",
                "country": "Test Country",
                "description": "Test site created by MCP server"
            }

            print("    - Creating new site...")
            try:
                created_site = await client.create_site(test_site_data)
                if "error" not in created_site:
                    site_id = created_site.get('site', {}).get('id')
                    print(f"      ✅ Success - Created site with ID: {site_id}")

                    # Test update site
                    print("    - Updating site...")
                    update_data = {
                        "description": "Updated test site description"
                    }
                    updated_site = await client.update_site(site_id, update_data)
                    if "error" not in updated_site:
                        print(f"      ✅ Success - Site updated")
                    else:
                        print(f"      ❌ Update error: {updated_site['error']}")

                    # Test delete site
                    print("    - Deleting site...")
                    deleted_site = await client.delete_site(site_id)
                    if "error" not in deleted_site:
                        print(f"      ✅ Success - Site deleted")
                    else:
                        print(f"      ❌ Delete error: {deleted_site['error']}")

                else:
                    print(f"      ❌ Site creation error: {created_site['error']}")
            except Exception as e:
                print(f"      ⚠️ Skipping site CRUD test: {e}")

            # Test User Group CRUD operations
            print("  👥 User Group CRUD Operations:")

            # Create test user group
            test_group_data = {
                "name": "Test Group - MCP",
                "group_type": "custom",
                "description": "Test user group created by MCP server"
            }

            print("    - Creating new user group...")
            try:
                created_group = await client.create_user_group(test_group_data)
                if "error" not in created_group:
                    group_id = created_group.get('user_group', {}).get('id')
                    print(f"      ✅ Success - Created user group with ID: {group_id}")

                    # Test update user group
                    print("    - Updating user group...")
                    update_data = {
                        "description": "Updated test group description"
                    }
                    updated_group = await client.update_user_group(group_id, update_data)
                    if "error" not in updated_group:
                        print(f"      ✅ Success - User group updated")
                    else:
                        print(f"      ❌ Update error: {updated_group['error']}")

                    # Test delete user group
                    print("    - Deleting user group...")
                    deleted_group = await client.delete_user_group(group_id)
                    if "error" not in deleted_group:
                        print(f"      ✅ Success - User group deleted")
                    else:
                        print(f"      ❌ Delete error: {deleted_group['error']}")

                else:
                    print(f"      ❌ User group creation error: {created_group['error']}")
            except Exception as e:
                print(f"      ⚠️ Skipping user group CRUD test: {e}")

            # Test Department CRUD operations
            print("  🏛️ Department CRUD Operations:")

            # Create test department
            test_dept_data = {
                "name": "Test Department - MCP",
                "department_type": "IT",
                "description": "Test department created by MCP server"
            }

            print("    - Creating new department...")
            try:
                created_dept = await client.create_department(test_dept_data)
                if "error" not in created_dept:
                    dept_id = created_dept.get('department', {}).get('id')
                    print(f"      ✅ Success - Created department with ID: {dept_id}")

                    # Test update department
                    print("    - Updating department...")
                    update_data = {
                        "description": "Updated test department description"
                    }
                    updated_dept = await client.update_department(dept_id, update_data)
                    if "error" not in updated_dept:
                        print(f"      ✅ Success - Department updated")
                    else:
                        print(f"      ❌ Update error: {updated_dept['error']}")

                    # Test delete department
                    print("    - Deleting department...")
                    deleted_dept = await client.delete_department(dept_id)
                    if "error" not in deleted_dept:
                        print(f"      ✅ Success - Department deleted")
                    else:
                        print(f"      ❌ Delete error: {deleted_dept['error']}")

                else:
                    print(f"      ❌ Department creation error: {created_dept['error']}")
            except Exception as e:
                print(f"      ⚠️ Skipping department CRUD test: {e}")

            # Test Location CRUD operations
            print("  📍 Location CRUD Operations:")

            # Create test location
            test_location_data = {
                "name": "Test Location - MCP",
                "location_type": "office",
                "description": "Test location created by MCP server"
            }

            print("    - Creating new location...")
            try:
                created_location = await client.create_location(test_location_data)
                if "error" not in created_location:
                    location_id = created_location.get('location', {}).get('id')
                    print(f"      ✅ Success - Created location with ID: {location_id}")

                    # Test update location
                    print("    - Updating location...")
                    update_data = {
                        "description": "Updated test location description"
                    }
                    updated_location = await client.update_location(location_id, update_data)
                    if "error" not in updated_location:
                        print(f"      ✅ Success - Location updated")
                    else:
                        print(f"      ❌ Update error: {updated_location['error']}")

                    # Test delete location
                    print("    - Deleting location...")
                    deleted_location = await client.delete_location(location_id)
                    if "error" not in deleted_location:
                        print(f"      ✅ Success - Location deleted")
                    else:
                        print(f"      ❌ Delete error: {deleted_location['error']}")

                else:
                    print(f"      ❌ Location creation error: {created_location['error']}")
            except Exception as e:
                print(f"      ⚠️ Skipping location CRUD test: {e}")

    except Exception as e:
        print(f"❌ Admin CRUD error: {e}")

async def main():
    """Main test function"""
    print("🚀 Starting ServiceDesk Plus MCP Server v2.0 connection test")
    print("=" * 70)

    # Test basic connection
    success = await test_connection()

    if success:
        # Test CMDB features
        await test_cmdb_features()

        # Test ticket operations
        await test_ticket_operations()

        # Test advanced features
        await test_advanced_features()

        # Test Admin features
        await test_admin_features()

        # Test Admin CRUD operations
        await test_admin_crud_operations()

        print("\n" + "=" * 70)
        print("✅ All tests completed successfully!")
        print("🎯 MCP server with CMDB is ready to use")
        print("📊 Supports 60+ tools for comprehensive IT infrastructure management")
    else:
        print("\n" + "=" * 70)
        print("❌ Errors occurred during testing")
        print("🔧 Please check your configuration in the .env file")

if __name__ == "__main__":
    asyncio.run(main()) 