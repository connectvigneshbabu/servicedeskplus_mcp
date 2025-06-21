# Admin Management Features

## 🎯 **Tổng quan**

ServiceDesk Plus MCP Server hỗ trợ đầy đủ các chức năng quản trị hệ thống (Admin Management) bao gồm quản lý sites, user groups, users, technicians, permissions, departments, locations và system settings.

## 🏢 **Site Management**

### **Tính năng:**
- ✅ **CRUD Operations** - Tạo, đọc, cập nhật, xóa sites
- ✅ **Site Types** - Hỗ trợ các loại site: headquarters, branch_office, data_center, warehouse, retail_store, manufacturing_plant
- ✅ **Location Details** - Địa chỉ, thành phố, quốc gia, mã bưu điện
- ✅ **Contact Information** - Số điện thoại, email liên hệ
- ✅ **Filtering** - Lọc theo loại site, trạng thái

### **Tools (6 tools):**
- `list_sites` - Lấy danh sách sites với bộ lọc
- `get_site` - Lấy thông tin chi tiết site
- `create_site` - Tạo site mới
- `update_site` - Cập nhật thông tin site
- `delete_site` - Xóa site
- `get_site_types` - Lấy danh sách loại sites

### **Ví dụ sử dụng:**
```
"Tạo site mới 'Branch Office Hanoi' với loại branch_office"
"Lấy danh sách tất cả data centers"
"Cập nhật địa chỉ cho site 'Headquarters'"
"Xóa site 'Old Warehouse' không còn sử dụng"
```

## 👥 **User Group Management**

### **Tính năng:**
- ✅ **CRUD Operations** - Tạo, đọc, cập nhật, xóa user groups
- ✅ **Group Types** - Hỗ trợ các loại group: department, project, location_based, role_based, custom
- ✅ **Permission Management** - Gán và quản lý permissions cho groups
- ✅ **Site Association** - Liên kết groups với sites
- ✅ **Manager Assignment** - Gán manager cho groups

### **Tools (8 tools):**
- `list_user_groups` - Lấy danh sách user groups
- `get_user_group` - Lấy thông tin chi tiết user group
- `create_user_group` - Tạo user group mới
- `update_user_group` - Cập nhật user group
- `delete_user_group` - Xóa user group
- `get_group_types` - Lấy danh sách loại groups
- `get_group_permissions` - Lấy permissions của group
- `update_group_permissions` - Cập nhật permissions cho group

### **Ví dụ sử dụng:**
```
"Tạo user group 'IT Support Team' với loại department"
"Gán permissions 'read' cho tickets và 'write' cho assets cho group 'IT Support'"
"Lấy danh sách tất cả user groups trong site 'Headquarters'"
"Cập nhật manager cho group 'Software Development'"
```

## 👤 **User & Technician Management**

### **Tính năng:**
- ✅ **CRUD Operations** - Tạo, đọc, cập nhật, xóa users và technicians
- ✅ **Role Management** - Hỗ trợ roles: admin, manager, technician, user, viewer
- ✅ **Status Management** - Quản lý trạng thái: active, inactive, locked, pending_activation
- ✅ **Site Assignment** - Gán users/technicians vào sites
- ✅ **Department Assignment** - Gán vào departments
- ✅ **Skills & Specializations** - Quản lý kỹ năng và chuyên môn (cho technicians)

### **Tools (12 tools):**
- `list_admin_users` - Lấy danh sách admin users
- `get_admin_user` - Lấy thông tin chi tiết admin user
- `create_admin_user` - Tạo admin user mới
- `update_admin_user` - Cập nhật admin user
- `delete_admin_user` - Xóa admin user
- `list_admin_technicians` - Lấy danh sách admin technicians
- `get_admin_technician` - Lấy thông tin chi tiết admin technician
- `create_admin_technician` - Tạo admin technician mới
- `update_admin_technician` - Cập nhật admin technician
- `delete_admin_technician` - Xóa admin technician
- `get_user_roles` - Lấy danh sách user roles
- `get_technician_roles` - Lấy danh sách technician roles

