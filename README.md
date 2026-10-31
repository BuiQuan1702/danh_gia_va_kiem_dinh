# Báo cáo kiểm thử và đánh giá chất lượng website bán hàng QUDENA

## Thông tin nhóm

- **Môn học:** [Đánh giá và kiểm định chất lượng phần mềm]
- **Giảng viên:** [TS. Trịnh Thanh Bình]
- **Thành viên 1 (thực hiện kiểm thử):** [Bùi Minh Quân] – MSSV 23010725
- **Thành viên 2 (viết báo cáo, video):** [Nguyễn Ngọc Trọng] – MSSV 23010763
- **Đối tượng kiểm thử:** website bán hàng thời trang QUDENA (PHP, Laravel), chạy local tại `http://127.0.0.1:8000`

## 1. Mục tiêu

- Kiểm thử và đánh giá chất lượng website bán hàng bằng các công cụ kiểm thử phần mềm.
- **Postman:** kiểm thử các request HTTP (trang công khai, bảo mật, đăng nhập, giỏ hàng) bằng test script.
- **Selenium:** kiểm thử tự động giao diện qua trình duyệt Chrome (đăng nhập, tìm kiếm, giỏ hàng, đăng xuất).
- **JMeter:** kiểm thử hiệu năng với nhiều người dùng đồng thời.

## 2. Môi trường kiểm thử

| Hạng mục | Thông tin |
|---|---|
| Website | QUDENA, Laravel/PHP, chạy bằng `php artisan serve` |
| Địa chỉ | `http://127.0.0.1:8000` |
| Hệ điều hành | Windows 11 |
| Postman | Desktop [phiên bản], chế độ Local |
| Selenium | Python 3.14.2, selenium 4.52.0, pytest 9.2.0, pytest-html 4.2.0 |
| Trình duyệt | Google Chrome 156 |
| JMeter | Apache JMeter 5.6.3 |
| Cấu hình máy | CPU [...], RAM [...] |
| Tài khoản test | Tài khoản khách hàng thường dùng riêng cho kiểm thử |

Lưu ý: toàn bộ kết quả đo trên máy local, phụ thuộc cấu hình máy và máy chủ phát triển `php artisan serve`.

## 3. Cấu trúc repository

```
.
├── README.md
├── .gitignore
├── images/                      # Ảnh minh hoạ kết quả
├── postman/                     # Collection và environment của Postman
│   ├── collections/Shop-Testing/
│   └── environments/
├── selenium/
│   ├── conftest.py              # Khởi tạo trình duyệt, tự chụp ảnh sau mỗi test
│   ├── test_shop.py             # 8 test case
│   └── report.html              # Báo cáo pytest
└── jmeter/
    └── JMeter-Shop.jmx          # Test Plan
```

## 4. Kiểm thử API/HTTP bằng Postman

### 4.1. Thiết lập

- Environment `Local`: `baseUrl = http://127.0.0.1:8000`, cùng các biến `testEmail`, `testPassword`, `productSlug`, `variantId`, `csrf_token` (token CSRF do script tự lấy).
- Collection `Shop-Testing` gồm 4 folder: `1-Public`, `2-Bao-mat`, `3-Dang-nhap`, `4-Gio-hang`.
- Do là ứng dụng Laravel nên các request POST cần CSRF token. Request GET trang đăng nhập lấy token bằng script rồi lưu vào biến `csrf_token`.

![Environment](images/postman-00-environment.png)
![Collection](images/postman-00-collection.png)

### 4.2. Danh sách request và kết quả

