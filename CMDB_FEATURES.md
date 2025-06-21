# CMDB Features - ServiceDesk Plus MCP Server

## 🎯 **Tổng quan về CMDB**

MCP server đã được mở rộng để hỗ trợ đầy đủ các chức năng CMDB (Configuration Management Database) của ServiceDesk Plus, bao gồm:

## 📋 **Các Module CMDB Đã Hỗ Trợ**

### 1. **Configuration Items (CIs) Management**
- ✅ `list_configuration_items` - Lấy danh sách CIs với bộ lọc
- ✅ `get_configuration_item` - Lấy chi tiết CI
- ✅ `create_configuration_item` - Tạo CI mới
- ✅ `update_configuration_item` - Cập nhật CI
- ✅ `delete_configuration_item` - Xóa CI
- ✅ `get_ci_types` - Lấy danh sách loại CIs
- ✅ `get_ci_relationships` - Lấy relationships của CI

**Ví dụ sử dụng:**
```
"Tạo Configuration Item mới cho server web với tên 'WEB-SRV-001', loại 'server', trạng thái 'active'"
"Lấy danh sách 20 Configuration Items có loại 'network_device' và trạng thái 'active'"
"Cập nhật CI WEB-SRV-001 với trạng thái 'under_maintenance'"
```

### 2. **Asset Management**
- ✅ `list_assets` - Lấy danh sách assets với bộ lọc
- ✅ `get_asset` - Lấy chi tiết asset
- ✅ `create_asset` - Tạo asset mới
- ✅ `update_asset` - Cập nhật asset
- ✅ `delete_asset` - Xóa asset
- ✅ `get_asset_types` - Lấy danh sách loại assets
- ✅ `get_asset_categories` - Lấy danh mục assets
- ✅ `get_asset_locations` - Lấy vị trí assets
- ✅ `get_asset_models` - Lấy model assets
- ✅ `get_asset_vendors` - Lấy vendor assets

**Ví dụ sử dụng:**
```
"Tạo asset mới với tên 'LAPTOP-001', loại 'laptop', trạng thái 'in_use', gán cho 'john.doe@company.com'"
"Lấy danh sách assets có trạng thái 'under_maintenance' và vị trí 'IT Department'"
"Cập nhật asset LAPTOP-001 với trạng thái 'retired'"
```

### 3. **Software License Management**
- ✅ `list_software_licenses` - Lấy danh sách software licenses
- ✅ `get_software_license` - Lấy chi tiết license
- ✅ `create_software_license` - Tạo license mới
- ✅ `update_software_license` - Cập nhật license
- ✅ `get_software_products` - Lấy danh sách software products
- ✅ `get_license_types` - Lấy loại licenses

**Ví dụ sử dụng:**
```
"Tạo software license mới cho 'Microsoft Office 365' với 100 licenses, vendor 'Microsoft'"
"Lấy danh sách licenses có vendor 'Adobe' và sản phẩm 'Photoshop'"
"Cập nhật license Office 365 với số lượng licenses mới là 150"
```

### 4. **Contract Management**
- ✅ `list_contracts` - Lấy danh sách contracts
- ✅ `get_contract` - Lấy chi tiết contract
- ✅ `create_contract` - Tạo contract mới
- ✅ `update_contract` - Cập nhật contract
- ✅ `get_contract_types` - Lấy loại contracts
- ✅ `get_contract_vendors` - Lấy vendor contracts

**Ví dụ sử dụng:**
```
"Tạo contract mới với vendor 'Dell', bắt đầu từ '2024-01-01', kết thúc '2024-12-31'"
"Lấy danh sách contracts có trạng thái 'active' và vendor 'Microsoft'"
"Cập nhật contract Dell với ngày kết thúc mới '2025-12-31'"
```

### 5. **Purchase Order Management**
- ✅ `list_purchase_orders` - Lấy danh sách purchase orders
- ✅ `get_purchase_order` - Lấy chi tiết purchase order
- ✅ `create_purchase_order` - Tạo purchase order mới
- ✅ `update_purchase_order` - Cập nhật purchase order
- ✅ `get_po_statuses` - Lấy trạng thái purchase orders

