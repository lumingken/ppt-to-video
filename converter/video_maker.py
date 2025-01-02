from pathlib import Path
from moviepy.editor import VideoFileClip, AudioFileClip, ImageClip, concatenate_videoclips

class VideoMaker:
    def create_video(self, slides_content, audio_files, output_path):
        """
        Create video from slides and audio files
        
        Args:
            slides_content: List of SlideContent objects containing image_path and text
            audio_files: List of tuples (audio_path, duration)
            output_path: Path to save the output video
        """
        clips = []
        
        print(f"Creating video with {len(slides_content)} slides")
        for i, (slide, (audio_path, duration)) in enumerate(zip(slides_content, audio_files)):
            print(f"Slide {i}: Image={slide.image_path} (exists={slide.image_path.exists()})")
            if audio_path:
                print(f"      Audio={audio_path} (exists={Path(audio_path).exists()})")
            
            # Create image clip from slide
            image_clip = ImageClip(str(slide.image_path))
            
            if audio_path:
                # If there's audio, use its duration and combine with image
                audio_clip = AudioFileClip(str(audio_path))
                video_clip = image_clip.set_duration(audio_clip.duration)
                video_clip = video_clip.set_audio(audio_clip)
            else:
                # If no audio, use the specified duration
                video_clip = image_clip.set_duration(duration)
            
            clips.append(video_clip)
        
        # Concatenate all clips
        final_clip = concatenate_videoclips(clips)
        
        # Write the result to a file
        final_clip.write_videofile(
            output_path,
            fps=24,
            codec='libx264',
            audio_codec='aac'
        )
        
        # Clean up
        final_clip.close()
        for clip in clips:
            clip.close() 