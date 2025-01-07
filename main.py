import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io

# Judul Aplikasi
st.title("Web untuk Menambahkan Watermark ke Gambar")

# Path gambar watermark (yang sudah ada)
watermark_image_path = "miyabi.jpg"

# Ukuran watermark gambar
watermark_size = (350, 350)

# Kolom untuk watermark
col1, col2 = st.columns(2)

# Kolom Kiri: Watermark Gambar
with col1:
    st.header("Watermark Gambar")
    uploaded_image = st.file_uploader("Upload gambar untuk watermark gambar:", type=["png", "jpg", "jpeg"], key="image_upload")
    if uploaded_image:
        # Buka gambar utama yang diupload (background image)
        main_image = Image.open(uploaded_image).convert("RGBA")
        
        # Tampilkan gambar utama
        st.image(main_image, caption="Gambar Utama yang Diupload", use_container_width=True)

        # Buka gambar watermark (yang sudah ada)
        watermark = Image.open(watermark_image_path).convert("RGBA")
        
        # Sesuaikan ukuran watermark
        watermark.thumbnail(watermark_size)
        
        # Buat transparansi pada watermark
        alpha = 0.7  # Opacity 70%
        watermark_with_alpha = Image.new("RGBA", watermark.size)
        for x in range(watermark.width):
            for y in range(watermark.height):
                r, g, b, a = watermark.getpixel((x, y))
                watermark_with_alpha.putpixel((x, y), (r, g, b, int(a * alpha)))
        
        # Salin gambar utama yang diupload dan tambahkan watermark di posisi tertentu
        copied_image = main_image.copy()
        position = (main_image.width - watermark.width - 10, main_image.height - watermark.height - 10)  # Posisi watermark (x, y)
        copied_image.paste(watermark_with_alpha, position, watermark_with_alpha)
        
        # Tampilkan hasil gambar dengan watermark
        st.image(copied_image, caption="Gambar dengan Watermark Gambar", use_container_width=True)
        
        # Tombol untuk mengunduh hasil gambar
        buffered = io.BytesIO()
        copied_image.save(buffered, format="PNG")
        st.download_button(
            "Download Gambar Hasil (Watermark Gambar)",
            data=buffered.getvalue(),
            file_name="hasil_watermark_gambar.png",
            mime="image/png",
        )

# Kolom Kanan: Watermark Teks
with col2:
    st.header("Watermark Teks")
    uploaded_image_text = st.file_uploader("Upload gambar untuk watermark teks:", type=["png", "jpg", "jpeg"], key="text_upload")
    if uploaded_image_text:
        # Buka gambar utama yang diupload (background image)
        main_image_text = Image.open(uploaded_image_text).convert("RGBA")
        
        # Tampilkan gambar utama
        st.image(main_image_text, caption="Gambar Utama yang Diupload", use_container_width=True)
        
        # Teks watermark default
        watermark_text = "MNC TV"  # Teks yang sudah ditentukan
        
        # Salin gambar utama yang diupload
        copied_image_text = main_image_text.copy()
        draw = ImageDraw.Draw(copied_image_text)
        
        # Tentukan font dan ukuran teks yang lebih besar
        font_size = 80  # Ukuran font tetap
        font = ImageFont.truetype("arial.ttf", font_size)
        
        # Hitung bounding box untuk teks
        bbox = draw.textbbox((0, 0), watermark_text, font=font)
        text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]
        
        # Tentukan posisi watermark di kanan bawah dengan margin
        margin = 20  # Margin dari sisi gambar
        position_text = (copied_image_text.width - text_width - margin, copied_image_text.height - text_height - margin)

        border_offset = 2  # Offset untuk border
        # Menggambar border teks dengan satu posisi offset
        draw.text((position_text[0]-border_offset, position_text[1]-border_offset), watermark_text, font=font, fill=(0, 0, 0))  # Border hitam
        
        # Tambahkan teks watermark dengan warna putih di atas border
        draw.text(position_text, watermark_text, font=font, fill=(255, 255, 255, 128))

        # Tambahkan teks watermark dengan ukuran font lebih besar
        draw.text(position_text, watermark_text, font=font, fill=(255, 255, 255, 128))

        # Tampilkan hasil gambar dengan watermark teks
        st.image(copied_image_text, caption="Gambar dengan Watermark Teks", use_container_width=True)
        
        # Tombol untuk mengunduh hasil gambar
        buffered_text = io.BytesIO()
        copied_image_text.save(buffered_text, format="PNG")
        st.download_button(
            "Download Gambar Hasil (Watermark Teks)",
            data=buffered_text.getvalue(),
            file_name="hasil_watermark_teks.png",
            mime="image/png",
        )
