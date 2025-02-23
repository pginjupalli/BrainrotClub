import os
from moviepy import VideoFileClip, concatenate_videoclips

def overlay(video_a_filename, video_b_filename):
  
  # Swapped filenames: now videoA has audio and videoB is silent.
  # video_a_filename = "videoA.mp4"  # This one has audio now.
  # video_b_filename = "videoB.mp4"  # This one is silent.
  
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
  final_clip.write_videofile(video_a_filename, codec="libx264", audio_codec="aac")
  
  
  
import os
from moviepy import VideoFileClip, CompositeVideoClip, vfx

def greenscreen_overlay(video_a_filename, video_b_filename):
    # Verify that both files exist.
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

    # Crop and resize both clips to a common resolution.
    common_size = (1080, 1920)
    clip_A = clip_A.cropped(x_center=clip_A.w/2, y_center=clip_A.h/2,
                            width=min(clip_A.w, clip_A.h*9/16),
                            height=min(clip_A.h, clip_A.w*16/9)).resized(common_size)
    clip_B = clip_B.cropped(x_center=clip_B.w/2, y_center=clip_B.h/2,
                            width=min(clip_B.w, clip_B.h*9/16),
                            height=min(clip_B.h, clip_B.w*16/9)).resized(common_size)

    # Apply green screen (chroma key) effect on clip_A.
    # This removes the green background color ([0, 255, 0]). Adjust 'thr' (threshold) and 's' (softness) as needed.
    clip_A = clip_A.fx(vfx.mask_color, color=[0,255,0], thr=50, s=5)

    # Composite clip_A (foreground) over clip_B (background).
    # Here, clip_A is centered over clip_B. You can adjust the position if necessary.
    composite_clip = CompositeVideoClip([clip_B, clip_A.set_position("center")], size=clip_B.size)

    # Use the audio from clip_A.
    if clip_A.audio is not None:
        composite_clip = composite_clip.set_audio(clip_A.audio)
    else:
        print("Warning: No audio found in clip_A.")

    # Write the final output video.
    composite_clip.write_videofile(video_a_filename, codec="libx264", audio_codec="aac")

# Example usage:
# green_screen_overlay("videoA.mp4", "videoB.mp4", "output_video.mp4")
