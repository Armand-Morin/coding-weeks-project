import face_detect.emotions as emo
import face_detect.recognition as recog
import video_conversion.split as video
import progressbar as pb


def get_emotions(film_file):
    video.get_frames(film_file)
    widgets = [' Progress: ', pb.Percentage(), ' ', 
            pb.Bar(marker=pb.RotatingMarker()), ' ', pb.ETA()]
    timer = pb.ProgressBar(widgets=widgets, maxval=4).start()
    print("Getting files...")
    frames = recog.get_filenames('data')
    timer.update(1)
    print(" ")
    print("Using neural model...")
    predicted_emotions = emo.get_emotion_embeddings(frames)
    timer.update(2)
    print(" ")
    print("Counting different emotions...")
    emotions = emo.emotion_count(predicted_emotions)
    timer.update(3)
    print(" ")
    print("Generating emotion statistics...")
    res = []
    total = 0
    for i in range(7):
        total += emotions[i][1]
    for emotion in emotions:
        emotion[1] = round(100*emotion[1]/total, 1)
    timer.update(4)
    return emotions

# emotions = [0: 'angry', 1: 'disgust', 2: 'happy', 3: 'fear', 4: 'sad', 5: 'surprise', 6: 'neutral']

'''def get_genre(film_file):
    emotions = get_emotions(film_file)
    if emotions[2] >= 66:
        return print("Ce film est joyeux!")
    if emotions[3]+emotions[1]+emotions[0] >= 66:
        return print("Ce film va plutôt faire peur...")
    if emotions[4] >= 40:
        return print("Le film est assez triste.")'''

if __name__=='__main__':
    var = get_emotions('crazy_trailer.mov')
    print(var)