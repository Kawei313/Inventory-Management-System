USE inventory_system;
INSERT INTO employee_data (empid, name, email, gender, dob, contact, employment_type, education, word_shift, address, doj, salary, usertype, password) VALUES
(1001, 'Nguyễn Văn An', 'an.nguyen@stockapp.com', 'Male', '1995-03-15', '0901234567', 'Full-time', 'Bachelor', 'Morning', '123 Đường Láng, Hà Nội', '2022-01-10', '15000000', 'admin', 'admin123'),
(1002, 'Trần Thị Bình', 'binh.tran@stockapp.com', 'Female', '1997-07-22', '0912345678', 'Part-time', 'College', 'Afternoon', '45 Nguyễn Trãi, TP.HCM', '2023-03-20', '8000000', 'user', 'user123'),
(1003, 'Lê Văn Cường', 'cuong.le@stockapp.com', 'Male', '1994-11-30', '0923456789', 'Full-time', 'Master', 'Morning', '78 Lê Lợi, Đà Nẵng', '2021-06-15', '18000000', 'user', 'cuong123'),
(1004, 'Phạm Minh Duy', 'duy.pham@stockapp.com', 'Male', '1996-05-18', '0934567890', 'Full-time', 'Bachelor', 'Night', '56 Trần Phú, Nha Trang', '2022-09-01', '14000000', 'user', 'duy123'),
(1005, 'Hoàng Thị Lan', 'lan.hoang@stockapp.com', 'Female', '1998-09-25', '0945678901', 'Part-time', 'High School', 'Afternoon', '89 Hùng Vương, Cần Thơ', '2023-07-10', '7000000', 'user', 'lan123'),
(1006, 'Vũ Anh Tuấn', 'tuan.vu@stockapp.com', 'Male', '1993-12-12', '0956789012', 'Full-time', 'Bachelor', 'Morning', '101 Pasteur, Hà Nội', '2021-11-05', '16000000', 'user', 'tuan123'),
(1007, 'Đỗ Thị Mai', 'mai.do@stockapp.com', 'Female', '1999-02-08', '0967890123', 'Intern', 'Student', 'Morning', '23 Nguyễn Huệ, Huế', '2024-01-15', '5000000', 'user', 'mai123'),
(1008, 'Bùi Văn Hùng', 'hung.bui@stockapp.com', 'Male', '1992-08-14', '0978901234', 'Full-time', 'Master', 'Night', '67 Hai Bà Trưng, Hải Phòng', '2020-04-20', '20000000', 'admin', 'hung123'),
(1009, 'Ngô Thị Ngọc', 'ngoc.ngo@stockapp.com', 'Female', '1997-04-19', '0989012345', 'Part-time', 'Bachelor', 'Afternoon', '34 Lê Hồng Phong, Quy Nhơn', '2023-05-12', '8500000', 'user', 'ngoc123'),
(1010, 'Đặng Văn Khánh', 'khanh.dang@stockapp.com', 'Male', '1995-10-03', '0990123456', 'Full-time', 'Bachelor', 'Morning', '12 Trần Hưng Đạo, Vũng Tàu', '2022-08-18', '14500000', 'user', 'khanh123'),
(1011, 'Lý Thị Kim', 'kim.ly@stockapp.com', 'Female', '1996-06-27', '0901122334', 'Full-time', 'College', 'Night', '90 Nguyễn Văn Cừ, Long Xuyên', '2021-12-01', '13000000', 'user', 'kim123'),
(1012, 'Trương Văn Long', 'long.truong@stockapp.com', 'Male', '1994-01-05', '0912233445', 'Full-time', 'Bachelor', 'Morning', '45 Phạm Ngũ Lão, Biên Hòa', '2022-02-28', '15500000', 'user', 'long123'),
(1013, 'Hà Thị Minh', 'minh.ha@stockapp.com', 'Female', '1998-11-11', '0923344556', 'Part-time', 'High School', 'Afternoon', '78 Võ Văn Tần, Đà Lạt', '2023-09-05', '7500000', 'user', 'minh123'),
(1014, 'Phan Văn Nam', 'nam.phan@stockapp.com', 'Male', '1993-07-07', '0934455667', 'Full-time', 'Master', 'Morning', '56 Bạch Đằng, Thanh Hóa', '2021-03-10', '19000000', 'user', 'nam123'),
(1015, 'Tô Thị Oanh', 'oanh.to@stockapp.com', 'Female', '1997-03-30', '0945566778', 'Intern', 'Student', 'Afternoon', '23 Nguyễn Thái Học, Vinh', '2024-02-20', '5500000', 'user', 'oanh123');

