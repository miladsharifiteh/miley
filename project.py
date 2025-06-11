import os,csv,queue,time,threading,re
from sys import exit
from wcmatch.pathlib import Path
from tinytag import TinyTag
from just_playback import Playback
from inputimeout import inputimeout


def main():

    welcome()
    
    while True:

        prompt = console("Command -> | enter " +
                         "'help' for more information |: ").strip()
        
        commands = prompt.split(":")
        commands_len = len(commands)

        re_track = r"([\w()-][\w() -]*[+])*[\w()-][\w() -]*"
        re_listname = r"[\w-]+"
        re_path = r"[\w/()-][\w/() -]*"
        re_help = re.search("^help$|^Help$|^HELP$", prompt)
        re_library = re.search("^library$", prompt)
        re_playlists = re.search("^playlists$", prompt)
        re_playlist = re.search(f"^playlist:{re_listname}$", prompt)
        re_create = re.search(f"^create:{re_listname}$", prompt)

        re_play = re.search(f"^play$|^play:{re_track}$" +
                            f"|^play:{re_listname}:<>$|^play:{re_listname}" +
                            f":{re_track}$|^play:<[0-9]+>$|^play:" +
                            f"{re_listname}:<[0-9]+>$", prompt)

        re_add = re.search(f"^add:{re_listname}:<>$|^add:{re_listname}:" +
                           f"{re_track}$|^add:{re_listname}:<[0-9]+>$", prompt)

        re_remove = re.search(f"^remove:<>$|^remove:{re_track}$" +
                              f"|^remove:<[0-9]+>$|^remove:{re_listname}:" +
                              f"<[0-9]+>$|^remove:{re_listname}:<>$" +
                              f"|^remove:{re_listname}:{re_track}$", prompt)
        
        re_load = re.search(f"^load:{re_path}$|^load:{re_path}:all$", 
                                prompt)
        
        re_find = re.search(f"^find:{re_track}$", prompt)
        re_exit = re.search("^exit$|^quit$", prompt)

        args1, args2 = None, None

        if commands_len > 1:
            raw_args1 = commands[1].split("+")
            args1 = tuple(map(str.strip, raw_args1))
        if commands_len > 2:
            raw_args2 = commands[2].split("+")
            args2 = tuple(map(str.strip, raw_args2))
        
        if re_help:
            help()
        elif re_library:
            table("library.csv")
        elif re_playlists:
            table(None)
        elif re_playlist:
            table(args1[0])
        elif re_create:
            print(playlist_maker(args1[0]))
        elif re_play:
            print(play(args1, args2))
        elif re_add:
            print(add(args1, args2))
        elif re_remove:
            print(remove(args1, args2))
        elif re_load:
            print(load(args1[0], args2))
        elif re_find:
            find(args1)
        elif re_exit:
            finish()
        else:
            print("Please enter a valid command")
        print()


def welcome():

    print()
    print("<- Welcome to Miley Audio Player and Manager ->")
    separator()
    print()


def console(prompt):
    
    separator()
    command = input(prompt)
    separator()
    print()
    return command


def separator():

    print("------------------------------------")


def not_found():

    return "No track matched with parameters specified found"


def help():

    print("""Help:

    library -> prints the current library database
    playlists -> prints playlist databases
    playlist:[playlist] -> prints "playlist" database
    create:[playlist] -> creates a new empty "playlist"
    play -> starts to play the current library
    play:<[id]> -> starts to play track number "id" from the library
    play:[args] -> starts to play matched tracks from the library
    play:[playlist]:<> -> starts to play "playlist"
    play:[playlist]:<[id]> -> starts to play track number "id" from "playlist"
    play:[playlist]:[args] -> starts to play matched tracks from "playlist"
    add:[playlist]:<> -> adds the entire library to "playlist"
    add:[playlist]:<[id]> -> adds track number "id" from library to "playlist"
    add:[playlist]:[args] -> adds the first matched track to "playlist"
    remove:<> -> removes the entire library
    remove:<[id]> -> removes track number "id" from the library
    remove:[args] -> removes the first matched track from the library
    remove:[playlist]:<> -> removes "playlist" from the database
    remove:[playlist]:<[id]> -> removes track number "id" from "playlist"
    remove:[playlist]:[args] -> removes the first matched track from "playlist"
    load:[path] -> loads tracks in "path" into the library
    load:[path]:all -> loads tracks in "path" into the library recursively
    find:[args] -> finds matched tracks in the library and/or playlists
    help -> prints this information
    exit -> exits the application
    [args] -> [string]+[string]+...
    """, end="")


