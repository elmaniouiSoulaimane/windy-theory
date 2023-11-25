SOURCES = [
    'Desktop',
    'Documents',
    'Downloads'
]
DESTINATIONS = [
    'videos',
    'audios',
    'archives',
    'programs',
    'documents',
    'images',
    'folders',
    'other'
]

SYS_DIRS = [
    'bin',
    'sbin',
    'lib',
    'usr'
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