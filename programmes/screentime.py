import face_detect.recognition as recog
import stats.basic_stats as stats
import video_conversion.split as video
import utils.load_info as info
import progressbar as pb
import affichage.creationPdf as crea


def get_screentime(film_name, film_file):
    characters = info.create_character_list(film_name)
    video.get_frames(film_file)
    widgets = [' Progress: ', pb.Percentage(), ' ', 
            pb.Bar(marker=pb.RotatingMarker()), ' ', pb.ETA()]
    timer = pb.ProgressBar(widgets=widgets, maxval=5).start()
    print("Getting files...")
    frames = recog.get_filenames('data')
    timer.update(1)
    print(" ")
    print("Using neural model...")
    film_embed = recog.get_embeddings(frames)
    timer.update(2)
    charact_embed = recog.get_charac_embed(characters)
    timer.update(3)
    print(" ")
    print("Linking to characters and counting frames...")
    recog.frame_charac_count(characters, film_embed, charact_embed)
    timer.update(4)
    print(" ")
    print("Generating character list...")
    res = []
    for character in characters:
        res.append([character[0], character[1], stats.screentime(character[2])])
    timer.update(5)
    return res

def get_screenshare(characters):
    runtime = 0
    for character in characters:
        runtime += character[2]
    for character in characters:
        character[2]=stats.screenshare(character[2], runtime)

def get_ethnic_screentime(characters):
    runtime = 0
    for character in characters:
        runtime += character[2]
    return stats.ethnic_screenshare(characters, runtime)

def get_female_screentime(characters):
    runtime = 0
    for character in characters:
        runtime += character[2]
    return stats.female_screenshare(characters, runtime)

def final(characters):
    crea.resultat(characters, get_female_screentime(characters),get_ethnic_screentime(characters))

if __name__ == "__main__":
    result = get_screentime('La_La_Land', 'La_La_Land.mov')
    print(result)
    pass

