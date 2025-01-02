import argparse
from pathlib import Path
from converter.ppt_reader import PPTReader
from converter.text_to_speech import TextToSpeech
from converter.video_maker import VideoMaker

def main():
    parser = argparse.ArgumentParser(description='Convert PowerPoint to Video with AI Voice')
    parser.add_argument('input_ppt', help='Path to input PowerPoint file')
    parser.add_argument('output_video', help='Path to output video file')
    parser.add_argument('--voice', default='en-US-JennyNeural', help='Voice to use for narration')
    parser.add_argument('--slide-duration', type=int, default=5, help='Duration for slides without text (seconds)')
    
    args = parser.parse_args()
    
    # Create temp directory for intermediate files
    temp_dir = Path('temp')
    temp_dir.mkdir(exist_ok=True)
    
    try:
        # Read PPT and extract content
        ppt_reader = PPTReader(args.input_ppt)
        slides_content = ppt_reader.extract_content()
        
        # Generate speech for each slide
        tts = TextToSpeech(args.voice)
        audio_files = []
        for i, content in enumerate(slides_content):
            if content.text:
                audio_file = temp_dir / f'slide_{i}.mp3'
                tts.generate_speech(content.text, str(audio_file))
                audio_files.append((audio_file, len(content.text.split()) / 3))  # Estimate duration
            else:
                audio_files.append((None, args.slide_duration))
        
        # Create video
        video_maker = VideoMaker()
        video_maker.create_video(
            slides_content,
            audio_files,
            args.output_video
        )
        
    finally:
        # Cleanup temp files
        if temp_dir.exists():
            for file in temp_dir.glob('*'):
                file.unlink()
            temp_dir.rmdir()

if __name__ == '__main__':
    main() 