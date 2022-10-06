[TOC]

# ScaleTraining
用于熟悉乐器的协议

## 乐理
```bash
# 作曲挑战，随机key x 随机调式 x 随机重音
python3 main.py --train motive [--len <重音长度>] [--interval <旋律间距，默认包含所有音程>]
```

## 吉他
```bash
# 随机固定音，找出所有品位
python3 main.py --train string [--cps <速度 bpm>] [--rnd <多少轮，12个音为一轮>]  
```

## 蓝调口琴

### 素材
挑选小于2个半音的音集，生成csv，可以导入excel或者腾讯文档，进行索引

```bash
# 进行
python3 main.py --train blues_prog > prog.csv

# 和弦
python3 main.py --train blues_chord > chord.csv

# 音阶
python3 main.py --train blues_scale > scale.csv
```
