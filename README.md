# pyPixelfix
Takes all fully transparent pixels in a PNG and sets their colors to the nearest non-transparent pixel's color without altering their alpha value.

## Usage
This Python script works in a very simple manner, it takes all of it's arguments and, if they are valid image files, will overwrite them with a "pixelfixed" version.
- "Pixelfixing" a single image
```bash
python3 main.py example1.png
```

- "Pixelfixing" multiple image files
```bash
python3 main.py example1.png example2.png example3.png
```

## Based on:
- [Pixelfix](https://github.com/Corecii/Transparent-Pixel-Fix)

## License
- [GPL-3.0](https://choosealicense.com/licenses/gpl-3.0/)