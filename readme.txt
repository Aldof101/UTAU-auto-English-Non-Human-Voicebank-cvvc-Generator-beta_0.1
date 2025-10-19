UTAU英语无中之人（无生物音源）CVVC自动制作工具ver1.0
这个自动工具基于我补充后的SaKe的ARPAsing的英语CVVC录音表，我在这个录音表原表59条的基础上增加了一倍多的录音条目，增加后的录音表在压缩包内，可以自行查看。
这个录音表采用ARPABET音标系统，要使用这个脚本制作的英语音源，请在openutau中选择ARPA音素器。不推荐在原版utau中使用。在使用之前，请您搜索并了解ARPABET音标。简单来说，它是国际音标转换成字母的形式。
vowels文件夹里就是您需要准备的12个元音。稍后我会简要说明这些元音如何制作。

以下所有操作的音频均为单声道, 44100Hz, 16位。

记事本或者文本编辑器打开autoeng.py，复制搜索如下的这几行。
consonant_dirs = [
        r"this\is\StandardC",
        r"this\is\addC"
    ]
    vowel_dir = r"this\is\vowels"
    output_dir = r"this\is\output_test"
分别改为压缩包内的StandardC（原录音表中使用的辅音）、addC（我增加的条目中需要的辅音）、vowels（元音路径）和output_test（输出可以改成您自己需要的路径，如果您还不太熟悉使用，可以先改成output_test，保存，使用包内自带的何雨_English元音进行测试）


以下提到的共振峰过滤插件（简称插件）的下载地址：https://kilohearts.com/products/formant_filter
以下提到的组合，可以在音频处理的宿主软件（DAW）中，新建多轨文件，使用默认的线性或余弦交叉淡化，在同一个轨道上拼接两个音频进行组合。


在vowels中，5个为日语的a.wav, i.wav, u.wav, e.wav, o.wav，剩下的则为ai.wav（发音/aɪ/，用a.wav和i.wav组合）, ax.wav（发音/ə/，通过插件调整o.wav的共振峰得到）, ei.wav（发音/eɪ/，用e.wav和i.wav组合）, er.wav（发音/ər/，用e.wav和辅音文件夹里的r-.wav组合）, ew.wav（发音/ɛw/，用ax.wav和u.wav组合）, oi.wav（发音/ɔɪ/，用o.wav和i.wav组合）, ou.wav（发音/ɔɪ/，用o.wav和i.wav组合）
在以上做好后，运行autoeng.py。运行完毕后，请把ALSO COPY THESE TO YOUR OUTPUT LIBRARY这个文件夹中的所有辅音复制粘贴到您的输出文件夹里，它们作为单独的、必需的音素一起参与oto制作和英语合成。
最后，请把这个总的文件夹一起拖动给moresampler.exe自动制作oto.ini。

如果您不熟悉元音发音，vowels里自带了一套何雨_English的元音，供您的参考和测试用。在熟悉后，您可以替换成您自己的文件。如果您想下载研究或是使用何雨_English音源，请访问https://bowlroll.net/file/342677

英语无中之人音源试听：
【【魏明_English】Duvet】 https://www.bilibili.com/video/BV1vUn5zBEZu/?
share_source=copy_web&vd_source=f6b117b0ee0fa920209a4fadd80d60e6
【【何雨_English】Trigonometric Functions/三角函数之歌【UTAU cover+UST】】 https://www.bilibili.com/video/BV1uxnzzhEHY/?share_source=copy_web&vd_source=f6b117b0ee0fa920209a4fadd80d60e6

此脚本开源，仅供无中之人音源的制作和学习参考用，禁止用于商业和非法用途。By Aldof


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


UTAU英語 無中之人（無生物音源）CVVC 自動制作ツール ver1.0

この自動ツールは、私が追加補完したSaKeのARPAsing用英語CVVC録音リストに基づいています。私は元の録音リストの59エントリから、2倍以上に録音エントリを増やしました。追加後の録音リストは圧縮パッケージ内に同梱されていますので、ご自身で確認してください。

