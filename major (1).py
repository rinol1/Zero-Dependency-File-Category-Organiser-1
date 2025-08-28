import os
import shutil
from pathlib import Path
import mimetypes

class ZeroDependencyFileCategorizer:
    def __init__(self, source_folder, destination_folder):
        self.source_folder = Path(source_folder)
        self.destination_folder = Path(destination_folder)
        
        # File categories based on extensions only
        self.categories = {
            'Documents': ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt', '.pages'],
            'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.svg', '.webp'],
            'Videos': ['.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm', '.mkv'],
            'Audio': ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma'],
            'Code': ['.py', '.js', '.html', '.css', '.java', '.cpp', '.c', '.php', '.rb', '.go', '.json', '.xml'],
            'Archives': ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2'],
            'Spreadsheets': ['.xls', '.xlsx', '.csv', '.ods'],
            'Presentations': ['.ppt', '.pptx', '.odp'],
            'Executables': ['.exe', '.msi', '.deb', '.rpm', '.dmg', '.app']
        }
        
        self.create_category_folders()

    def create_category_folders(self):
        """Create category folders if they don't exist"""
        for category in list(self.categories.keys()) + ['Others']:
            folder_path = self.destination_folder / category
            folder_path.mkdir(parents=True, exist_ok=True)

    def categorize_file(self, file_path):
        """Categorize file based on extension only"""
        file_ext = file_path.suffix.lower()
        
        for category, extensions in self.categories.items():
            if file_ext in extensions:
                return category
        
        return 'Others'

    def smart_rename_if_duplicate(self, destination_path):
        """Rename file if it already exists at destination"""
        if not destination_path.exists():
            return destination_path
        
        counter = 1
        stem = destination_path.stem
        suffix = destination_path.suffix
        parent = destination_path.parent
        
        while destination_path.exists():
            new_name = f"{stem}_{counter}{suffix}"
            destination_path = parent / new_name
            counter += 1
        
        return destination_path

    def process_files(self, move_files=False):
        """Process all files in the source folder"""
        if not self.source_folder.exists():
            print(f"Source folder {self.source_folder} does not exist!")
            return
        
        processed_count = 0
        results = {}
        
        for file_path in self.source_folder.rglob('*'):
            if file_path.is_file():
                try:
                    category = self.categorize_file(file_path)
                    
                    # Create destination path
                    dest_folder = self.destination_folder / category
                    dest_path = dest_folder / file_path.name
                    dest_path = self.smart_rename_if_duplicate(dest_path)
                    
                    # Move or copy file
                    if move_files:
                        shutil.move(str(file_path), str(dest_path))
                        action = "Moved"
                    else:
                        shutil.copy2(str(file_path), str(dest_path))
                        action = "Copied"
                    
                    print(f"{action}: {file_path.name} → {category}/")
                    
                    # Track results
                    if category not in results:
                        results[category] = 0
                    results[category] += 1
                    processed_count += 1
                    
                except Exception as e:
                    print(f"Error processing {file_path.name}: {str(e)}")
        
        print(f"\n--- Categorization Summary ---")
        print(f"Total files processed: {processed_count}")
        for category, count in sorted(results.items()):
            print(f"{category}: {count} files")

def main():
    print("=== Zero-Dependency File Categorizer ===")
    source_folder = input("Enter source folder path: ").strip()
    destination_folder = input("Enter destination folder path: ").strip()
    
    if not source_folder:
        source_folder = "./test_files"
    if not destination_folder:
        destination_folder = "./categorized_files"
    
    move_choice = input("Move files (M) or Copy files (C)? [C]: ").strip().upper()
    move_files = move_choice == 'M'
    
    source_folder = r"C:\Users\User\Downloads"  # Your source folder
    destination_folder = r"C:\Users\User\Documents\categorized"  # Where to put organized files

# Create the categorizer with arguments
    categorizer = ZeroDependencyFileCategorizer(source_folder, destination_folder)

# Process the files
    categorizer.process_files(move_files=move_files)
    
    print("\nCategorization complete!")

if __name__ == "__main__":
    main()