def table(csv_file):

    if not csv_file:
        print("Playlist Databases:")
        playlists = get_playlists()
        if playlists:
            print()
        for playlist in playlists:
            print(playlist[1])
            separator()
        return
    
    elif csv_file == "library.csv":
        path = csv_file
        print("Library Database:")

    else:
        found = False
        playlists = get_playlists()
        for playlist in playlists:
            if csv_file == playlist[1]:
                found = True
                path = f"playlists/{csv_file}.csv"
                print(f"Playlist '{csv_file}':")
                break
        if not found:
            print(f"No playlist with name '{csv_file}' found")
            return

    tracks = get_tracks(path)
    if tracks:
        print()
        separator()
        table_maker(path)


def table_maker(path):

    with open(path) as file:

        raw_tracks = csv.DictReader(file)
        tracks = tuple(raw_tracks)

        for track in tracks:
            print(f"ID: {track["ID"]} | Title: {track["Title"]} | Artist: " +
                  f"{track["Artist"]} | Album: {track["Album"]} | Track: " +
                  f"{track["Track"]} | Date: {track["Date"]} | Length: " +
                  f"{track["Length"]} | Path: {track["Path"]} | " +
                  f"Format: {track["Format"]}")
            separator()


def playlist_maker(filename):

    with open(f"playlists/{filename}.csv", "w") as file:

        writer = csv.writer(file)
        writer.writerow(get_headers())

    return f"Playlist '{filename}' is created"


def get_playlists():

    raw_files = os.listdir("playlists/")
    playlists = []

    for raw_file in raw_files:
        fullname = raw_file.split(".")
        if len(fullname) == 2 and fullname[1] == "csv":
            playlists.append((f"playlists/{raw_file}", fullname[0]))
            
    return tuple(playlists)


def play(args1, args2):

    queue = []
    path = None

    if not args1 or not args2:
        path = "library.csv"
        source = "Library"
        args = args1

    else:
        playlists = get_playlists()
        for playlist in playlists:
            if args1[0] == playlist[1]:
                path = playlist[0]
                source = f"'{playlist[1]}' playlist"
                break
        args = args2

        if not playlists:
            return "Your playlist database is empty"
        elif not path:
            return f"No playlist with name {args1[0]} found" 

    tracks = get_tracks(path)

    if not args1 or args2 and args2[0] == "<>":
        queue = list(tracks)
    
    else:
        for track in tracks:
            select = track_validator(track, args)
            if select[0]:
                queue.append(track)
                if select[1]:
                    break
    
    if not queue:
        return not_found()
    
    play_tracks(queue, source)
    return "Playback is finished"


def play_tracks(tracks, source):

    current = 0
    total = len(tracks)

    while 0 <= current < total:
        result = player(tracks[current], total, current + 1, source)
        if result == "stop":
            return
        elif result == "next":
            current += 1
        elif result == "prev":
            current -= 1
        elif result[0] == "skip":
            current = result[1] - 1


def player(track, total, current, source):

    separator()
    print(f"Playing {current} of {total} | Title: {track['Title']} | " +
          f"Artist: {track['Artist']} | Album: {track['Album']} | Track: " +
          f"{track['Track']} | Date: {track['Date']} | Length: " +
          f"{track['Length']} | Source: {source}")
    separator()

    playback = Playback()

    try:
        playback.load_file(track["Path"])
    except:
        print()
        print("Wrong file path (you may need to update the library " +
              "and/or playlists)")
        print()
        time.sleep(3)
        return "next"
    
    playback.play()
    control_queue = queue.Queue()
    control_thread = threading.Thread(target=control, args=(control_queue, 
                                      playback, total, current), daemon=True)
    control_thread.start()

    while playback.active:

        try:
            mediactl = control_queue.get(timeout=1)  
        except queue.Empty:
            continue
     
        match mediactl[0]:
            case "pause":
                playback.pause()
                print("Playback is paused")
                separator()
            case "resume":
                playback.resume()
                print("Playback is resumed")
                separator()
            case "seek":
                position = mediactl[1]
                playback.seek(position)
                print(f"Playback is seeked to position {position} seconds")
                separator()
            case "stop":
                playback.stop()
                print()
                return "stop"
            case "next":
                playback.stop()
                print("Next track is playing")
                separator()
                print()
                return "next"
            case "prev":
                playback.stop()
                print("Previous track is playing")
                separator()
                print()
                return "prev"
            case "skip":
                playback.stop()
                print(f"Item {mediactl[1]} is playing")
                separator()
                print()
                return ("skip", mediactl[1])
            case "current":
                print("Selected track is already playing")
                separator()
            case "out-of-range":
                print("Selected track is out of range")
                separator()
            case "out-of-position":
                print("Selected position is out of range")
                separator()
            case "not-paused":
                print("Playback is not paused")
                separator()
            case _:
                print("Please enter a valid command")
                separator()


