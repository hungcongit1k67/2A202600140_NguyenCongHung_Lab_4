from langchain_core.tools import tool


FLIGHTS_DB = {
    ("Hà Nội", "Đà Nẵng"): [
        {"airline": "Vietnam Airlines", "departure": "06:00", "arrival": "07:20", "price": 1_450_000, "class": "economy"},
        {"airline": "Vietnam Airlines", "departure": "14:00", "arrival": "15:20", "price": 2_800_000, "class": "business"},
        {"airline": "VietJet Air", "departure": "08:30", "arrival": "09:50", "price": 890_000, "class": "economy"},
        {"airline": "Bamboo Airways", "departure": "11:00", "arrival": "12:20", "price": 1_200_000, "class": "economy"},
    ],
    ("Hà Nội", "Phú Quốc"): [
        {"airline": "Vietnam Airlines", "departure": "07:00", "arrival": "09:15", "price": 2_100_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "10:00", "arrival": "12:15", "price": 1_350_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "16:00", "arrival": "18:15", "price": 1_100_000, "class": "economy"},
    ],
    ("Hà Nội", "Hồ Chí Minh"): [
        {"airline": "Vietnam Airlines", "departure": "06:00", "arrival": "08:10", "price": 1_600_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "07:30", "arrival": "09:40", "price": 950_000, "class": "economy"},
        {"airline": "Bamboo Airways", "departure": "12:00", "arrival": "14:10", "price": 1_300_000, "class": "economy"},
        {"airline": "Vietnam Airlines", "departure": "18:00", "arrival": "20:10", "price": 3_200_000, "class": "business"},
    ],
    ("Hồ Chí Minh", "Đà Nẵng"): [
        {"airline": "Vietnam Airlines", "departure": "09:00", "arrival": "10:20", "price": 1_300_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "13:00", "arrival": "14:20", "price": 780_000, "class": "economy"},
    ],
    ("Hồ Chí Minh", "Phú Quốc"): [
        {"airline": "Vietnam Airlines", "departure": "08:00", "arrival": "09:00", "price": 1_100_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "15:00", "arrival": "16:00", "price": 650_000, "class": "economy"},
    ],
}

HOTELS_DB = {
    "Đà Nẵng": [
        {"name": "Mường Thanh Luxury", "stars": 5, "price_per_night": 1_800_000, "area": "Mỹ Khê", "rating": 4.5},
        {"name": "Sala Danang Beach", "stars": 4, "price_per_night": 1_200_000, "area": "Mỹ Khê", "rating": 4.3},
        {"name": "Fivitel Danang", "stars": 3, "price_per_night": 650_000, "area": "Sơn Trà", "rating": 4.1},
        {"name": "Memory Hostel", "stars": 2, "price_per_night": 250_000, "area": "Hải Châu", "rating": 4.6},
        {"name": "Christina's Homestay", "stars": 2, "price_per_night": 350_000, "area": "An Thượng", "rating": 4.7},
    ],
    "Phú Quốc": [
        {"name": "Vinpearl Resort", "stars": 5, "price_per_night": 3_500_000, "area": "Bãi Dài", "rating": 4.4},
        {"name": "Sol by Meliá", "stars": 4, "price_per_night": 1_500_000, "area": "Bãi Trường", "rating": 4.2},
        {"name": "Lahana Resort", "stars": 3, "price_per_night": 800_000, "area": "Dương Đông", "rating": 4.0},
        {"name": "9Station Hostel", "stars": 2, "price_per_night": 200_000, "area": "Dương Đông", "rating": 4.5},
    ],
    "Hồ Chí Minh": [
        {"name": "Rex Hotel", "stars": 5, "price_per_night": 2_800_000, "area": "Quận 1", "rating": 4.3},
        {"name": "Liberty Central", "stars": 4, "price_per_night": 1_400_000, "area": "Quận 1", "rating": 4.1},
        {"name": "Cochin Zen Hotel", "stars": 3, "price_per_night": 550_000, "area": "Quận 3", "rating": 4.4},
        {"name": "The Common Room", "stars": 2, "price_per_night": 180_000, "area": "Quận 1", "rating": 4.6},
    ],
}


def format_vnd(amount: int) -> str:
    return f"{amount:,}".replace(",", ".")


def normalize_text(text: str) -> str:
    return " ".join(text.strip().split())


@tool
def search_flights(origin: str, destination: str) -> str:
    """
    Tìm kiếm các chuyến bay giữa hai thành phố.

    Tham số:
    - origin: thành phố khởi hành (VD: 'Hà Nội', 'Hồ Chí Minh')
    - destination: thành phố đến (VD: 'Đà Nẵng', 'Phú Quốc')

    Trả về danh sách chuyến bay với hãng, giờ bay, giá vé.
    Nếu không tìm thấy tuyến bay, trả về thông báo không có chuyến.
    """
    origin = normalize_text(origin)
    destination = normalize_text(destination)

    direct_key = (origin, destination)
    reverse_key = (destination, origin)

    flights = FLIGHTS_DB.get(direct_key)
    used_reverse = False

    if flights is None:
        flights = FLIGHTS_DB.get(reverse_key)
        used_reverse = flights is not None

    if not flights:
        return f"Không tìm thấy chuyến bay từ {origin} đến {destination}."

    flights = sorted(flights, key=lambda x: (x["price"], x["departure"]))

    lines = []
    if used_reverse:
        lines.append(f"Không có dữ liệu chiều {origin} -> {destination}.")
        lines.append(f"Hiện chỉ tìm thấy dữ liệu chiều ngược lại {destination} -> {origin}:")
    else:
        lines.append(f"Các chuyến bay từ {origin} đến {destination}:")

    for idx, flight in enumerate(flights, start=1):
        ticket_class = "phổ thông" if flight["class"] == "economy" else "thương gia"
        lines.append(
            f"{idx}. {flight['airline']} | "
            f"{flight['departure']} - {flight['arrival']} | "
            f"{ticket_class} | {format_vnd(flight['price'])}đ"
        )

    return "\n".join(lines)


