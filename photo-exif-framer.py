from PIL import Image, ImageDraw, ImageFont
import sys
import re
import exifread

border_percentage = 0.02
exif_font = 'font/HarmonyOS_Sans_Condensed_Bold.ttf'
watermark_font = 'font/HarmonyOS_Sans_SC_Bold.ttf'
watermark_text = '@Fidel'


class GetExif:
    def __init__(self, filename):
        self.tags = {}
        with open(filename, 'rb') as f:
            self.tags = exifread.process_file(f, details=False)

    def get(self, key, pattern='%s  '):
        if key not in self.tags.keys():
            return ''
        return pattern % str(self.tags[key])


def get_font_size(font_height, text='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'):
    l, r = 1, 500
    while l + 1 < r:
        mid = (l + r) // 2
        if ImageFont.truetype(exif_font, mid).getsize(text)[1] < font_height:
            l = mid + 1
        else:
            r = mid - 1
    return r if ImageFont.truetype(exif_font, r).getsize(text)[1] <= font_height else l


def work(filename_in, filename_out=''):
    # Process output image name
    if filename_out == '':
        filename_out = re.sub(r'\.([^.]+$)', r'.out.\1', filename_in)
        if filename_out == filename_in:
            filename_out = f'{filename_in}.out'

    # Read image
    img = Image.open(filename_in)

    # Calculate new size
    (w_in, h_in) = img.size
    border = int(border_percentage * max(img.size))
    w_out = int(w_in + border * 2)
    h_out = int(h_in + border * 5.5)

    # Create output image
    img_out = Image.new('RGB', (w_out, h_out), 'white')
    img_out.paste(img, (border, border))

    # Read EXIF
    exif = GetExif(filename_in)
    shutter = exif.get('EXIF ExposureTime', '%s sec  ')
    aperture = exif.get('EXIF FNumber', '%s')
    aperture = f'f/{eval(aperture)}  ' if aperture else ''
    iso = exif.get('EXIF ISOSpeedRatings', 'ISO %s  ')
    focal_length = exif.get('EXIF FocalLength', '%smm  ')
    time = exif.get('Image DateTime', '%s  ')
    brand = exif.get('Image Make', '%s ')
    model = exif.get('Image Model', '%s  ')
    brand = brand if model.find(brand) == -1 else ''
    lens = exif.get('EXIF LensModel', '%s  ')

    # Draw EXIF
    font = ImageFont.truetype(exif_font, size=get_font_size(border * 1.3))
    draw = ImageDraw.Draw(img_out)
    draw.text((border * 1.5, border * 1.75 + h_in), shutter + aperture + iso + focal_length, fill=0, font=font)
    draw.text((border * 1.5, border * 3.5 + h_in), time, fill='hsl(0, 0%, 60%)', font=font)
    draw.text((border * 1.5 + w_in * 0.6, border * 1.75 + h_in), brand + model, fill=0, font=font)
    draw.text((border * 1.5 + w_in * 0.6, border * 3.5 + h_in), lens, fill='hsl(0, 0%, 60%)', font=font)

    # Draw watermark
    img_watermark = Image.new('RGBA', img_out.size, (0, 0, 0, 0))
    font = ImageFont.truetype(watermark_font, size=get_font_size(border * 1.3, watermark_text))
    draw = ImageDraw.Draw(img_watermark)
    draw.text((border * 1.5, h_in - border), watermark_text, fill=(255, 255, 255, 128), font=font)
    img_out = Image.alpha_composite(img_out.convert('RGBA'), img_watermark)

    img_out = img_out.convert('RGB')
    img_out.save(filename_out, 'JPEG', quality=95)


if __name__ == '__main__':
    work(*sys.argv[1:])