| Mã | Request | Kết quả mong đợi | Kết quả |
|---|---|---|---|
| PM01 | GET `/` (trang chủ) | 200, có thương hiệu QUDENA | PASS |
| PM02 | GET `/products` | 200, trả về HTML | PASS |
| PM03 | GET `/products/{slug}` | 200 | PASS |
| PM04 | GET đường dẫn không tồn tại | 404 | PASS |
| PM05 | GET `/admin/dashboard` khi chưa đăng nhập | 302 về `/login` | PASS |
| PM06 | POST `/login` thiếu CSRF token | 419 | PASS |
| PM07 | GET `/login` (lấy CSRF token) | 200, có token | PASS |
| PM08 | POST `/login` sai mật khẩu | 302 về `/login` | PASS |
| PM09 | POST `/login` đúng | 302, không về `/login` | PASS |
| PM10 | GET `/profile` khi đã đăng nhập | 200, hiện email tài khoản | PASS |
| PM11 | GET `/cart` | 200, giỏ có sản phẩm | PASS |
| PM12 | GET `/orders` | 200 | PASS |
| PM13 | GET `/wishlist` | 200 | PASS |
| PM14 | POST `/cart` thêm sản phẩm | 302, không về `/login` | PASS |
| PM15 | POST `/cart` số lượng 999 (vượt tồn kho 11) | Phản hồi có kiểm soát, không lỗi 500 | [PASS/ghi chú] |
| PM16 | GET `/products?q=len` (tìm kiếm) | 200, có sản phẩm khớp | PASS |
| PM17 | POST `/logout` | 302 | PASS |
| PM18 | GET `/admin/dashboard` bằng tài khoản thường | 403 | PASS |

### 4.3. Ảnh minh hoạ từng request

(Thay tên ảnh cho khớp thư mục `images/` của bạn.)

![PM01](images/postman-pm01-home.png)
![PM02](images/postman-pm02-products.png)
![PM03](images/postman-pm03-detail.png)
![PM04](images/postman-pm04-404.png)
![PM05](images/postman-pm05-admin-guard.png)
![PM06](images/postman-pm06-csrf.png)
![PM07](images/postman-pm07-login-page.png)
![PM08](images/postman-pm08-login-fail.png)
![PM09](images/postman-pm09-login-ok.png)
![PM10](images/postman-pm10-profile.png)
![PM11](images/postman-pm11-cart.png)
![PM12](images/postman-pm12-orders.png)
![PM13](images/postman-pm13-wishlist.png)
![PM14](images/postman-pm14-add-cart.png)
![PM15](images/postman-pm15-over-stock.png)
![PM16](images/postman-pm16-search.png)
![PM17](images/postman-pm17-logout.png)
![PM18](images/postman-pm18-user-admin.png)

### 4.4. Collection Runner

Chạy toàn bộ collection theo thứ tự folder: [x] test, [x] passed, [x] failed.

![Runner tóm tắt](images/postman-runner-summary.png)
![Runner chi tiết](images/postman-runner-detail.png)

### 4.5. Nhận xét

- **Bảo mật:** khách chưa đăng nhập vào trang quản trị bị chuyển về `/login` (302); người dùng thường đã đăng nhập bị chặn bằng 403; form đăng nhập từ chối request thiếu CSRF token (419).
- **Chức năng:** đăng nhập đúng/sai, thêm sản phẩm vào giỏ, xem giỏ hàng, đăng xuất hoạt động đúng.
- **Kiểm tra tồn kho (PM15):** thêm 999 sản phẩm trong khi kho còn 11. Kết quả trên giỏ hàng: [ghi số lượng thực tế và thông báo của website].
- **Thời gian phản hồi:** thường 0,6 đến 1,8 giây mỗi trang; có lúc chậm bất thường (khoảng 22 đến 27 giây) khi chạy bằng `php artisan serve`.

### 4.6. Cách chạy lại

Mở thư mục `postman/` bằng Postman ở chế độ Local, chọn environment `Local`, điền `testEmail`, `testPassword` của tài khoản test, bật website rồi chạy collection bằng Runner. Trước khi chạy Runner cần xoá cookie của `127.0.0.1` để các request bắt đầu ở trạng thái chưa đăng nhập.

## 5. Kiểm thử giao diện tự động bằng Selenium

### 5.1. Danh sách test case