def control(control_queue, playback, total, current):

    prompt = "Control -> | pause | resume | seek-position | stop | " + \
             "next | prev | item |: "
    option = None

    while True:

        if playback.paused:
            ctl = input(prompt).strip()
        else:
            try:
                timeout = playback.duration - playback.curr_pos
                ctl = inputimeout(prompt=prompt, timeout=timeout).strip()
            except Exception:
                separator()
                control_queue.put(("next", option))
                return

        re_seek = re.search("^seek-[0-9]+$", ctl)
        re_skip = re.search("^[0-9]+$", ctl)
        re_ctl = re.search("^pause$|^resume$|^stop$|^next$|^prev$", ctl)

        if re_seek:
            seek_command = ctl.split("-")
            ctl = seek_command[0]
            option = int(seek_command[1])
        
        elif re_skip:
            skip_command = ("skip", int(ctl))
            ctl = skip_command[0]
            option = skip_command[1]

        separator()

        if re_ctl or re_seek or re_skip:

            if (ctl == "next" and current + 1 > total) or \
               (ctl == "prev" and current - 1 < 1) or \
               (ctl == "skip" and (option > total or option == 0)):
                
                control_queue.put(("out-of-range", option))
            
            elif ctl == "skip" and option == current:
                control_queue.put(("current", option))
        
            elif ctl == "seek" and option >= playback.duration:
                control_queue.put(("out-of-position", option))

            elif ctl == "resume" and not playback.paused:
                control_queue.put(("not-paused", option))

            elif ctl in ("pause", "resume", "seek"):
                control_queue.put((ctl, option))

            else:
                control_queue.put((ctl, option))
                return

        else:
            control_queue.put(("invalid", option))

        time.sleep(1)


def get_tracks(path):

    with open(path) as file:

        raw_tracks = csv.DictReader(file)
        tracks = tuple(raw_tracks)

    return tracks


def add(args1, args2):

    tracks = get_tracks("library.csv")
    playlists = get_playlists()
    
    for playlist in playlists:
        if args1[0] == playlist[1]:
            id = get_last_id(playlist[0]) + 1

            with open(playlist[0], "a") as file:
                writer = csv.writer(file)
                if args2[0] == "<>":
                    if not tracks:
                        return "The library is empty"
                    for track in tracks:
                        writer.writerow([id] + list(track.values())[1:])
                        id += 1
                    return f"The entire library is added to '{args1[0]}' " + \
                            "playlist"
                else:
                    for track in tracks:
                        if track_validator(track, args2)[0]:
                            writer.writerow([id] + list(track.values())[1:])
                            return f"Track '{track["Title"]}' is added to " + \
                                   f"'{args1[0]}' playlist"
                        
                    return not_found() + " in the library"
                
    return f"No playlist with name '{args1[0]}' found"


