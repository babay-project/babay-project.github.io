import zlib
import os
import sys
import subprocess
import platform
import json  # Tambahan modul untuk merapikan teks

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def buka_di_notepad(path_file):
    """Membuka file text secara otomatis sesuai OS"""
    if platform.system() == 'Windows':
        os.startfile(path_file)
    elif platform.system() == 'Darwin':
        subprocess.call(('open', path_file))
    else:
        subprocess.call(('xdg-open', path_file))

def main():
    clear_screen()
    print("==========================================")
    print("    TOOL BONGKAR PASANG BIN (AUTO RAPI)   ")
    print("==========================================")

    target_file = input("Masukkan nama file .bin: ").strip().replace('"', '')

    if not os.path.exists(target_file):
        print(f"\n[!] Error: File '{target_file}' tidak ditemukan.")
        input("Tekan Enter untuk keluar...")
        return

    header_data = b""
    mode_alternatif = False
    file_txt_edit = target_file + ".txt"

    # ---------------------------------------------------------
    # TAHAP 1: BONGKAR (DEKOMPRESI & RAPIDKAN)
    # ---------------------------------------------------------
    print(f"\n[1/3] Sedang membongkar & merapikan {target_file}...")

    try:
        with open(target_file, "rb") as f:
            data_mentah = f.read()

        data_bytes = None

        # Coba metode standar
        try:
            data_bytes = zlib.decompress(data_mentah)
        except:
            # Coba metode skip 4 byte
            try:
                header_data = data_mentah[:4]
                data_bytes = zlib.decompress(data_mentah[4:])
                mode_alternatif = True
                print(" -> Mode Alternatif (Header 4 bytes disimpan).")
            except Exception as e:
                print(f"[!] GAGAL membongkar. Error: {e}")
                input("Tekan Enter untuk keluar...")
                return

        # --- PROSES MERAPIKAN (PRETTY PRINT) ---
        try:
            # Ubah bytes jadi string
            text_content = data_bytes.decode('utf-8')
            # Coba baca sebagai JSON
            json_obj = json.loads(text_content)
            # Tulis ulang dengan indentasi (agar rapi ke bawah)
            content_final = json.dumps(json_obj, indent=4)
            print(" -> Berhasil merapikan format JSON (Auto-Indent).")
        except:
            # Jika bukan JSON, biarkan apa adanya
            print(" -> Bukan format JSON, menulis raw text.")
            content_final = data_bytes.decode('utf-8', errors='ignore')

        # Simpan ke TXT
        with open(file_txt_edit, "w", encoding='utf-8') as f_out:
            f_out.write(content_final)
            
        print(f" -> File siap edit: {file_txt_edit}")

    except Exception as e:
        print(f"[!] Error sistem: {e}")
        return

    # ---------------------------------------------------------
    # TAHAP 2: EDITING
    # ---------------------------------------------------------
    print(f"\n[2/3] Membuka Notepad...")
    buka_di_notepad(file_txt_edit)
    
    print("-" * 50)
    print("FILE SUDAH RAPI. SILAKAN EDIT.")
    print("Jangan lupa SAVE di Notepad sebelum lanjut.")
    print("-" * 50)
    
    while True:
        konfirmasi = input("Ketik 'y' jika sudah selesai edit & save: ").lower()
        if konfirmasi == 'y':
            break

    # ---------------------------------------------------------
    # TAHAP 3: BUNGKUS (MINIFY & KOMPRESI)
    # ---------------------------------------------------------
    print(f"\n[3/3] Sedang memadatkan & membungkus...")

    try:
        # Baca file TXT
        with open(file_txt_edit, "r", encoding='utf-8') as f:
            text_edit = f.read()

        # --- PROSES MEMADATKAN KEMBALI (MINIFY) ---
        try:
            # Kita load lagi sebagai JSON
            json_obj = json.loads(text_edit)
            # Kita dump TANPA spasi (separators) agar kembali jadi 1 baris
            # Ini penting agar ukuran file kecil dan game tidak error membaca spasi aneh
            data_siap_kompres = json.dumps(json_obj, separators=(',', ':')).encode('utf-8')
            print(" -> JSON berhasil dipadatkan kembali (Minified).")
        except:
            print(" -> Gagal memadatkan JSON (mungkin error sintaks), menggunakan raw text.")
            data_siap_kompres = text_edit.encode('utf-8')

        # Kompresi Zlib
        data_kompres = zlib.compress(data_siap_kompres, level=9)

        nama_output = "NEW_" + target_file

        with open(nama_output, "wb") as f_out:
            if mode_alternatif:
                f_out.write(header_data)
            f_out.write(data_kompres)

        print(f"\n[SUKSES] File baru: {nama_output}")
        print("Silakan rename dan copy ke folder game.")
        
        # Hapus file sisa
        if input("\nHapus file .txt sisa? (y/n): ").lower() == 'y':
            os.remove(file_txt_edit)

    except Exception as e:
        print(f"[!] Gagal membungkus: {e}")
        print("Cek apakah kamu salah hapus tanda koma/kurung kurawal di JSON.")

    input("\nTekan Enter untuk keluar...")

if __name__ == "__main__":
    main()