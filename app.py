import streamlit as st
import pandas as pd
import numpy as np
import os
from streamlit_autorefresh import st_autorefresh

# --- CẤU HÌNH TRANG ---
st.set_page_config(page_title="Báo Cáo BMI", page_icon="💪", layout="wide")

# --- BIẾN TOÀN CỤC VÀ TÊN FILE ---
DATA_FILE = "bmi_data.csv"
# Các cột gốc trong file CSV
COLUMN_NAMES = [
    "Họ và tên", "Lớp", "Nhóm", "Chiều cao (m)",
    "Cân nặng (kg)", "Chỉ số BMI", "Lời khuyên"
]
# Các cột sẽ hiển thị trong bảng (Thêm cột tính toán)
DISPLAY_COLUMNS = [
    "Họ và tên", "Lớp", "Nhóm", "Chiều cao (m)", "Cân nặng (kg)",
    "Chỉ số BMI", "BMI (Tự động tính)", "Lời khuyên"
]
# Các cột sẽ có trong file tải về (Thêm cột tính toán)
DOWNLOAD_COLUMNS = [
    "STT", "Họ và tên", "Lớp", "Nhóm", "Chiều cao (m)", "Cân nặng (kg)",
    "Chỉ số BMI", "BMI (Tự động tính)", "Lời khuyên"
]


# --- HÀM KHỞI TẠO FILE DỮ LIỆU ---
def initialize_data_file():
    """
    Kiểm tra và tạo file CSV nếu chưa tồn tại.
    """
    if not os.path.exists(DATA_FILE):
        df_init = pd.DataFrame(columns=COLUMN_NAMES)
        # Dùng encoding 'utf-8-sig' để Excel đọc tiếng Việt có dấu
        df_init.to_csv(DATA_FILE, index=False, encoding='utf-8-sig')


# Khởi tạo file khi app chạy
initialize_data_file()

# --- GIAO DIỆN CHÍNH (SỬ DỤNG TABS) ---
st.title("💪 Ứng dụng Báo Cáo Chỉ Số BMI")
st.caption("Dữ liệu được lưu trữ vĩnh viễn và cập nhật thời gian thực.")

tab1, tab2 = st.tabs(["📝 Trang Nhập Liệu", "📊 Bảng Báo Cáo"])

# --- TAB 1: TRANG NHẬP LIỆU ---
with tab1:
    st.header("📝 Biểu mẫu nhập thông tin")

    # Quản lý trạng thái đã gửi (giống file khaosat.py)
    if "submitted" not in st.session_state:
        st.session_state.submitted = False

    if st.session_state.submitted:
        st.info("✅ Bạn đã gửi phản hồi thành công trong phiên này.")
        if st.button("Nhập thêm dữ liệu mới"):
            st.session_state.submitted = False
            st.rerun()
    else:
        # --- Biểu mẫu (Form) Nhập Liệu ---
        with st.form(key="student_form"):
            # Hàng 1: Tên và Lớp
            col1, col2 = st.columns(2)
            with col1:
                ho_va_ten = st.text_input("Họ và tên")
            with col2:
                lop = st.text_input("Lớp")

            # Hàng 2: Chọn Nhóm
            ten_nhom = st.selectbox(
                "Chọn nhóm",
                ["Nhóm 1", "Nhóm 2", "Nhóm 3", "Nhóm 4", "Nhóm 5"],
                index=None,
                placeholder="Vui lòng chọn nhóm..."
            )

            # Hàng 3: Chiều cao và Cân nặng
            col3, col4 = st.columns(2)
            with col3:
                chieu_cao = st.number_input(
                    "Chiều cao (mét)", min_value=0.0, max_value=2.5, step=0.01, format="%.2f", help="Ví dụ: 1.75")
            with col4:
                can_nang = st.number_input(
                    "Cân nặng (kg)", min_value=0.0, max_value=200.0, step=0.1, format="%.1f")

            # Hàng 4: Ô nhập Chỉ số BMI
            chi_so_bmi = st.number_input(
                "Nhập Chỉ số BMI", min_value=0.0, max_value=50.0, step=0.1, format="%.2f")

            # Hàng 5: Ô nhập lời khuyên
            loi_khuyen = st.text_area("Nhập lời khuyên")

            submit_button = st.form_submit_button(label="Thêm vào danh sách")

        # --- Xử lý dữ liệu sau khi nhấn nút ---
        if submit_button:
            if ho_va_ten and lop and ten_nhom and chieu_cao > 0 and can_nang > 0:

                new_data = {
                    "Họ và tên": ho_va_ten,
                    "Lớp": lop,
                    "Nhóm": ten_nhom,
                    "Chiều cao (m)": chieu_cao,
                    "Cân nặng (kg)": can_nang,
                    "Chỉ số BMI": chi_so_bmi,
                    "Lời khuyên": loi_khuyen
                }

                # --- LƯU VÀO FILE CSV ---
                try:
                    df_old = pd.read_csv(DATA_FILE)
                    new_row_df = pd.DataFrame([new_data], columns=COLUMN_NAMES)
                    df_new = pd.concat([df_old, new_row_df], ignore_index=True)

                    df_new.to_csv(DATA_FILE, index=False, encoding='utf-8-sig')

                    st.session_state.submitted = True
                    st.success(
                        f"Đã thêm thành công: {ho_va_ten} (Nhóm: {ten_nhom})!")
                    st.balloons()
                    # ĐÃ XÓA st.rerun() Ở ĐÂY ĐỂ SỬA LỖI GHI FILE

                except Exception as e:
                    st.error(f"Lỗi khi đang lưu file: {e}")
            else:
                st.error(
                    "Vui lòng nhập đầy đủ Họ tên, Lớp, Nhóm, Chiều cao và Cân nặng.")

    # --- Khu vực Admin (giống file khaosat.py) ---
    st.divider()
    with st.expander("🔐 Quản lý dữ liệu (Dành cho Quản trị viên)"):
        password = st.text_input(
            "Nhập mật khẩu để xóa dữ liệu", type="password", key="admin_pass")
        if st.button("🗑️ Xóa toàn bộ dữ liệu"):
            if password == "admin123":  # Bạn có thể đổi mật khẩu ở đây

                # SỬA LỖI: Xóa file cũ trước khi tạo file mới
                if os.path.exists(DATA_FILE):
                    os.remove(DATA_FILE)

                initialize_data_file()  # Tạo lại file rỗng
                st.session_state.submitted = False  # Reset trạng thái
                st.success("✅ Đã xóa toàn bộ dữ liệu. Trang sẽ tự làm mới.")
                st.rerun()
            elif password:
                st.error("❌ Mật khẩu không chính xác.")

