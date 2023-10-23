# Hướng dẫn Cài Đặt và Chạy Hệ Thống ChatbotVN

Hệ thống ChatbotVN là sự kết hợp của nhiều công nghệ và ứng dụng khác nhau. Để có thể tự chạy và sử dụng hệ thống này, bạn cần thực hiện các bước sau:

## Yêu Cầu

- Cài đặt Java 1.8+.
- Cài đặt Python 3+.

## Cài Đặt XAMPP

1. Tải XAMPP từ [đây](https://sourceforge.net/projects/xampp/).

2. Sau khi tải xong, mở XAMPP và khởi động Apache và MySQL

3. Sau đó, nhấp vào "Admin" để truy cập trang web.

4. Tạo một cơ sở dữ liệu mới và đặt tên là "chatbotvn"

5. Import file "chatbotvn.sql" vào cơ sở dữ liệu vừa tạo.

## Cài Đặt Môi Trường Python

Mở cmd trong thư mục của dự án "chatbotvn" và chạy lệnh sau để cài đặt các thư viện cần thiết:

```python
pip install torch numpy py_vncorenlp nltk scikit-learn flask mysql-connector-python transform bardapi
```
## Chạy Hệ Thống
Chạy chương trình bằng cách chạy tệp "main.py" trong thư mục "front_end":
```python
python main.py
```
Truy cập hệ thống thông qua trình duyệt web tại địa chỉ http://127.0.0.1:5000.
## Các Lỗi Thường Gặp
Lỗi Unable to Find JAVA_HOME
Nếu bạn gặp lỗi như sau:
```python
File "c:\users\admin\appdata\local\programs\python\python311\lib\site-packages\jnius\env.py", line 335, in get_jdk_home
  raise Exception('Unable to find JAVA_HOME')
builtins.Exception: Unable to find JAVA_HOME
```
Để đặt biến môi trường JAVA_HOME, bạn cần biết vị trí cài đặt của JDK (Java Development Kit) trên máy tính của bạn. Hãy thực hiện các bước sau:

1. Tìm và mở "System" hoặc "System and Security" (tùy theo phiên bản Windows).
   
2. Chọn "Advanced system settings" hoặc "Advanced" (tùy theo phiên bản Windows).
   
3. Trong cửa sổ "System Properties," chọn tab "Advanced."
   
4. Sau khi truy cập vào Environment Variables
   
5. Tạo biến môi trường JAVA_HOME và gán giá trị đường dẫn đến thư mục cài đặt của JDK, ví dụ: "C:\Program Files\Java\jdk1.8.0_381."
   
6. Nhấp vào nút "OK" để lưu các thay đổi.
   
7. Nhấp vào nút "OK" và khởi động lại máy tính.
### Environment Variables <a name="models2"></a>
Variable  | Value 
---|---
JAVA_HOME   | C:\Program Files\java\jre-1.8 |

### Example usage <a name="usage2"></a>
Đối với lỗi 
```python
Lỗi "SNlM0e value not found. Double-check __Secure-1PSID value or pass it as token='xxxxx'"
```
Nếu bạn gặp lỗi này, thực hiện các bước sau:

1. Đăng nhập vào [Bard](https://bard.google.com/chat?hl=en) bằng tài khoản Gmail cá nhân.
   
2. Mở Developer Tools (F12), chọn tab "Application," xóa hết dữ liệu trong "Cookies," sau đó tải lại trang và đăng nhập lại.
   
3. Sao chép giá trị trong cookie "__Secure-1PSID."
   
4. Mở tệp "chatbotvn/natural_language_processing/bard.py" và thay thế giá trị "_BARD_API_KEY" bằng giá trị bạn vừa sao chép.
   
```python
import os 
os.environ["_BARD_API_KEY"] = "cQh9MiwI3L1hbB6gsOWWFbzKUNmoyR65if7wP_1_vyoJ_mkKzxOlVpgjIjG6BiB-PvGx2Q."
```