@tool
def search_hotels(city: str, max_price_per_night: int = 99999999) -> str:
    """
    Tìm kiếm khách sạn tại một thành phố, có thể lọc theo giá tối đa mỗi đêm.

    Tham số:
    - city: tên thành phố (VD: 'Đà Nẵng', 'Phú Quốc', 'Hồ Chí Minh')
    - max_price_per_night: giá tối đa mỗi đêm (VND), mặc định không giới hạn

    Trả về danh sách khách sạn phù hợp với tên, số sao, giá, khu vực, rating.
    """
    city = normalize_text(city)
    hotels = HOTELS_DB.get(city)

    if hotels is None:
        return f"Không tìm thấy dữ liệu khách sạn tại {city}."

    filtered_hotels = [
        hotel for hotel in hotels
        if hotel["price_per_night"] <= max_price_per_night
    ]

    filtered_hotels.sort(key=lambda x: (-x["rating"], x["price_per_night"]))

    if not filtered_hotels:
        return (
            f"Không tìm thấy khách sạn tại {city} với giá dưới "
            f"{format_vnd(max_price_per_night)}đ/đêm. Hãy thử tăng ngân sách."
        )

    lines = [f"Khách sạn phù hợp tại {city}:"]
    for idx, hotel in enumerate(filtered_hotels, start=1):
        lines.append(
            f"{idx}. {hotel['name']} | "
            f"{hotel['stars']} sao | "
            f"{hotel['area']} | "
            f"rating {hotel['rating']} | "
            f"{format_vnd(hotel['price_per_night'])}đ/đêm"
        )

    return "\n".join(lines)


@tool
def calculate_budget(total_budget: int, expenses: str) -> str:
    """
    Tính toán ngân sách còn lại sau khi trừ các khoản chi phí.

    Tham số:
    - total_budget: tổng ngân sách ban đầu (VND)
    - expenses: chuỗi mô tả các khoản chi, mỗi khoản cách nhau bởi dấu phẩy,
      định dạng 'tên_khoản:số_tiền' (VD: 'vé_máy_bay:890000,khách_sạn:650000')

    Trả về bảng chi tiết các khoản chi và số tiền còn lại.
    Nếu vượt ngân sách, cảnh báo rõ ràng số tiền thiếu.
    """
    try:
        if total_budget < 0:
            return "Lỗi: total_budget phải là số không âm."

        raw_expenses = expenses.strip()
        if not raw_expenses:
            return (
                "Bảng chi phí:\n"
                "- Chưa có khoản chi nào\n"
                "---\n"
                f"Tổng chi: 0đ\n"
                f"Ngân sách: {format_vnd(total_budget)}đ\n"
                f"Còn lại: {format_vnd(total_budget)}đ"
            )

        expense_dict = {}
        parts = [part.strip() for part in raw_expenses.split(",") if part.strip()]

        for part in parts:
            if ":" not in part:
                return (
                    f"Lỗi định dạng expenses tại mục '{part}'. "
                    "Hãy dùng dạng ten_khoan:so_tien,ten_khoan:so_tien"
                )

            name, amount_str = part.split(":", 1)
            name = name.strip()
            amount_str = amount_str.strip().replace(".", "").replace("_", "").replace(" ", "")

            if not name:
                return "Lỗi: tên khoản chi không được để trống."

            if not amount_str.isdigit():
                return (
                    f"Lỗi: số tiền của khoản '{name}' không hợp lệ. "
                    "Chỉ dùng chữ số, ví dụ: ve_may_bay:890000"
                )

            amount = int(amount_str)
            expense_dict[name] = expense_dict.get(name, 0) + amount

        total_expense = sum(expense_dict.values())
        remaining = total_budget - total_expense

        lines = ["Bảng chi phí:"]
        for name, amount in expense_dict.items():
            pretty_name = name.replace("_", " ").strip().capitalize()
            lines.append(f"- {pretty_name}: {format_vnd(amount)}đ")

        lines.append("---")
        lines.append(f"Tổng chi: {format_vnd(total_expense)}đ")
        lines.append(f"Ngân sách: {format_vnd(total_budget)}đ")

        if remaining >= 0:
            lines.append(f"Còn lại: {format_vnd(remaining)}đ")
        else:
            lines.append(f"Vượt ngân sách {format_vnd(abs(remaining))}đ. Cần điều chỉnh.")

        return "\n".join(lines)

    except Exception as e:
        return f"Lỗi khi tính ngân sách: {str(e)}"