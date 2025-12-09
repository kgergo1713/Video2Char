# 🎬 ASCII Video Player

A hobby project that plays popular video formats on a character-based screen! Videos are displayed as colored ASCII art with a small original preview in the bottom-right corner.

## ✨ Features

- **Colored ASCII Display** - Videos converted to colored ASCII characters in real-time
- **Original Preview** - Small original video preview in the bottom-right corner
- **Live Playback** - Proper FPS timing and smooth playback
- **Interactive Controls** - Pause, restart, toggle preview
- **Customizable** - Resolution, colors, character sets
- **Automatic Aspect Ratio** - Just specify width, height is calculated automatically

## 📋 Requirements

- Python 3.7+
- OpenCV (opencv-python)
- NumPy
- Pygame
- Pillow

## 🚀 Installation

### 1. Create Virtual Environment (Recommended)

```powershell
# Using Python 3.13
python3.13 -m venv venv

# Activate
.\venv\Scripts\Activate.ps1
```

If you get an ExecutionPolicy error:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 2. Install Dependencies

```powershell
pip install -r requirements.txt
```

Or manually:
```powershell
pip install opencv-python numpy pygame pillow
```

## 🎮 Usage

### Quick Start

**Option 1: Interactive Mode** (easiest)
```powershell
# Windows batch file
start.bat

# Or PowerShell script
.\start.ps1

# Or Python
python run_player.py
```

**Option 2: Direct Playback**
```powershell
# Basic usage - only width needed!
python ascii_video_player.py video.mp4 --width 150

# With options
python ascii_video_player.py video.mp4 --width 200 --extended

# Without preview
python ascii_video_player.py video.mp4 --width 180 --no-preview

# Grayscale mode
python ascii_video_player.py video.mp4 --width 120 --no-color
```

### Command Line Options

| Option | Default | Description |
|--------|---------|-------------|
| `--width <N>` | 120 | ASCII width (characters) |
| `--height <N>` | auto | ASCII height (auto = maintains aspect ratio) |
| `--no-color` | false | Grayscale mode |
| `--extended` | false | Extended character set (70 characters) |
| `--no-preview` | false | Hide original video preview |

### Controls During Playback

- **SPACE** - Pause/Resume
- **P** - Toggle preview on/off
- **R** - Restart from beginning
- **ESC** or **Q** - Quit

## 🎨 How It Works

1. **Video Loading**: Read video frame-by-frame using OpenCV
2. **Resize**: Scale each frame to ASCII resolution
3. **Conversion**: 
   - Convert to grayscale for character selection
   - Apply contrast enhancement (histogram equalization)
   - Map pixel brightness → ASCII character
   - Preserve color information for rendering
4. **Display**: 
   - Render ASCII characters with Pygame (colored or grayscale)
   - Draw small original preview
   - Maintain proper FPS timing

## 🔧 Character Sets

**Standard** (12 characters):
```
 .':!*oe&#%@
```

**Extended** (70 characters):
```
 .'`^",:;Il!i><~+_-?][}{1)(|\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$
