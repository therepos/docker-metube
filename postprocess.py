#!/usr/bin/env python3
import os
import sys
import re
import logging
from pathlib import Path
from mutagen.id3 import ID3, APIC, TIT2, TPE1, TALB, ID3NoHeaderError
from mutagen.mp3 import MP3
from mutagen.flac import FLAC, Picture
from mutagen.mp4 import MP4, MP4Cover
from mutagen.oggvorbis import OggVorbis

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class MusicPostProcessor:
    def __init__(self, cover_path="/app/cover.png"):
        self.cover_path = cover_path
        
    def clean_filename(self, filename):
        """Extract clean title from filename, removing common patterns"""
        # Remove file extension
        name = Path(filename).stem
        
        # Remove common patterns like [Official Video], (Official Audio), etc.
        patterns = [
            r'\[.*?\]',  # Remove [anything]
            r'\(.*?\)',  # Remove (anything)
            r'Official.*',  # Remove Official Video/Audio
            r'HD.*',     # Remove HD quality indicators
            r'4K.*',     # Remove 4K quality indicators
            r'\s*-\s*YouTube.*',  # Remove YouTube suffixes
            r'\s*\|\s*.*',  # Remove | separators and everything after
        ]
        
        for pattern in patterns:
            name = re.sub(pattern, '', name, flags=re.IGNORECASE)
        
        # Clean up extra whitespace
        name = ' '.join(name.split())
        return name.strip()
    
    def parse_filename(self, filename):
        """Parse filename to extract artist, title, and album"""
        clean_name = self.clean_filename(filename)
        
        # Try to split by common separators
        if ' - ' in clean_name:
            parts = clean_name.split(' - ', 1)
            artist = parts[0].strip()
            title = parts[1].strip()
        elif ' by ' in clean_name.lower():
            parts = re.split(r'\s+by\s+', clean_name, 1, flags=re.IGNORECASE)
            title = parts[0].strip()
            artist = parts[1].strip() if len(parts) > 1 else "Unknown Artist"
        else:
            # If no clear separator, use the whole name as title
            artist = "Unknown Artist"
            title = clean_name
        
        # Use title as album if no album is specified
        album = title
        
        return artist, title, album
    
    def load_cover_image(self):
        """Load the cover image"""
        try:
            with open(self.cover_path, 'rb') as f:
                return f.read()
        except Exception as e:
            logger.error(f"Failed to load cover image: {e}")
            return None
    
    def process_mp3(self, file_path, artist, title, album):
        """Process MP3 files"""
        try:
            # Load or create ID3 tags
            try:
                audio = ID3(file_path)
            except ID3NoHeaderError:
                audio = ID3()
            
            # Clear existing tags
            audio.clear()
            
            # Set basic tags
            audio['TIT2'] = TIT2(encoding=3, text=title)
            audio['TPE1'] = TPE1(encoding=3, text=artist)
            audio['TALB'] = TALB(encoding=3, text=album)
            
            # Add cover art
            cover_data = self.load_cover_image()
            if cover_data:
                audio['APIC'] = APIC(
                    encoding=3,
                    mime='image/png',
                    type=3,  # Cover (front)
                    desc='Cover',
                    data=cover_data
                )
            
            # Save tags
            audio.save(file_path)
            logger.info(f"Successfully processed MP3: {file_path}")
            
        except Exception as e:
            logger.error(f"Failed to process MP3 {file_path}: {e}")
    
    def process_flac(self, file_path, artist, title, album):
        """Process FLAC files"""
        try:
            audio = FLAC(file_path)
            
            # Clear existing tags
            audio.clear()
            
            # Set basic tags
            audio['TITLE'] = title
            audio['ARTIST'] = artist
            audio['ALBUM'] = album
            
            # Add cover art
            cover_data = self.load_cover_image()
            if cover_data:
                picture = Picture()
                picture.type = 3  # Cover (front)
                picture.mime = 'image/png'
                picture.desc = 'Cover'
                picture.data = cover_data
                audio.add_picture(picture)
            
            # Save tags
            audio.save()
            logger.info(f"Successfully processed FLAC: {file_path}")
            
        except Exception as e:
            logger.error(f"Failed to process FLAC {file_path}: {e}")
    
    def process_mp4(self, file_path, artist, title, album):
        """Process MP4/M4A files"""
        try:
            audio = MP4(file_path)
            
            # Clear existing tags
            audio.clear()
            
            # Set basic tags
            audio['\xa9nam'] = [title]  # Title
            audio['\xa9ART'] = [artist]  # Artist
            audio['\xa9alb'] = [album]  # Album
            
            # Add cover art
            cover_data = self.load_cover_image()
            if cover_data:
                audio['covr'] = [MP4Cover(cover_data, MP4Cover.FORMAT_PNG)]
            
            # Save tags
            audio.save()
            logger.info(f"Successfully processed MP4: {file_path}")
            
        except Exception as e:
            logger.error(f"Failed to process MP4 {file_path}: {e}")
    
    def process_ogg(self, file_path, artist, title, album):
        """Process OGG files"""
        try:
            audio = OggVorbis(file_path)
            
            # Clear existing tags
            audio.clear()
            
            # Set basic tags
            audio['TITLE'] = title
            audio['ARTIST'] = artist
            audio['ALBUM'] = album
            
            # Note: OGG doesn't support embedded images in the same way
            # You might need additional libraries like mutagen with picture support
            
            # Save tags
            audio.save()
            logger.info(f"Successfully processed OGG: {file_path}")
            
        except Exception as e:
            logger.error(f"Failed to process OGG {file_path}: {e}")
    
    def process_file(self, file_path):
        """Process a single music file"""
        file_path = Path(file_path)
        
        if not file_path.exists():
            logger.error(f"File not found: {file_path}")
            return
        
        # Parse filename to get metadata
        artist, title, album = self.parse_filename(file_path.name)
        logger.info(f"Processing: {file_path.name}")
        logger.info(f"Extracted - Artist: {artist}, Title: {title}, Album: {album}")
        
        # Process based on file extension
        ext = file_path.suffix.lower()
        
        if ext == '.mp3':
            self.process_mp3(str(file_path), artist, title, album)
        elif ext == '.flac':
            self.process_flac(str(file_path), artist, title, album)
        elif ext in ['.mp4', '.m4a']:
            self.process_mp4(str(file_path), artist, title, album)
        elif ext == '.ogg':
            self.process_ogg(str(file_path), artist, title, album)
        else:
            logger.warning(f"Unsupported file format: {ext}")

def main():
    if len(sys.argv) != 2:
        logger.error("Usage: postprocess.py <file_path>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    processor = MusicPostProcessor()
    processor.process_file(file_path)

if __name__ == "__main__":
    main()