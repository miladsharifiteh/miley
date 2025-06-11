# Miley - Simple Command Line Audio Player and Library Manager for Linux

### Video Demo:  https://youtu.be/Ta8q-cCsUYI

### Description:

#### Introduction

**Miley** is my final project for CS50P course from Harvard. It is a simple 
command-line audio player and library manager for Linux. It is written in 
Python and can play MP3, WAV, and FLAC files. **Miley** uses the 
"just_playback" library from "pypi" for playing and playback controls of 
tracks. Furthermore, it is designed to use simple CSV files for storing and 
managing audio libraries. Finally, although its capabilities are limited, 
basic operations needed for playing and managing audio files efficiently are 
included.

#### Python Requirements

The source code of **Miley** requires some of the "pypi" libraries to run.
These requirements are:

- wcmatch
- tinytag
- just_playback
- inputimeout

You can install them in a virtual Python environment with the command:

```python -m pip install wcmatch tinytag just_playback inputimeout```

> [!NOTE]
> If you use the binary distribution of the software, you don't need to install
> Python requirements as they are included in the binary file.

#### Source Content

Source folder and files:

- The "playlists" folder hosts all of the playlist CSV files you have created
using **Miley's** user interface.
- The "library.csv" file hosts all of the tracks you have loaded into the 
library using **Miley's** user interface.
- The "project.py" file is the actual source of the software Python code.
- The "README.md" file is the document you are reading now.
- The "requirements.txt" file includes the list of all Python external 
libraries mentioned in the previous section.
- The "test_project.py" file includes all of the test functions that the 
"pytest" module runs to test the software.
- The "miley" file is the binary for running the software without any concerns 
about Python and its requirements.

#### Design Philosophy

I have written **Miley** in a way that is function-based and modular. The 
source code of the software consists of 26 functions that are as minimal as 
possible in the task they do. Code clarity and conciseness have been my ideal 
approach in developing **Miley**; however, I believe that there is always a 
more acceptable result. Also, I believe that a good written software doesn't 
need comments.

#### Usage

To run the software from the source:
`python project.py`. To run the software from the binary file: `./miley`

When you run **Miley**, you are in the main UI of the software. The 
available commands in this stage are:

- `Help`, `HELP`, or `help` -> prints the software guidance.
- `library` -> prints the current library database.
- `playlists` -> prints playlist databases.
- `playlist:[playlist]` -> prints "playlist" database. example: 
`playlist:M-Jackson`.
- `create:[playlist]` -> creates a new empty "playlist", overwriting the 
existing one. example: `create:M-Jackson`. You can only use [a-Z], [0-9], 
underline, and hyphen in a playlist name.
- `play` -> starts to play the current library from the beginning to the end.
- `play:<[id]>` -> starts to play track number "id" from the library. example: 
`play:<10>`.
- `play:[args]` -> starts to play matched tracks from the library. see 
`args` at the end of the list for more information.
- `play:[playlist]:<>` -> starts to play "playlist" from the beginning to 
the end. example: `play:M-Jackson:<>`.
- `play:[playlist]:<[id]>` -> starts to play track number "id" from "playlist".
 example: `play:M-Jackson:<5>`.
- `play:[playlist]:[args]` -> starts to play matched tracks from "playlist". 
see `args` at the end of the list for more information.
- `add:[playlist]:<>` -> adds the entire library to "playlist". example: 
`add:Happy:<>`.
- `add:[playlist]:<[id]>` -> adds track number "id" from library to "playlist". 
example: `add:Happy:<3>`.
- `add:[playlist]>:[args]` -> adds the first matched track to "playlist". see 
`args` at the end of the list for more information.
- `remove:<>` -> removes the entire library.
- `remove:<[id]>` -> removes track number "id" from the library. example: 
`remove:<2>`.
- `remove:[args]` -> removes the first matched track from the library. see 
`args` at the end of the list for more information.
- `remove:[playlist]:<>` -> removes "playlist" from the database. example: 
`remove:Happy:<>`.
- `remove:[playlist]:<[id]>` -> removes track number "id" from "playlist". 
Example: `remove:M-Jackson:<7>`.
- `remove:[playlist]:[args]` -> removes the first matched track from 
"playlist". see `args` at the end of the list for more information.
- `load:[path]` -> loads tracks in "path" into the library. example: 
`load:/var/home/username/Music`.
- `load:[path]:all` -> loads tracks in "path" into the library recursively. 
example: `load:/home/username/Music:all`.
- `find:[args]` -> finds matched tracks in the library and/or playlists. 
see `args` at the end of the list for more information.
- `exit` or `quit` -> exits the application.
- `[args]` -> `[string]+[string]+...`. example: `sad+Moon+2+Rock and Roll`.

When **Miley** is playing a track, you are in the control UI of the software. 
The available commands in this stage are:

- `pause` -> pauses the playback.
- `resume` -> resumes the playback, refuses when the track is already playing.
- `seek-[seconds]` -> jumps to the "seconds" position of the track. example: 
`seek-100`.
- `stop` -> terminates the current playback and takes you to the main UI.
- `next` -> terminates the current playback and starts to play the next one.
- `prev` -> terminates the current playback and starts to play the previous 
one.
- `[item]` -> terminates the current playback and jumps to "item" in the 
playback list. example: `9`.

#### Appreciation

I want to thank D.J. Malan and the CS50 team for their years of effort and 
dedication to empower human resources around the world. Furthermore, 
I want to thank you for being here and testing my project.

**Have Fun**

> [!NOTE]
> This software is licensed under the MIT License.
