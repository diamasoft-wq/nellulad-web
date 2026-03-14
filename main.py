import streamlit as st
import os
import img2pdf
import pytesseract
import subprocess
from PIL import Image
from PyPDF2 import PdfMerger
from pdf2docx import Converter
import tempfile

# --- CONFIGURACIÓN ESTÉTICA (CSS) ---
st.set_page_config(page_title="Nellulad Studio", page_icon="🌸", layout="centered")

st.markdown("""
    <style>
    /* Fondo principal y textos */
    .stApp {
        background-color: #FFF0F5;
    }
    h1, h2, h3 {
        color: #D87093 !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .stButton>button {
        background-color: #FFB6C1;
        color: white;
        border-radius: 20px;
        border: none;
        padding: 10px 25px;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #DB7093;
        color: white;
        transform: scale(1.05);
    }
    /* Estilo de las cajas de subida */
    .stFileUploader {
        border: 2px dashed #FFC0CB;
        border-radius: 15px;
        padding: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- TÍTULO CREATIVO ---
st.markdown("<h1 style='text-align: center; margin-bottom: 0;'>🌸 Nellulad 🌸</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; margin-top: 0; color: #DB7093;'>CONVERTIDOR</h2>", unsafe_allow_html=True)
st.write("---")

# --- FUNCIONES DE APOYO ---
def save_temp(uploaded_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp:
        tmp.write(uploaded_file.getvalue())
        return tmp.name

# --- MENÚ DE NAVEGACIÓN ---
opcion = st.sidebar.radio(
    "🎀 Herramientas",
    ["📄 Word a PDF", "📘 PDF a Word", "🖼️ Imagen a PDF", "🔗 Unir PDFs", "🔍 Extraer Texto (OCR)"]
)

# --- LÓGICA DE LAS FUNCIONES ---

if opcion == "📄 Word a PDF":
    st.subheader("Convertir Word (.docx) a PDF")
    archivo = st.file_uploader("Elige tu documento Word", type=['docx'])
    if archivo and st.button("✨ ¡Convertir a PDF!"):
        with st.spinner("Haciendo magia rosa..."):
            word_path = save_temp(archivo)
            try:
                subprocess.run(['lowriter', '--headless', '--convert-to', 'pdf', '--outdir', os.path.dirname(word_path), word_path], check=True)
                pdf_path = os.path.splitext(word_path)[0] + ".pdf"
                with open(pdf_path, "rb") as f:
                    st.download_button("💖 Descargar mi PDF", data=f, file_name="convertido_por_nellulad.pdf")
            except Exception as e:
                st.error("¡Ups! Asegúrate de que el servidor tenga LibreOffice instalado.")

elif opcion == "📘 PDF a Word":
    st.subheader("Convertir PDF a Word")
    archivo = st.file_uploader("Sube tu PDF", type=['pdf'])
    if archivo and st.button("✨ ¡Convertir a Word!"):
        with st.spinner("Transformando archivo..."):
            pdf_path = save_temp(archivo)
            word_path = pdf_path.replace(".pdf", ".docx")
            cv = Converter(pdf_path)
            cv.convert(word_path); cv.close()
            with open(word_path, "rb") as f:
                st.download_button("💖 Descargar mi Word", data=f, file_name="convertido_por_nellulad.docx")

elif opcion == "🖼️ Imagen a PDF":
    st.subheader("Convertir Fotos a PDF")
    archivos = st.file_uploader("Sube tus imágenes", type=['png', 'jpg', 'jpeg'], accept_multiple_files=True)
    if archivos and st.button("✨ Crear PDF"):
        rutas = [save_temp(a) for a in archivos]
        pdf_bytes = img2pdf.convert(rutas)
        st.download_button("💖 Descargar PDF", data=pdf_bytes, file_name="fotos_nellulad.pdf")

elif opcion == "🔗 Unir PDFs":
    st.subheader("Juntar varios PDFs en uno")
    archivos = st.file_uploader("Selecciona los archivos", type=['pdf'], accept_multiple_files=True)
    if archivos and len(archivos) > 1 and st.button("✨ Unir archivos"):
        merger = PdfMerger()
        for a in archivos: merger.append(a)
        output = "final.pdf"
        merger.write(output)
        with open(output, "rb") as f:
            st.download_button("💖 Descargar PDF Unido", data=f, file_name="unido_nellulad.pdf")
        merger.close()

elif opcion == "🔍 Extraer Texto (OCR)":
    st.subheader("Leer texto de una imagen")
    archivo = st.file_uploader("Sube la foto con texto", type=['png', 'jpg', 'jpeg'])
    if archivo:
        img = Image.open(archivo)
        st.image(img, use_container_width=True)
        if st.button("✨ Leer texto"):
            texto = pytesseract.image_to_string(img, lang='spa')
            st.text_area("Aquí tienes el texto:", texto, height=250)
            st.download_button("💖 Guardar como .txt", data=texto, file_name="texto_nellulad.txt")

st.sidebar.markdown("---")
st.sidebar.write("🌸 Hecho con amor para Nelly, Luna y Lady")