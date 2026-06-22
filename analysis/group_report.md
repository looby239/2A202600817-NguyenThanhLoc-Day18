# Group Report — Lab 18: Production RAG

**Tên:** Nguyễn Thành Lộc
**MSSV:** 2A202600817

## Thành viên & Phân công

| Tên | Module | Hoàn thành | Tests pass |
|-----|--------|-----------|-----------|
| Nguyễn Thành Lộc | M1: Chunking | ☑ | 8/8 |
| Nguyễn Thành Lộc | M2: Hybrid Search | ☑ | 5/5 |
| Nguyễn Thành Lộc | M3: Reranking | ☑ | 5/5 |
| Nguyễn Thành Lộc | M4: Evaluation | ☑ | 4/4 |

## Kết quả RAGAS

| Metric | Naive | Production | Δ |
|--------|-------|-----------|---|
| Faithfulness | 0.8250 | 0.7750 | -0.0500 |
| Answer Relevancy | 0.7177 | 0.8207 | +0.1031 |
| Context Precision | 0.9250 | 0.9417 | +0.0167 |
| Context Recall | 0.9250 | 0.8167 | -0.1083 |

## Key Findings

1. **Biggest improvement:** Answer Relevancy tăng mạnh (+0.1031) và Context Precision tăng nhẹ (+0.0167). Việc áp dụng Hybrid Search (kết hợp Dense Search và BM25) cùng với Reranking (Cohere/FlashRank) giúp đẩy các chunk có chứa thông tin trả lời trực tiếp lên top đầu, giúp câu trả lời của LLM trúng đích hơn thay vì lan man.
2. **Biggest challenge:** Việc xử lý các query chứa điều kiện số (ví dụ: "55 triệu", "15 triệu", "20 ngày") hoặc các con số mang tính chất phân cấp ngưỡng (thresholds). Semantic search thông thường gặp khó khăn trong việc hiểu các điều kiện lớn hơn/nhỏ hơn, dẫn đến Context Recall bị giảm (giảm -0.1083) và LLM dễ bị hallucinate khi phải làm các bài toán tính lương/phạt (Faithfulness giảm -0.0500).
3. **Surprise finding:** Production RAG không phải lúc nào cũng tốt hơn Naive Baseline ở mọi mặt. Context Recall và Faithfulness đã bị giảm đi trong trường hợp này. Điều này cho thấy khi context được rerank quá chặt chẽ, một số context bao quát chứa thông tin quan trọng lại bị rớt khỏi top-k, làm LLM thiếu dữ kiện để đưa ra câu trả lời đầy đủ hoặc tự suy diễn sai.

## Presentation Notes (5 phút)

1. RAGAS scores (naive vs production): Nhấn mạnh sự đánh đổi giữa việc tăng Answer Relevancy & Context Precision so với việc làm giảm Context Recall & Faithfulness.
2. Biggest win — module nào, tại sao: Module Reranking và Hybrid Search là điểm sáng nhất vì nó đảm bảo context tốt nhất nằm ở vị trí cao nhất (tăng Context Precision).
3. Case study — 1 failure, Error Tree walkthrough: Phân tích câu hỏi "Muốn mua thiết bị trị giá 55 triệu cần ai phê duyệt?". Đây là một failure về Context Recall do hệ thống không map được số "55 triệu" với rule ">50 triệu" trong vector space.
4. Next optimization nếu có thêm 1 giờ: Tối ưu hoá System Prompt để LLM "tuyệt đối không bịa số liệu nếu không có trong context", và thêm pipeline phân loại entity (Entity Extraction) để trích xuất con số và áp dụng Metadata Filtering cho các ngưỡng số học.
