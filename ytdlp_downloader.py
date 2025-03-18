import yt_dlp
import os
import shutil

"""
Video Downloader Script: ytdlp_downloader.py

This script processes text files containing video URLs from YouTube and Vimeo, downloading videos
to a local directory and organizing processed text files.

Usage:
1. Place text files with YouTube or Vimeo URLs (one per line) into the `input_folder`.
2. Run the script to download videos to the `downloads` directory.
3. Processed text files are moved to the `processed_folder`.

Dependencies:
- yt-dlp: A command-line program to download videos from YouTube and other sites.
- Ensure Python is installed and yt-dlp is available via pip.

Directory Structure:
- input_folder: Directory containing .txt files with video URLs.
- processed_folder: Directory where processed .txt files are moved after processing.
"""

def is_youtube(url):
    """
    Check if the given URL is a YouTube link.
    :param url: URL string to check
    :return: Boolean indicating if the URL is a YouTube link
    """
    return "youtube.com" in url or "youtu.be" in url

def is_vimeo(url):
    """
    Check if the given URL is a Vimeo link.
    :param url: URL string to check
    :return: Boolean indicating if the URL is a Vimeo link
    """
    return "vimeo.com" in url

def download_videos_from_file(file_path, processed_folder):
    """
    Download the best quality videos from a file containing URLs.
    :param file_path: Path to the text file with video URLs
    :param processed_folder: Folder to move the processed text file into
    """
    with open(file_path, 'r') as url_file:
        urls = url_file.readlines()

    for url in urls:
        url = url.strip()
        if is_youtube(url):
            # yt-dlp options for YouTube: best video and audio quality
            ydl_opts = {
                'format': 'bestvideo+bestaudio/best',
                'outtmpl': './downloads/%(title)s.%(ext)s',
                'merge_output_format': 'mp4',
            }
        elif is_vimeo(url):
            # yt-dlp options for Vimeo: best format available
            ydl_opts = {
                'format': 'best',
                'outtmpl': './downloads/%(title)s.%(ext)s',
            }
        else:
            print(f"Unknown URL platform for {url}. Skipping.")
            continue

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                # Download and process the video
                ydl.download([url])
            except yt_dlp.utils.DownloadError as e:
                print(f"Failed to download {url}: {e}")

    # Move the processed text file to the processed folder
    destination = os.path.join(processed_folder, os.path.basename(file_path))
    shutil.move(file_path, destination)
    print(f"Moved {file_path} to {destination}")

if __name__ == '__main__':
    # Define the input and processed folders
    input_folder = '/path/to/your/shared/folder'
    processed_folder = '/path/to/your/processed/folder'

    # Process and download videos from each URL file in the input folder
    for file_name in os.listdir(input_folder):
        file_path = os.path.join(input_folder, file_name)
        if os.path.isfile(file_path) and file_path.endswith('.txt'):
            download_videos_from_file(file_path, processed_folder)