| Mã | Tên test case | Các bước chính | Kết quả mong đợi | Kết quả |
|---|---|---|---|---|
| TC01 | Đăng nhập thành công | Nhập email, mật khẩu đúng, bấm Đăng nhập | Rời khỏi trang `/login` | PASS |
| TC02 | Đăng nhập sai mật khẩu | Nhập mật khẩu sai | Ở lại trang đăng nhập | PASS |
| TC03 | Bỏ trống email | Chỉ nhập mật khẩu, bấm Đăng nhập | Trình duyệt báo thiếu email, không gửi form | PASS |
| TC04 | Tìm kiếm sản phẩm | Mở ô tìm kiếm, nhập "len", Enter | Trang `/products?q=len` có "Váy len basic" | PASS |
| TC05 | Xem chi tiết sản phẩm | Mở `/products/vay-len-basic` | Đúng tên sản phẩm, giá 289.000 | PASS |
| TC06 | Thêm sản phẩm vào giỏ | Đăng nhập, bấm "Thêm vào giỏ" | Giỏ có sản phẩm, biểu tượng giỏ hiện số lượng | PASS |
| TC07 | Cập nhật số lượng trong giỏ | Đổi số lượng thành 3 | Số lượng trong giỏ là 3 | PASS |
| TC08 | Đăng xuất | Mở menu tài khoản, bấm Đăng xuất | Menu tài khoản biến mất, có liên kết đăng nhập | PASS |

### 5.2. Kết quả chạy

Lệnh chạy:

```bash
pytest selenium -v --html=selenium/report.html --self-contained-html
```

Kết quả: **8 passed** trong 104,56 giây.

![Kết quả pytest](images/selenium-result.png)
![Báo cáo HTML](images/selenium-report-html.png)
![Cấu trúc thư mục](images/selenium-structure.png)

### 5.3. Ảnh từng test case

Mỗi test tự chụp màn hình trình duyệt khi kết thúc.

![TC01](images/selenium-test_tc01_login_thanh_cong.png)
![TC02](images/selenium-test_tc02_login_sai_mat_khau.png)
![TC03](images/selenium-test_tc03_login_bo_trong_email.png)
![TC04](images/selenium-test_tc04_tim_kiem_san_pham.png)
![TC05](images/selenium-test_tc05_xem_chi_tiet_san_pham.png)
![TC06](images/selenium-test_tc06_them_san_pham_vao_gio.png)
![TC07](images/selenium-test_tc07_cap_nhat_so_luong_trong_gio.png)
![TC08](images/selenium-test_tc08_dang_xuat.png)

### 5.4. Cách chạy lại

