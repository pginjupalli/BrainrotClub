import os

# def overlay(video_a_filename, video_b_filename):
  
#   # Swapped filenames: now videoA has audio and videoB is silent.
#   # video_a_filename = "videoA.mp4"  # This one has audio now.
#   # video_b_filename = "videoB.mp4"  # This one is silent.
  
#   # Verify files exist.
#   if not os.path.exists(video_a_filename):
#       raise FileNotFoundError(f"{video_a_filename} not found.")
#   if not os.path.exists(video_b_filename):
#       raise FileNotFoundError(f"{video_b_filename} not found.")
  
#   # Load the video clips.
  
#   clip_A = VideoFileClip(video_a_filename)
#   clip_B = VideoFileClip(video_b_filename)
  
#   # Debug: Print original resolutions.
#   print("clip_A resolution:", clip_A.size)
#   print("clip_B resolution:", clip_B.size)
  
#   # Choose a common resolution for both videos.
#   # clip_A = clip_A.cropped(x_center=clip_A.w/2, y_center=clip_A.h/2, width=1080/2, height=1920/2)
#   # clip_B = clip_B.cropped(x_center=clip_B.w/2, y_center=clip_B.h/2, width=1080/2, height=1920/2)
#   # common_resolution = (1080/2, 1920/2)
#   # clip_A = clip_A.resized(common_resolution)
#   # clip_B = clip_B.resized(common_resolution)
#   clip_A = clip_A.cropped(x_center=clip_A.w/2, y_center=clip_A.h/2, width=min(clip_A.w, clip_A.h*9/16), height=min(clip_A.h, clip_A.w*16/9)).resized((1080,1920))
#   clip_B = clip_B.cropped(x_center=clip_B.w/2, y_center=clip_B.h/2, width=min(clip_B.w, clip_B.h*9/16), height=min(clip_B.h, clip_B.w*16/9)).resized((1080,1920))
  
  
  
#   # Duration of each segment (seconds)
#   segment_duration = 2
  
#   # Calculate the number of full segments each clip can provide.
#   num_segments_A = int(clip_A.duration // segment_duration)
#   num_segments_B = int(clip_B.duration // segment_duration)
#   num_segments = min(num_segments_A, num_segments_B)
  
#   segments = []
#   for i in range(num_segments):
#       start = i * segment_duration
#       end = start + segment_duration
#       # Alternate segments: even from clip_A, odd from clip_B.
#       if i % 2 == 0:
#           segment = clip_A.subclipped(start, end)
#       else:
#           segment = clip_B.subclipped(start, end)
#       # Remove the segment's own audio.
#       segments.append(segment.without_audio())
  
#   # Concatenate segments.
#   final_clip = concatenate_videoclips(segments)
  
#   # Use audio from clip_A (which now has audio) for the entire final video.
#   if clip_A.audio is not None:
#       # Use subclipped (if that's what your version provides) to trim the audio.
#       audio_source = clip_A.audio.subclipped(0, final_clip.duration)
#       final_clip = final_clip.with_audio(audio_source)
#   else:
#       print("Warning: No audio found in clip_A.")
  
#   # Write the output video.
#   final_clip.write_videofile(video_a_filename, codec="libx264", audio_codec="aac")
  
  
  
import os
from moviepy.editor import VideoFileClip, CompositeVideoClip
from moviepy.video.fx.mask_color import mask_color

def greenscreen_overlay(video_a_filename, video_b_filename, output_name):
    # Verify that both files exist.
    if not os.path.exists(video_a_filename):
        raise FileNotFoundError(f"{video_a_filename} not found.")
    if not os.path.exists(video_b_filename):
        raise FileNotFoundError(f"{video_b_filename} not found.")

    # Load the video clips.
    clip_A = VideoFileClip(video_a_filename)
    clip_B = VideoFileClip(video_b_filename)
    
    side = min(clip_A.w, clip_A.h)
    clip_A = clip_A.crop(
    x_center=clip_A.w / 2,
    y_center=clip_A.h / 2,
    width=side,
    height=side)

    # Debug: Print original resolutions.
    print("clip_A resolution:", clip_A.size)
    print("clip_B resolution:", clip_B.size)

    # Crop and resize both clips to a common resolution.
    common_size = (1080/4, 1920/4)
    clip_A = clip_A.crop(x_center=clip_A.w/2, y_center=clip_A.h/2,
                            width=min(clip_A.w, clip_A.h*9/16),
                            height=min(clip_A.h, clip_A.w*16/9)).resize(common_size)
    clip_B = clip_B.crop(x_center=clip_B.w/2, y_center=clip_B.h/2,
                            width=min(clip_B.w, clip_B.h*9/16),
                            height=min(clip_B.h, clip_B.w*16/9)).resize(common_size)
    


    # Apply green screen (chroma key) effect on clip_A.
    # This removes the green background color ([0, 255, 0]). Adjust 'thr' (threshold) and 's' (softness) as needed.from moviepy.video.fx.mask_color import mask_color

    # Then apply the effect directly:
    clip_A = mask_color(clip_A, color=[0,128,0], thr=100, s=60)

    final_duration = min(clip_A.duration, clip_B.duration)
    
    # Trim both clips to the final duration
    clip_A = clip_A.subclip(0, final_duration)
    clip_B = clip_B.subclip(0, final_duration)
    
    # fps = 30
    # clip_A = clip_A.set_fps(fps)
    # clip_B = clip_B.set_fps(fps)
    
    # Resize clip_A (scale down to 80% of its size)
    clip_A = clip_A.resize(0.6)

    # Calculate centered position
    x_pos = (clip_B.w - clip_A.w) / 2
    y_pos = (clip_B.h - clip_A.h) / 2 + 150  # shift down by 50 pixels

    # Clamp the positions to ensure clip_A stays within clip_B
    x_pos = max(0, min(x_pos, clip_B.w - clip_A.w))
    y_pos = max(0, min(y_pos, clip_B.h - clip_A.h))

    # Composite clip_A over clip_B with the clamped position
    composite_clip = CompositeVideoClip(
        [clip_B, clip_A.set_position((x_pos, y_pos))],
        size=clip_B.size
    )
    
    # Composite clip_A (foreground) over clip_B (background).
    # Here, clip_A is centered over clip_B. You can adjust the position if necessary.
    # composite_clip = CompositeVideoClip([clip_B, clip_A.set_position("center")], size=clip_B.size)
    # composite_clip = CompositeVideoClip(
    #     [clip_B, clip_A.set_position(("center", "60%"))],  # "60%" moves it lower than center
    #     size=clip_B.size
    # )
    # Use the audio from clip_A.
    if clip_A.audio is not None:
        composite_clip = composite_clip.set_audio(clip_A.audio)
    else:
        print("Warning: No audio found in clip_A.")

    # Write the final output video.
    composite_clip.write_videofile(output_name, codec="libx264", audio_codec="aac", threads=4, preset="ultrafast", fps=30)

# Example usage:
# green_screen_overlay("videoA.mp4", "videoB.mp4", "output_video.mp4")
