# Hướng dẫn sử dụng ServiceDesk Plus MCP Server

## Cài đặt và Cấu hình

### 1. Cài đặt Dependencies

```bash
pip install -r requirements.txt
```

### 2. Cấu hình Environment Variables

Tạo file `.env` từ file `env.example`:

```bash
cp env.example .env
```

Chỉnh sửa file `.env` với thông tin thực tế của bạn:

```env
SDP_BASE_URL=https://your-servicedesk-plus-instance.com
SDP_USERNAME=your_username
SDP_PASSWORD=your_password
SDP_API_KEY=your_api_key_here
```

### 3. Kiểm tra Kết nối

Chạy script test để kiểm tra kết nối:

```bash
python test_connection.py
```

## Cấu hình MCP Client

### Với Claude Desktop

Thêm vào file cấu hình MCP (thường ở `~/.config/claude/desktop-config.json`):

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

### Với Cursor

Thêm vào file cấu hình MCP:

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

## Các Tools Có Sẵn

### Quản lý Tickets

#### `list_tickets`
Lấy danh sách tickets với các bộ lọc tùy chọn.

**Parameters:**
- `limit` (optional): Số lượng tickets tối đa (mặc định: 50, tối đa: 1000)
- `status` (optional): Lọc theo trạng thái (open, pending, resolved, closed, cancelled, on_hold)
- `priority` (optional): Lọc theo mức độ ưu tiên (low, medium, high, critical)
- `requester` (optional): Lọc theo người yêu cầu

**Ví dụ:**
```
Lấy 10 tickets có trạng thái "open" và mức độ ưu tiên "high"
```

#### `get_ticket`
Lấy thông tin chi tiết của một ticket.

**Parameters:**
- `ticket_id` (required): ID của ticket

**Ví dụ:**
```
Lấy thông tin chi tiết của ticket có ID "TKT-001"
```

#### `create_ticket`
Tạo ticket mới.

**Parameters:**
- `subject` (required): Tiêu đề ticket
- `description` (required): Mô tả chi tiết
- `requester` (required): Email hoặc ID người yêu cầu
- `priority` (optional): Mức độ ưu tiên
- `category` (optional): Danh mục
- `technician` (optional): ID technician được gán

**Ví dụ:**
```
Tạo ticket mới với tiêu đề "Máy in không hoạt động", mô tả "Máy in HP LaserJet không in được", người yêu cầu "user@company.com", mức độ ưu tiên "medium"
```

#### `update_ticket`
Cập nhật thông tin ticket.

**Parameters:**
- `ticket_id` (required): ID của ticket
- `subject` (optional): Tiêu đề mới
- `description` (optional): Mô tả mới
- `status` (optional): Trạng thái mới
- `priority` (optional): Mức độ ưu tiên mới
- `technician` (optional): ID technician mới

**Ví dụ:**
```
Cập nhật ticket TKT-001 với trạng thái "resolved" và mức độ ưu tiên "low"
```

#### `delete_ticket`
Xóa một ticket.

**Parameters:**
- `ticket_id` (required): ID của ticket

### Quản lý Users

#### `list_users`
Lấy danh sách users.

**Parameters:**
- `limit` (optional): Số lượng users tối đa

#### `get_user`
Lấy thông tin chi tiết của một user.

**Parameters:**
- `user_id` (required): ID của user

### Quản lý Assets

#### `list_assets`
Lấy danh sách assets.

**Parameters:**
- `limit` (optional): Số lượng assets tối đa

#### `get_asset`
Lấy thông tin chi tiết của một asset.

**Parameters:**
- `asset_id` (required): ID của asset

### Quản lý Technicians

#### `list_technicians`
Lấy danh sách technicians.

**Parameters:**
- `limit` (optional): Số lượng technicians tối đa

### Tìm kiếm và Tham chiếu

#### `search_tickets`
Tìm kiếm tickets theo từ khóa.

**Parameters:**
- `query` (required): Từ khóa tìm kiếm
- `limit` (optional): Số lượng kết quả tối đa

#### `get_categories`
Lấy danh sách các danh mục có sẵn.

#### `get_priorities`
Lấy danh sách các mức độ ưu tiên có sẵn.

#### `get_statuses`
Lấy danh sách các trạng thái có sẵn.

### Quản lý Comments

#### `add_ticket_comment`
Thêm comment vào ticket.

**Parameters:**
- `ticket_id` (required): ID của ticket
- `comment` (required): Nội dung comment

#### `get_ticket_comments`
Lấy danh sách comments của ticket.

**Parameters:**
- `ticket_id` (required): ID của ticket

## Quản lý Admin

### Quản lý Sites

