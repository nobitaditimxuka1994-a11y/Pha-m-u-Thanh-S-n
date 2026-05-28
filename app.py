
import streamlit as st
import numpy as np
import PIL.Image as Image

# --- 1. CẤU HÌNH TRANG ---
st.set_page_config(page_title="Rio Mixer Pro", layout="wide")

def hex_to_rgb(h):
    h = h.lstrip('#')
    if len(h) > 6: h = h[:6]
    return list(int(h[i:i+2], 16) for i in (0, 2, 4))

# --- 2. KHO MÀU RIO (GIỮ NGUYÊN 100% CỦA BẠN) ---
RIO_MASTER = {
    "MÀU ĐẶC (SOLID)": {
        "W010-Trắng Tinh": "#FFFFFF", "W020-Trắng Sữa": "#F5F5DC", "BK01-Đen Tuyền": "#000000",
        "R110-Đỏ Tươi": "#FF0000", "R239-Đỏ Hoa Hồng": "#DC143C", "R240-Đỏ Sậm": "#8B0000",
        "Y120-Vàng Chanh": "#FFF44F", "Y101-Vàng Nghệ": "#FFC107", "Y105-Vàng Cam": "#FF8C00",
        "B310-Xanh Dương Cốt": "#0000FF", "B302-Xanh Tím": "#4B0082", "B305-Xanh Lơ": "#00BFFF",
        "G410-Xanh Lá": "#008000", "OR210-Cam": "#FF4500", "BR510-Nâu": "#5D3A1A", "V11-Tím Sen": "#FF00FF",
        "V15-Tím Cà": "#800080"
    },
    "MÀU NHŨ (SILVER/METALLIC)": {
        "M80-Bạc Siêu Mịn": "#C0C0C0", "M81-Bạc Mịn": "#D3D3D3", "M82-Bạc Trung": "#BEBEBE",
        "M90-Bạc Thô": "#E0E0E0", "M91-Bạc Đại": "#E5E5E5", "M92-Bạc Ánh Kim (Sparkle)": "#F5F5F5",
        "M95-Bạc Ánh Vàng": "#D4AF37", "M98-Bạc Ánh Đỏ": "#E9967A"
    },
    "MÀU CAMAY (PEARL)": {
        "P101-Camay Trắng": "#FBFCF8", "P202-Camay Đỏ": "#FFC0CB", "P303-Camay Vàng": "#FFD700", 
        "P305-Camay Đồng": "#B87333", "P404-Camay Xanh Dương": "#87CEEB", "P505-Camay Xanh Lá": "#98FB98", 
        "P606-Camay Tím": "#D8BFD8", "P707-Camay Xanh Ngọc": "#7FFFD4"
    },
    "MÀU TRONG & PHỤ GIA": {
        "CL01-Bóng Trong": "#FFFFFF",
        "MAT-Chất Làm Mờ": "#CCCCCC"
    }
}

# --- 3. KHO DỮ LIỆU AI MÃ MÀU CÁC HÃNG XE (TOYOTA, HONDA, MAZDA, HYUNDAI, KIA, FORD) ---
CAR_BRANDS_DB = {
    "Toyota": {
        "040": "#FFFFFF", "089": "#F8FBF8", "1D6": "#B2B2B2", "1G3": "#4B4C4E", "218": "#0A0B0C", 
        "3R3": "#8B0000", "4V8": "#A58D75", "8X2": "#1E3F5A", "X12": "#050505", "202": "#000000"
    },
    "Honda": {
        "NH731P": "#0A0A0A", "NH578": "#FFFFFF", "NH788P": "#FDFDF5", "NH830M": "#A9A9A9", 
        "R513": "#FF0000", "B593M": "#4682B4", "YR538M": "#B8860B"
    },
    "Mazda": {
        "46V": "#8B0000", "46G": "#708090", "25D": "#F5F5F5", "41W": "#000000", "42S": "#B0C4DE"
    },
    "Hyundai/Kia": {
        "WC9": "#FFFFFF", "RHM": "#C0C0C0", "M8N": "#4F4F4F", "M7B": "#0F1011", "PR2": "#990000", "SWP": "#F8F8F8"
    },
    "Ford": {
        "YZ": "#FFFFFF", "UX": "#B2B2B2", "M7343": "#000000", "D7": "#8B0000"
    }
}

st.title("🎨 AUTO BODY MINH KHANG PHA SƠN CHUYÊN NGHIỆP")

