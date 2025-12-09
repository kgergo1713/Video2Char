"""
Quick Launcher - ASCII Video Player easy start
"""

import sys
import os

def main():
    print("=" * 60)
    print("ASCII VIDEO PLAYER - Character-based Video Player")
    print("=" * 60)
    print()
    
    # Search for videos in sample_videos folder
    sample_dir = "sample_videos"
    if os.path.exists(sample_dir):
        videos = [f for f in os.listdir(sample_dir) 
                 if f.endswith(('.mp4', '.avi', '.mov', '.mkv', '.webm'))]
        
        if videos:
            print(f"Found videos in '{sample_dir}' folder:")
            for i, video in enumerate(videos, 1):
                size = os.path.getsize(os.path.join(sample_dir, video)) / 1024
                print(f"  {i}. {video} ({size:.1f} KB)")
            print()
            
            try:
                choice = input("Select video (1-{}) or 'q' to quit: ".format(len(videos)))
                
                if choice.lower() == 'q':
                    return
                
                idx = int(choice) - 1
                if 0 <= idx < len(videos):
                    video_path = os.path.join(sample_dir, videos[idx])
                    print()
                    print(f"Starting video: {video_path}")
                    print("-" * 60)
                    
                    # Launch ASCII player
                    from ascii_video_player import ASCIIVideoPlayer
                    
                    player = ASCIIVideoPlayer(
                        video_path=video_path,
                        width=120,
                        height=None,
                        use_color=True
                    )
                    player.play()
                else:
                    print("Invalid selection!")
            except (ValueError, KeyboardInterrupt):
                print("\nExiting...")
        else:
            print(f"No videos in '{sample_dir}' folder.")
            print()
            print("To generate demo videos run:")
            print("  python create_demo_video.py")
    else:
        print(f"'{sample_dir}' folder not found.")
        print()
        print("Create demo videos:")
        print("  python create_demo_video.py")
    
    print()
    print("Or use the program directly:")
    print("  python ascii_video_player.py <video_file>")
    print()


if __name__ == "__main__":
    main()