#### `list_sites`
Lấy danh sách sites với bộ lọc.

**Parameters:**
- `limit` (optional): Số lượng sites tối đa (mặc định: 50)
- `site_type` (optional): Lọc theo loại site (headquarters, branch_office, data_center, warehouse, retail_store, manufacturing_plant)
- `status` (optional): Lọc theo trạng thái site

**Ví dụ:**
```
Lấy danh sách 10 sites có loại "branch_office"
```

#### `get_site`
Lấy thông tin chi tiết của một site.

**Parameters:**
- `site_id` (required): ID của site

#### `create_site`
Tạo site mới.

**Parameters:**
- `name` (required): Tên site
- `site_type` (required): Loại site
- `address` (optional): Địa chỉ
- `city` (optional): Thành phố
- `state` (optional): Tỉnh/Bang
- `country` (optional): Quốc gia
- `zip_code` (optional): Mã bưu điện
- `phone` (optional): Số điện thoại
- `email` (optional): Email liên hệ
- `description` (optional): Mô tả

**Ví dụ:**
```
Tạo site mới "Branch Office Hanoi" với loại "branch_office", địa chỉ "123 Nguyen Trai, Hanoi, Vietnam"
```

#### `update_site`
Cập nhật thông tin site.

**Parameters:**
- `site_id` (required): ID của site
- `name` (optional): Tên mới
- `site_type` (optional): Loại site mới
- `address` (optional): Địa chỉ mới
- `city` (optional): Thành phố mới
- `state` (optional): Tỉnh/Bang mới
- `country` (optional): Quốc gia mới
- `zip_code` (optional): Mã bưu điện mới
- `phone` (optional): Số điện thoại mới
- `email` (optional): Email liên hệ mới
- `description` (optional): Mô tả mới

#### `delete_site`
Xóa một site.

**Parameters:**
- `site_id` (required): ID của site

#### `get_site_types`
Lấy danh sách các loại site có sẵn.

### Quản lý User Groups

#### `list_user_groups`
Lấy danh sách user groups.

**Parameters:**
- `limit` (optional): Số lượng groups tối đa
- `group_type` (optional): Lọc theo loại group (department, project, location_based, role_based, custom)
- `site_id` (optional): Lọc theo site ID

#### `get_user_group`
Lấy thông tin chi tiết của một user group.

**Parameters:**
- `group_id` (required): ID của user group

#### `create_user_group`
Tạo user group mới.

**Parameters:**
- `name` (required): Tên group
- `group_type` (required): Loại group
- `description` (optional): Mô tả
- `site_id` (optional): ID của site liên quan
- `manager` (optional): ID của manager

**Ví dụ:**
```
Tạo user group "IT Support Team" với loại "department", mô tả "Team hỗ trợ IT"
```

#### `update_user_group`
Cập nhật thông tin user group.

**Parameters:**
- `group_id` (required): ID của user group
- `name` (optional): Tên mới
- `group_type` (optional): Loại group mới
- `description` (optional): Mô tả mới
- `site_id` (optional): ID của site liên quan mới
- `manager` (optional): ID của manager mới

#### `delete_user_group`
Xóa một user group.

**Parameters:**
- `group_id` (required): ID của user group

#### `get_group_types`
Lấy danh sách các loại group có sẵn.

#### `get_group_permissions`
Lấy permissions của một user group.

**Parameters:**
- `group_id` (required): ID của user group

#### `update_group_permissions`
Cập nhật permissions cho một user group.

**Parameters:**
- `group_id` (required): ID của user group
- `permissions` (required): Object chứa các permissions với level tương ứng (none, read, write, admin)

**Ví dụ:**
```
Cập nhật permissions cho group "IT Support" với "read" cho tickets và "write" cho assets
```

### Quản lý Users & Technicians (Admin)

#### `list_admin_users`
Lấy danh sách admin users.

**Parameters:**
- `limit` (optional): Số lượng users tối đa
- `status` (optional): Lọc theo trạng thái (active, inactive, locked, pending_activation)
- `role` (optional): Lọc theo role (admin, manager, technician, user, viewer)
- `site_id` (optional): Lọc theo site ID

#### `get_admin_user`
Lấy thông tin chi tiết của một admin user.

**Parameters:**
- `user_id` (required): ID của user

#### `create_admin_user`
Tạo admin user mới.

**Parameters:**
- `username` (required): Tên đăng nhập
- `email` (required): Email
- `first_name` (required): Tên
- `last_name` (required): Họ
- `password` (optional): Mật khẩu
- `role` (optional): Role (admin, manager, technician, user, viewer)
- `site_id` (optional): ID của site
- `department` (optional): Phòng ban
- `phone` (optional): Số điện thoại
- `status` (optional): Trạng thái (active, inactive, locked, pending_activation)