# --- TAB 2: BẢNG BÁO CÁO ---
with tab2:
    st.title("📊 BÁO CÁO THỰC HÀNH")
    st.header("ĐO CHỈ SỐ ĐÁNH GIÁ THỂ TRẠNG BMI")

    # Tự động làm mới trang này mỗi 5 giây
    st_autorefresh(interval=5000, key="data_refresh")

    # --- ĐỌC DỮ LIỆU TỪ FILE CSV ---
    try:
        df_all = pd.read_csv(DATA_FILE)
    except FileNotFoundError:
        st.info("Hiện chưa có file dữ liệu. Vui lòng nhập dữ liệu ở 'Trang Nhập Liệu'.")
        st.stop()
    except pd.errors.EmptyDataError:
        # BẮT LỖI KHI FILE ĐANG GHI (BỊ TRỐNG TẠM THỜI)
        st.info("⏳ Dữ liệu đang được cập nhật, vui lòng chờ trong giây lát...")
        st.stop()
    except Exception as e:
        st.error(f"Lỗi không xác định khi đọc file: {e}")
        st.stop()

    # --- HIỂN THỊ DỮ LIỆU ---
    if not df_all.empty:
        st.success(f"**Tổng số lượt nhập: {len(df_all)}**")

        # --- TÍNH TOÁN CỘT BMI MỚI ĐỂ KIỂM TRA ---
        try:
            # Chuyển đổi kiểu dữ liệu để tính toán, phòng lỗi
            can_nang_kg = pd.to_numeric(df_all["Cân nặng (kg)"])
            # Thay thế 0 bằng NaN để tránh lỗi chia cho 0
            chieu_cao_m = pd.to_numeric(
                df_all["Chiều cao (m)"]).replace(0, np.nan)

            df_all["BMI (Tự động tính)"] = (
                can_nang_kg / (chieu_cao_m ** 2)).round(2)
        except Exception as e:
            st.warning(f"Không thể tính toán BMI tự động. Lỗi: {e}")
            df_all["BMI (Tự động tính)"] = "Lỗi"

        # ---------------------------------------------

        all_groups = ["Nhóm 1", "Nhóm 2", "Nhóm 3", "Nhóm 4", "Nhóm 5"]

        # Tạo các tab cho từng nhóm
        group_tabs = st.tabs(all_groups)

        for i, tab in enumerate(group_tabs):
            with tab:
                group_name = all_groups[i]
                st.subheader(f"Dữ liệu cho {group_name}")

                group_df = df_all[df_all["Nhóm"] == group_name]

                if group_df.empty:
                    st.info(f"Hiện chưa có dữ liệu nào cho {group_name}.")
                else:
                    # Dùng .copy() và chỉ chọn các cột cần hiển thị
                    df_display = group_df[DISPLAY_COLUMNS].copy()

                    df_display.index = np.arange(1, len(df_display) + 1)
                    df_display = df_display.rename_axis('STT').reset_index()

                    st.dataframe(df_display, use_container_width=True)

        # --- Nút Tải Xuống (Đã cập nhật sang CSV) ---
        st.divider()
        st.subheader("Tải xuống toàn bộ dữ liệu")

        # Chuẩn bị dữ liệu để tải xuống
        df_all_with_stt = df_all.copy()

        # Đảm bảo cột STT được thêm vào đúng
        df_all_with_stt.index = np.arange(1, len(df_all_with_stt) + 1)
        df_all_with_stt = df_all_with_stt.rename_axis('STT').reset_index()

        # Sắp xếp lại các cột cho file tải về
        # Đảm bảo 'BMI (Tự động tính)' có trong df_all_with_stt trước khi chọn
        if "BMI (Tự động tính)" not in df_all_with_stt.columns:
            # Thêm cột nếu bị thiếu
            df_all_with_stt["BMI (Tự động tính)"] = "Lỗi"

        df_all_with_stt = df_all_with_stt[DOWNLOAD_COLUMNS]

        # Chuyển DataFrame thành chuỗi CSV (định dạng UTF-8-sig để hỗ trợ tiếng Việt)
        csv_data = df_all_with_stt.to_csv(index=False).encode('utf-8-sig')

        st.download_button(
            label="Tải xuống toàn bộ báo cáo (.csv)",
            data=csv_data,
            file_name="bao_cao_bmi.csv",
            mime="text/csv",
        )

    else:
        st.info(
            "Hiện chưa có ai trong danh sách. Vui lòng quay lại trang 'Trang Nhập Liệu'.")
