"""
ASCII Video Size Calculator
Estimates ASCII video size compared to original
"""

import cv2
import sys
import os


def calculate_ascii_video_size(video_path, ascii_width=120):
    """
    Estimate ASCII video size
    """
    # Load video
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Failed to open: {video_path}")
        return
    
    # Video properties
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    duration = frame_count / fps if fps > 0 else 0
    
    # ASCII dimensions
    video_aspect = width / height
    ascii_height = int(ascii_width / video_aspect * 0.5)
    
    # Original file size
    original_size = os.path.getsize(video_path)
    
    cap.release()
    
    # ASCII video size estimation
    # -------------------------------
    
    # 1. Raw text format (.txt files)
    chars_per_frame = ascii_width * ascii_height
    bytes_per_char = 1  # 1 byte / character (ASCII)
    color_bytes_per_char = 3  # RGB colors
    
    # Characters only (gray)
    txt_size_gray = chars_per_frame * bytes_per_char * frame_count
    # Characters + colors
    txt_size_color = chars_per_frame * (bytes_per_char + color_bytes_per_char) * frame_count
    
    # 2. Compressed text format (gzip)
    # ASCII characters compress well (lots of repetition)
    # Typical compression ratio: ~10:1 or better
    txt_compressed_gray = txt_size_gray / 10
    txt_compressed_color = txt_size_color / 8  # slightly worse with colors
    
    # 3. Re-encoded video (H.264)
    # ASCII rendered to new video
    render_width = ascii_width * 6  # ~6px / character width
    render_height = ascii_height * 12  # ~12px / character height
    
    # H.264 typical bitrate: 0.1-0.2 bits/pixel/frame on average
    bitrate_medium = render_width * render_height * fps * 0.1
    reencoded_medium = (bitrate_medium * duration) / 8  # bits -> bytes
    
    # Print results
    print("=" * 70)
    print(f"ASCII VIDEO SIZE CALCULATOR")
    print("=" * 70)
    print(f"\n📹 ORIGINAL VIDEO:")
    print(f"   File: {os.path.basename(video_path)}")
    print(f"   Size: {original_size:,} bytes ({original_size/1024/1024:.2f} MB)")
    print(f"   Resolution: {width}x{height}")
    print(f"   FPS: {fps:.2f}")
    print(f"   Frames: {frame_count}")
    print(f"   Duration: {duration:.1f} sec")
    
    print(f"\n🔤 ASCII CONVERSION:")
    print(f"   ASCII resolution: {ascii_width}x{ascii_height}")
    print(f"   Characters/frame: {chars_per_frame:,}")
    print(f"   Aspect ratio maintained: ✓")
    
    print(f"\n📊 ESTIMATED ASCII VIDEO SIZES:")
    print(f"\n1️⃣  RAW TEXT (.txt files):")
    print(f"   Characters only: {txt_size_gray:,} bytes ({txt_size_gray/1024/1024:.2f} MB)")
    print(f"   Ratio: {txt_size_gray/original_size:.2f}x {'LARGER' if txt_size_gray > original_size else 'SMALLER'}")
    print(f"   With colors: {txt_size_color:,} bytes ({txt_size_color/1024/1024:.2f} MB)")
    print(f"   Ratio: {txt_size_color/original_size:.2f}x {'LARGER' if txt_size_color > original_size else 'SMALLER'}")
    
    print(f"\n2️⃣  COMPRESSED TEXT (.txt.gz):")
    print(f"   Characters only: {txt_compressed_gray:,} bytes ({txt_compressed_gray/1024/1024:.2f} MB)")
    print(f"   Ratio: {txt_compressed_gray/original_size:.2f}x {'LARGER' if txt_compressed_gray > original_size else 'SMALLER'}")
    print(f"   With colors: {txt_compressed_color:,} bytes ({txt_compressed_color/1024/1024:.2f} MB)")
    print(f"   Ratio: {txt_compressed_color/original_size:.2f}x {'LARGER' if txt_compressed_color > original_size else 'SMALLER'}")
    
    print(f"\n3️⃣  RE-ENCODED VIDEO (H.264):")
    print(f"   Render resolution: {render_width}x{render_height} px")
    print(f"   Medium quality: {reencoded_medium:,} bytes ({reencoded_medium/1024/1024:.2f} MB)")
    print(f"   Ratio: {reencoded_medium/original_size:.2f}x {'LARGER' if reencoded_medium > original_size else 'SMALLER'}")
    
    print(f"\n💡 CONCLUSIONS:")
    print(f"   • ASCII video is MUCH larger in uncompressed form")
    print(f"   • With compression (gzip) can be competitive")
    print(f"   • Re-encoded as H.264 video: {reencoded_medium/original_size:.1f}x original size")
    print(f"   • Best ratio: compressed text or re-encoded video")
    
    print(f"\n📝 NOTES:")
    print(f"   • These are estimated values, actual size may vary")
    print(f"   • Compression efficiency depends on video content")
    print(f"   • More motion = worse compression")
    print(f"   • ASCII characters compress well (repeating patterns)")
    
    print("=" * 70)


def main():
    if len(sys.argv) < 2:
        print("Usage: python video_size_calculator.py <video_file> [ascii_width]")
        print("\nExample:")
        print("  python video_size_calculator.py video.mp4")
        print("  python video_size_calculator.py video.mp4 200")
        sys.exit(1)
    
    video_path = sys.argv[1]
    ascii_width = int(sys.argv[2]) if len(sys.argv) > 2 else 120
    
    if not os.path.exists(video_path):
        print(f"Error: File not found: {video_path}")
        sys.exit(1)
    
    calculate_ascii_video_size(video_path, ascii_width)


if __name__ == "__main__":
    main()
