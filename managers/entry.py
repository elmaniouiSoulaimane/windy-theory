import os

class EntryManager:
    DEFAULT_DIRS = [
        'videos',
        'audios',
        'archives',
        'programs',
        'documents',
        'images',
        'folders',
        'other'
    ]

    SOURCES = [
        'Desktop',
        'Documents',
        'Downloads'
    ]


    FILE_TYPES_AND_EXTENSIONS = [
        {
            "type": "videos",
            "extensions": [
                [".mp4", "MPEG-4 Part 14"],
                [".avi", "Audio Video Interleave"],
                [".mkv", "Matroska"],
                [".mov", "QuickTime Movie"],
                [".wmv", "Windows Media Video"],
                [".flv", "Flash Video"],
                [".webm", "WebM"],
                [".m4v", "iTunes Video"],
                [".3gp", "3GPP"],
                [".mpeg", "MPEG-1 or MPEG-2"],
                [".rmvb", "RealMedia Variable Bitrate"],
                [".ogv", "Ogg Video"],
                [".ts", "MPEG-2 Transport Stream"],
                [".m2ts", "Blu-ray BDAV Video"]
            ]
        },
        {
            "type": "archives",
            "extensions": [
                [".zip", "ZIP"],
                [".rar", "RAR"],
                [".7z", "7-Zip"],
                [".tar", "TAR"],
                [".gz", "GZIP"],
                [".bz2", "BZIP2"],
                [".xz", "XZ"],
                [".lzh", "LHA"],
                [".cab", "CAB"],
                [".iso", "ISO"],
                [".dmg", "DMG"],
                [".jar", "JAR"],
                [".cpio", "CPIO"],
                [".arj", "ARJ"],
                [".ace", "ACE"],
                [".lzh", "LZH"],
                [".sit", "StuffIt"],
                [".udf", "UDF"],
                [".gz", "GZ (short for .gzipped)"],
                [".Z", "Z (short for .Z)"],
                [".run", "Self-extracting shell script (Linux/Unix)"]
            ]
        },
        {
            "type": "programs",
            "extensions": [
                [".exe", "Executable files"],
                [".dll", "Dynamic Link Library files"],
                [".so", "Shared Object files (Linux)"],
                [".dylib", "Dynamic Library files (macOS)"],
                [".app", "Application bundle (macOS)"],
                [".msi", "Windows Installer package"],
                [".deb", "Debian package (Linux)"],
                [".rpm", "Red Hat package (Linux)"],
                [".bat", "Batch script (Windows)"],
                [".sh", "Shell script (Linux/Unix)"],
                [".cmd", "Windows Command script"],
                [".ps1", "PowerShell script (Windows)"],
                [".jar", "Java Archive file"],
                [".py", "Python script"],
                [".pl", "Perl script"],
                [".rb", "Ruby script"],
                [".run", "Self-extracting shell script (Linux/Unix)"]
            ]
        },
        {
            "type": "audios",
            "extensions": [
                [".mp3", "MPEG-3 Audio"],
                [".wav", "Waveform Audio File Format"],
                [".flac", "Free Lossless Audio Codec"],
                [".m4a", "MPEG-4 Audio"],
                [".ogg", "Ogg Vorbis"],
                [".aac", "Advanced Audio Coding"],
                [".wma", "Windows Media Audio"],
                [".amr", "Adaptive Multi-Rate audio codec"],
                [".aiff", "Audio Interchange File Format"],
                [".opus", "Opus Audio Codec"]
            ]
        },
        {
            "type": "documents",
            "extensions": [
                [".pdf", "Portable Document Format"],
                [".doc", "Microsoft Word Document"],
                [".docx", "Microsoft Word Open XML Document"],
                [".ppt", "Microsoft PowerPoint Presentation"],
                [".pptx", "Microsoft PowerPoint Open XML Presentation"],
                [".xls", "Microsoft Excel Spreadsheet"],
                [".xlsx", "Microsoft Excel Open XML Spreadsheet"],
                [".odt", "Open Document Text"],
                [".ods", "Open Document Spreadsheet"],
                [".odp", "Open Document Presentation"],
                [".rtf", "Rich Text Format"],
                [".txt", "Plain Text"],
                [".csv", "Comma-Separated Values"],
                [".html", "Hypertext Markup Language"],
                [".xml", "Extensible Markup Language"],
                [".json", "JavaScript Object Notation"]
            ]
        },
        {
            "type": "images",
            "extensions": [
                [".jpg", "JPEG Image"],
                [".png", "Portable Network Graphics"],
                [".gif", "Graphics Interchange Format"],
                [".bmp", "Bitmap Image"],
                [".tiff", "Tagged Image File Format"],
                [".svg", "Scalable Vector Graphics"],
                [".webp", "WebP Image"],
                [".ico", "Icon Image"],
                [".heif", "High Efficiency Image File Format"],
                [".raw", "Raw Image Data"],
                [".jpeg", ""],
                [".fig", ""]
            ]
        }
    ]

    def __init__(self):
        pass

    @staticmethod
    def get_target_dir_paths(target_dir: str) -> list:
        """
        Returns a list of paths to directories that match the given target directory name.

        Args:
            target_dir (str): The name of the target directory.

        Returns:
            list: A list of paths to directories that match the given target directory name.
        """
        found_dirs = list()
        user = os.environ.get('USER')

        for root, dirs, files in os.walk(f'/home/{user}/', topdown=True, onerror=None, followlinks=False):

            # Filter out hidden directories
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            
            # TO DO: This should also check if the typed name string is found in the dir name, not just the exact name,
            # might also add the possibility to type both the name and the dir to look into
            if target_dir in dirs:
                target_dir_path = os.path.join(root, target_dir)
                found_dirs.append(target_dir_path)

        return found_dirs

    @staticmethod
    def make_dir(name):
        new_dir_path = os.path.join(os.getcwd(), name)

        if os.path.exists(new_dir_path):
            return new_dir_path
        else:
            try:
                os.mkdir(new_dir_path)
                return new_dir_path
            except OSError as error:
                print(error)
                return None

    @staticmethod
    def get_exact_type(entry):
        for dict in EntryManager.FILE_TYPES_AND_EXTENSIONS:
            if any(
                    ((extension[0] in entry) or (extension[0].upper() in entry))
                    for extension in dict.get("extensions", [])):
                return dict.get("type")
        return None
    
    @staticmethod
    def get_general_type(entry)-> str:
        if os.path.isfile(entry):
            return "file"
        elif os.path.isdir(entry):
            return "dir"