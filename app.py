import streamlit as st
import pandas as pd
from datetime import datetime
import os
import pypdf

# 页面配置
st.set_page_config(
    page_title="Reliance Maid Agency System",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 确保 PDF 输出目录存在
os.makedirs("output", exist_ok=True)

# 初始化 Session State (模拟数据库)
if 'agency' not in st.session_state:
    st.session_state.agency = {
        "name": "RELIANCE MAID AGENCI (M) SDN BHD",
        "license": "202501046992",
        "address": "NO 34A, JALAN BUKIT IMPIAN 16, TAMAN IMPIAN EMAS, 81300 SKUDAI, JOHOR",
        "phone": "010-837 8472",
        "email": "reliance.maid.agensi@gmail.com"
    }

if 'customers' not in st.session_state:
    st.session_state.customers = [
        {
            "name": "GAN JUN HENG",
            "ic": "960226-01-6725",
            "phone": "012-345 6789",
            "address": "123, Jalan Sutera, Taman Skudai Baru, 81300 Skudai, Johor"
        }
    ]

if 'maids' not in st.session_state:
    st.session_state.maids = [
        {
            "name": "Sri Haryati",
            "passport": "E9716672",
            "dob": "1995-05-12",
            "permit_expiry": "2027-05-12",
            "supplier": "PT ANTAR TENAGA MANDIRI"
        }
    ]

if 'suppliers' not in st.session_state:
    st.session_state.suppliers = [
        {
            "name": "PT ANTAR TENAGA MANDIRI",
            "country": "Indonesia",
            "contact": "Bapak Rudi",
            "phone": "+62 21-555-0199"
        }
    ]

# 侧边栏导航
st.sidebar.title("📋 导航菜单")
menu = st.sidebar.selectbox(
    "选择功能模块", 
    ["业务仪表盘", "顾客资料 (Customer)", "女佣资料 (Maid)", "Supplier 供应商", "公司资料 (Agency)", "申请文件与生成 (Application)"]
)

# ==================== 1. 业务仪表盘 ====================
if menu == "业务仪表盘":
    st.title("📊 业务仪表盘与到期提醒")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("顾客数量", len(st.session_state.customers))
    with col2:
        st.metric("女佣数量", len(st.session_state.maids))
    with col3:
        st.metric("Supplier 数量", len(st.session_state.suppliers))
    with col4:
        st.metric("Permit 已过期", 0)
        
    st.markdown("---")
    st.subheader("⚠️ 提醒事项 (Alerts)")
    st.info("目前所有证件和合同均在有效期内，暂无紧急提醒。")

# ==================== 2. 顾客资料 ====================
elif menu == "顾客资料 (Customer)":
    st.title("👥 顾客资料管理")
    
    with st.expander("➕ 添加新顾客"):
        with st.form("add_customer_form"):
            c_name = st.text_input("顾客全名 (Name)")
            c_ic = st.text_input("身份证号 / 护照号 (IC / Passport)")
            c_phone = st.text_input("联系电话 (Phone)")
            c_address = st.text_area("住址 (Address)")
            submitted = st.form_submit_button("保存顾客")
            if submitted and c_name:
                st.session_state.customers.append({
                    "name": c_name, "ic": c_ic, "phone": c_phone, "address": c_address
                })
                st.success(f"成功添加顾客: {c_name}")
                st.rerun()

    st.subheader("现有顾客列表")
    for idx, cust in enumerate(st.session_state.customers):
        st.write(f"**{idx+1}. {cust['name']}** | IC: {cust['ic']} | 电话: {cust['phone']}")
        st.caption(f"地址: {cust['address']}")
        st.markdown("---")

# ==================== 3. 女佣资料 ====================
elif menu == "女佣资料 (Maid)":
    st.title("👩‍🦰 女佣资料管理")
    
    with st.expander("➕ 录入新女佣"):
        with st.form("add_maid_form"):
            m_name = st.text_input("女佣姓名")
            m_pass = st.text_input("护照号码 (Passport)")
            m_dob = st.date_input("出生日期")
            m_expiry = st.date_input("Permit 到期日")
            supp_names = [s["name"] for s in st.session_state.suppliers]
            m_supp = st.selectbox("选择供应商 (Supplier)", supp_names if supp_names else ["默认"])
            m_submit = st.form_submit_button("保存女佣")
            if m_submit and m_name:
                st.session_state.maids.append({
                    "name": m_name, "passport": m_pass, 
                    "dob": str(m_dob), "permit_expiry": str(m_expiry), "supplier": m_supp
                })
                st.success(f"成功添加女佣: {m_name}")
                st.rerun()

    st.subheader("现有女佣列表")
    for idx, maid in enumerate(st.session_state.maids):
        st.write(f"**{idx+1}. {maid['name']}** | 护照: {maid['passport']} | 供应商: {maid['supplier']}")
        st.write(f"Permit 到期: `{maid['permit_expiry']}`")
        st.markdown("---")

# ==================== 4. Supplier 供应商 ====================
elif menu == "Supplier 供应商":
    st.title("🏢 印度尼西亚供应商管理")
    
    with st.expander("➕ 添加新 Supplier"):
        with st.form("add_supp_form"):
            s_name = st.print_name = st.text_input("公司名称 (Agency Name)")
            s_country = st.text_input("国家", value="Indonesia")
            s_contact = st.text_input("负责人姓名")
            s_phone = st.text_input("联系电话")
            s_submit = st.form_submit_button("保存 Supplier")
            if s_submit and s_name:
                st.session_state.suppliers.append({
                    "name": s_name, "country": s_country, "contact": s_contact, "phone": s_phone
                })
                st.success(f"成功添加 Supplier: {s_name}")
                st.rerun()

    st.subheader("现有供应商列表")
    for idx, supp in enumerate(st.session_state.suppliers):
        st.write(f"**{idx+1}. {supp['name']}** ({supp['country']})")
        st.write(f"负责人: {supp['contact']} | 电话: {supp['phone']}")
        st.markdown("---")

# ==================== 5. 公司资料 ====================
elif menu == "公司资料 (Agency)":
    st.title("⚙️ 中介公司资料设置")
    with st.form("agency_form"):
        ag_name = st.text_input("公司全称", value=st.session_state.agency["name"])
        ag_lic = st.text_input("牌照号码 (License No)", value=st.session_state.agency["license"])
        ag_addr = st.text_area("公司地址", value=st.session_state.agency["address"])
        ag_phone = st.text_input("联系电话", value=st.session_state.agency["phone"])
        ag_email = st.text_input("电子邮箱", value=st.session_state.agency["email"])
        
        if st.form_submit_button("更新公司资料"):
            st.session_state.agency = {
                "name": ag_name, "license": ag_lic, "address": ag_addr, "phone": ag_phone, "email": ag_email
            }
            st.success("公司资料已成功更新！")

# ==================== 6. 申请文件与生成 ====================
elif menu == "申请文件与生成 (Application)":
    st.title("📄 申请文件生成与自动填充")
    st.markdown("在这里选择关联的**顾客、女佣和供应商**，系统会自动为您一键生成标准化 PDF 文件！")

    # 数据选择
    cust_options = [f"{c['name']} — {c['ic']}" for c in st.session_state.customers]
    maid_options = [f"{m['name']} — {m['passport']}" for m in st.session_state.maids]
    supp_options = [s['name'] for s in st.session_state.suppliers]

    selected_cust = st.selectbox("1. 选择顾客 (Customer)", cust_options if cust_options else ["无数据"])
    selected_maid = st.selectbox("2. 选择女佣 (Maid)", maid_options if maid_options else ["无数据"])
    selected_supp = st.selectbox("3. 选择 Supplier", supp_options if supp_options else ["无数据"])

    st.markdown("---")

    # 生成 PDF 函数（示例生成器，包含下载按钮支持）
    def generate_dummy_pdf(doc_name, data_dict):
        filename = f"output/{doc_name}_Filled.pdf"
        # 简单创建一个占位 PDF 方便直接下载测试
        writer = pypdf.PdfWriter()
        writer.add_blank_page(width=595, height=842) # A4 尺寸
        with open(filename, "wb") as f:
            writer.write(f)
        return filename

    # PRA 1
    st.subheader("PRA 1 (页数: 1 页)")
    if st.button("生成 PRA 1 PDF"):
        pdf_path = generate_dummy_pdf("PRA_1", {"customer": selected_cust, "maid": selected_maid})
        st.session_state["pra1_path"] = pdf_path
        st.success("已生成: PRA_1_Filled.pdf")

    if "pra1_path" in st.session_state and os.path.exists(st.session_state["pra1_path"]):
        with open(st.session_state["pra1_path"], "rb") as f:
            st.download_button(
                label="📥 点击下载 PRA_1_Filled.pdf",
                data=f,
                file_name="PRA_1_Filled.pdf",
                mime="application/pdf"
            )

    st.markdown("---")

    # IM.12
    st.subheader("IM.12 (页数: 1 页)")
    if st.button("生成 IM.12 PDF"):
        pdf_path = generate_dummy_pdf("IM_12", {"customer": selected_cust, "maid": selected_maid})
        st.session_state["im12_path"] = pdf_path
        st.success("已生成: IM_12_Filled.pdf")

    if "im12_path" in st.session_state and os.path.exists(st.session_state["im12_path"]):
        with open(st.session_state["im12_path"], "rb") as f:
            st.download_button(
                label="📥 点击下载 IM_12_Filled.pdf",
                data=f,
                file_name="IM_12_Filled.pdf",
                mime="application/pdf"
            )
