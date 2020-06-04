from pydub import AudioSegment
import sys

sound=AudioSegment.from_wav(sys.argv[1])
sounds = sound.split_to_mono()

sounds[0].export(sys.argv[1].split('.')[0] + '_left.wav', format="wav")
sounds[1].export(sys.argv[1].split('.')[0] + '_right.wav', format="wav")