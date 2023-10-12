import os
import zipfile
from concurrent.futures import ThreadPoolExecutor
import argparse

#    Mod Zipper

#    Script to zip mods in mod directory. Tool for modders to make releasing mods easier
#
#    @author: 	[LSFM] Bone2510
#    @date: 	12.10.20233
#    @version:	1.0
#
#    History:	v1.0 @12.10.2023 - Initial implementation
#    --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Funktion, um zu überprüfen, ob eine modDesc.xml-Datei im Verzeichnis existiert
def check_moddesc_exists(subdirectory):
    moddesc_path = os.path.join(subdirectory, "modDesc.xml")
    return os.path.isfile(moddesc_path)

# Funktion, um ein Verzeichnis zu zippen
def zip_directory(source_directory, zip_filename):
    with zipfile.ZipFile(source_directory + ".zip", "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(source_directory):
            if not any(root.startswith(os.path.join(source_directory, x)) for x in ['.'] + [f for f in os.listdir(source_directory) if f.startswith('.')]):
                for file in files:
                    if not file.endswith(('.code-workspace', '.zip')) and not file.startswith('.'):
                        file_path = os.path.join(root, file)
                        archive_name = os.path.relpath(file_path, source_directory)
                        zipf.write(file_path, archive_name)

# Hauptfunktion zum Verarbeiten der ZIP-Vorgänge asynchron
def process_zipping(source_directory, dir_prefix, to_ignore):
    # Alle Ordner im aktuellen Verzeichnis auflisten
    directories = [d for d in os.listdir(source_directory) if os.path.isdir(os.path.join(source_directory, d))]

    # Filtern nach dem Präfix und modDesc.xml überprüfen
    valid_directories = [d for d in directories if d.startswith(dir_prefix) and check_moddesc_exists(os.path.join(source_directory, d))]

    if not valid_directories:
        print("No valid mod directories found. Quitting...")
        return

    print(f"Valid mod directories found: {valid_directories}")

    with ThreadPoolExecutor(max_workers=5) as executor:
        for directory in valid_directories:
            sub_dir = os.path.join(source_directory, directory)
            print(f"Queuing ZIP operation for directory: {sub_dir}")
            executor.submit(zip_directory, sub_dir, directory)

if __name__ == '__main__':
    is_valid_path = lambda path: os.path.exists(path)
    parser = argparse.ArgumentParser(description="Mod Zipper v1.0 by [LSFM] Bone2510")
    parser.add_argument("--path", help="Path to the working directory", default=os.getcwd())
    args = parser.parse_args()

    if not is_valid_path(args.path):
        print("Error: Entered path does not exist")

    if args.path.endswith("/") or args.path.endswith("\\"):
        args.path = args.path[:-1]

    working_directory = args.path  # Verwenden Sie den angegebenen Pfad oder das aktuelle Arbeitsverzeichnis
    dir_prefix = input("Enter Directory Prefix: ")
    to_ignore = set(['.code-workspace', '.zip'])

    process_zipping(working_directory, dir_prefix, to_ignore)