### **Ví dụ sử dụng:**
```
"Tạo admin user 'john.doe' với role technician và gán vào site 'Headquarters'"
"Tạo technician 'jane.smith' với skills 'network, security' và specializations 'firewall'"
"Cập nhật role của user 'mike.wilson' từ user lên manager"
"Lấy danh sách tất cả technicians trong department 'IT Support'"
"Khóa user 'inactive.user' do không hoạt động"
```

## 🔐 **Permission Management**

### **Tính năng:**
- ✅ **Permission Levels** - Hỗ trợ các mức: none, read, write, admin
- ✅ **Role-based Permissions** - Quản lý permissions theo roles
- ✅ **User-specific Permissions** - Gán permissions riêng cho từng user
- ✅ **Permission Inheritance** - Kế thừa permissions từ roles và groups

### **Tools (5 tools):**
- `get_permissions` - Lấy danh sách tất cả permissions
- `get_role_permissions` - Lấy permissions của role
- `update_role_permissions` - Cập nhật permissions cho role
- `get_user_permissions` - Lấy permissions của user
- `update_user_permissions` - Cập nhật permissions cho user

### **Ví dụ sử dụng:**
```
"Lấy danh sách tất cả permissions có sẵn trong hệ thống"
"Gán permission 'admin' cho tickets và 'write' cho assets cho role 'manager'"
"Cập nhật permissions cho user 'john.doe' với 'read' cho reports"
"Kiểm tra permissions hiện tại của role 'technician'"
```

## 🏛️ **Department Management**

### **Tính năng:**
- ✅ **CRUD Operations** - Tạo, đọc, cập nhật, xóa departments
- ✅ **Department Types** - Hỗ trợ các loại department khác nhau
- ✅ **Site Association** - Liên kết departments với sites
- ✅ **Manager Assignment** - Gán manager cho departments
- ✅ **Organizational Structure** - Xây dựng cấu trúc tổ chức

### **Tools (6 tools):**
- `list_departments` - Lấy danh sách departments
- `get_department` - Lấy thông tin chi tiết department
- `create_department` - Tạo department mới
- `update_department` - Cập nhật department
- `delete_department` - Xóa department
- `get_department_types` - Lấy danh sách loại departments

### **Ví dụ sử dụng:**
```
"Tạo department 'Software Development' với loại IT"
"Gán manager 'tech.lead' cho department 'Development'"
"Lấy danh sách tất cả departments trong site 'Headquarters'"
"Cập nhật mô tả cho department 'Quality Assurance'"
"Xóa department 'Legacy Support' không còn hoạt động"
```

## 📍 **Location Management**

### **Tính năng:**
- ✅ **CRUD Operations** - Tạo, đọc, cập nhật, xóa locations
- ✅ **Location Types** - Hỗ trợ các loại location khác nhau
- ✅ **Site Association** - Liên kết locations với sites
- ✅ **Physical Details** - Địa chỉ, tầng, phòng
- ✅ **Hierarchical Structure** - Cấu trúc phân cấp locations

### **Tools (6 tools):**
- `list_locations` - Lấy danh sách locations
- `get_location` - Lấy thông tin chi tiết location
- `create_location` - Tạo location mới
- `update_location` - Cập nhật location
- `delete_location` - Xóa location
- `get_location_types` - Lấy danh sách loại locations

### **Ví dụ sử dụng:**
```
"Tạo location 'Server Room A' với loại data_center trong site 'Headquarters'"
"Lấy danh sách tất cả locations trên tầng 3"
"Cập nhật thông tin phòng cho location 'Conference Room 1'"
"Tạo location 'Warehouse Section B' với loại storage"
"Xóa location 'Old Office Space' không còn sử dụng"
```

## ⚙️ **System Settings**

