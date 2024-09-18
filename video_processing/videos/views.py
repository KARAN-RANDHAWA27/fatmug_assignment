from django.shortcuts import render, redirect
from .forms import VideoUploadForm
from .models import Video, Subtitle
import subprocess
import os
from datetime import timedelta
import re
from .utils import convert_srt_to_vtt  # Import the function

# Create your views here.

def upload_video(request):
    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save()
            extract_subtitles(video)  # Pass the video object directly
            return redirect('upload_success')  # Redirect to a success page
    else:
        form = VideoUploadForm()
    return render(request, 'videos/upload.html', {'form': form})

def extract_subtitles(video):
    # Define the path for the subtitle file
    subtitle_file_path = f'{video.file.path}.srt'  # Use video.file.path to create the subtitle file path
    print(subtitle_file_path)
    vtt_file_path = f'{video.file.path}.vtt'  # Define the VTT file path

    # Example command to extract subtitles
    command = ['ffmpeg', '-i', video.file.path, '-map', '0:s:0', subtitle_file_path]
    subprocess.run(command)

    # Convert SRT to VTT
    convert_srt_to_vtt(subtitle_file_path, vtt_file_path)

    # Read the extracted subtitles and save them to the database
    if os.path.exists(subtitle_file_path):
        with open(subtitle_file_path, 'r', encoding='utf-8') as file:
            content = file.readlines()
        
        # Regular expression to match the timestamp format
        timestamp_pattern = re.compile(r'^\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}$')

        # Parse the SRT file and save subtitles
        for i in range(0, len(content), 4):  # SRT format has 4 lines per subtitle
            if i + 2 < len(content):  # Ensure there are enough lines
                # Extract timestamp and subtitle text
                timestamp_line = content[i + 1].strip()  # Get the line with the timestamp
                subtitle_text = content[i + 2].strip()  # Get the subtitle text

                # Check if the timestamp line matches the expected format
                if timestamp_pattern.match(timestamp_line):
                    # Extract the start timestamp
                    timestamp = timestamp_line.split(' --> ')[0].replace(',', '.')
                    
                    # Convert timestamp to a DurationField (timedelta)
                    hours, minutes, seconds = map(float, timestamp.split(':'))
                    total_duration = timedelta(hours=int(hours), minutes=int(minutes), seconds=seconds)
                    
                    # Create and save the Subtitle object
                    Subtitle.objects.create(
                        video=video,  # Use the video object directly
                        language='en',  # Set the language as needed
                        content=subtitle_text,
                        timestamp=total_duration  # Save the timestamp as a timedelta
                    )
                else:
                    print(f"Skipping invalid timestamp line: '{timestamp_line}'")

def search_subtitles(request):
    query = request.GET.get('q', '')
    results = Subtitle.objects.filter(content__icontains=query) if query else []
    return render(request, 'videos/search.html', {'results': results, 'query': query})

def video_list(request):
    videos = Video.objects.all()
    
    return render(request, 'videos/video_list.html', {'videos': videos})
    

def video_detail(request, video_id):
    video = Video.objects.get(id=video_id)
    return render(request, 'videos/video_detail.html', {'video': video})

def upload_success(request):
    return render(request, 'videos/upload_success.html')  # Create this template