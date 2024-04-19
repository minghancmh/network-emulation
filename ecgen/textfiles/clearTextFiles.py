import glob, os
for f in glob.glob("sampleText*.txt"):
    os.remove(f)