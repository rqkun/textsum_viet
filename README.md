# **Website tóm tắt văn bản báo chí và luật pháp**
## 1. Project Description
Vì nhu cầu cập nhật tin tức một các cụ thể và nhanh chóng mà không tốn nhiều thời gian trong thời buổi hiện nay, chúng tôi quyết định xây dựng một ứng dụng hỗ trợ cho việc tóm tắt văn bản tiếng Việt trên 2 phương diện đó là báo chí và luật pháp.

Website có một số chức năng hữu ích như sau:
1. Tóm tắt tin tức báo chí mới nhất.
2. Tóm báo chí thông qua văn bản nhập vào.
3. Tóm tắt điều luật thông qua văn bản nhập vào và đường dẫn được nhập vào.

Chúng tôi đã sử dụng [Streamlit](https://streamlit.io/) framework để xây dựng lên website này, cùng với thư viện [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/) và [NEWSDATA.IO](https://newsdata.io/) API cho chức năng tóm tắt tin tức báo chí mới nhất. Đồng thời chứng tôi đã tinh chỉnh mô hình BART trên tập dữ liệu báo chí và luật pháp trên ngôn ngữ tiếng Việt để tạo nên mô hình được sử dụng trong website này.
## 2. Khởi chạy ứng dụng
Để có thể khởi chạy ứng dụng có 2 cách:
1. Cách đầu tiên là mở cửa sổ command prompt ngay trong thư mục và chạy lệnh
```
streamlit run Main.py
```

2. Ngoài cách đầu tiên, người dùng có thể chạy tệp tin ```run.bat``` trong cùng thư mục để khởi chạy chương trình.
## 3. Sử dụng ứng dụng website
Để truy cập vào các chức năng của ứng dụng, chỉ cần nhấn vào các tab chức năng phía bên trái màn hình để điều hướng đến trang có chức năng tương ứng. Ở lần đầu truy cập sẽ tốn một khoảng thời gian để có thể tải model lên. Sau khi đã tải model xong thì trang web sẽ hiển thị giao diện để cho người dùng có thể sử dụng.

Ở trang đầu tiên là **Laws**, người dùng có thể sử dụng để tóm tắt điều luật mong muốn. Với đầu vào có thể tùy chỉnh là URL hoặc Text. Sau khi nhập đầu vào, nhấn tổ hợp phím ```Ctrl + Enter``` để ứng dụng xử lý và phân tách đầu vào ra thành các điều luật cho người dùng chọn lựa. Sau khi chọn được điều luật để tóm tắt chỉ cần nhấn ```Summary``` để thực hiện tóm tắt. Kết quả sẽ được hiển thị dưới dạng pop up.

Một trang chức năng khác đó là tóm tắt tin tức mới nhất, **Newsletter**. Chúc năng này sẽ hiển thị các tin tức mới nhất từ 4 nguồn báo là **báo Dân Việt, báo Tuổi Trẻ, báo Lao Động và báo VnExpress**. Các tin tức mới sẽ được hiển thị theo dừng dòng với hình ảnh minh họa, nội dung tóm tắt cũng như một nút điều hướng đến trang báo gốc.

Ngoài ra người dùng có thể lựa chọn việc tóm tắt tin tức báo chí bằng văn bản nhập vào ở trang chức năng **News**. Tại đây người dùng chỉ cần nhập nội dung vào và nhấn ```Summary``` thì website sẽ tóm tắt và trả về kết quả tương tự như ở chức năng luật.

> [!TIP]
> Có một số tùy chọn đáng chú ý khi tóm tắt văn bản là ```Length Penalty``` và ```Number of Beams```. ```Length Penalty``` càng lớn thì văn bản tóm tắt sẽ càng có xu hướng dài hơn so với ```Length Penalty``` thấp; và giá trị ```Number of Beams``` càng lớn thì tóm tắt được tạo sẽ càng có khả năng dùng từ phong phú hơn.
## 4. Data
Bộ dữ liệu về báo chí được lấy từ 3 nguồn sau:
1. [ViMs Dataset](https://github.com/CLC-HCMUS/ViMs-Dataset)
2. [vietnews](https://huggingface.co/datasets/harouzie/vietnews)
3. [VnExpress](https://vnexpress.net/)

Bộ dữ liệu luật pháp Việt Nam được lấy từ:
1. [Cơ sở dữ liệu Quốc gia về văn bản pháp luật](https://vbpl.vn/pages/portal.aspx)
## 5. Người thực hiện
1. Ngô Hoàng Khánh Duy
2. Huỳnh Nhật Minh
### Người hướng dẫn
ThS. Trần Trọng Bình