INSERT INTO supplier_data (invoice, name, contact, description) VALUES
(5001, 'Công ty TNHH Thực phẩm ABC', '0281234567', 'Chuyên cung cấp thực phẩm tươi sống'),
(5002, 'Nhà máy Điện tử XYZ', '0249876543', 'Sản xuất linh kiện điện tử, smartphone'),
(5003, 'Xí nghiệp May mặc Việt', '0253698741', 'Sản xuất quần áo thời trang'),
(5004, 'Công ty Giấy Sài Gòn', '0287418523', 'Cung cấp giấy A4, văn phòng phẩm'),
(5005, 'Nhà máy Xi măng Hà Tiên', '0289638521', 'Xi măng chất lượng cao'),
(5006, 'Công ty Dụng cụ Y tế MediCo', '0247412589', 'Khẩu trang, găng tay y tế'),
(5007, 'Cửa hàng Nội thất LuxHome', '0278529631', 'Ghế văn phòng, bàn làm việc'),
(5008, 'Đại lý Lốp xe Bridgestone', '0281597536', 'Lốp xe ô tô, xe máy'),
(5009, 'Công ty Hóa chất CleanPro', '0243698521', 'Nước lau sàn, chất tẩy rửa'),
(5010, 'Nhà phân phối Thực phẩm khô', '0258741963', 'Gạo, mì gói, gia vị'),
(5011, 'Công ty Điện lạnh Panasonic', '0287531594', 'Máy lạnh, tủ lạnh'),
(5012, 'Nhà máy Nhựa Duy Tân', '0279514832', 'Ống nhựa, thùng chứa');

INSERT INTO category_data (id, name, description) VALUES
(1, 'Văn phòng phẩm', 'Giấy, bút, dụng cụ văn phòng'),
(2, 'Thực phẩm tươi', 'Rau củ, trái cây, thịt cá'),
(3, 'Điện tử', 'Điện thoại, máy tính, linh kiện'),
(4, 'Thời trang', 'Quần áo, giày dép, phụ kiện'),
(5, 'Xây dựng', 'Xi măng, sắt thép, vật liệu'),
(6, 'Y tế', 'Khẩu trang, thuốc, thiết bị y tế'),
(7, 'Nội thất', 'Bàn ghế, tủ, giường'),
(8, 'Ô tô - Xe máy', 'Lốp xe, phụ tùng'),
(9, 'Hóa chất', 'Xà phòng, nước tẩy, chất vệ sinh'),
(10, 'Thực phẩm khô', 'Gạo, mì, đồ hộp'),
(11, 'Điện lạnh', 'Máy lạnh, tủ lạnh, quạt'),
(12, 'Nhựa gia dụng', 'Thùng, xô, chậu nhựa');

