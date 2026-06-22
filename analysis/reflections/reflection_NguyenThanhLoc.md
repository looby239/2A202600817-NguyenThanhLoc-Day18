# Personal Reflection — Lab 18

**Tên:** Nguyễn Thành Lộc
**MSSV:** 2A202600817

## 1. Những điều học được
Qua Lab 18 này, tôi đã hiểu rõ hơn về cách xây dựng một Production RAG Pipeline thực tế không chỉ đơn thuần là đẩy dữ liệu vào Vector DB và query. Các thành phần quan trọng bao gồm:
- **Hybrid Search**: Kết hợp Dense Retrieval (hiểu ngữ nghĩa qua embeddings) và Sparse Retrieval (BM25 - tìm từ khóa chính xác), giúp hệ thống hoạt động ổn định với cả các câu hỏi khái niệm lẫn các câu hỏi chứa keyword cụ thể.
- **Reranking**: Cải thiện đáng kể độ liên quan của các context bằng cách dùng mô hình Cross-Encoder (FlashRank) để đánh giá lại top-k chunks, giúp đẩy Answer Relevancy và Context Precision lên cao.
- **RAGAS Evaluation**: Sử dụng LLM-as-a-judge (RAGAS framework) để đánh giá định lượng được các metric quan trọng (Faithfulness, Answer Relevancy, Context Precision, Context Recall) một cách khách quan thay vì chỉ đánh giá cảm tính.

## 2. Khó khăn lớn nhất
Khó khăn lớn nhất là việc tuning và tối ưu để các metric đồng loạt tăng. Kết quả cho thấy khi áp dụng Production Pipeline, một số metric tăng (Answer Relevancy) nhưng một số lại giảm (Context Recall, Faithfulness). 
Đặc biệt là việc xử lý các document chứa nhiều policy chồng chéo hoặc yêu cầu tính toán logic (ví dụ: các mức tiền duyệt chi lớn hơn/nhỏ hơn một số tiền cố định, số ngày nghỉ được tính theo thâm niên). LLM rất dễ bị hallucinate khi phải làm toán học đơn giản dựa trên text context hoặc hệ thống retrieval bỏ qua các đoạn context quan trọng do không match được giá trị số tiền.

## 3. Nếu làm lại sẽ thay đổi gì?
Nếu có cơ hội làm lại hoặc mở rộng hệ thống, tôi sẽ:
1. Áp dụng kỹ thuật chunking thông minh hơn (Semantic Chunking) hoặc Rule-based chunking thay vì chia theo đoạn văn bản dựa trên RecursiveCharacterTextSplitter.
2. Cải thiện việc xử lý bảng biểu và số liệu bằng cách trích xuất Metadata và sử dụng Filter Parameters của Qdrant thay vì để mọi thứ ở dạng text embedding.
3. Thử nghiệm Prompt Engineering kỹ càng hơn (sử dụng Chain-of-Thought) để ép LLM phải diễn giải từng bước logic thay vì chỉ đưa ra câu trả lời cuối cùng, và nhắc nhở LLM từ chối trả lời nếu không chắc chắn (nhằm cải thiện chỉ số Faithfulness).