この録音リストはARPABET音標システムを採用しています。このスクリプトで作成された英語音源を使用するには、openutauでARPA音素器を選択してください。原版UTAUでの使用は推奨しません。使用前に、ARPABET音標について検索して学んでください。簡単に言えば、国際音声記号を文字に変換した形式です。

「vowels」フォルダ内には、準備が必要な12の母音が入ります。後ほど、これらの母音の作り方を簡単に説明します。

以下全ての操作におけるオーディオは、モノラル、44100Hz、16ビットです。

メモ帳やテキストエディタで「autoeng.py」を開き、以下の行を探してコピーします。
consonant_dirs = [ r"this\is\StandardC", r"this\is\addC" ] vowel_dir = r"this\is\vowels" output_dir = r"this\is\output_test"
それぞれ、圧縮包内の「StandardC」（原録音リストで使用された子音）、「addC」（私が追加したエントリに必要な子音）、「vowels」（母音のパス）、「output_test」（出力先。ご自身の必要なパスに変更できます。まだ使い慣れていない場合は、まず「output_test」のままにして保存し、パッケージに同梱の何雨_English母音を使用してテストしてください）に変更してください。

以下で言及されているフォルマントフィルタープラグイン（略してプラグイン）のダウンロード先： https://kilohearts.com/products/formant_filter

以下で言及されている組み合わせについては、オーディオ処理のDAWソフトウェアで、新しいマルチトラックファイルを作成し、デフォルトのリニアまたはコサインクロスフェードを使用し、同一トラック上で2つのオーディオをスプライスして組み合わせることができます。

「vowels」内の5つは、日本語の a.wav, i.wav, u.wav, e.wav, o.wav です。残りは、ai.wav（発音 /aɪ/、a.wav と i.wav を組み合わせて作成）、ax.wav（発音 /ə/、プラグインを使用して o.wav のフォルマントを調整して得到）、ei.wav（発音 /eɪ/、e.wav と i.wav を組み合わせて作成）、er.wav（発音 /ər/、e.wav と子音フォルダ内の r-.wav を組み合わせて作成）、ew.wav（発音 /ɛw/、ax.wav と u.wav を組み合わせて作成）、oi.wav（発音 /ɔɪ/、o.wav と i.wav を組み合わせて作成）、ou.wav（発音 /ɔɪ/、o.wav と i.wav を組み合わせて作成）です。

以上が完了したら、「autoeng.py」を実行してください。実行が完了したら、「ALSO COPY THESE TO YOUR OUTPUT LIBRARY」フォルダ内の全ての子音を、あなたの出力フォルダにコピー＆ペーストしてください。これらは、単独の必須音素として、oto.iniの作成と英語合成に一緒に参加します。

最後に、この出力されたメインフォルダ全体を「moresampler.exe」にドラッグして、oto.iniを自動制作してください。

母音の発音に慣れていない場合、「vowels」フォルダ内には「何雨_English」の母音セットが同梱されており、参考およびテスト用としてご利用いただけます。慣れた後、ご自身のファイルに置き換えることができます。何雨_English音源をダウンロードして研究または使用したい場合は、https://bowlroll.net/file/342677 にアクセスしてください。

英語無中人音源試聴：
【【魏明_English】Duvet】 https://www.bilibili.com/video/BV1vUn5zBEZu/?
share_source=copy_web&vd_source=f6b117b0ee0fa920209a4fadd80d60e6
【【何雨_English】Trigonometric Functions/三角函数之歌【UTAU cover+UST】】 https://www.bilibili.com/video/BV1uxnzzhEHY/?share_source=copy_web&vd_source=f6b117b0ee0fa920209a4fadd80d60e6

このスクリプトはオープンソースです。無中人音源の制作および学習参考のみを目的としており、商業用途および違法な用途への使用を禁止します。By Aldof