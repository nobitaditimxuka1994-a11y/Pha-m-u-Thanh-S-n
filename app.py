import streamlit as st
import numpy as np

# DANH MỤC MÀU RIO ĐẦY ĐỦ
RIO_MASTER = {
    "MÀU ĐẶC (SOLID)": {
        "W010-Trắng Tinh": "#FFFFFF", "W020-Trắng Sữa": "#F2F2E6", "BK01-Đen Tuyền": "#050505",
        "R110-Đỏ Cờ": "#D31212", "R239-Đỏ Hoa Hồng": "#C21E2F", "Y120-Vàng Nghệ": "#FFD700",
        "Y101-Vàng Công Nghiệp": "#DAA520", "B310-Xanh Dương Đậm": "#003366", "B302-Xanh Tím": "#4B0082",
        "G410-Xanh Lá Cây": "#006400", "OR210-Cam Sáng": "#FF4500", "BR510-Nâu Đất": "#5D3A1A", "V11-Tím Sen": "#8B008B"
    },
    "MÀU NHŨ (SILVER)": {
        "M80-Bạc Mịn": "#C0C0C0", "M81-Bạc Trung": "#D3D3D3", "M90-Bạc Thô": "#E0E0E0",
        "M91-Bạc Cực Thô": "#E5E5E5", "M92-Bạc Ánh Kim": "#F0F0F0"
    },
    "MÀU CAMAY (PEARL)": {
        "P101-Camay Trắng": "#F8F8FF", "P202-Camay Đỏ": "#FFB6C1", "P303-Camay Vàng": "#FFF700",
        "P404-Camay Xanh Dương": "#ADD8E6", "P505-Camay Xanh Lá": "#90EE90", "P606-Camay Tím": "#E6E6FA"
    }
}

def hex_to_rgb(h):
    h = h.lstrip('#')
    return list(int(h[i:i+2], 16) for i in (0, 2, 4))

st.set_page_config(page_title="Rio Mixer Pro", layout="centered")

st.title("🎨 MÁY PHA SƠN RIO 1K/2K")

# --- Ô CHỌN HỆ SƠN (HIỆN NGAY ĐẦU APP) ---
st.subheader("1. Chọn Hệ Sơn Rio")
sys_type = st.radio("Hệ thống sơn đang dùng:", ["Hệ 1K (Phủ bóng sau)", "Hệ 2K (Tự bóng - Có đóng rắn)"], horizontal=True)

col_input1, col_input2 = st.columns(2)

with col_input1:
    group = st.selectbox("Nhóm màu Rio:", list(RIO_MASTER.keys()))
    color_name = st.selectbox("Mã màu Rio gốc:", list(RIO_MASTER[group].keys()))
    target_hex = RIO_MASTER[group][color_name]
    st.color_picker("Màu kiểm tra", target_hex, disabled=True)

with col_input2:
    total_vol = st.number_input("Dung tích sơn màu (ml):", value=1000, step=100)
    if "2K" in sys_type:
        ratio = st.selectbox("Tỷ lệ Đóng rắn:", ["4:1 (4 Sơn : 1 Đóng rắn)", "2:1 (2 Sơn : 1 Đóng rắn)"])
    thinner_rate = st.slider("Xăng pha (Thinner) %:", 10, 100, 20 if "2K" in sys_type else 70)

st.divider()

# --- NÚT XUẤT CÔNG THỨC ---
if st.button("🚀 XUẤT CÔNG THỨC PHA CHẾ", type="primary", use_container_width=True):
    target_rgb = hex_to_rgb(target_hex)
    all_colors = {k: v for d in RIO_MASTER.values() for k, v in d.items()}
    
    weights = []
    total_w = 0
    for name, h in all_colors.items():
        dist = np.linalg.norm(np.array(target_rgb) - np.array(hex_to_rgb(h)))
        w = 1 / (dist + 0.1) if dist < 150 else 0
        weights.append((name, w))
        total_w += w

    if total_w > 0:
        st.subheader("📊 BẢNG HƯỚNG DẪN PHA")
        c1, c2 = st.columns(2)
        
        with c1:
            st.markdown("### 🧪 Tinh màu Rio")
            for n, w in weights:
                amt = (w / total_w) * total_vol
                if amt > 0.5:
                    st.info(f"**{n}:** {amt:.1f} ml")
        
        with c2:
            st.markdown("### ⚙️ Phụ gia pha kèm")
            if "2K" in sys_type:
                h_div = 4 if "4:1" in ratio else 2
                h_amt = total_vol / h_div
                t_amt = (total_vol + h_amt) * (thinner_rate / 100)
                st.error(f"**Đóng rắn (Hardener):** {h_amt:.1f} ml")
                st.warning(f"**Xăng pha (Thinner):** {t_amt:.1f} ml")
                st.write(f"**Tổng hỗn hợp:** {total_vol + h_amt + t_amt:.1f} ml")
            else:
                t_amt = total_vol * (thinner_rate / 100)
                st.warning(f"**Xăng pha (Thinner):** {t_amt:.1f} ml")
                st.write(f"**Tổng hỗn hợp:** {total_vol + t_amt:.1f} ml")
    else:
        st.error("Lỗi thuật toán màu!")
