import streamlit as st
import json
import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

st.set_page_config(page_title="Reliance Maid Management System", layout="wide")

DB_FILE = "maid_system_db.json"

DEFAULT_DATA = {
    "agency": {
        "name": "AGENSI PEKERJAAN RELIANCE MAID SDN BHD",
        "director": "CHIOW TECK SENG",
        "ic": "821220-01-6169",
        "license": "202501046992",
        "address": "NO 34A, JALAN BUKIT IMPIAN 16, TAMAN IMPIAN EMAS, 81300 SKUDAI, JOHOR.",
        "phone": "010-837 8472",
        "email": "reliance.maid.agensi@gmail.com"
    },
    "customers": [
        {
            "id": "C001",
            "name": "GAN JUN HENG",
            "ic": "960226-01-6725",
            "phone": "010-663 5035",
            "email": "gan@example.com",
            "occupation": "Engineer",
            "monthly_income": "8000",
            "marital_status": "Single",
            "spouse_name": "",
            "spouse_ic": "",
            "address": "NO 79, JLN NAKHODA 14, TAMAN UNGKU TUN AMINAH, 81300 SKUDAI JOHOR",
            "state": "Johor",
            "postcode": "81300",
            "children": "0",
            "children_ages": "",
            "elderly": "0",
            "purpose": "take care children"
        }
    ],
    "maids": [
        {
            "id": "M001",
            "name": "Sri Haryati",
            "gender": "Female",
            "dob": "1988-10-23",
            "pob": "Kendal",
            "nationality": "Indonesia",
            "religion": "Islam",
            "marital_status": "Married",
            "occupation": "Domestic Worker",
            "phone": "-",
            "passport_no": "E9716672",
            "passport_issue": "2026-07-29",
            "passport_expiry": "2029-07-29",
            "overseas_address": "TLANGU RT 005 RW 004 DESA SUKOREJO KEC SUKOREJO KAB KENDAL PROV JAWA TENGAH",
            "arrival_date": "",
            "permit_no": "",
            "permit_expiry": "",
            "contract_start": "",
            "contract_expiry": "",
            "skills": "General housework"
        }
    ],
    "suppliers": [
        {
            "id": "S001",
            "company_name": "PT ANTAR TENAGA MANDIRI",
            "sip3mi": "91206027420450002",
            "director_name": "SANGAB BARUS",
            "director_id": "3215030508580002",
            "address": "JALAN SERMA MARJUKI RT 006 RW 002 NO 7, BEKASI SELATAN 17141 BEKASI",
            "phone": "081298785620",
            "email": "yuliatm1717@gmail.com"
        }
    ]
}

def load_data():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return DEFAULT_DATA
    return DEFAULT_DATA