# --- CHỌN HỆ SƠN 1K/2K ---
sys_type = st.radio("Hệ thống sơn:", ["1K (Phủ bóng)", "2K (Sơn tự bóng)"], horizontal=True)
st.divider()

col_in1, col_in2 = st.columns(2)

with col_in1:
    input_method = st.radio("Cách thức lấy màu mục tiêu:", 
                             ["Tra cứu Mã Màu Xe (Hãng)", "Quét Camera thực tế", "Chọn từ bảng gốc Rio"])
    
    target_rgb = [255, 255, 255] 
    
    if input_method == "Quét Camera thực tế":
        img_file = st.camera_input("Chụp mẫu màu xe")
        if img_file:
            img = Image.open(img_file)
            target_rgb = np.array(img).mean(axis=(0,1)).astype(int).tolist()
            st.success("Đã nhận diện màu từ Camera")

    elif input_method == "Tra cứu Mã Màu Xe (Hãng)":
        brand_choice = st.selectbox("Chọn hãng xe:", list(CAR_BRANDS_DB.keys()) + ["Khác"])
        car_code = st.text_input("Nhập mã màu xe (VD: 1D6, NH731P, 46V...):").upper().strip()
        
        if car_code:
            # Thuật toán AI thông minh: Tìm kiếm xuyên thấu Database
            found_hex = None
            if brand_choice != "Khác" and car_code in CAR_BRANDS_DB[brand_choice]:
                found_hex = CAR_BRANDS_DB[brand_choice][car_code]
            else:
                # Nếu chọn "Khác" hoặc sai hãng, AI sẽ tự tìm trong toàn bộ kho xe
                for b in CAR_BRANDS_DB:
                    if car_code in CAR_BRANDS_DB[b]:
                        found_hex = CAR_BRANDS_DB[b][car_code]
                        st.info(f"💡 AI tìm thấy mã {car_code} thuộc hãng {b}")
                        break
            
            if found_hex:
                target_rgb = hex_to_rgb(found_hex)
                st.success(f"✅ Đã nhận diện màu {car_code}")
                st.color_picker("Sắc độ mục tiêu:", found_hex, disabled=True)
            else:
                st.error("❌ Mã màu chưa có trong bộ nhớ. Hãy dùng Camera!")

    elif input_method == "Chọn từ bảng gốc Rio":
        g = st.selectbox("Chọn nhóm:", list(RIO_MASTER.keys()))
        n = st.selectbox("Chọn mã:", list(RIO_MASTER[g].keys()))
        target_rgb = hex_to_rgb(RIO_MASTER[g][n])

with col_in2:
    st.write("### Thông số pha chế")
    total_vol = st.number_input("Tổng dung tích CỐT MÀU (ml):", value=1000, step=100)
    if "2K" in sys_type:
        ratio = st.selectbox("Tỷ lệ Đóng rắn:", ["4:1", "2:1"])
    st.warning("💡 Lưu ý: Xăng pha thợ tự tính theo kinh nghiệm.")

st.divider()

# --- NÚT TÍNH CÔNG THỨC ---
if st.button("🚀 XUẤT CÔNG THỨC CHI TIẾT", type="primary", use_container_width=True):
    all_colors = {}
    for group_name, colors in RIO_MASTER.items():
        if group_name != "MÀU TRONG & PHỤ GIA":
            all_colors.update(colors)
            
    weights = []
    total_w = 0
    
    for name, h in all_colors.items():
        dist = np.linalg.norm(np.array(target_rgb) - np.array(hex_to_rgb(h)))
        # Thuật toán AI: Tính toán tỷ lệ dựa trên khoảng cách màu sắc học thuật
        w = 1 / (dist + 0.1) if dist < 180 else 0
        weights.append((name, w))
        total_w += w

    if total_w > 0:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("#### 🧪 Tinh màu Rio (Đủ 100% cốt)")
            for n, w in weights:
                amt = (w / total_w) * total_vol
                if amt > 0.5: st.success(f"{n}: **{amt:.1f} ml**")
        with c2:
            st.markdown("#### ⚙️ Phụ gia bắt buộc")
            if "2K" in sys_type:
                h_div = 4 if "4:1" in ratio else 2
                h_amt = total_vol / h_div
                st.error(f"Đóng rắn (Hardener): **{h_amt:.1f} ml**")
            else:
                st.info("Hệ 1K: Không cần đóng rắn.")
            st.write(f"**Tổng tinh màu: {total_vol} ml**")
    else:
        st.error("Lỗi: Không thể phân tích màu mục tiêu.")
