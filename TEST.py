import os
import re
import numpy as np

path = r"F:\VoiceDataset\KSponSpeech\KsponSpeech_01/"
txt = "KsponSpeech_0001.txt"

with open(path + txt, "r", encoding='utf-8') as f:
    symbol = ["o/", "b/", "l/", "n/", "u/", "+", "*", "(", "/"]
    punctuation = ["  ", ",", ".", "?", "!"]
    texts = f.readlines()
    print(len(texts))
    for i, text in enumerate(texts):
        text = re.sub('\)\/\([가-힣\s\w]*\)', "", text)
        for sym in symbol:
            text = text.replace(sym, "")
        for pun in punctuation:
            text = text.replace(pun, " ")
        while text[0] == " ":
            text = text[1:]
        texts[i] = text


with open(path + "alignment.txt", "w", encoding='utf-8') as f:
    for text in texts:
        f.write(text)
        print(text)
