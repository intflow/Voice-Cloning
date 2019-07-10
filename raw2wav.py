import sys
import wave
import os

path = "F:\VoiceDataset\KOR\KorEng/"
speaker_list = os.listdir(path)
for folder in speaker_list:
    files = os.listdir(os.path.join(path, folder))
    audio_list = list()
    for f in files:
        if f.endswith(".pcm") or f.endswith(".raw"):
            audio_list.append(os.path.join(path, folder, f))

    for audio in audio_list:
        with open(audio, 'rb') as pcmfile:
            pcmdata = pcmfile.read()


            audio_file = audio.split("\\")[-1]

            print(audio[:-4] + ".wav")
            print()

            wavfile = wave.open(audio[:-4] + ".wav", 'wb')
            wavfile.setparams((1, 2, 16000, 0, 'NONE', 'NONE'))
            wavfile.writeframes(pcmdata)
            wavfile.close()