def remove(args1, args2):
    
    playlists = get_playlists()
    
    if not args2:

        if args1[0] == "<>":
            with open("library.csv", "w") as file:
                writer_object = csv.DictWriter(file, fieldnames=get_headers())
                writer_object.writeheader()
            return "The library is wiped out"
        
        tracks = get_tracks("library.csv")
        track = remove_track("library.csv", tracks, args1)

        if track:
            return f"'{track}' track is removed from the library"
        return not_found() + " in the library"
         
    elif args1 and args2[0] == "<>":

        for playlist in playlists:
            if args1[0] == playlist[1]:
                os.remove(playlist[0])
                return f"Playlist '{args1[0]}' is removed"
        return f"No playlist with name '{args1[0]}' found"
    
    else:

        for playlist in playlists:
            if args1[0] == playlist[1]:
                tracks = get_tracks(playlist[0])
                track = remove_track(playlist[0], tracks, args2)
                if track:
                    return f"Track '{track}' is removed from " + \
                           f"'{args1[0]}' playlist"
                return not_found() + f" in '{args1[0]}' playlist"
        return f"No playlist with name '{args1[0]}' found"


def remove_track(path, tracks, args):

    is_removed = False
    
    with open(path, "w") as file:

        writer_object = csv.writer(file)
        writer_object.writerow(get_headers())

        for i in range(len(tracks)):

            if not is_removed and track_validator(tracks[i], args)[0]:
                is_removed = True
                result = tracks[i]

            else:
                id = i if is_removed else i + 1
                writer_object.writerow([id] + list(tracks[i].values())[1:])

        if is_removed:
            return result["Title"]
        
        return None


def load(path, arg):

    file_types = ["*.mp3", "*.MP3", "*.wav", "*.WAV", "*.flac", "*.FLAC"]
    updated = False
    id = get_last_id("library.csv") + 1

    with open("library.csv", "a") as file:
        if not path.endswith("/"):
            path = path + "/"
        if not arg:
            tracks = Path(path).glob(file_types)
        else:
            tracks = Path(path).rglob(file_types)
        
        for track in tracks:
            updated = True
            track = str(track)

            if os.path.isfile(track):
                file_type = track.split(".")[-1].lower()
                tags = TinyTag.get(track)

                if not tags.track:
                    album_track = "-"
                else:
                    album_track = tags.track

                metadata = [id, tags.title, tags.artist, tags.album, 
                            album_track, tags.year, 
                            f"{int(tags.duration / 60):02d}:" +
                            f"{int(tags.duration % 60):02d}", track, file_type]
                
                writer = csv.writer(file)
                writer.writerow(metadata)
                id += 1
    
    if updated:
        return "The library is updated"
    
    return "No audio file (mp3, wav, or flac) found"


def find(args):

    library_tracks = get_tracks("library.csv")
    playlists = get_playlists()

    count = track_finder(library_tracks, args, 0)

    for playlist in playlists:

        for arg in args:
            if arg.lower() in playlist[1].lower():
                print(f"Playlist '{playlist[1]}' found")
                separator()

        count = track_finder(get_tracks(playlist[0]), args, count, 
                             f"'{playlist[1]}' Playlist")

    
def track_finder(tracks, args, counted, source="Library"):

    for track in tracks:

        if track_validator(track, args)[0]:
            print(f"{counted + 1} | ID: {track["ID"]} | Title: " +
                  f"{track["Title"]} | Artist: {track["Artist"]} | " +
                  f"Album: {track["Album"]} | Track: {track["Track"]} " +
                  f"| Date: {track["Date"]} | Length: {track["Length"]} | " +
                  f"Source: {source}")
            separator()
            counted += 1
    
    return counted


def track_validator(track, args):

    if args[0][0] == "<":
        id = args[0][1:-1]
        if id == track["ID"]:
            return (True, True)
        return (False, True)

    for arg in args:

        if not arg.lower() in track["Title"].lower() and \
           not arg.lower() in track["Artist"].lower() and \
           not arg.lower() in track["Album"].lower() and \
           not arg == track["Date"] and \
           not arg == track["Track"] and \
           not arg == track_name(track["Path"]) and \
           not arg == track["Format"]:
            
            return (False, False)
    
    return (True, False)


def track_name(path):

    try:
        name = path.split("/")[-1].split(".")[0]
    except:
        name = path.split(".")[0]

    return name


def get_headers():

    headers = ("ID", "Title", "Artist", "Album", "Track", "Date", "Length", 
               "Path", "Format")
    return headers


def get_last_id(path):
    
    id = -1
    with open(path, "r") as file:
        reader = csv.reader(file)
        for line in reader:
            id += 1
    return id


def finish():

    exit("Have a nice day!\n")


if __name__ == "__main__":
    main()
