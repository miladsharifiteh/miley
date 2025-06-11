from project import get_last_id,track_name,track_validator,add


def test_get_last_id():
    
    assert get_last_id("playlists/Sample.csv") == 136


def test_track_name():
    
    assert track_name("path/to/the/track/sample_track.mp3") == "sample_track"
    assert track_name("path/to/the/track/sample_track$.wav") == "sample_track$"
    assert track_name("path/to/the/track/@sample_track.flac") \
    == "@sample_track"


def test_track_validator():
    
    assert track_validator({"ID": "1", "Title": "Test Title", "Artist": 
                            "Test Artist", "Album": "Test Album", 
                            "Track": "2", "Date": "1000", "Length": 
                            "10:00", "Path": "/path/file.flac", "Format": 
                            "flac"}, ("<1>",)) == (True, True)
    
    assert track_validator({"ID": "1", "Title": "Test Title", "Artist": 
                            "Test Artist", "Album": "Test Album", 
                            "Track": "2", "Date": "1000", "Length": 
                            "10:00", "Path": "/path/file.flac", "Format": 
                            "flac"}, ("<10>",)) == (False, True)
    
    assert track_validator({"ID": "1", "Title": "Test Title", "Artist": 
                            "Test Artist", "Album": "Test Album", 
                            "Track": "2", "Date": "1000", "Length": 
                            "10:00", "Path": "/path/file.flac", "Format": 
                            "flac"}, ("Sample", "Music")) == (False, False)
    
    assert track_validator({"ID": "1", "Title": "Test Title", "Artist": 
                            "Test Artist", "Album": "Test Album", 
                            "Track": "2", "Date": "1000", "Length": 
                            "10:00", "Path": "/path/file.flac", "Format": 
                            "flac"}, ("1000", "test", "wav")) == (False, False)
    
    assert track_validator({"ID": "1", "Title": "Test Title", "Artist": 
                            "Test Artist", "Album": "Test Album", 
                            "Track": "2", "Date": "1000", "Length": 
                            "10:00", "Path": "/path/file.flac", "Format": 
                            "flac"}, ("flac", "test", "2")) == (True, False)


def test_add():
    
    assert add(("Sample",), ("<>",)) == "The library is empty"
    assert add(("Sample",), ("music",)) == ("No track matched with param" + 
                                            "eters specified found in the " +
                                            "library")
    
    assert add(("Test",), ("music", "country")) == ("No playlist with name" +
                                                    " 'Test' found")
