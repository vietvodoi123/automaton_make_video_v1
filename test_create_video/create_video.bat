@echo off
setlocal

REM Cài đặt thông số
set INPUT_DIR=frames
set OUTPUT=cuon_text.mp4
set FPS=30

REM Dùng GPU AMD (AMF)
ffmpeg -y -hwaccel auto -framerate %FPS% -i %INPUT_DIR%\frame_%%05d.png -c:v h264_amf -pix_fmt yuv420p %OUTPUT%

echo ✅ Video đã được tạo: %OUTPUT%
pause
