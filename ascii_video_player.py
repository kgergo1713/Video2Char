"""
ASCII Video Player - Character-based video player
Plays videos as colored ASCII characters + small original preview
"""

import cv2
import numpy as np
import pygame
import sys
from typing import Tuple, Optional

# ASCII characters from dark to bright - optimized scale
ASCII_CHARS = " .':!*oe&#%@"
# Alternative character set with more gradations
ASCII_CHARS_EXTENDED = " .'`^\",:;Il!i><~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"


class ASCIIVideoPlayer:
    """Video player with ASCII characters"""
    
    def __init__(self, video_path: str, width: int = 120, height: int = None, 
                 use_color: bool = True, use_extended_chars: bool = False,
                 show_preview: bool = True):
        """
        Args:
            video_path: Video file path
            width: Number of ASCII characters horizontally
            height: Number of ASCII characters vertically (None = automatic based on aspect ratio)
            use_color: Color display
            use_extended_chars: Use extended character set
            show_preview: Show original video preview
        """
        self.video_path = video_path
        self.ascii_width = width
        self.use_color = use_color
        self.chars = ASCII_CHARS_EXTENDED if use_extended_chars else ASCII_CHARS
        self.show_preview = show_preview
        
        # Load video
        self.cap = cv2.VideoCapture(video_path)
        if not self.cap.isOpened():
            raise ValueError(f"Failed to open video: {video_path}")
        
        # Video properties
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.frame_count = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.original_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.original_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        # Calculate ASCII height if not provided
        # Characters are ~2x taller than wide, so use 0.5 correction
        if height is None:
            video_aspect = self.original_width / self.original_height
            self.ascii_height = int(self.ascii_width / video_aspect * 0.5)
        else:
            self.ascii_height = height
        
        # Initialize Pygame
        pygame.init()
        
        # Screen settings - MONOSPACE font!
        self.font_size = 10
        # Courier New monospace font - all characters same width
        try:
            self.font = pygame.font.SysFont('Courier New', self.font_size)
        except:
            # If Courier unavailable, use monospace
            self.font = pygame.font.SysFont('monospace', self.font_size)
        
        # ASCII area size - EXACT calculation
        # Use 'W' width as reference
        test_char = 'W'
        char_width = self.font.size(test_char)[0]
        char_height = self.font.get_height()
        self.ascii_screen_width = self.ascii_width * char_width
        self.ascii_screen_height = self.ascii_height * char_height
        
        # Preview size (bottom-right corner) - smaller so it doesn't cover too much
        self.preview_width = 240
        self.preview_height = int(self.preview_width * self.original_height / self.original_width)
        
        # Total window size - exactly ASCII content size
        # No extra space, window is exactly ASCII size + small margin
        self.screen_width = self.ascii_screen_width + 20
        # Height: only need space for ASCII, preview overlays on top
        self.screen_height = self.ascii_screen_height + 20
        
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("ASCII Video Player")
        
        self.clock = pygame.time.Clock()
        self.running = False
        
    def frame_to_ascii(self, frame: np.ndarray) -> Tuple[str, Optional[np.ndarray]]:
        """
        Convert frame to ASCII characters
        
        Returns:
            (ascii_string, color_array): ASCII text and optional color array
        """
        # Resize - directly to target resolution
        resized = cv2.resize(frame, (self.ascii_width, self.ascii_height))
        
        # Convert to grayscale for character selection
        gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
        
        # Increase contrast (histogram equalization)
        gray = cv2.equalizeHist(gray)
        
        # Convert to characters
        ascii_frame = ""
        color_array = None
        
        if self.use_color:
            color_array = resized.copy()
        
        for row in gray:
            for pixel_value in row:
                # Pixel value -> character index (improved mapping)
                # 0-255 range -> character index, non-linear
                normalized = pixel_value / 255.0
                char_index = int(normalized ** 0.5 * (len(self.chars) - 1))
                char_index = min(max(char_index, 0), len(self.chars) - 1)
                ascii_frame += self.chars[char_index]
            ascii_frame += "\n"
        
        return ascii_frame, color_array
    
    def draw_ascii_frame(self, ascii_text: str, color_array: Optional[np.ndarray] = None):
        """Draw ASCII frame on screen"""
        y = 10
        lines = ascii_text.split('\n')
        
        # Monospace character width
        char_width = self.font.size('W')[0]
        char_height = self.font.get_height()
        
        for row_idx, line in enumerate(lines):
            if not line:
                continue
                
            x = 10
            for col_idx, char in enumerate(line):
                if self.use_color and color_array is not None:
                    # BGR -> RGB
                    b, g, r = color_array[row_idx, col_idx]
                    color = (int(r), int(g), int(b))
                else:
                    # Grayscale
                    gray_val = int((self.chars.index(char) / len(self.chars)) * 255)
                    color = (gray_val, gray_val, gray_val)
                
                text_surface = self.font.render(char, True, color)
                self.screen.blit(text_surface, (x, y))
                # FIXED width for every character!
                x += char_width
            
            y += char_height
    
    def draw_preview(self, frame: np.ndarray):
        """Original video small preview in bottom-right corner"""
        # Resize
        preview = cv2.resize(frame, (self.preview_width, self.preview_height))
        
        # BGR -> RGB
        preview = cv2.cvtColor(preview, cv2.COLOR_BGR2RGB)
        
        # NumPy array -> Pygame surface
        preview = np.transpose(preview, (1, 0, 2))
        preview_surface = pygame.surfarray.make_surface(preview)
        
        # Bottom-right corner position - 15px margin within ASCII area
        x = self.screen_width - self.preview_width - 15
        y = self.screen_height - self.preview_height - 15
        
        # Semi-transparent background under preview (black)
        bg_surface = pygame.Surface((self.preview_width + 4, self.preview_height + 4))
        bg_surface.fill((0, 0, 0))
        bg_surface.set_alpha(200)
        self.screen.blit(bg_surface, (x - 2, y - 2))
        
        # Frame around preview
        pygame.draw.rect(self.screen, (255, 255, 255), 
                        (x - 2, y - 2, self.preview_width + 4, self.preview_height + 4), 2)
        
        self.screen.blit(preview_surface, (x, y))
    
    def play(self):
        """Play video"""
        self.running = True
        frame_delay = int(1000 / self.fps) if self.fps > 0 else 30
        
        print(f"Starting playback...")
        print(f"Video: {self.video_path}")
        print(f"Resolution: {self.original_width}x{self.original_height}")
        print(f"FPS: {self.fps}")
        print(f"Frames: {self.frame_count}")
        print(f"ASCII size: {self.ascii_width}x{self.ascii_height}")
        print(f"\nControls:")
        print("  SPACE - Pause/Resume")
        print("  P - Toggle preview on/off")
        print("  R - Restart")
        print("  ESC or Q - Quit")
        
        paused = False
        
        while self.running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                        self.running = False
                    elif event.key == pygame.K_SPACE:
                        paused = not paused
                    elif event.key == pygame.K_r:
                        # Restart
                        self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                        paused = False
                    elif event.key == pygame.K_p:
                        # Toggle preview on/off
                        self.show_preview = not self.show_preview
                        print(f"Preview: {'ON' if self.show_preview else 'OFF'}")
            
            if not paused:
                # Read frame
                ret, frame = self.cap.read()
                
                if not ret:
                    # End of video - restart
                    self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    continue
                
                # Clear background
                self.screen.fill((0, 0, 0))
                
                # ASCII conversion
                ascii_text, color_array = self.frame_to_ascii(frame)
                
                # Draw ASCII
                self.draw_ascii_frame(ascii_text, color_array)
                
                # Draw preview - only if enabled
                if self.show_preview:
                    self.draw_preview(frame)
                
                # Status info - bottom-left corner
                current_frame = int(self.cap.get(cv2.CAP_PROP_POS_FRAMES))
                info_text = f"Frame: {current_frame}/{self.frame_count}"
                
                # Black background behind text
                info_surface = self.font.render(info_text, True, (200, 200, 200))
                text_width, text_height = self.font.size(info_text)
                bg_rect = pygame.Surface((text_width + 10, text_height + 6))
                bg_rect.fill((0, 0, 0))
                bg_rect.set_alpha(200)
                self.screen.blit(bg_rect, (8, self.screen_height - text_height - 12))
                self.screen.blit(info_surface, (10, self.screen_height - text_height - 10))
                
                # Update screen
                pygame.display.flip()
                
                # FPS control
                self.clock.tick(self.fps)
            else:
                # Paused - only handle events
                pygame.time.wait(100)
                
                # "PAUSED" text
                pause_text = "PAUSED - Press SPACE to continue"
                pause_surface = pygame.font.Font(None, 36).render(pause_text, True, (255, 255, 0))
                text_rect = pause_surface.get_rect(center=(self.screen_width // 2, 30))
                self.screen.blit(pause_surface, text_rect)
                pygame.display.flip()
        
        self.cleanup()
    
    def cleanup(self):
        """Release resources"""
        self.cap.release()
        pygame.quit()
        print("\nPlayback finished.")


def main():
    """Main program"""
    if len(sys.argv) < 2:
        print("Usage: python ascii_video_player.py <video_file>")
        print("\nOptional parameters:")
        print("  --width <N>     ASCII width (default: 120)")
        print("  --height <N>    ASCII height (default: automatic based on aspect ratio)")
        print("  --no-color      Grayscale mode")
        print("  --extended      Extended character set")
        print("  --no-preview    Hide original video preview")
        print("\nExample:")
        print("  python ascii_video_player.py sample_videos/video.mp4")
        print("  python ascii_video_player.py video.mp4 --width 160")
        print("  python ascii_video_player.py video.mp4 --width 200 --extended")
        print("  python ascii_video_player.py video.mp4 --no-preview")
        sys.exit(1)
    
    video_path = sys.argv[1]
    
    # Process parameters
    width = 120
    height = None  # None = automatic aspect ratio
    use_color = True
    use_extended = False
    show_preview = True
    
    i = 2
    while i < len(sys.argv):
        if sys.argv[i] == '--width' and i + 1 < len(sys.argv):
            width = int(sys.argv[i + 1])
            i += 2
        elif sys.argv[i] == '--height' and i + 1 < len(sys.argv):
            height = int(sys.argv[i + 1])
            i += 2
        elif sys.argv[i] == '--no-color':
            use_color = False
            i += 1
        elif sys.argv[i] == '--extended':
            use_extended = True
            i += 1
        elif sys.argv[i] == '--no-preview':
            show_preview = False
            i += 1
        else:
            i += 1
    
    try:
        player = ASCIIVideoPlayer(
            video_path=video_path,
            width=width,
            height=height,
            use_color=use_color,
            use_extended_chars=use_extended,
            show_preview=show_preview
        )
        player.play()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
