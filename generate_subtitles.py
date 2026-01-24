import pysrt

script = open("output/script.txt", encoding="utf-8").read()
sentences = [s.strip() for s in script.split("।") if s.strip()]

subs = pysrt.SubRipFile()
time = 0

for i, s in enumerate(sentences, start=1):
    subs.append(
        pysrt.SubRipItem(
            index=i,
            start=pysrt.SubRipTime(seconds=time),
            end=pysrt.SubRipTime(seconds=time+3),
            text=s
        )
    )
    time += 3

subs.save("output/subs.srt")
