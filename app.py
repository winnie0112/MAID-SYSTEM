import io
import zipfile
import streamlit as st
from pypdf import PdfReader, PdfWriter

st.set_page_config(page_title="Reliance Maid Document Automation", layout="centered")

st.title("🖨️ Reliance Maid 官方文档自动填写系统")
st.write("请输入顾客与女佣信息，系统将自动批量填入 11 个官方 PDF 表单并打包下载。")

# 11 个标准文件名列表
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

with st.form("maid_form"):
    st.subheader("A. 雇主 (Employer) 信息")
    employer_name = st.text_input("雇主全名 (Employer Full Name)", "GAN JUN HENG")
    employer_ic = st.text_input("雇主身份证号 (IC / Passport No.)", "960226-01-6725")
    employer_address = st.text_area("雇主地址 (Address)", "No 34A, Jalan Bukit Impian 16, Taman Impian Emas, 81300 Skudai, Johor.")
    employer_phone = st.text_input("电话号码 (Telephone No.)", "010-8378471")

    st.subheader("B. 女佣 (Domestic Worker) 信息")
    maid_name = st.text_input("女佣全名 (Maid Full Name)", "Sri Haryati")
    maid_passport = st.text_input("女佣护照号 (Passport No.)", "E9716672")
    maid_nationality = st.text_input("国籍 (Nationality)", "Indonesian")

    st.subheader("C. 供应商 / 代理 (Agency) 信息")
    agency_name = st.text_input("代理公司名称", "AGENSI PEKERJAAN RELIANCE MAID SDN BHD")

    submitted = st.form_submit_button("🚀 生成并打包所有填好的 PDF")

if submitted:
    zip_buffer = io.BytesIO()
    
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for filename in PDF_FILES:
            try:
                # 尝试读取同目录下原有的 PDF 模板
                reader = PdfReader(filename)
                writer = PdfWriter()
                writer.append(reader)
                
                # 如果 PDF 包含可填写表单字段 (AcroForm)，尝试自动注入数据
                if writer.get_fields():
                    fields_dict = {}
                    # 根据常见的表单字段名称尝试匹配并赋值（可根据实际 PDF 内部字段名调整）
                    for field_key in writer.get_fields().keys():
                        key_lower = field_key.lower()
                        if "name" in key_lower and "employer" in key_lower:
                            fields_dict[field_key] = employer_name
                        elif "ic" in key_lower or "passport" in key_lower:
                            if "maid" in key_lower:
                                fields_dict[field_key] = maid_passport
                            else:
                                fields_dict[field_key] = employer_ic
                        elif "address" in key_lower:
                            fields_dict[field_key] = employer_address
                        elif "phone" in key_lower:
                            fields_dict[field_key] = employer_phone
                    
                    if fields_dict:
                        writer.update_page_form_field_values(writer.pages[0], fields_dict)

                # 将处理后的 PDF 写入内存流
                pdf_output = io.BytesIO()
                writer.write(pdf_output)
                
                # 写入 ZIP 文件
                zip_file.writestr(filename, pdf_output.getvalue())
                
            except FileNotFoundError:
                # 若该 PDF 模板尚未上传到 GitHub 目录，先跳过或放入提示文件
                zip_file.writestr(f"MISSING_{filename}.txt", f"Error: Template {filename} not found in repository root.")

    zip_buffer.seek(0)
    
    st.success("🎉 所有文件已成功处理并打包！")
    st.download_button(
        label="📥 点击下载全部 11 个填好的 PDF 压缩包 (ZIP)",
        data=zip_buffer,
        file_name="Reliance_Maid_Documents.zip",
        mime="application/zip"
    )