**Ví dụ sử dụng:**
```
"Tạo purchase order mới với vendor 'HP' cho 10 laptops"
"Lấy danh sách purchase orders có trạng thái 'pending_approval'"
"Cập nhật PO HP-001 với trạng thái 'approved'"
```

### 6. **Vendor Management**
- ✅ `list_vendors` - Lấy danh sách vendors
- ✅ `get_vendor` - Lấy chi tiết vendor
- ✅ `create_vendor` - Tạo vendor mới
- ✅ `update_vendor` - Cập nhật vendor
- ✅ `get_vendor_types` - Lấy loại vendors

**Ví dụ sử dụng:**
```
"Tạo vendor mới 'Dell Technologies' với email 'contact@dell.com'"
"Lấy thông tin chi tiết của vendor 'Microsoft'"
"Cập nhật vendor Dell với số điện thoại mới"
```

## 🔧 **Các Trạng Thái và Loại Dữ Liệu**

### **Asset Statuses:**
- `in_use` - Đang sử dụng
- `in_stock` - Trong kho
- `under_maintenance` - Đang bảo trì
- `retired` - Đã nghỉ hưu
- `lost` - Bị mất
- `stolen` - Bị đánh cắp

### **CI Statuses:**
- `active` - Hoạt động
- `inactive` - Không hoạt động
- `under_maintenance` - Đang bảo trì
- `retired` - Đã nghỉ hưu

### **Contract Statuses:**
- `active` - Đang hiệu lực
- `expired` - Đã hết hạn
- `pending` - Chờ xử lý
- `terminated` - Đã chấm dứt

### **Purchase Order Statuses:**
- `draft` - Bản nháp
- `pending_approval` - Chờ phê duyệt
- `approved` - Đã phê duyệt
- `ordered` - Đã đặt hàng
- `received` - Đã nhận hàng
- `cancelled` - Đã hủy

## 🎯 **Ví dụ Sử Dụng Thực Tế**

### **Quản lý Infrastructure:**
```
"Tạo Configuration Item cho server database mới 'DB-SRV-001'"
"Lấy danh sách tất cả network devices đang hoạt động"
"Tạo asset cho switch mới và gán vào data center"
```

### **Quản lý Software:**
```
"Tạo software license cho Adobe Creative Suite với 50 licenses"
"Kiểm tra số lượng licenses còn lại cho Microsoft Office"
"Cập nhật license Adobe với ngày hết hạn mới"
```

### **Quản lý Contracts:**
```
"Tạo contract bảo trì với vendor Dell cho 3 năm"
"Lấy danh sách contracts sắp hết hạn trong 30 ngày tới"
"Cập nhật contract Microsoft với giá trị mới"
```

### **Quản lý Procurement:**
```
"Tạo purchase order cho 20 monitors từ vendor HP"
"Kiểm tra trạng thái purchase order PO-2024-001"
"Cập nhật PO với ngày giao hàng mới"
```

## 🔍 **Tìm Kiếm và Báo Cáo**

Tất cả các tools đều hỗ trợ:
- **Pagination** - Giới hạn số lượng kết quả
- **Filtering** - Lọc theo các tiêu chí khác nhau
- **Search** - Tìm kiếm theo từ khóa
- **Sorting** - Sắp xếp kết quả

## 📊 **Tích Hợp với AI**

MCP server cho phép AI assistant:
- **Tự động tạo** CIs, assets, licenses, contracts
- **Theo dõi** trạng thái và lifecycle của các items
- **Báo cáo** về inventory và compliance
- **Quản lý** relationships giữa các items
- **Tối ưu hóa** procurement và vendor management

## 🚀 **Lợi Ích**

1. **Centralized Management** - Quản lý tập trung tất cả configuration items
2. **Compliance Tracking** - Theo dõi compliance với licenses và contracts
3. **Asset Lifecycle** - Quản lý toàn bộ lifecycle của assets
4. **Vendor Management** - Quản lý hiệu quả các vendor relationships
5. **Procurement Automation** - Tự động hóa quy trình mua sắm
6. **Reporting & Analytics** - Báo cáo và phân tích dữ liệu CMDB

Với các chức năng CMDB này, MCP server cung cấp một giải pháp hoàn chỉnh để quản lý toàn bộ IT infrastructure thông qua AI assistant! 