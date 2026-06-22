# Failure Analysis — Lab 18: Production RAG

**Tên:** Nguyễn Thành Lộc
**MSSV:** 2A202600817

---

## RAGAS Scores

| Metric | Naive Baseline | Production | Δ |
|--------|---------------|------------|---|
| Faithfulness | 0.8250 | 0.7750 | -0.0500 |
| Answer Relevancy | 0.7177 | 0.8207 | +0.1031 |
| Context Precision | 0.9250 | 0.9417 | +0.0167 |
| Context Recall | 0.9250 | 0.8167 | -0.1083 |

## Bottom-5 Failures

### #1
- **Question:** Nhân viên thử việc có được hưởng bảo hiểm sức khỏe PVI không?
- **Expected:** KHÔNG. Nhân viên thử việc chưa được hưởng gói bảo hiểm sức khỏe PVI. Chỉ được tham gia bảo hiểm xã hội bắt buộc.
- **Got:** (LLM Hallucinated)
- **Worst metric:** Faithfulness (0.0)
- **Error Tree:** Output sai → Context đúng? (Có thể) → Query OK? → LLM bị hallucinate thông tin không có trong Context.
- **Root cause:** LLM hallucinating
- **Suggested fix:** Tighten prompt, lower temperature, yêu cầu LLM trích dẫn nguyên văn context.

### #2
- **Question:** Muốn mua thiết bị trị giá 55 triệu cần ai phê duyệt?
- **Expected:** Đơn hàng trên 50.000.000 VNĐ cần Tổng Giám đốc (CEO) phê duyệt.
- **Got:** (Sai vai trò người phê duyệt do miss context)
- **Worst metric:** Context Recall (0.0)
- **Error Tree:** Output sai → Context sai (thiếu chunk quy định >50tr) → Query OK?
- **Root cause:** Missing relevant chunks (hệ thống không nhận diện được 55 triệu thuộc nhóm >50 triệu).
- **Suggested fix:** Improve chunking or add BM25.

### #3
- **Question:** Lương thử việc của nhân viên Junior mức cao nhất là bao nhiêu?
- **Expected:** Junior cao nhất là 20.000.000 VNĐ/tháng. Lương thử việc = 85% x 20.000.000 = 17.000.000 VNĐ/tháng.
- **Got:** (LLM tính sai toán học hoặc bịa ra con số khác)
- **Worst metric:** Faithfulness (0.0)
- **Error Tree:** Output sai → Context đúng? → LLM Hallucinated math/numbers
- **Root cause:** LLM hallucinating (LLM tính toán yếu).
- **Suggested fix:** Tighten prompt, yêu cầu LLM dùng Chain-of-Thought để diễn giải từng bước tính toán.

### #4
- **Question:** Nhân viên tạm ứng 15 triệu, sau 20 ngày mới thanh toán. Bị phạt bao nhiêu?
- **Expected:** Thời hạn thanh toán là 15 ngày. Quá hạn 5 ngày, bị tính phí 2%/tháng trên 15.000.000 VNĐ = 300.000 VNĐ/tháng (tính pro-rata khoảng 50.000 VNĐ cho 5 ngày).
- **Got:** (LLM tính sai số tiền phạt hoặc sai thời hạn thanh toán)
- **Worst metric:** Faithfulness (0.1667)
- **Error Tree:** Output sai → Context đúng? → LLM Hallucinated calculation
- **Root cause:** LLM hallucinating.
- **Suggested fix:** Tighten prompt, yêu cầu giải thích từng tham số trong công thức tính.

### #5
- **Question:** Nếu cần mua một chiếc laptop 30 triệu cho nhân viên mới, ai phê duyệt và cần gì từ phòng CNTT?
- **Expected:** Laptop 30 triệu nằm trong khoảng 5-50 triệu nên cần Giám đốc phòng ban (Director) phê duyệt. Ngoài ra, mua sắm thiết bị CNTT cần có xác nhận cấu hình kỹ thuật từ phòng CNTT trước khi đề xuất. Cần đính kèm ít nhất 3 báo giá vì trên 10 triệu.
- **Got:** (Thiếu sót một số chi tiết, hoặc nhầm vai trò phê duyệt)
- **Worst metric:** Faithfulness (0.5)
- **Error Tree:** Output thiếu → Context đúng? → LLM Missed details.
- **Root cause:** LLM hallucinating (Bỏ sót thông tin từ context).
- **Suggested fix:** Tighten prompt.

## Case Study (cho presentation)

**Question chọn phân tích:** Muốn mua thiết bị trị giá 55 triệu cần ai phê duyệt?

**Error Tree walkthrough:**
1. Output đúng? → KHÔNG. Mô hình có thể đưa ra sai người phê duyệt (ví dụ: Director thay vì CEO).
2. Context đúng? → KHÔNG. Context Recall đạt 0.0, nghĩa là các chunk chứa thông tin "trên 50.000.000 VNĐ cần Tổng Giám đốc phê duyệt" không được retrieve thành công trong top-k.
3. Query rewrite OK? → Cần kiểm tra xem từ khóa "55 triệu" có match được với "50.000.000 VNĐ" trong vector space hay không. Nếu chỉ dùng Dense Search, mô hình embedding có thể không map "55 triệu" vào ngưỡng ">50 triệu".
4. Fix ở bước: Retrieval (Cần Entity Extraction để filter mức tiền, hoặc BM25).

**Nếu có thêm 1 giờ, sẽ optimize:**
- Thêm Metadata filter để trích xuất các điều kiện lớn hơn/nhỏ hơn số tiền (ví dụ: amount > 50M).
- Tinh chỉnh Prompt để giảm thiểu hallucination (Faithfulness đang giảm).
