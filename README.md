# 软著代码自动生成PDF报告

## 功能
自动扫描代码目录，并输出PDF，，每页50行。如果超出600行，自动截取前后各300行代码。

## 推荐使用go版本
go编译好的，不需要下载第三方库，更方便

[软著代码自动生成PDF报告GO语言版本：https://github.com/gamefriends/sc_code2pdf_go](https://github.com/gamefriends/sc_code2pdf_go)

## 使用方法

将代码目录生成PDF文件，每页50行代码，支持中文。

```shell
options:
  -h, --help           show this help message and exit
  -i, --input INPUT    源代码目录路径
  -o, --output OUTPUT  保存PDF文件的路径
```

> 示例:

```shell
python3 code2pdf.py -i path/code_dir -p path/output.pdf
```
