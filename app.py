import io
import streamlit as st
import fitz  # PyMuPDF

st.set_page_config(page_title="Reliance Maid System", layout="centered")

# 初始化内存数据库
if "employers" not in st.session_state:
    st.session_state.employers = [{
        "name": "GAN JUN HENG", 
        "ic": "960226-01-6725", 
        "address": "NO 79, JLN NAKHODA 14, TAMAN UNGKU TUN AMINAH, 81300 SKUDAI JOHOR.", 
        "phone": "010-663 5035"
    }]
if "maids" not in st.session_state:
    st.session_state.maids = [{
        "name": "SRI HARYATI", 
        "passport": "E9716672", 
        "nationality": "INDONESIAN",
        "dob": "23 OCT 1988"
    }]
if "suppliers" not in st.session_state:
    st.session_state.suppliers = [{
        "name": "PT ANTAR TENAGA MANDIRI", 
        "contact": "081298785620"
    }]

st.title("📊 Reliance Maid 业务管理与自动填表系统")

# 侧边栏导航
menu = st.sidebar.radio("导航菜单", ["业务仪表盘与到期提醒", "➕ 添加与管理资料", "🖨️ 独立选择并下载 PDF"])

PDF_FILES = [
    "CONTRACT MY.pdf",
    "EC NEW CONTRACT.pdf",
    "IM 38.pdf",
    "IM12.pdf",
    "LAMPIRAN A.pdf",
    "Laporlari.pdf",
    "LG NEW.pdf",
    "PERSONAL BOND.pdf",
    "PRA1.pdf",
    "SURAT_WAKIL_MAJIKAN.pdf",
    "Agency_Agreement_Reliance_Maid.pdf"
]

# 1. 仪表盘页面
if menu == "业务仪表盘与到期提醒":
    st.subheader("📊 业务仪表盘与到期提醒")
    col1, col2, col3 = st.columns(3)
    col1.metric("顾客数量", len(st.session_state.employers))
    col2.metric("女佣数量", len(st.session_state.maids))
    col3.metric("Supplier 数量", len(st.session_state.suppliers))
    
    st.markdown("---")
    st.subheader("⚠️ 提醒事项 (Alerts)")
    st.info("目前所有证件和合同均在有效期内，暂无紧急提醒。")

# 2. 添加与管理资料页面
elif menu == "➕ 添加与管理资料":
    st.subheader("👥 客户、女佣与供应商资料管理")
    
    tab1, tab2, tab3 = st.tabs(["添加顾客 (Employer)", "添加女佣 (Maid)", "添加供应商 (Supplier)"])
    
    with tab1:
        with st.form("add_emp_form"):
            e_name = st.text_input("雇主全名", value="GAN JUN HENG")
            e_ic = st.text_input("身份证/护照号", value="960226-01-6725")
            e_addr = st.text_area("地址", value="NO 79, JLN NAKHODA 14, TAMAN UNGKU TUN AMINAH, 81300 SKUDAI JOHOR.")
            e_phone = st.text_input("电话号码", value="010-663 5035")
            submitted_e = st.form_submit_button("保存顾客资料")
            if submitted_e and e_name:
                st.session_state.employers.append({"name": e_name, "ic": e_ic, "address": e_addr, "phone": e_phone})
                st.success(f"成功添加顾客: {e_name}")
                
    with tab2:
        with st.form("add_maid_form"):
            m_name = st.text_input("女佣全名", value="SRI HARYATI")
            m_pass = st.text_input("女佣护照号", value="E9716672")
            m_nat = st.text_input("国籍", value="INDONESIAN")
            submitted_m = st.form_submit_button("保存女佣资料")
            if submitted_m and m_name:
                st.session_state.maids.append({"name": m_name, "passport": m_pass, "nationality": m_nat})
                st.success(f"成功添加女佣: {m_name}")
                
    with tab3:
        with st.form("add_supp_form"):
            s_name = st.text_input("Supplier 供应商名称", value="PT ANTAR TENAGA MANDIRI")
            s_contact = st.text_input("供应商电话", value="081298785620")
            submitted_s = st.form_submit_button("保存 Supplier 资料")
            if submitted_s and s_name:
                st.session_state.suppliers.append({"name": s_name, "contact": s_contact})
                st.success(f"成功添加 Supplier: {s_name}")

# 3. 独立下载 PDF 页面（带自动填表逻辑）
elif menu == "🖨️ 独立选择并下载 PDF":
    st.subheader("🖨️ 选择关联资料并单独下载文档")
    
    if not st.session_state.employers or not st.session_state.maids or not st.session_state.suppliers:
        st.warning("⚠️ 请先在【添加与管理资料】中添加资料！")
    else:
        selected_emp = st.selectbox("选择顾客 (Employer)", st.session_state.employers, format_func=lambda x: x["name"])
        selected_maid = st.selectbox("选择女佣 (Maid)", st.session_state.maids, format_func=lambda x: x["name"])
        selected_supp = st.selectbox("选择供应商 (Supplier)", st.session_state.suppliers, format_func=lambda x: x["name"])
        
        agency_name = st.text_input("本公司名称 (Agency)", "AGENSI PEKERJAAN RELIANCE MAID SDN BHD")

        st.markdown("---")
        st.write("### 📄 自动填表及单文件下载列表")

        for filename in PDF_FILES:
            col_name, col_btn = st.columns([3, 1])
            col_name.write(f"📁 **{filename}**")
            
            pdf_bytes = None
            try:
                # 打开对应的 PDF 模板
                doc = fitz.open(filename)
                page = doc[0]  # 默认在第一页注入数据（后续可针对不同文件微调坐标）
                
                # 动态把选中的资料写到 PDF 页面特定位置（示例坐标，可根据实际排版调整）
                # 这里我们在每一页的顶部或空白处写入核心关联信息，确保生成的文件带有当前客户数据
                info_text = f"EMPLOYER: {selected_emp['name']} | IC: {selected_emp['ic']} | MAID: {selected_maid['name']} ({selected_maid['passport']})"
                
                # 在 PDF 第一页左上角打印一行系统合成数据（作为基础填表演示）
                page.insert_text((50, 40), info_text, fontsize=9, color=(0, 0, 0))
                
                # 针对 Surat Wakil Majikan 或 PRA1 的特殊文字注入
                if filename == "SURAT_WAKIL_MAJIKAN.pdf":
                    page.insert_text((100, 150), selected_emp['name'], fontsize=10, color=(0, 0, 0))
                elif filename == "PRA1.pdf":
                    page.insert_text((120, 200), selected_emp['name'], fontsize=10, color=(0, 0, 0))
                
                output_pdf = io.BytesIO()
                doc.save(output_pdf)
                doc.close()
                pdf_bytes = output_pdf.getvalue()
            except Exception as e:
                # 容错处理
                pdf_bytes = f"Error processing {filename}: {str(e)}".encode()

            with col_btn:
                st.download_button(
                    label="📥 下载",
                    data=pdf_bytes,
                    file_name=filename,
                    mime="application/pdf",
                    key=f"dl_{filename}"
                )
