import streamlit as st
import numpy as np
import PIL.Image as Image

# --- KHO DỮ LIỆU MÀU RIO (Bạn có thể thêm mã màu vào đây) ---
RIO_MASTER = {
    
    "MÀU ĐẶC (SOLID)": {
        "W010-Trắng Tinh": "#FFFFFF", 
        "W020-Trắng Sữa": "#F5F5DC", 
        "BK01-Đen Tuyền": "#000000",
        "R110-Đỏ Tươi": "#FF0000", 
        "R239-Đỏ Hoa Hồng": "#DC143C",
        "R240-Đỏ Sậm": "#8B0000",
        "Y120-Vàng Chanh": "#FFF44F", 
        "Y101-Vàng Nghệ": "#FFC107",
        "Y105-Vàng Cam": "#FF8C00",
        "B310-Xanh Dương Cốt": "#0000FF", 
        "B302-Xanh Tím": "#4B0082",
        "B305-Xanh Lơ": "#00BFFF",
        "G410-Xanh Lá": "#008000", 
        "OR210-Cam": "#FF4500", 
        "BR510-Nâu": "#5D3A1A", 
        "V11-Tím Sen": "#FF00FF",
        "V15-Tím Cà": "#800080"
    },
    "MÀU NHŨ (SILVER/METALLIC)": {
        "M80-Bạc Siêu Mịn": "#C0C0C0", 
        "M81-Bạc Mịn": "#D3D3D3", 
        "M82-Bạc Trung": "#BEBEBE",
        "M90-Bạc Thô": "#E0E0E0", 
        "M91-Bạc Đại": "#E5E5E5", 
        "M92-Bạc Ánh Kim (Sparkle)": "#F5F5F5",
        "M95-Bạc Ánh Vàng": "#D4AF37",
        "M98-Bạc Ánh Đỏ": "#E9967A"
    },
    "MÀU CAMAY (PEARL)": {
        "P101-Camay Trắng": "#FBFCF8", 
        "P202-Camay Đỏ": "#FFC0CB", 
        "P303-Camay Vàng": "#FFD700", 
        "P305-Camay Đồng": "#B87333",
        "P404-Camay Xanh Dương": "#87CEEB", 
        "P505-Camay Xanh Lá": "#98FB98", 
        "P606-Camay Tím": "#D8BFD8",
        "P707-Camay Xanh Ngọc": "#7FFFD4"
    },
    "MÀU TRONG & PHỤ GIA": {
        "CL01-Bóng Trong": "#FFFFFF00",
        "MAT-Chất Làm Mờ": "#FFFFFF55"
    }
  }
# --- CHỌN HỆ SƠN 1K/2K ---
sys_type = st.radio("Hệ thống sơn:", ["1K (Phủ bóng)", "2K (Sơn tự bóng)"], horizontal=True)

st.divider()

# --- INPUT MÀU SẮC (CAMERA / MÃ XE / RIO) ---
col_in1, col_in2 = st.columns(2)

with col_in1:
    input_method = st.radio("Cách thức lấy màu mục tiêu:", 
                             ["Quét Camera thực tế", "Nhập mã màu Xe/Hãng khác", "Chọn từ bảng gốc Rio"])
    
    target_rgb = [255, 255, 255] # Mặc định
    
    if input_method == "Quét Camera thực tế":
        img_file = st.camera_input("Chụp mẫu màu xe")
        if img_file:
            img = Image.open(img_file)
            target_rgb = np.array(img).mean(axis=(0,1)).astype(int).tolist()
            st.success("Đã nhận diện màu từ Camera")

    elif input_method == "Nhập mã màu Xe/Hãng khác":
        car_code = st.text_input("Nhập mã màu xe hoặc mã HEX (VD: NH731P hoặc #FF0000):")
        if car_code.startswith("#"):
            target_rgb = hex_to_rgb(car_code)
        else:
            st.info("Hệ thống đang giả lập mã xe... (Để chuẩn nhất hãy nhập mã HEX hoặc dùng Camera)")
            target_rgb = [150, 150, 150] # Placeholder

    elif input_method == "Chọn từ bảng gốc Rio":
        g = st.selectbox("Chọn nhóm:", list(RIO_MASTER.keys()))
        n = st.selectbox("Chọn mã:", list(RIO_MASTER[g].keys()))
        target_rgb = hex_to_rgb(RIO_MASTER[g][n])
with col_in2:
    st.write("### Thông số pha chế")
    total_vol = st.number_input("Dung tích sơn màu (ml):", value=1000, step=100)
    if "2K" in sys_type:
        ratio = st.selectbox("Tỷ lệ Đóng rắn:", ["4:1", "2:1"])
    thinner_rate = st.slider("Tỷ lệ xăng pha %:", 10, 100, 30 if "2K" in sys_type else 70)

st.divider()

# --- NÚT TÍNH CÔNG THỨC ---
if st.button("🚀 XUẤT CÔNG THỨC CHI TIẾT", type="primary", use_container_width=True):
    all_colors = {k: v for d in RIO_MASTER.values() for k, v in d.items()}
    weights = []
    total_w = 0
    
    for name, h in all_colors.items():
        dist = np.linalg.norm(np.array(target_rgb) - np.array(hex_to_rgb(h)))
        w = 1 / (dist + 0.1) if dist < 180 else 0
        weights.append((name, w))
        total_w += w

    if total_w > 0:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("#### 🧪 Tinh màu Rio")
            for n, w in weights:
                amt = (w / total_w) * total_vol
                if amt > 0.5: st.success(f"{n}: **{amt:.1f} ml**")
        with c2:
            st.markdown("#### ⚙️ Phụ gia")
            if "2K" in sys_type:
                h_div = 4 if "4:1" in ratio else 2
                h_amt = total_vol / h_div
                t_amt = (total_vol + h_amt) * (thinner_rate / 100)
                st.error(f"Đóng rắn: {h_amt:.1f} ml")
            else:
                t_amt = total_vol * (thinner_rate / 100)
            st.warning(f"Xăng pha: {t_amt:.1f} ml")
            total_final = total_vol + (h_amt if "2K" in sys_type else 0) + t_amt
            st.write(f"**Tổng hỗn hợp: {total_final:.1f} ml**")


def hex_to_rgb(h):
    h = h.lstrip('#')
    return list(int(h[i:i+2], 16) for i in (0, 2, 4))

st.set_page_config(page_title="Rio Mixer Pro", layout="wide")
st.title("🎨 AUTO BODY MINH KHANG PHA SƠN CHUYÊN NGHIỆP")
