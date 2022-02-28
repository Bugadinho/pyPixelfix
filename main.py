import os
import time
import argparse
from PIL import Image
from pixelfix import PixelFix

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Takes all fully transparent pixels in a PNG and sets their colors to the nearest non-transparent pixel\'s color without altering their alpha value.')
    parser.add_argument('path', nargs='+', help='Path of the files')
    parser.add_argument('-t', '--threshold',
                        type=int, default=0,
                        choices=range(0, 255),
                        metavar="[0-254]",
                        help='maximum alpha value to fix (default: 0)')
    args = parser.parse_args()

    for path in args.path:
        print('Processing \'{}\'...'.format(path), end=' ', flush=True)
        full_path = os.path.join(os.getcwd(), path)
        if os.path.isfile(full_path):
            start_time = time.time()
            try:
                image = Image.open(full_path)
                try:
                    new_image = PixelFix(image, args.threshold)
                    try:
                        new_image.save(full_path)
                        end_time = time.time()
                        print('{:.2f}s'.format(end_time - start_time))
                    except:
                        print('Error while saving image!')
                except:
                    print('Error while fixing image!')
            except:
                print('Error while opening image!')
        else:
            print('Invalid file!')