### **Tính năng:**
- ✅ **System Configuration** - Cài đặt hệ thống chung
- ✅ **Email Settings** - Cấu hình email notifications
- ✅ **Notification Settings** - Cài đặt thông báo
- ✅ **Security Settings** - Cài đặt bảo mật
- ✅ **Performance Settings** - Tối ưu hiệu suất

### **Tools (6 tools):**
- `get_system_settings` - Lấy system settings
- `update_system_settings` - Cập nhật system settings
- `get_email_settings` - Lấy email settings
- `update_email_settings` - Cập nhật email settings
- `get_notification_settings` - Lấy notification settings
- `update_notification_settings` - Cập nhật notification settings

### **Ví dụ sử dụng:**
```
"Lấy cài đặt hệ thống hiện tại"
"Cập nhật email settings để gửi thông báo tickets"
"Cấu hình notification settings cho high priority tickets"
"Kiểm tra email settings cho automated reports"
"Cập nhật system settings cho performance optimization"
```

## 🔄 **Workflow Integration**

### **Tính năng:**
- ✅ **Automated User Provisioning** - Tự động tạo users dựa trên rules
- ✅ **Role-based Access Control** - Kiểm soát truy cập theo roles
- ✅ **Permission Inheritance** - Kế thừa permissions tự động
- ✅ **Site-based Organization** - Tổ chức theo sites
- ✅ **Department Hierarchy** - Cấu trúc phân cấp departments

### **Ví dụ workflows:**
```
"Khi tạo user mới, tự động gán vào department và site tương ứng"
"Khi thay đổi role của user, tự động cập nhật permissions"
"Khi tạo site mới, tự động tạo default locations và departments"
"Khi tạo department, tự động tạo user group tương ứng"
```

## 📊 **Reporting & Analytics**

### **Tính năng:**
- ✅ **User Activity Reports** - Báo cáo hoạt động users
- ✅ **Permission Audit** - Kiểm tra permissions
- ✅ **Site Utilization** - Sử dụng sites
- ✅ **Department Performance** - Hiệu suất departments
- ✅ **System Health** - Tình trạng hệ thống

### **Ví dụ reports:**
```
"Báo cáo số lượng users theo roles và sites"
"Kiểm tra permissions của tất cả admin users"
"Báo cáo utilization của các sites"
"Phân tích hiệu suất của departments"
"Audit log của các thay đổi permissions"
```

## 🛡️ **Security Features**

### **Tính năng:**
- ✅ **Role-based Security** - Bảo mật theo roles
- ✅ **Permission Validation** - Kiểm tra permissions
- ✅ **Audit Logging** - Ghi log các thay đổi
- ✅ **Access Control** - Kiểm soát truy cập
- ✅ **Data Protection** - Bảo vệ dữ liệu

### **Security Best Practices:**
```
"Luôn sử dụng principle of least privilege"
"Regular audit of permissions và access rights"
"Logging tất cả admin activities"
"Regular review của user roles và permissions"
"Backup và recovery của admin configurations"
```

## 🚀 **Benefits**

1. **Centralized Administration** - Quản trị tập trung toàn bộ hệ thống
2. **Role-based Access Control** - Kiểm soát truy cập theo roles
3. **Organizational Structure** - Cấu trúc tổ chức rõ ràng
4. **Automated Workflows** - Tự động hóa các quy trình
5. **Security Compliance** - Tuân thủ bảo mật
6. **Scalability** - Khả năng mở rộng
7. **Audit Trail** - Theo dõi lịch sử thay đổi

## 📈 **Performance**

- **Async Operations** - Tất cả operations đều async
- **Batch Processing** - Xử lý hàng loạt
- **Caching** - Cache dữ liệu thường dùng
- **Optimized Queries** - Tối ưu queries
- **Connection Pooling** - Quản lý connections hiệu quả

---

**Total Admin Tools:** 49 tools  
**Coverage:** ✅ Complete Admin Management  
**Integration:** ✅ Full CMDB Integration  
**Security:** ✅ Role-based Access Control 