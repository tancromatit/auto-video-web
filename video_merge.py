from moviepy.editor import VideoFileClip, concatenate_videoclips

def ghep_video(video_paths, output):
    clips = []

    for path in video_paths:
        clips.append(VideoFileClip(path))

    final = concatenate_videoclips(clips)
    final.write_videofile(output)

    for c in clips:
        c.close()

    final.close()