INSERT INTO product_data (category, supplier, name, price, quantity, status) VALUES
('Văn phòng phẩm', 'Công ty Giấy Sài Gòn', 'Giấy A4 Double A 70gsm', 75000.00, 150, 'In Stock'),
('Văn phòng phẩm', 'Công ty Giấy Sài Gòn', 'Bút bi Thiên Long', 5000.00, 500, 'In Stock'),
('Thực phẩm tươi', 'Công ty TNHH Thực phẩm ABC', 'Táo Fuji New Zealand', 45000.00, 80, 'In Stock'),
('Thực phẩm tươi', 'Công ty TNHH Thực phẩm ABC', 'Rau bina hữu cơ', 15000.00, 120, 'In Stock'),
('Điện tử', 'Nhà máy Điện tử XYZ', 'Điện thoại Samsung A54', 8500000.00, 25, 'In Stock'),
('Điện tử', 'Nhà máy Điện tử XYZ', 'Máy khoan Bosch GSB 550', 1250000.00, 40, 'In Stock'),
('Thời trang', 'Xí nghiệp May mặc Việt', 'Áo thun nam cotton', 150000.00, 200, 'In Stock'),
('Xây dựng', 'Nhà máy Xi măng Hà Tiên', 'Xi măng Hà Tiên PCB40', 85000.00, 300, 'In Stock'),
('Y tế', 'Công ty Dụng cụ Y tế MediCo', 'Khẩu trang y tế 4 lớp', 45000.00, 1000, 'In Stock'),
('Nội thất', 'Cửa hàng Nội thất LuxHome', 'Ghế xoay văn phòng', 890000.00, 35, 'In Stock'),
('Ô tô - Xe máy', 'Đại lý Lốp xe Bridgestone', 'Lốp xe Michelin 185/60R14', 1350000.00, 60, 'In Stock'),
('Hóa chất', 'Công ty Hóa chất CleanPro', 'Nước lau sàn Sunlight 1L', 35000.00, 180, 'In Stock'),
('Thực phẩm khô', 'Nhà phân phối Thực phẩm khô', 'Gạo ST25 5kg', 125000.00, 90, 'In Stock'),
('Điện lạnh', 'Công ty Điện lạnh Panasonic', 'Máy lạnh Panasonic 1HP', 8500000.00, 15, 'Low Stock'),
('Nhựa gia dụng', 'Nhà máy Nhựa Duy Tân', 'Thùng rác nhựa 60L', 180000.00, 70, 'In Stock'),
('Văn phòng phẩm', 'Công ty Giấy Sài Gòn', 'Sổ tay lò xo A5', 25000.00, 300, 'In Stock'),
('Thực phẩm tươi', 'Công ty TNHH Thực phẩm ABC', 'Thịt bò nhập khẩu', 350000.00, 50, 'In Stock'),
('Điện tử', 'Nhà máy Điện tử XYZ', 'Tai nghe Bluetooth Sony', 1200000.00, 80, 'In Stock'),
('Thời trang', 'Xí nghiệp May mặc Việt', 'Quần jeans nam slimfit', 350000.00, 120, 'In Stock'),
('Y tế', 'Công ty Dụng cụ Y tế MediCo', 'Găng tay y tế Latex', 85000.00, 400, 'In Stock'),
('Ô tô - Xe máy', 'Đại lý Lốp xe Bridgestone', 'Dầu nhớt Castrol 4T', 135000.00, 150, 'In Stock');

INSERT INTO sales_items (invoice_no, product_name, quantity, price, discount, final_price) VALUES
(100001, 'Giấy A4 Double A 70gsm', 3, 75000.00, 22500.00, 202500.00),
(100001, 'Bút bi Thiên Long', 5, 5000.00, 0.00, 25000.00),
(100002, 'Điện thoại Samsung A54', 1, 8500000.00, 850000.00, 7650000.00),
(100003, 'Áo thun nam cotton', 1, 150000.00, 0.00, 150000.00),
(100004, 'Máy khoan Bosch GSB 550', 1, 1250000.00, 125000.00, 1125000.00),
(100004, 'Lốp xe Michelin 185/60R14', 1, 1350000.00, 135000.00, 1215000.00),
(100005, 'Táo Fuji New Zealand', 10, 45000.00, 45000.00, 405000.00),
(100006, 'Ghế xoay văn phòng', 1, 890000.00, 0.00, 890000.00),
(100007, 'Lốp xe Michelin 185/60R14', 1, 1350000.00, 135000.00, 1215000.00),
(100008, 'Gạo ST25 5kg', 1, 125000.00, 0.00, 125000.00),
(100009, 'Nước lau sàn Sunlight 1L', 1, 35000.00, 0.00, 35000.00),
(100010, 'Tai nghe Bluetooth Sony', 1, 1200000.00, 120000.00, 1080000.00),
(100011, 'Thùng rác nhựa 60L', 1, 180000.00, 18000.00, 162000.00),
(100012, 'Bút bi Thiên Long', 1, 5000.00, 0.00, 5000.00),
(100013, 'Máy lạnh Panasonic 1HP', 1, 8500000.00, 850000.00, 7650000.00),
(100014, 'Dầu nhớt Castrol 4T', 1, 135000.00, 0.00, 135000.00),
(100015, 'Ghế xoay văn phòng', 1, 890000.00, 89000.00, 801000.00);

INSERT INTO user_accounts (empid, username, password, role) VALUES
(1001, 'an.nguyen', 'admin123', 'admin'),   -- admin
(1002, 'binh.tran', 'user123', 'user'),     -- user
(1003, 'cuong.le', 'cuong123', 'user'),     -- user
(1004, 'duy.pham', 'duy123', 'user');       -- user