def save_data(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

db = load_data()

st.sidebar.title("🛠️ Reliance Maid System")
menu = st.sidebar.selectbox("导航菜单", [
    "Dashboard 仪表盘", 
    "顾客资料 (Customer)", 
    "女佣资料 (Maid)", 
    "Supplier 供应商", 
    "Agency Details 公司资料", 
    "申请文件与生成 (Application)",
    "数据备份与恢复 (Backup)"
])

if menu == "Dashboard 仪表盘":
    st.title("📊 业务仪表盘与到期提醒")
    today = datetime.today().date()
    permit_90, permit_60, permit_expired = 0, 0, 0
    passport_renew, contract_renew = 0, 0
    
    for m in db["maids"]:
        if m.get("permit_expiry"):
            pe = datetime.strptime(m["permit_expiry"], "%Y-%m-%d").date()
            diff = (pe - today).days
            if diff < 0: permit_expired += 1
            elif diff <= 60: permit_60 += 1
            elif diff <= 90: permit_90 += 1
        if m.get("passport_expiry"):
            pse = datetime.strptime(m["passport_expiry"], "%Y-%m-%d").date()
            if (pse - today).days <= 90: passport_renew += 1
        if m.get("contract_expiry"):
            ce = datetime.strptime(m["contract_expiry"], "%Y-%m-%d").date()
            if (ce - today).days <= 60: contract_renew += 1

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("顾客数量", len(db["customers"]))
    col2.metric("女佣数量", len(db["maids"]))
    col3.metric("Supplier 数量", len(db["suppliers"]))
    col4.metric("Permit 已过期", permit_expired, delta_color="inverse")

    st.markdown("---")
    st.subheader("⚠️ 提醒事项 (Alerts)")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Permit ≤ 90 天", permit_90)
    c2.metric("Permit ≤ 60 天 (紧急)", permit_60, delta_color="inverse")
    c3.metric("Passport 到期提醒", passport_renew)
    c4.metric("Contract 到期提醒", contract_renew)

elif menu == "顾客资料 (Customer)":
    st.title("👤 顾客资料管理")
    tab1, tab2 = st.tabs(["查看/修改顾客", "新增顾客"])
    
    with tab1:
        if not db["customers"]:
            st.info("暂无顾客资料")
        else:
            cust_names = [f"{c['name']} ({c['ic']})" for c in db["customers"]]
            selected_cust = st.selectbox("选择要修改的顾客", cust_names)
            idx = cust_names.index(selected_cust)
            c = db["customers"][idx]
            
            with st.form(f"edit_cust_{idx}"):
                name = st.text_input("Name", c.get("name", ""))
                ic = st.text_input("IC", c.get("ic", ""))
                phone = st.text_input("Phone / WhatsApp", c.get("phone", ""))
                email = st.text_input("Email", c.get("email", ""))
                occupation = st.text_input("Occupation", c.get("occupation", ""))
                monthly_income = st.text_input("Monthly Income", c.get("monthly_income", ""))
                
                marital_status = st.selectbox("Marital Status", ["Married", "Single", "Divorced", "Widowed"], index=["Married", "Single", "Divorced", "Widowed"].index(c.get("marital_status", "Single")))
                
                spouse_name, spouse_ic = "", ""
                if marital_status == "Married":
                    spouse_name = st.text_input("Spouse Name", c.get("spouse_name", ""))
                    spouse_ic = st.text_input("Spouse IC", c.get("spouse_ic", ""))
                
                address = st.text_area("Address", c.get("address", ""))
                state = st.text_input("State", c.get("state", ""))
                postcode = st.text_input("Postcode", c.get("postcode", ""))
                children = st.text_input("Children", c.get("children", ""))
                children_ages = st.text_input("Children Ages", c.get("children_ages", ""))
                elderly = st.text_input("Elderly", c.get("elderly", ""))
                purpose = st.selectbox("Application Purpose", ["take care children", "take care elderly", "other"], index=["take care children", "take care elderly", "other"].index(c.get("purpose", "take care children")))
                
                col_u, col_d = st.columns(2)
                if col_u.form_submit_button("更新资料"):
                    db["customers"][idx].update({
                        "name": name, "ic": ic, "phone": phone, "email": email,
                        "occupation": occupation, "monthly_income": monthly_income,
                        "marital_status": marital_status, "spouse_name": spouse_name,
                        "spouse_ic": spouse_ic, "address": address, "state": state,
                        "postcode": postcode, "children": children, "children_ages": children_ages,
                        "elderly": elderly, "purpose": purpose
                    })
                    save_data(db)
                    st.success("顾客资料更新成功！")
                    st.rerun()
                if col_d.form_submit_button("删除顾客"):
                    db["customers"].pop(idx)
                    save_data(db)
                    st.success("顾客已删除！")
                    st.rerun()

    with tab2:
        with st.form("add_customer_form"):
            st.subheader("新增顾客")
            n_name = st.text_input("Name")
            n_ic = st.text_input("IC")
            n_phone = st.text_input("Phone / WhatsApp")
            n_email = st.text_input("Email")
            n_occ = st.text_input("Occupation")
            n_inc = st.text_input("Monthly Income")
            n_mar = st.selectbox("Marital Status", ["Married", "Single", "Divorced", "Widowed"])
            n_sname, n_sic = "", ""
            if n_mar == "Married":
                n_sname = st.text_input("Spouse Name")
                n_sic = st.text_input("Spouse IC")
            n_addr = st.text_area("Address")
            n_state = st.text_input("State")
            n_post = st.text_input("Postcode")
            n_child = st.text_input("Children")
            n_cages = st.text_input("Children Ages")
            n_eld = st.text_input("Elderly")
            n_pur = st.selectbox("Application Purpose", ["take care children", "take care elderly", "other"])
            
            if st.form_submit_button("保存新顾客"):
                db["customers"].append({
                    "id": f"C{len(db['customers'])+1:03d}", "name": n_name, "ic": n_ic,
                    "phone": n_phone, "email": n_email, "occupation": n_occ, "monthly_income": n_inc,
                    "marital_status": n_mar, "spouse_name": n_sname, "spouse_ic": n_sic,
                    "address": n_addr, "state": n_state, "postcode": n_post,
                    "children": n_child, "children_ages": n_cages, "elderly": n_eld, "purpose": n_pur
                })
                save_data(db)
                st.success("添加成功！")
                st.rerun()

elif menu == "女佣资料 (Maid)":
    st.title("👩‍maid 女佣资料管理")
    tab1, tab2 = st.tabs(["查看/更新女佣", "新增女佣"])
    
    with tab1:
        if not db["maids"]:
            st.info("暂无女佣资料")
        else:
            maid_names = [f"{m['name']} ({m['passport_no']})" for m in db["maids"]]
            sel_m = st.selectbox("选择女佣", maid_names)
            midx = maid_names.index(sel_m)
            m = db["maids"][midx]
            
            with st.form(f"edit_maid_{midx}"):
                name = st.text_input("Name", m.get("name", ""))
                gender = st.selectbox("Gender", ["Female", "Male"], index=0 if m.get("gender","Female")=="Female" else 1)
                dob = st.text_input("DOB (YYYY-MM-DD)", m.get("dob", ""))
                pob = st.text_input("Place of Birth", m.get("pob", ""))
                nationality = st.text_input("Nationality", m.get("nationality", "Indonesia"))
                religion = st.text_input("Religion", m.get("religion", ""))
                marital_status = st.selectbox("Marital Status", ["Single", "Married", "Divorced", "Widowed"])
                occupation = st.text_input("Occupation", m.get("occupation", ""))
                phone = st.text_input("Phone", m.get("phone", ""))
                passport_no = st.text_input("Passport No.", m.get("passport_no", ""))
                passport_issue = st.text_input("Passport Issue Date", m.get("passport_issue", ""))
                passport_expiry = st.text_input("Passport Expiry", m.get("passport_expiry", ""))
                overseas_address = st.text_area("Overseas Address", m.get("overseas_address", ""))
                
                arrival_date = st.text_input("Arrival Date (YYYY-MM-DD - 抵达大马日期，空则未到)", m.get("arrival_date", ""))
                permit_no, permit_expiry = "", ""
                if arrival_date.strip() != "":
                    st.info("✅ 女佣已抵达大马，可维护 Permit 信息：")
                    permit_no = st.text_input("Permit No.", m.get("permit_no", ""))
                    permit_expiry = st.text_input("Permit Expiry (YYYY-MM-DD)", m.get("permit_expiry", ""))
                else:
                    st.warning("⚠️ 暂无 Arrival Date，Permit 栏目隐藏。")
                
                contract_start = st.text_input("Contract Start", m.get("contract_start", ""))
                contract_expiry = st.text_input("Contract Expiry", m.get("contract_expiry", ""))
                skills = st.text_area("Skills / Preference", m.get("skills", ""))
                
                col_u, col_d = st.columns(2)
                if col_u.form_submit_button("更新女佣资料"):
                    db["maids"][midx].update({
                        "name": name, "gender": gender, "dob": dob, "pob": pob,
                        "nationality": nationality, "religion": religion, "marital_status": marital_status,
                        "occupation": occupation, "phone": phone, "passport_no": passport_no,
                        "passport_issue": passport_issue, "passport_expiry": passport_expiry,
                        "overseas_address": overseas_address, "arrival_date": arrival_date,
                        "permit_no": permit_no, "permit_expiry": permit_expiry,
                        "contract_start": contract_start, "contract_expiry": contract_expiry, "skills": skills
                    })
                    save_data(db)
                    st.success("女佣资料更新成功！")
                    st.rerun()
                if col_d.form_submit_button("删除女佣"):
                    db["maids"].pop(midx)
                    save_data(db)
                    st.success("已删除女佣")
                    st.rerun()

    with tab2:
        with st.form("add_maid_form"):
            st.subheader("新增女佣")
            an_name = st.text_input("Name")
            an_pno = st.text_input("Passport No.")
            an_dob = st.text_input("DOB (YYYY-MM-DD)")
            an_nat = st.text_input("Nationality", value="Indonesia")
            an_arr = st.text_input("Arrival Date (留空代表未到马)")
            
            if st.form_submit_button("保存女佣"):
                db["maids"].append({
                    "id": f"M{len(db['maids'])+1:03d}", "name": an_name, "passport_no": an_pno,
                    "dob": an_dob, "nationality": an_nat, "arrival_date": an_arr, "permit_no": "", "permit_expiry": ""
                })
                save_data(db)
                st.success("女佣添加成功！")
                st.rerun()

elif menu == "Supplier 供应商":
    st.title("🏢 印尼供应商 (Supplier P3MI) 管理")
    if not db["suppliers"]: db["suppliers"] = []
    for i, sup in enumerate(db["suppliers"]):
        with st.expander(f"{sup.get('company_name')} (SIP3MI: {sup.get('sip3mi')})"):
            with st.form(f"sup_{i}"):
                cname = st.text_input("Supplier Company Name", sup.get("company_name", ""))
                sip3mi = st.text_input("No. SIP3MI", sup.get("sip3mi", ""))
                dname = st.text_input("Director Name", sup.get("director_name", ""))
                did = st.text_input("Director ID / KTP", sup.get("director_id", ""))
                addr = st.text_area("Address", sup.get("address", ""))
                tel = st.text_input("Telephone", sup.get("phone", ""))
                email = st.text_input("Email", sup.get("email", ""))
                if st.form_submit_button("保存修改"):
                    db["suppliers"][i] = {
                        "id": sup["id"], "company_name": cname, "sip3mi": sip3mi,
                        "director_name": dname, "director_id": did, "address": addr, "phone": tel, "email": email
                    }
                    save_data(db)
                    st.success("供应商信息已更新")
                    st.rerun()
    st.markdown("---")
    with st.form("add_supplier"):
        st.subheader("新增供应商")
        nx_name = st.text_input("Company Name")
        nx_sip = st.text_input("No. SIP3MI")
        if st.form_submit_button("添加供应商"):
            db["suppliers"].append({"id": f"S{len(db['suppliers'])+1:03d}", "company_name": nx_name, "sip3mi": nx_sip})
            save_data(db)
            st.success("添加成功！")
            st.rerun()

elif menu == "Agency Details 公司资料":
    st.title("🏛️ 本公司中介资料设置")
    ag = db["agency"]
    with st.form("agency_form"):
        name = st.text_input("Agency Name", ag.get("name", ""))
        director = st.text_input("Director Name", ag.get("director", ""))
        ic = st.text_input("Director IC", ag.get("ic", ""))
        license_no = st.text_input("License / Registration No.", ag.get("license", ""))
        address = st.text_area("Address", ag.get("address", ""))
        phone = st.text_input("Telephone", ag.get("phone", ""))
        email = st.text_input("Email", ag.get("email", ""))
        if st.form_submit_button("更新公司资料"):
            db["agency"] = {"name": name, "director": director, "ic": ic, "license": license_no, "address": address, "phone": phone, "email": email}
            save_data(db)
            st.success("公司资料已更新！")
            st.rerun()

elif menu == "申请文件与生成 (Application)":
    st.title("📄 申请文件自动生成中心")
    if not db["customers"] or not db["maids"] or not db["suppliers"]:
        st.warning("请确保系统中至少存在一个【顾客】、【女佣】和【Supplier】。")
    else:
        sel_c = st.selectbox("1. 选择顾客 (Customer)", [f"{c['name']} — {c['ic']}" for c in db["customers"]])
        sel_m = st.selectbox("2. 选择女佣 (Maid)", [f"{m['name']} — {m['passport_no']}" for m in db["maids"]])
        sel_s = st.selectbox("3. 选择 Supplier", [s['company_name'] for s in db["suppliers"]])
        st.markdown("---")
        
        documents = [("PRA 1", 1), ("IM.12", 1), ("IM.38", 1), ("Personal Bond", 1), ("Contract of Employment", 5), ("EC New Contract", 17), ("Surat Wakil Majikan", 1), ("Letter of Guarantee", 2), ("Agency Agreement", 1)]
        for doc_name, pages in documents:
            c1, c2, c3 = st.columns([3, 2, 2])
            c1.markdown(f"**{doc_name}** (页数: {pages} 页)")
            if c2.button(f"生成 PDF", key=f"gen_{doc_name}"):
                pdf_filename = f"{doc_name.replace(' ', '_')}_Filled.pdf"
                pdf = canvas.Canvas(pdf_filename, pagesize=A4)
                pdf.drawString(100, 800, f"Generated: {doc_name}")
                pdf.drawString(100, 770, f"Customer: {sel_c}")
                pdf.drawString(100, 740, f"Maid: {sel_m}")
                pdf.drawString(100, 710, f"Supplier: {sel_s}")
                pdf.save()
                st.success(f"已生成: {pdf_filename}")
            c3.write("✅ 就绪")

elif menu == "数据备份与恢复 (Backup)":
    st.title("💾 数据备份与恢复")
    st.write("随时导出完整的 JSON 备份，防止换手机或浏览器导致资料丢失。")
    st.download_button("📥 导出全部资料备份 (.json)", data=json.dumps(db, ensure_ascii=False, indent=4), file_name="maid_system_backup.json", mime="application/json")
    st.markdown("---")
    uploaded = st.file_uploader("上传备份 JSON 文件以恢复", type=["json"])
    if uploaded:
        try:
            save_data(json.load(uploaded))
            st.success("数据恢复成功！请刷新页面。")
        except Exception as e:
            st.error(f"恢复失败: {e}")
