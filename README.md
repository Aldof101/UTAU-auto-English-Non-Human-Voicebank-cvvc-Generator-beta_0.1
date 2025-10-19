UTAU English Non-Human Voicebank (Non-Hiological Voicebank) CVVC Automatic Maker ver1.0

This automatic tool is based on the English CVVC recording list for SaKe's ARPAsing, which I have supplemented. I have more than doubled the number of recording entries from the original list's 59 entries. The supplemented recording list is included in the compressed package; you can view it yourself.

This recording list uses the ARPABET phonetic system. To use an English voicebank created with this script, please select the ARPA phonemizer in OpenUtau. It is not recommended for use in the original UTAU. Before using, please search for and learn about the ARPABET phonetic system. Simply put, it is a representation of the International Phonetic Alphabet using letters.

The "vowels" folder contains the 12 vowels you need to prepare. I will briefly explain how to produce these vowels later.

The audio for all following operations should be mono, 44100Hz, 16-bit.

Open "autoeng.py" with a text editor like Notepad, find and copy the following lines:
consonant_dirs = [ r"this\is\StandardC", r"this\is\addC" ] vowel_dir = r"this\is\vowels" output_dir = r"this\is\output_test"
Change them to the paths for "StandardC" (the consonants used in the original recording list), "addC" (the consonants required for the entries I added), "vowels" (the vowel path), and "output_test" (the output directory; you can change this to your desired path. If you are not very familiar with using it yet, you can change it to "output_test" first, save the file, and test using the He Yu_English vowels included in the package) respectively.

Download link for the formant filter plugin mentioned below: https://kilohearts.com/products/formant_filter

Regarding the combinations mentioned below: In your Digital Audio Workstation (DAW), create a new multitrack file. Use the default linear or cosine crossfade to splice two audio clips together on the same track for combination.

In the "vowels" folder, 5 are the Japanese vowels: a.wav, i.wav, u.wav, e.wav, o.wav. The remaining ones are: ai.wav (pronounced /aɪ/, combine a.wav and i.wav), ax.wav (pronounced /ə/, obtained by adjusting the formants of o.wav using the plugin), ei.wav (pronounced /eɪ/, combine e.wav and i.wav), er.wav (pronounced /ər/, combine e.wav and r-.wav from the consonant folder), ew.wav (pronounced /ɛw/, combine ax.wav and u.wav), oi.wav (pronounced /ɔɪ/, combine o.wav and i.wav), ou.wav (pronounced /ɔɪ/, combine o.wav and i.wav).

After completing the above, run "autoeng.py". After the process finishes, please copy and paste all the consonants from the "ALSO COPY THESE TO YOUR OUTPUT LIBRARY" folder into your output folder. They are necessary, separate phonemes that participate together in oto.ini creation and English synthesis.

Finally, drag the entire main output folder onto "moresampler.exe" to automatically create the oto.ini.

If you are unfamiliar with vowel pronunciation, the "vowels" folder includes a set of "He Yu_English" vowels for your reference and testing. Once familiar, you can replace them with your own files. If you want to download and study or use the He Yu_English voicebank, please visit: https://bowlroll.net/file/342677

English Non-Human Voicebank Demos:
【【Wei Ming_English】Duvet】 https://www.bilibili.com/video/BV1vUn5zBEZu/?
share_source=copy_web&vd_source=f6b117b0ee0fa920209a4fadd80d60e6
【【He Yu_English】Trigonometric Functions【UTAU cover+UST】】 https://www.bilibili.com/video/BV1uxnzzhEHY/?share_source=copy_web&vd_source=f6b117b0ee0fa920209a4fadd80d60e6

This script is open source and is intended only for the creation and learning reference of non-human voicebanks. Commercial use and illegal use are prohibited. By Aldof

