from pydub import AudioSegment
 
sound=AudioSegment.from_wav('chopin.wav')
sounds = sound.split_to_mono()

sounds[0].export('chopin_left.wav')
sounds[1].export('chopin_right.wav')