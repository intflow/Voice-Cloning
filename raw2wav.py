from utils.argutils import print_args
from pathlib import Path
import argparse
import sys
import wave
import os
from itertools import chain
from tqdm import tqdm


def raw2wav(input_dirs):
    folders = list(chain.from_iterable(input_dir.glob("*") for input_dir in input_dirs))

    for folder in tqdm(folders, "folders", len(folders), unit="folders"):
        for file in folder.glob("*"):
            audio_list = list()
            if str(file).endswith(".pcm") or str(file).endswith(".raw"):
                audio_list.append(os.path.join(dataset_root, folder, file))

            for audio in audio_list:
                with open(audio, 'rb') as pcmfile:
                    pcmdata = pcmfile.read()

                    audio_file = audio.split("\\")[-1]

                    wavfile = wave.open(audio[:-4] + ".wav", 'wb')
                    wavfile.setparams((1, 2, 16000, 0, 'NONE', 'NONE'))
                    wavfile.writeframes(pcmdata)
                    wavfile.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="pcm, raw 확장자 파일을 wav확장자로 변환",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument("path", type=str, help="처리할 폴더 경로")
    args = parser.parse_args()

    dataset_root = Path(args.path)
    input_dirs = [dataset_root.joinpath("KsponSpeech_01"),
                  dataset_root.joinpath("KsponSpeech_02"),
                  dataset_root.joinpath("KsponSpeech_03"),
                  dataset_root.joinpath("KsponSpeech_04"),
                  dataset_root.joinpath("KsponSpeech_05")]
    raw2wav(input_dirs)