Mật khẩu tài khoản test không ghi trong mã nguồn mà truyền qua biến môi trường. Bật website (`php artisan serve`), rồi trong thư mục repo:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install selenium pytest pytest-html
set SHOP_EMAIL=<email-tai-khoan-test>
set SHOP_PASSWORD=<mat-khau-tai-khoan-test>
pytest selenium -v
```

## 6. Kiểm thử hiệu năng bằng JMeter

### 6.1. Kịch bản

- Mỗi người dùng truy cập 4 trang công khai: trang chủ `/`, danh sách sản phẩm `/products`, chi tiết sản phẩm `/products/vay-len-basic`, tìm kiếm `/products?q=len`.
- Thread Group: ramp-up 10 giây, lặp 5 lần; chạy với 5, 10 và 20 người dùng.
- HTTP Request Defaults: `http`, `127.0.0.1`, cổng `8000`.
- Response Assertion: mã phản hồi bằng 200.
- Listener: View Results Tree, Summary Report, Aggregate Report.

![Thread Group](images/jmeter-01-thread-group.png)
![HTTP Request Defaults](images/jmeter-02-defaults.png)
![Test Plan](images/jmeter-03-test-plan.png)
![HTTP Request](images/jmeter-04-request.png)
![Response Assertion](images/jmeter-05-assertion.png)

### 6.2. Kết quả

![View Results Tree](images/jmeter-06-results-tree.png)
![Summary Report](images/jmeter-07-summary.png)

**5 người dùng**

![Aggregate 5](images/jmeter-09-aggregate-5users.png)

**10 người dùng**

![Aggregate 10](images/jmeter-10-aggregate-10users.png)

**20 người dùng**

![Aggregate 20](images/jmeter-08-aggregate-20users.png)

| Người dùng | Samples | Average (ms) | Median (ms) | 90% Line (ms) | 95% Line (ms) | 99% Line (ms) | Max (ms) | Error % | Throughput |
|---|---|---|---|---|---|---|---|---|---|
| 5 | 100 | 4.106 | 4.384 | 4.965 | 5.308 | 5.424 | 5.462 | 0.00% | 1,1/giây |
| 10 | 200 | 7.875 | 8.311 | 8.789 | 9.097 | 9.568 | 9.751 | 0.00% | 1,2/giây |
| 20 | 400 | 17.790 | 18.136 | 19.249 | 19.476 | 20.964 | 21.167 | 0.00% | 1,1/giây |

### 6.3. Phân tích

- **Tính đúng đắn:** 700/700 request thành công, Error % bằng 0.00% ở cả ba mức tải, các Response Assertion đều đạt.
- **Hiệu năng:** thời gian phản hồi trung bình tăng gần tuyến tính theo số người dùng (4,1 → 7,9 → 17,8 giây), trong khi thông lượng gần như không đổi (khoảng 1,1 đến 1,2 request/giây).
- **Nhận định:** bốn trang có thời gian gần như nhau, nên nút thắt nằm ở khả năng xử lý đồng thời của máy chủ chứ không ở một trang cụ thể. Máy chủ phát triển `php artisan serve` xử lý các request gần như tuần tự nên request phải xếp hàng chờ. Đây là suy luận từ số liệu đo được.
- **Kết luận:** website hoạt động đúng nhưng chưa phù hợp để phục vụ nhiều người dùng đồng thời trong môi trường kiểm thử này. Khi triển khai thật nên dùng máy chủ đa tiến trình (Apache hoặc Nginx với PHP-FPM) và đo lại. Kết quả chỉ phản ánh môi trường local.

### 6.4. Cách chạy lại

Mở `jmeter/JMeter-Shop.jmx` bằng JMeter, bật website, đổi **Number of Threads** trong Thread Group (5, 10 hoặc 20), bấm **Clear All** rồi **Start**.

## 7. Tổng hợp

| Công cụ | Phạm vi | Số kịch bản | Kết quả |
|---|---|---|---|
| Postman | Request HTTP, bảo mật, đăng nhập, giỏ hàng | 18 request | [x/x] test passed |
| Selenium | Giao diện: đăng nhập, tìm kiếm, giỏ hàng, đăng xuất | 8 test case | 8/8 passed |
| JMeter | Hiệu năng: 5, 10, 20 người dùng | 3 lần chạy, 700 request | 0% lỗi, thời gian phản hồi tăng theo tải |

## 8. Khó khăn và cách khắc phục

- **Postman bị lỗi do cài đặt tự theo chuyển hướng:** các request cần kiểm tra mã 302 trả về 200. Đã tắt "Automatically follow redirects" cho các request đó.
- **Cookie cũ làm sai kết quả Runner:** tài khoản đã đăng nhập sẵn nên request kiểm tra khách chưa đăng nhập bị lệch kết quả. Đã xoá cookie `127.0.0.1` trước khi chạy.
- **CSRF token:** các request POST bị 419 nếu thiếu token. Đã dùng script lấy token từ trang đăng nhập và trang cá nhân rồi lưu vào biến môi trường.
- **Selenium báo `StaleElementReferenceException`:** test không chờ trang tải lại sau khi gửi form. Đã sửa bằng explicit wait (`WebDriverWait`).
- **JMeter lỗi 100% do SSLHandshakeException:** JMeter gọi web bằng `https` trong khi máy chủ chỉ chạy `http`. Đã sửa Protocol trong HTTP Request Defaults thành `http`.
- **Thời gian phản hồi cao khi tăng tải:** do máy chủ `php artisan serve` xử lý tuần tự, đã chạy ba mức tải để chứng minh.

## 9. Kết luận

- Đã kiểm thử website QUDENA bằng cả ba công cụ ở các khía cạnh: chức năng, bảo mật cơ bản và hiệu năng.
- Chức năng và cơ chế bảo mật cơ bản (phân quyền, CSRF) hoạt động đúng ở các kịch bản đã kiểm thử.
- Hiệu năng là điểm hạn chế trong môi trường local: máy chủ phát triển không phục vụ tốt nhiều người dùng đồng thời.
- Hướng phát triển: bổ sung kiểm thử đặt hàng và thanh toán, kiểm thử mã giảm giá, kiểm thử hiệu năng trên máy chủ đa tiến trình.

## 10. Tài liệu tham khảo

- Postman Learning Center: https://learning.postman.com
- Selenium: https://www.selenium.dev/documentation/
- Apache JMeter: https://jmeter.apache.org
- Laravel: https://laravel.com/docs
