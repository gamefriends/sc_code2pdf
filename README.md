# 软著代码自动生成PDF报告

## 功能
自动扫描代码目录，如果超出60行，自动截取前后各300行代码，每页50行。

## 使用方法

将代码目录生成PDF文件，每页50行代码，支持中文

```shell
options:
  -h, --help           show this help message and exit
  -i, --input INPUT    源代码目录路径
  -o, --output OUTPUT  保存PDF文件的路径
```

```shell

# 示例:
python3 code2pdf.py -i path/code_dir -p path/output.pdf
```
