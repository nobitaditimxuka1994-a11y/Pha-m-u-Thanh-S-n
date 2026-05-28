import streamlit as st
import numpy as np

# Cấu hình danh mục màu gốc Rio (Bạn có thể thêm bớt tùy ý)
BASE_COLORS = {
    "Trắng Base": [255, 255, 255],
    "Đỏ Rio": [255, 0, 0],
    "Vàng Rio": [255, 255, 0],
    "Xanh Dương": [0, 0, 255],
    "Đen Rio": [0, 0, 0],
    "Nâu Đất": [139, 69, 19]
}

def hex_to_rgb(hex):
    hex = hex.lstrip('#')
    return list(int(hex[i:i+2], 16) for i in (0, 2, 4))

st.set_page_config(page_title="Pha Màu Rio Pro", layout="centered")

st.title("🎨 Hệ Thống Pha Màu Rio Online")
st.subheader("Quét màu & Tính công thức miễn phí")

# 1. Tính năng quét màu qua Camera
img_file = st.camera_input("Chụp ảnh mẫu màu cần pha")

target_rgb = [255, 255, 255] # Mặc định

if img_file:
    import PIL.Image as Image
    img = Image.open(img_file)
    img_array = np.array(img)
    # Lấy màu trung bình của ảnh chụp được làm màu mục tiêu
    target_rgb = img_array.mean(axis=(0,1)).astype(int).tolist()
    st.write(f"Màu đã nhận diện: RGB {target_rgb}")
    st.color_picker("Màu mục tiêu", '#%02x%02x%02x' % tuple(target_rgb))

# 2. Nhập thông số pha
volume = st.number_input("Tổng dung tích cần pha (ml):", value=1000, step=100)

# 3. Thuật toán tính tỷ lệ
if st.button("TÍNH CÔNG THỨC"):
    st.write("### Kết quả pha trộn:")
    
    total_weight = 0
    weights = []
    
    for name, rgb in BASE_COLORS.items():
        # Thuật toán tính khoảng cách màu Delta E đơn giản
        dist = np.linalg.norm(np.array(target_rgb) - np.array(rgb))
        weight = 1 / (dist + 0.1)
        weights.append((name, weight))
        total_weight += weight
    
    col1, col2 = st.columns(2)
    with col1:
        for name, w in weights:
            amount = (w / total_weight) * volume
            st.info(f"**{name}:** {amount:.2f} ml")
    
    with col2:
        st.success("Hướng dẫn: Đổ sơn trắng vào trước, sau đó thêm tinh màu theo thứ tự từ nhiều đến ít.")

st.markdown("---")
st.caption("Ứng dụng chạy trên nền tảng GitHub & Streamlit Cloud miễn phí.")
