import os
from moviepy import VideoFileClip, concatenate_videoclips

# Swapped filenames: now videoA has audio and videoB is silent.
video_a_filename = "videoA.mp4"  # This one has audio now.
video_b_filename = "videoB.mp4"  # This one is silent.

# Verify files exist.
if not os.path.exists(video_a_filename):
    raise FileNotFoundError(f"{video_a_filename} not found.")
if not os.path.exists(video_b_filename):
    raise FileNotFoundError(f"{video_b_filename} not found.")

# Load the video clips.

clip_A = VideoFileClip(video_a_filename)
clip_B = VideoFileClip(video_b_filename)

# Debug: Print original resolutions.
print("clip_A resolution:", clip_A.size)
print("clip_B resolution:", clip_B.size)

# Choose a common resolution for both videos.
# clip_A = clip_A.cropped(x_center=clip_A.w/2, y_center=clip_A.h/2, width=1080/2, height=1920/2)
# clip_B = clip_B.cropped(x_center=clip_B.w/2, y_center=clip_B.h/2, width=1080/2, height=1920/2)
# common_resolution = (1080/2, 1920/2)
# clip_A = clip_A.resized(common_resolution)
# clip_B = clip_B.resized(common_resolution)
clip_A = clip_A.cropped(x_center=clip_A.w/2, y_center=clip_A.h/2, width=min(clip_A.w, clip_A.h*9/16), height=min(clip_A.h, clip_A.w*16/9)).resized((1080,1920))
clip_B = clip_B.cropped(x_center=clip_B.w/2, y_center=clip_B.h/2, width=min(clip_B.w, clip_B.h*9/16), height=min(clip_B.h, clip_B.w*16/9)).resized((1080,1920))



# Duration of each segment (seconds)
segment_duration = 2

# Calculate the number of full segments each clip can provide.
num_segments_A = int(clip_A.duration // segment_duration)
num_segments_B = int(clip_B.duration // segment_duration)
num_segments = min(num_segments_A, num_segments_B)

segments = []
for i in range(num_segments):
    start = i * segment_duration
    end = start + segment_duration
    # Alternate segments: even from clip_A, odd from clip_B.
    if i % 2 == 0:
        segment = clip_A.subclipped(start, end)
    else:
        segment = clip_B.subclipped(start, end)
    # Remove the segment's own audio.
    segments.append(segment.without_audio())

# Concatenate segments.
final_clip = concatenate_videoclips(segments)

# Use audio from clip_A (which now has audio) for the entire final video.
if clip_A.audio is not None:
    # Use subclipped (if that's what your version provides) to trim the audio.
    audio_source = clip_A.audio.subclipped(0, final_clip.duration)
    final_clip = final_clip.with_audio(audio_source)
else:
    print("Warning: No audio found in clip_A.")

# Write the output video.
final_clip.write_videofile("output.mp4", codec="libx264", audio_codec="aac")
