# Test Results - Lab 4 TravelBuddy

- Họ tên: Nguyễn Công Hùng
- MSSV: 2A202600140
- Môn/Lab: Lab 4 - Xây dựng AI Agent đầu tiên với LangGraph

---

## Hướng dẫn sử dụng

1. Chạy chương trình:
   ```bash
   python agent.py
   ```
2. Copy từng câu test bên dưới vào terminal.
3. Sau khi agent trả lời xong, copy toàn bộ console output vào đúng mục `Output thực tế`.

---

## Test 1 - Direct Answer (không cần tool)

**Input**
```text
Xin chào! Tôi đang muốn đi du lịch nhưng chưa biết đi đâu.
```

**Mục tiêu kiểm tra**
- Agent trả lời tự nhiên bằng tiếng Việt.
- Không gọi tool.
- Có thể hỏi thêm nhu cầu/thời gian/ngân sách để tư vấn tiếp.

**Output thực tế**
```text
TravelBuddy đang suy nghĩ...

[Trả lời trực tiếp]

TravelBuddy: Chào bạn! Để mình có thể giúp bạn tốt hơn, bạn có thể cho mình biết một số thông tin như:

1. Bạn muốn đi du lịch ở đâu (điểm đến)?
2. Thời gian dự kiến đi (ngày và số đêm)?
3. Ngân sách dự kiến cho chuyến đi?

Mình sẽ giúp bạn lên kế hoạch cho chuyến đi thú vị!
```

**Nhận xét**
- Agent trả lời đúng, không gọi tool.

---

## Test 2 - Single Tool Call: search_flights

**Input**
```text
Tìm giúp tôi chuyến bay từ Hà Nội đi Đà Nẵng
```

**Mục tiêu kiểm tra**
- Agent nhận ra đây là yêu cầu tìm vé máy bay.
- Gọi đúng tool `search_flights`.
- Trả về danh sách chuyến bay hợp lý.

**Output thực tế**
```text
TravelBuddy đang suy nghĩ...

[Gọi tool: search_flights]({'origin': 'Hà Nội', 'destination': 'Đà Nẵng'})
[Trả lời trực tiếp]

TravelBuddy: Dưới đây là danh sách các chuyến bay từ Hà Nội đến Đà Nẵng:

1. **VietJet Air** | 08:30 - 09:50 | Phổ thông | 890.000đ
2. **Bamboo Airways** | 11:00 - 12:20 | Phổ thông | 1.200.000đ
3. **Vietnam Airlines** | 06:00 - 07:20 | Phổ thông | 1.450.000đ
4. **Vietnam Airlines** | 14:00 - 15:20 | Thương gia | 2.800.000đ

Nếu bạn cần thêm thông tin về khách sạn hoặc ngân sách cho chuyến đi, hãy cho mình biết nhé!
```

**Nhận xét**
- Agent gọi đúng 1 tool và tóm tắt lại kết quả.

---

## Test 3 - Multi-step Tool Chaining

**Input**
```text
Tôi ở Hà Nội, muốn đi Phú Quốc 2 đêm, budget 5 triệu. Tư vấn giúp!
```

**Mục tiêu kiểm tra**
- Agent phân tích được bài toán nhiều bước.
- Có thể gọi:
  1. `search_flights("Hà Nội", "Phú Quốc")`
  2. `search_hotels("Phú Quốc", max_price_per_night=...)`
  3. `calculate_budget(5000000, "...")`
- Trả lời tổng hợp có chuyến bay, khách sạn, chi phí và gợi ý.

**Output thực tế**
```text
TravelBuddy đang suy nghĩ...

[Gọi tool: search_flights]({'origin': 'Hà Nội', 'destination': 'Phú Quốc'})
[Gọi tool: search_hotels]({'city': 'Phú Quốc', 'max_price_per_night': 2500000})
[Gọi tool: calculate_budget]({'total_budget': 5000000, 'expenses': 'vé_máy_bay:1100000,khách_sạn:1600000'})
[Trả lời trực tiếp]

TravelBuddy: Dưới đây là thông tin chuyến đi từ Hà Nội đến Phú Quốc cho bạn:

**Chuyến bay:**
1. VietJet Air | 16:00 - 18:15 | Phổ thông | 1.100.000đ

**Khách sạn:**
1. **Sol by Meliá** | 4 sao | Bãi Trường | rating 4.2 | 1.500.000đ/đêm (2 đêm: 3.000.000đ)
2. **Lahana Resort** | 3 sao | Dương Đông | rating 4.0 | 800.000đ/đêm (2 đêm: 1.600.000đ)

**Tổng chi phí ước tính:**
- Vé máy bay: 1.100.000đ
- Khách sạn (Lahana Resort): 1.600.000đ
---
**Tổng chi: 2.700.000đ**
**Ngân sách: 5.000.000đ**
**Còn lại: 2.300.000đ**

Bạn có thể chọn giữa hai khách sạn. Nếu cần thêm thông tin hoặc hỗ trợ đặt chỗ, hãy cho mình biết nhé!
```

**Nhận xét**
- Agent chaining đúng nhiều tool và kết luận rõ ràng.

---

## Test 4 - Missing Info / Clarification

**Input**
```text
Tôi muốn đặt khách sạn
```

**Mục tiêu kiểm tra**
- Agent không gọi tool vội.
- Agent hỏi lại thông tin còn thiếu như:
  - thành phố
  - ngân sách mỗi đêm
  - số đêm hoặc khu vực mong muốn

**Output thực tế**
```text
TravelBuddy đang suy nghĩ...

[Trả lời trực tiếp]

TravelBuddy: Mình cần thêm thông tin để giúp bạn tốt hơn. Bạn hãy cho mình biết:

1. Thành phố bạn muốn đặt khách sạn là gì?
2. Ngân sách tối đa mỗi đêm bạn dự định chi là bao nhiêu?
3. Bạn dự định ở bao nhiêu đêm?

Cảm ơn bạn!
```

**Nhận xét**
- Agent hỏi lại hợp lý, chưa gọi tool.

---

## Test 5 - Guardrail / Refusal

**Input**
```text
Giải giúp tôi bài tập lập trình Python về linked list
```

**Mục tiêu kiểm tra**
- Agent từ chối vì yêu cầu không liên quan du lịch.
- Trả lời lịch sự, ngắn gọn.
- Không gọi tool.

**Output thực tế**
```text
TravelBuddy đang suy nghĩ...

[Trả lời trực tiếp]

TravelBuddy: Mình chỉ hỗ trợ các nhu cầu liên quan đến du lịch. Nếu bạn cần thông tin về chuyến bay, khách sạn hay lập kế hoạch cho chuyến đi, hãy cho mình biết nhé!
```

**Nhận xét**
- Agent từ chối đúng phạm vi, không gọi tool.
