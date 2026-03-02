from moviepy.editor import VideoFileClip, concatenate_videoclips
import os
import uuid


def ghep_video(video_paths, output_folder="outputs"):
    os.makedirs(output_folder, exist_ok=True)

    output_path = os.path.join(
        output_folder,
        f"output_{uuid.uuid4().hex}.mp4"
    )

    clips = []

    for path in video_paths:
        clips.append(VideoFileClip(path))

    final = concatenate_videoclips(clips)

    final.write_videofile(
        output_path,
        codec="libx264",
        audio_codec="aac"
    )

    return output_path