from utils.argutils import print_args
from pathlib import Path
import argparse
import sys
import wave
import os
from itertools import chain
from tqdm import tqdm
import re


# def raw2wav(input_dirs):
#     folders = list(chain.from_iterable(input_dir.glob("*") for input_dir in input_dirs))
#
#     for folder in tqdm(folders, "folders", len(folders), unit="folders"):
#         for file in folder.glob("*"):
#             audio_list = list()
#             if str(file).endswith(".pcm") or str(file).endswith(".raw"):
#                 audio_list.append(os.path.join(dataset_root, folder, file))
#
#             for audio in audio_list:
#                 with open(audio, 'rb') as pcmfile:
#                     pcmdata = pcmfile.read()
#
#                     audio_file = audio.split("\\")[-1]
#
#                     wavfile = wave.open(audio[:-4] + ".wav", 'wb')
#                     wavfile.setparams((1, 2, 16000, 0, 'NONE', 'NONE'))
#                     wavfile.writeframes(pcmdata)
#                     wavfile.close()

def preprocess_kspon(input_dirs):
    folders = list(chain.from_iterable(input_dir.glob("*") for input_dir in input_dirs))

    for folder in tqdm(folders, "folders", len(folders), unit="folders"):
        texts = list()
        symbol = ["o/", "b/", "l/", "n/", "u/", "+", "*", "(", "/"]
        punctuation = ["  ", ".", "?", "!"]
        white = [" ", "  ", ",,", ",,,"]

        existing_fnames = list()
        for file in folder.glob("*"):
            existing_fnames.append(file)

            # #Preprocessing Audio
            # for file in folder.glob("*"):
            #     audio_list = list()
            #     if str(file).endswith(".pcm"):
            #         audio_list.append(file)
            #
            #     for audio in audio_list:
            #         audio=str(audio)
            #         wavfile = "".join(audio.split(".")[:-1]) + ".wav"
            #         if Path(wavfile) in existing_fnames:
            #             continue
            #         else:
            #             with open(audio, 'rb') as pcmfile:
            #                 pcmdata = pcmfile.read()
            #
            #                 wavfile = wave.open(wavfile, 'wb')
            #                 wavfile.setparams((1, 2, 16000, 0, 'NONE', 'NONE'))
            #                 wavfile.writeframes(pcmdata)
            #                 wavfile.close()

            if str(file).endswith(".txt") and not str(file).endswith("alignment.txt"):
                s = os.path.splitext(file)  # 확장자와 확장자 아닌부분
                s = os.path.split(s[0])  # 확장자아닌 부분에서 분리

                with open(file, "r", encoding='utf-8') as f:
                    texts.append(s[1] + "$\"" + "|" + " ".join(f.read().splitlines()) + "|" + "\"\n")

        for i, text in enumerate(texts):
            text = re.sub('\)\/\([가-힣\s\w]*\)', "", text)
            for sym in symbol:
                text = text.replace(sym, "")
            for pun in punctuation:
                text = text.replace(pun, " ")
            for wh in white:
                text = text.replace(wh, ",")
            text = text.replace("$", " ")
            text = text.replace("|", ",")
            text = text.replace(",,", ",")
            texts[i] = text
        with open(os.path.join(folder, os.path.basename(folder) + "_alignment.txt"), "w", encoding='utf-8') as a:
            for text in texts:
                a.write(text)


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

    preprocess_kspon(input_dirs)
