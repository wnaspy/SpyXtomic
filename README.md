# SpyXtomic 
- Project này cho Redteam thực hiện kiểm thử EDR/AV cho hệ thống
# Cách dùng
- thêm file Dll.dll vào thư mục C:/Windows/Temp
- Mỗi tatics sẽ có các testcase tương ứng đã được build ra .exe
- Nếu file chạy thành công thì sẽ ghi logs vào C:/Windows/Temp/SpyGenLog.txt với format 
[Tatic] - [testcase] - [Fail/Susscess]
- ví dụ: 1003.001 - testcase 1 - Fail
# Chú ý
- Các tatic lưu ở định dạng file khác exe đều có thể tấn công được và không bị detect, mình chưa chuyển thành dạng exe nên có thể sẽ phải đợi chuyển sau
