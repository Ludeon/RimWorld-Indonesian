import os
import xml.etree.ElementTree as ET
from langdetect import detect, DetectorFactory
DetectorFactory.seed = 0

# Folder tempat DefInjected berada
target_folder = os.path.join("Indonesian", "DefInjected")

# Lokasi file progress
progress_file = "PROGRESS.md"

translated_files = []
untranslated_files = []

def is_translated(texts):
    for text in texts:
        try:
            if detect(text.strip()) == 'id':
                return True
        except:
            continue
    return False

def contains_skip_translation(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
            return "<!-- SKIP_TRANSLATION -->" in content
    except:
        return False

def get_all_texts_from_xml(filepath):
    try:
        tree = ET.parse(filepath)
        root = tree.getroot()
        return [elem.text for elem in root.iter() if elem.text]
    except Exception as e:
        # Coba baca manual jika XML tidak valid
        texts = []
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                for line in file:
                    line = line.strip()
                    if line.startswith("<") and ">" in line and not line.startswith("<?"):
                        content = line.split(">", 1)[-1].rsplit("<", 1)[0].strip()
                        if content:
                            texts.append(content)
            return texts
        except:
            return []

# Ambil semua file .xml dari target_folder
xml_files = []
for root, dirs, files in os.walk(target_folder):
    for file in files:
        if file.endswith(".xml"):
            full_path = os.path.join(root, file)
            xml_files.append(full_path)

# Proses file
for file_path in xml_files:
    if contains_skip_translation(file_path):
        translated_files.append(file_path)
    else:
        texts = get_all_texts_from_xml(file_path)
        if is_translated(texts):
            translated_files.append(file_path)
        else:
            untranslated_files.append(file_path)

# Hitung persentase
total_files = len(xml_files)
translated_count = len(translated_files)
percentage = (translated_count / total_files) * 100 if total_files else 0

# Tulis ke PROGRESS.md
with open(progress_file, "w", encoding="utf-8") as f:
    f.write("# 📊 Progress Penerjemahan DefInjected\n\n")
    f.write(f"**Selesai:** {translated_count} / {total_files} file\n")
    f.write(f"**Progres:** {percentage:.2f}%\n\n")

    for file in sorted(translated_files):
        relative_path = os.path.relpath(file, "Indonesian")
        f.write(f"- [x] {relative_path}\n")

    for file in sorted(untranslated_files):
        relative_path = os.path.relpath(file, "Indonesian")
        f.write(f"- [ ] {relative_path}\n")

print(f"[✓] PROGRESS.md diperbarui. {translated_count}/{total_files} file selesai ({percentage:.2f}%).")