```

The extended character set provides finer gradations but may be less readable at lower resolutions.

## 📁 Supported Formats

All formats supported by OpenCV:
- MP4 (H.264, HEVC)
- AVI
- MOV (QuickTime)
- MKV (Matroska)
- WebM
- FLV

## 🎯 Recommended Settings

**Normal PC:**
```powershell
python ascii_video_player.py video.mp4 --width 120
# 120 characters wide, color, standard charset
```

**Best Quality:**
```powershell
python ascii_video_player.py video.mp4 --width 200 --extended
# High resolution, extended character set
```

**Fastest Performance:**
```powershell
python ascii_video_player.py video.mp4 --width 80 --no-color
# Low resolution, grayscale
```

## 📊 File Size Comparison

Curious about ASCII video sizes? Run the calculator:

```powershell
python video_size_calculator.py your_video.mp4 120
```

**Results (typical):**
- **Original video**: 62 MB (1920x1080, 21s)
- **ASCII video** (re-encoded H.264): ~4 MB
- **Compression**: ~**94% smaller!**

Why? Because ASCII uses far fewer data points:
- Original: 1920×1080 = 2,073,600 pixels/frame
- ASCII: 120×33 = 3,960 characters/frame
- **500× less data!**

## 🎪 Demo Videos

Create test videos:
```powershell
python create_demo_video.py
```

This generates:
- `demo_short.mp4` - 5 second test video
- `demo_medium.mp4` - 10 second test video

## 📝 Project Structure

```
VideoPlayerChar/
├── ascii_video_player.py      # Main video player
├── create_demo_video.py        # Demo video generator
├── video_size_calculator.py    # Size comparison tool
├── run_player.py               # Interactive launcher
├── start.bat                   # Windows batch launcher
├── start.ps1                   # PowerShell launcher
├── requirements.txt            # Python dependencies
├── README.md                   # This file
└── sample_videos/              # Video folder
    ├── demo_short.mp4
    └── demo_medium.mp4
```

## ⚡ Performance Tips

**If playback is slow:**
1. Reduce resolution: `--width 80`
2. Disable colors: `--no-color`
3. Hide preview: `--no-preview`
4. Use smaller video file

**Optimal settings by system:**
- **Low-end PC**: `--width 60 --no-color`
- **Average PC**: `--width 120` (default)
- **High-end PC**: `--width 200 --extended`

## 🐛 Troubleshooting

**"Module not found" error:**
```powershell
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

**"ExecutionPolicy" error:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Video won't open:**
- Check file path
- Try MP4 format
- Ensure video isn't corrupted

**Green screen / artifacts:**
- Codec compatibility issue
- Try converting to MP4/H.264:
```powershell
ffmpeg -i input.mov -c:v libx264 output.mp4
```

## 💡 Tips

1. **Best results**: High contrast, colorful videos work best
2. **Video conversion**: If a video doesn't work, convert it to MP4
3. **Custom characters**: Modify `ASCII_CHARS` in the code
4. **Frame capture**: Take screenshots during playback with your OS tools

## 🚀 Example Session

```powershell
# 1. Activate virtual environment
.\venv\Scripts\Activate.ps1

# 2. Create demo videos
python create_demo_video.py

# 3. Interactive mode
python run_player.py
# Select a video from the menu

# 4. Or play directly
python ascii_video_player.py sample_videos/demo_short.mp4

# 5. Try different settings
python ascii_video_player.py video.mp4 --width 180 --extended

# 6. Calculate size comparison
python video_size_calculator.py video.mp4 150
```

## 🎯 Known Limitations

1. **No audio** - Current version is video-only (no sound)
2. **FPS limits** - Very high FPS videos may have delays
3. **Codec support** - Some exotic codecs may not work
4. **Memory usage** - High resolution videos need more RAM

## 🔮 Possible Enhancements

- [ ] Audio support
- [ ] Fullscreen mode
- [ ] Screen recording of ASCII playback
- [ ] Speed controls (faster/slower)
- [ ] Seek forward/backward
- [ ] Playlist support
- [ ] Export ASCII to GIF/video
- [ ] Web interface
- [ ] Custom color schemes
- [ ] Terminal output mode (Windows Terminal, CMD)

## 📚 Technical Details

**Libraries Used:**
- `opencv-python` 4.12.0 - Video processing
- `numpy` 2.2.6+ - Array operations
- `pygame` 2.6.1+ - Graphics rendering
- `pillow` 12.0.0+ - Image handling

**Python Version:** 3.7+

**Rendering:**
- Font: Courier New (monospace)
- Character size: 10px
- Aspect ratio correction: 0.5× height multiplier
- Contrast enhancement: Histogram equalization
- Brightness mapping: Non-linear (square root transform)

## 📄 License

This is a hobby project, free to use and modify.

## 🎉 Enjoy!

Experiment with different videos and settings. Watch your favorite videos come to life as ASCII art! 🚀

---

**Created:** December 9, 2025  
**Version:** 1.0
