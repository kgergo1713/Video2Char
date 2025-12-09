"""
Demo Video Generator - create simple test video using OpenCV
"""

import cv2
import numpy as np
import os

def create_demo_video(output_path: str, duration: int = 5, fps: int = 30):
    """
    Create simple demo video with various colored patterns
    
    Args:
        output_path: Output video file
        duration: Video length in seconds
        fps: Frames per second
    """
    width, height = 640, 480
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    total_frames = duration * fps
    
    print(f"Creating demo video: {output_path}")
    print(f"Size: {width}x{height}, FPS: {fps}, Duration: {duration}s")
    
    for frame_num in range(total_frames):
        # Empty frame
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Background gradient
        for y in range(height):
            color_val = int(255 * y / height)
            frame[y, :] = [color_val // 3, color_val // 2, color_val]
        
        # Moving circle
        center_x = int(width * (0.5 + 0.3 * np.sin(2 * np.pi * frame_num / fps)))
        center_y = int(height * (0.5 + 0.3 * np.cos(2 * np.pi * frame_num / fps)))
        radius = 50
        cv2.circle(frame, (center_x, center_y), radius, (0, 255, 255), -1)
        cv2.circle(frame, (center_x, center_y), radius, (255, 255, 255), 3)
        
        # Moving square
        rect_x = int(width * frame_num / total_frames)
        rect_y = height // 4
        cv2.rectangle(frame, (rect_x, rect_y), (rect_x + 60, rect_y + 60), 
                     (255, 100, 200), -1)
        cv2.rectangle(frame, (rect_x, rect_y), (rect_x + 60, rect_y + 60), 
                     (255, 255, 255), 2)
        
        # Text
        text = f"Frame: {frame_num + 1}/{total_frames}"
        cv2.putText(frame, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 
                   0.7, (255, 255, 255), 2)
        
        text2 = "ASCII Video Player Demo"
        cv2.putText(frame, text2, (width // 2 - 150, height - 20), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)
        
        # Color stripes
        stripe_height = 30
        colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), 
                 (255, 255, 0), (255, 0, 255), (0, 255, 255)]
        
        for i, color in enumerate(colors):
            y_start = height // 2 + i * stripe_height
            offset = int(30 * np.sin(2 * np.pi * (frame_num / fps + i * 0.2)))
            cv2.rectangle(frame, (offset, y_start), 
                         (width - offset, y_start + stripe_height - 2), 
                         color, -1)
        
        out.write(frame)
        
        if (frame_num + 1) % fps == 0:
            print(f"  {(frame_num + 1) // fps}/{duration} seconds completed")
    
    out.release()
    print(f"✓ Video ready: {output_path}")
    print(f"  File size: {os.path.getsize(output_path) / 1024:.1f} KB")


if __name__ == "__main__":
    # Create sample_videos folder if it doesn't exist
    os.makedirs("sample_videos", exist_ok=True)
    
    # Create demo videos with different parameters
    create_demo_video("sample_videos/demo_short.mp4", duration=5, fps=30)
    create_demo_video("sample_videos/demo_medium.mp4", duration=10, fps=30)
    
    print("\n✓ All demo videos created!")
    print("\nStart the player:")
    print("  python ascii_video_player.py sample_videos/demo_short.mp4")
