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

1. Bạn muốn đi đâu? (Ví dụ: Đà Nẵng, Phú Quốc, Hà Nội, Hồ Chí Minh...)
2. Thời gian dự kiến đi và về?
3. Ngân sách cho chuyến đi là bao nhiêu?
4. Bạn thích loại hình lưu trú nào? (khách sạn, homestay, resort...)

Mình sẽ giúp bạn lên kế hoạch cho chuyến đi!
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

TravelBuddy: Dưới đây là các chuyến bay từ Hà Nội đi Đà Nẵng:

1. **VietJet Air**: 08:30 - 09:50 | Phổ thông | 890.000đ
2. **Bamboo Airways**: 11:00 - 12:20 | Phổ thông | 1.200.000đ
3. **Vietnam Airlines**: 06:00 - 07:20 | Phổ thông | 1.450.000đ
4. **Vietnam Airlines**: 14:00 - 15:20 | Thương gia | 2.800.000đ

Nếu bạn cần thêm thông tin hoặc muốn đặt vé, hãy cho mình biết nhé!
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
[Trả lời trực tiếp]

TravelBuddy: Chuyến bay:
1. VietJet Air | 16:00 - 18:15 | phổ thông | 1.100.000đ
2. VietJet Air | 10:00 - 12:15 | phổ thông | 1.350.000đ
3. Vietnam Airlines | 07:00 - 09:15 | phổ thông | 2.100.000đ

Khách sạn:
1. 9Station Hostel | 2 sao | Dương Đông | rating 4.5 | 200.000đ/đêm
2. Sol by Meliá | 4 sao | Bãi Trường | rating 4.2 | 1.500.000đ/đêm
3. Lahana Resort | 3 sao | Dương Đông | rating 4.0 | 800.000đ/đêm

Chi phí dự tính:
- Vé máy bay (VietJet Air, 16:00 - 18:15): 1.100.000đ
- Khách sạn (9Station Hostel, 2 đêm): 400.000đ
- Tổng chi phí: 1.500.000đ

Ngân sách còn lại: 5.000.000đ - 1.500.000đ = 3.500.000đ

Gợi ý thêm:
- Bạn có thể chọn chuyến bay VietJet Air lúc 16:00 để tiết kiệm chi phí.
- Nếu muốn trải nghiệm tốt hơn, có thể chọn Lahana Resort với giá 800.000đ/đêm.
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

TravelBuddy: Bạn có thể cho mình biết thêm thông tin về khách sạn mà bạn muốn đặt không? Cụ thể là:

1. Thành phố bạn muốn đặt khách sạn?
2. Ngân sách tối đa mỗi đêm là bao nhiêu?
3. Số đêm bạn dự định lưu trú?

Mình sẽ giúp bạn tìm kiếm khách sạn phù hợp!
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

TravelBuddy: Mình chỉ hỗ trợ các nhu cầu liên quan đến du lịch. Nếu bạn có câu hỏi nào về chuyến đi, vé máy bay, khách sạn hay lịch trình, hãy cho mình biết nhé!  ```

**Nhận xét**
- Agent từ chối đúng phạm vi, không gọi tool.

---

## Test 6 - Hotel Search With Budget Filter

**Input**
```text
Tìm khách sạn ở Phú Quốc dưới 1 triệu một đêm
```

**Mục tiêu kiểm tra**
- Agent gọi `search_hotels`.
- Có lọc theo `max_price_per_night`.
- Trả về danh sách khách sạn phù hợp.

**Output thực tế**
```text
TravelBuddy đang suy nghĩ...

[Gọi tool: search_hotels]({'city': 'Phú Quốc', 'max_price_per_night': 1000000})
[Trả lời trực tiếp]

TravelBuddy: Dưới đây là một số khách sạn ở Phú Quốc dưới 1 triệu đồng một đêm:

1. **9Station Hostel**
   - **Sao:** 2 sao
   - **Khu vực:** Dương Đông
   - **Giá:** 200.000đ/đêm
   - **Rating:** 4.5

2. **Lahana Resort**
   - **Sao:** 3 sao
   - **Khu vực:** Dương Đông
   - **Giá:** 800.000đ/đêm
   - **Rating:** 4.0

Nếu bạn cần thêm thông tin hoặc hỗ trợ gì khác, hãy cho mình biết nhé!
```

**Nhận xét**
- Danh sách đúng, có mức giá phù hợp.

---

## Test 7 - Budget Calculation

**Input**
```text
Tính giúp tôi ngân sách 5 triệu, gồm vé máy bay 890000 và khách sạn 650000
```

**Mục tiêu kiểm tra**
- Agent gọi `calculate_budget`.
- Trả về bảng chi phí rõ ràng.
- Tính đúng tổng chi và số tiền còn lại.

**Output thực tế**
```text
TravelBuddy đang suy nghĩ...

[Gọi tool: calculate_budget]({'total_budget': 5000000, 'expenses': 'vé_máy_bay:890000,khách_sạn:650000'})
[Trả lời trực tiếp]

TravelBuddy: Ngân sách của bạn được tính như sau:

Bảng chi phí:
- Vé máy bay: 890.000đ
- Khách sạn: 650.000đ
---
Tổng chi: 1.540.000đ
Ngân sách: 5.000.000đ
Còn lại: 3.460.000đ

Bạn còn 3.460.000đ để chi tiêu cho các khoản khác trong chuyến đi. Nếu cần thêm thông tin gì, hãy cho mình biết nhé!
```

**Nhận xét**
- Tính đúng và format dễ đọc.

---

## Test 8 - Route Not Found / Reverse Data Check

**Input**
```text
Tìm chuyến bay từ Đà Nẵng đi Hà Nội
```

**Mục tiêu kiểm tra**
- Nếu không có dữ liệu đúng chiều, tool có thể báo không có dữ liệu chiều đó.
- Nếu code của bạn hỗ trợ tra chiều ngược, agent cần diễn giải rõ.
- Không được bịa dữ liệu.

**Output thực tế**
```text
TravelBuddy đang suy nghĩ...

[Gọi tool: search_flights]({'origin': 'Đà Nẵng', 'destination': 'Hà Nội'})
[Trả lời trực tiếp]

TravelBuddy: Hiện tại không có chuyến bay từ Đà Nẵng đi Hà Nội. Tuy nhiên, mình có thông tin về các chuyến bay từ Hà Nội đến Đà Nẵng như sau:

1. **VietJet Air**: 08:30 - 09:50 | Phổ thông | 890.000đ
2. **Bamboo Airways**: 11:00 - 12:20 | Phổ thông | 1.200.000đ
3. **Vietnam Airlines**: 06:00 - 07:20 | Phổ thông | 1.450.000đ
4. **Vietnam Airlines**: 14:00 - 15:20 | Thương gia | 2.800.000đ

Nếu bạn cần thêm thông tin hoặc có kế hoạch khác, hãy cho mình biết nhé!
```

**Nhận xét**
- Tool xử lý đúng trường hợp thiếu dữ liệu.
