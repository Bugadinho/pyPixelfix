import sys
import time
from PIL import Image
from pixelfix import pixelFix

if len(sys.argv) <= 1:
    sys.exit("A file was expected!")

print("Beginning processing...")

for file in sys.argv[1:]:
    startTime = time.time()
    image = Image.open(file)
    newImage = pixelFix(image)
    newImage.save(file)
    endTime = time.time()
    print("Done processing " + file + ". Took " + str(endTime - startTime) + " seconds!")