**Ví dụ:**
```
Tạo admin user "john.doe" với email "john.doe@company.com", role "technician", gán vào site "Headquarters"
```

#### `update_admin_user`
Cập nhật thông tin admin user.

**Parameters:**
- `user_id` (required): ID của user
- `username` (optional): Tên đăng nhập mới
- `email` (optional): Email mới
- `first_name` (optional): Tên mới
- `last_name` (optional): Họ mới
- `role` (optional): Role mới
- `site_id` (optional): ID của site mới
- `department` (optional): Phòng ban mới
- `phone` (optional): Số điện thoại mới
- `status` (optional): Trạng thái mới

#### `delete_admin_user`
Xóa một admin user.

**Parameters:**
- `user_id` (required): ID của user

#### `list_admin_technicians`
Lấy danh sách admin technicians.

**Parameters:**
- `limit` (optional): Số lượng technicians tối đa
- `status` (optional): Lọc theo trạng thái
- `role` (optional): Lọc theo role
- `site_id` (optional): Lọc theo site ID

#### `get_admin_technician`
Lấy thông tin chi tiết của một admin technician.

**Parameters:**
- `technician_id` (required): ID của technician

#### `create_admin_technician`
Tạo admin technician mới.

**Parameters:**
- `username` (required): Tên đăng nhập
- `email` (required): Email
- `first_name` (required): Tên
- `last_name` (required): Họ
- `password` (optional): Mật khẩu
- `role` (optional): Role
- `site_id` (optional): ID của site
- `department` (optional): Phòng ban
- `phone` (optional): Số điện thoại
- `status` (optional): Trạng thái
- `skills` (optional): Danh sách kỹ năng
- `specializations` (optional): Danh sách chuyên môn

**Ví dụ:**
```
Tạo technician "jane.smith" với skills "network, security" và specializations "firewall"
```

#### `update_admin_technician`
Cập nhật thông tin admin technician.

**Parameters:**
- `technician_id` (required): ID của technician
- `username` (optional): Tên đăng nhập mới
- `email` (optional): Email mới
- `first_name` (optional): Tên mới
- `last_name` (optional): Họ mới
- `role` (optional): Role mới
- `site_id` (optional): ID của site mới
- `department` (optional): Phòng ban mới
- `phone` (optional): Số điện thoại mới
- `status` (optional): Trạng thái mới
- `skills` (optional): Danh sách kỹ năng mới
- `specializations` (optional): Danh sách chuyên môn mới

#### `delete_admin_technician`
Xóa một admin technician.

**Parameters:**
- `technician_id` (required): ID của technician

#### `get_user_roles`
Lấy danh sách các user roles có sẵn.

#### `get_technician_roles`
Lấy danh sách các technician roles có sẵn.

### Quản lý Permissions

#### `get_permissions`
Lấy danh sách tất cả permissions có sẵn.

#### `get_role_permissions`
Lấy permissions của một role.

**Parameters:**
- `role_id` (required): ID của role

#### `update_role_permissions`
Cập nhật permissions cho một role.

**Parameters:**
- `role_id` (required): ID của role
- `permissions` (required): Object chứa các permissions với level tương ứng

#### `get_user_permissions`
Lấy permissions của một user.

**Parameters:**
- `user_id` (required): ID của user

#### `update_user_permissions`
Cập nhật permissions cho một user.

**Parameters:**
- `user_id` (required): ID của user
- `permissions` (required): Object chứa các permissions với level tương ứng

### Quản lý Departments

#### `list_departments`
Lấy danh sách departments.

**Parameters:**
- `limit` (optional): Số lượng departments tối đa
- `department_type` (optional): Lọc theo loại department
- `site_id` (optional): Lọc theo site ID

#### `get_department`
Lấy thông tin chi tiết của một department.

**Parameters:**
- `department_id` (required): ID của department

#### `create_department`
Tạo department mới.

**Parameters:**
- `name` (required): Tên department
- `department_type` (required): Loại department
- `description` (optional): Mô tả
- `site_id` (optional): ID của site liên quan
- `manager` (optional): ID của manager

#### `update_department`
Cập nhật thông tin department.

**Parameters:**
- `department_id` (required): ID của department
- `name` (optional): Tên mới
- `department_type` (optional): Loại department mới
- `description` (optional): Mô tả mới
- `site_id` (optional): ID của site liên quan mới
- `manager` (optional): ID của manager mới

#### `delete_department`
Xóa một department.

**Parameters:**
- `department_id` (required): ID của department

