# hoto-exif-framer

一个给照片自动添加水印、边框及 EXIF 信息的 Python 脚本。

A Python script that automatically adds border and EXIF information to images.

## 示例 / Example

![](https://cdn.jsdelivr.net/gh/Fidelxyz/PicBed@latest/20210724155409.jpg)

## 用法 / Usage

```bash
python photo-exif-framer <inputfile> [outputfile]
```

### 参数 / Parameters

`<inputfile>`: 输入图片的路径。The path of the input image.

`[outputfile]`: 【可选】输出图片的路径。若为空，则默认为相同目录下输入文件名的后缀名前添加`.out`。[Optional] The path of the output file. If empty, the default is to add `.out` to the suffix of the input file name in the same directory.

### 配置 / Configuration

**在 `photo-exif.framer.py` 开头处可进行配置。**

`border_percentage`: 边框占图片大小百分比。边框宽度等于 `border_percentage` 乘以输入图片的宽度和高度中的**最大值**。The border as a percentage of the image size. The border width is equal to `border_percentage` multiplied by the **maximum** of the width and height of the input image.

`exif_font`: EXIF 信息的字体文件路径。The path to the font file of the EXIF information.

`watermark_font`: 水印文字的字体文件路径。The path to the font file of the watermark text.

`watermark_text`: 水印文字内容。Watermark text content.

## 版权相关 / Copyright Notice

**使用时请遵守相关协议。**

**Please observe the relevant agreement when using it. **

`HarmonyOS Sans SC` 和 `HarmonyOS Sans Condensed` 在本项目中被用作默认字体。

`HarmonyOS Sans SC` and `HarmonyOS Sans Condensed` are used as default fonts in this project.

依赖 / Dependence：

- ExifRead
- Pillow

详见 `requirements.txt`。

See `requirements.txt` for details.