#### `get_department_types`
Lấy danh sách các loại department có sẵn.

### Quản lý Locations

#### `list_locations`
Lấy danh sách locations.

**Parameters:**
- `limit` (optional): Số lượng locations tối đa
- `location_type` (optional): Lọc theo loại location
- `site_id` (optional): Lọc theo site ID

#### `get_location`
Lấy thông tin chi tiết của một location.

**Parameters:**
- `location_id` (required): ID của location

#### `create_location`
Tạo location mới.

**Parameters:**
- `name` (required): Tên location
- `location_type` (required): Loại location
- `description` (optional): Mô tả
- `site_id` (optional): ID của site liên quan
- `address` (optional): Địa chỉ
- `floor` (optional): Tầng
- `room` (optional): Phòng

#### `update_location`
Cập nhật thông tin location.

**Parameters:**
- `location_id` (required): ID của location
- `name` (optional): Tên mới
- `location_type` (optional): Loại location mới
- `description` (optional): Mô tả mới
- `site_id` (optional): ID của site liên quan mới
- `address` (optional): Địa chỉ mới
- `floor` (optional): Tầng mới
- `room` (optional): Phòng mới

#### `delete_location`
Xóa một location.

**Parameters:**
- `location_id` (required): ID của location

#### `get_location_types`
Lấy danh sách các loại location có sẵn.

### Quản lý System Settings

#### `get_system_settings`
Lấy cài đặt hệ thống hiện tại.

#### `update_system_settings`
Cập nhật cài đặt hệ thống.

**Parameters:**
- `settings` (required): Object chứa các cài đặt hệ thống cần cập nhật

#### `get_email_settings`
Lấy cài đặt email hiện tại.

#### `update_email_settings`
Cập nhật cài đặt email.

**Parameters:**
- `settings` (required): Object chứa các cài đặt email cần cập nhật

#### `get_notification_settings`
Lấy cài đặt thông báo hiện tại.

#### `update_notification_settings`
Cập nhật cài đặt thông báo.

**Parameters:**
- `settings` (required): Object chứa các cài đặt thông báo cần cập nhật

## Ví dụ Sử Dụng Thực Tế

### Quản lý Infrastructure
```
"Tạo site mới 'Data Center Singapore' với loại data_center"
"Tạo location 'Server Room A' trong site 'Data Center Singapore'"
"Tạo department 'Infrastructure Team' và gán manager"
"Tạo user group 'Network Admins' với permissions phù hợp"
```

### Quản lý Users
```
"Tạo admin user 'john.doe' với role technician"
"Gán user 'john.doe' vào department 'IT Support'"
"Cập nhật permissions cho role 'manager'"
"Tạo technician 'jane.smith' với skills 'network, security'"
```

### Quản lý Permissions
```
"Lấy danh sách tất cả permissions có sẵn"
"Gán permission 'admin' cho tickets cho role 'manager'"
"Cập nhật permissions cho user 'john.doe'"
"Kiểm tra permissions của group 'IT Support'"
```

### Quản lý System
```
"Lấy cài đặt hệ thống hiện tại"
"Cập nhật email settings để gửi thông báo tickets"
"Cấu hình notification settings cho high priority tickets"
"Kiểm tra email settings cho automated reports"
```

## Troubleshooting

### Lỗi thường gặp

1. **Authentication Error**
   - Kiểm tra username/password trong file .env
   - Đảm bảo API key hợp lệ (nếu sử dụng)

2. **Connection Error**
   - Kiểm tra URL trong SDP_BASE_URL
   - Đảm bảo ServiceDesk Plus instance đang hoạt động

3. **Permission Error**
   - Kiểm tra quyền của user trong ServiceDesk Plus
   - Đảm bảo user có quyền admin cho các thao tác admin

4. **Validation Error**
   - Kiểm tra các trường bắt buộc trong request
   - Đảm bảo định dạng dữ liệu đúng

### Debug

Chạy test connection để kiểm tra:
```bash
python test_connection.py
```

Kiểm tra logs chi tiết:
```bash
python main.py --verbose
```

## Best Practices

1. **Security**
   - Luôn sử dụng principle of least privilege
   - Regular audit permissions và access rights
   - Logging tất cả admin activities

2. **Performance**
   - Sử dụng pagination cho danh sách lớn
   - Cache dữ liệu thường dùng
   - Batch operations khi có thể

3. **Maintenance**
   - Regular backup admin configurations
   - Review và cleanup unused users/groups
   - Monitor system performance

4. **Documentation**
   - Document tất cả custom workflows
   - Maintain user role matrix
   - Keep site/department hierarchy updated 