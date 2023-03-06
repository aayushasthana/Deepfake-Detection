# Deepfake-Detection

 
usage: main.py [-h] -c COUNT -n FRAMECOUNT -j JSON -t TEST [-r RESULTS]
> python main.py -c 100 -n -1 -j metadata.json -t "face" -r results.txt

--Log of run with MTCNN facedetection and embedded RSA signature comparision--

Metadata Count = 1591, Count = 5
Video name : hntguogkqd.mp4 Frame count 299
Detecting Face:  35%|███▌      | 105/299 [00:22<00:40,  4.84it/s]*
Detecting Face:  55%|█████▌    | 165/299 [00:34<00:27,  4.87it/s]*
Detecting Face: 100%|██████████| 299/299 [01:02<00:00,  4.78it/s]
Embed Signature   : 100%|██████████| 263120/263120 [00:10<00:00, 24934.47it/s]
Check for Signatures: 100%|██████████| 4784/4784 [00:00<00:00, 9655.60it/s]
Video name:zumqqvixhu.mp4 FC:299 Mismatch:4024 Match:760 %Mismatch: 84.11371237458194%  FDC:2 time:75.4955358505249s
Detecting Face:   0%|          | 0/300 [00:00<?, ?it/s]Video name : nswtvttxre.mp4 Frame count 300
Detecting Face: 100%|██████████| 300/300 [01:09<00:00,  4.33it/s]
Embed Signature   : 100%|██████████| 264000/264000 [00:10<00:00, 24823.37it/s]
Check for Signatures: 100%|██████████| 4800/4800 [00:00<00:00, 9461.21it/s]
Video name:utdlsqfykm.mp4 FC:300 Mismatch:3560 Match:1240 %Mismatch: 74.16666666666667%  FDC:0 time:82.78762173652649s
Video name : ptkcmwnfjv.mp4 Frame count 299
Detecting Face:  25%|██▌       | 76/299 [00:17<00:51,  4.29it/s]*
Detecting Face:  26%|██▌       | 77/299 [00:17<00:51,  4.34it/s]*
*
Detecting Face:  26%|██▋       | 79/299 [00:18<00:50,  4.32it/s]*
Detecting Face:  27%|██▋       | 80/299 [00:18<00:50,  4.35it/s]*
Detecting Face:  27%|██▋       | 81/299 [00:18<00:49,  4.38it/s]*
*
Detecting Face:  28%|██▊       | 83/299 [00:19<00:50,  4.31it/s]*
Detecting Face:  28%|██▊       | 84/299 [00:19<00:49,  4.36it/s]*
*
Detecting Face:  29%|██▉       | 86/299 [00:20<00:50,  4.25it/s]*
*
Detecting Face:  29%|██▉       | 88/299 [00:20<00:49,  4.28it/s]*
Detecting Face:  30%|██▉       | 89/299 [00:20<00:48,  4.30it/s]*
Detecting Face:  34%|███▍      | 102/299 [00:23<00:45,  4.33it/s]*
*
Detecting Face:  35%|███▍      | 104/299 [00:24<00:44,  4.36it/s]*
*
Detecting Face:  36%|███▋      | 109/299 [00:25<00:43,  4.35it/s]*
*
Detecting Face:  37%|███▋      | 111/299 [00:25<00:43,  4.35it/s]*
Detecting Face:  40%|████      | 121/299 [00:28<00:40,  4.41it/s]*
Detecting Face:  42%|████▏     | 126/299 [00:29<00:39,  4.33it/s]*
Detecting Face:  45%|████▍     | 134/299 [00:31<00:37,  4.39it/s]*
Detecting Face:  45%|████▌     | 135/299 [00:31<00:37,  4.39it/s]*
*
Detecting Face:  46%|████▌     | 137/299 [00:31<00:36,  4.42it/s]*
Detecting Face:  46%|████▌     | 138/299 [00:31<00:36,  4.44it/s]*
Detecting Face:  46%|████▋     | 139/299 [00:32<00:36,  4.39it/s]*
Detecting Face:  47%|████▋     | 141/299 [00:32<00:36,  4.33it/s]*
Detecting Face:  47%|████▋     | 142/299 [00:32<00:36,  4.35it/s]*
Detecting Face:  48%|████▊     | 143/299 [00:33<00:36,  4.30it/s]*
Detecting Face:  49%|████▉     | 146/299 [00:33<00:34,  4.42it/s]*
Detecting Face:  51%|█████     | 152/299 [00:35<00:34,  4.28it/s]*
Detecting Face:  51%|█████     | 153/299 [00:35<00:33,  4.33it/s]*
Detecting Face:  52%|█████▏    | 154/299 [00:35<00:33,  4.31it/s]*
*
Detecting Face:  52%|█████▏    | 156/299 [00:36<00:32,  4.36it/s]*
Detecting Face:  53%|█████▎    | 157/299 [00:36<00:32,  4.39it/s]*
*
Detecting Face:  53%|█████▎    | 159/299 [00:36<00:32,  4.35it/s]*
Detecting Face:  54%|█████▎    | 160/299 [00:37<00:31,  4.37it/s]*
Detecting Face:  54%|█████▍    | 161/299 [00:37<00:31,  4.33it/s]*
Detecting Face:  54%|█████▍    | 162/299 [00:37<00:31,  4.36it/s]*
*
Detecting Face:  55%|█████▍    | 164/299 [00:37<00:29,  4.54it/s]*
*
Detecting Face:  56%|█████▌    | 166/299 [00:38<00:29,  4.48it/s]*
Detecting Face:  56%|█████▌    | 167/299 [00:38<00:29,  4.46it/s]*
*
Detecting Face:  57%|█████▋    | 169/299 [00:39<00:29,  4.44it/s]*
*
Detecting Face:  57%|█████▋    | 171/299 [00:39<00:28,  4.52it/s]*
*
Detecting Face:  58%|█████▊    | 173/299 [00:39<00:28,  4.40it/s]*
*
Detecting Face:  59%|█████▊    | 175/299 [00:40<00:27,  4.43it/s]*
*
Detecting Face:  59%|█████▉    | 177/299 [00:40<00:27,  4.44it/s]*
Detecting Face:  60%|█████▉    | 178/299 [00:41<00:27,  4.36it/s]*
Detecting Face:  60%|█████▉    | 179/299 [00:41<00:27,  4.36it/s]*
Detecting Face:  61%|██████    | 183/299 [00:42<00:26,  4.34it/s]*
*
Detecting Face:  62%|██████▏   | 185/299 [00:42<00:26,  4.38it/s]*
Detecting Face:  62%|██████▏   | 186/299 [00:42<00:25,  4.38it/s]*
Detecting Face:  63%|██████▎   | 188/299 [00:43<00:25,  4.35it/s]*
*
Detecting Face:  64%|██████▍   | 192/299 [00:44<00:24,  4.37it/s]*
Detecting Face:  65%|██████▍   | 194/299 [00:44<00:24,  4.37it/s]*
Detecting Face:  65%|██████▌   | 195/299 [00:44<00:23,  4.42it/s]*
Detecting Face:  67%|██████▋   | 199/299 [00:45<00:22,  4.36it/s]*
Detecting Face:  68%|██████▊   | 203/299 [00:46<00:21,  4.42it/s]*
Detecting Face:  68%|██████▊   | 204/299 [00:47<00:21,  4.42it/s]*
Detecting Face:  69%|██████▊   | 205/299 [00:47<00:21,  4.38it/s]*
*
Detecting Face:  70%|██████▉   | 208/299 [00:47<00:21,  4.24it/s]*
Detecting Face:  70%|██████▉   | 209/299 [00:48<00:21,  4.18it/s]*
Detecting Face:  70%|███████   | 210/299 [00:48<00:21,  4.17it/s]*
Detecting Face:  71%|███████   | 211/299 [00:48<00:21,  4.17it/s]*
*
Detecting Face:  71%|███████   | 213/299 [00:49<00:20,  4.15it/s]*
Detecting Face:  72%|███████▏  | 214/299 [00:49<00:20,  4.12it/s]*
Detecting Face:  72%|███████▏  | 215/299 [00:49<00:20,  4.12it/s]*
Detecting Face:  80%|███████▉  | 238/299 [00:55<00:13,  4.37it/s]*
Detecting Face:  80%|███████▉  | 239/299 [00:55<00:13,  4.31it/s]*
*
Detecting Face:  81%|████████  | 241/299 [00:55<00:13,  4.33it/s]*
Detecting Face:  81%|████████  | 242/299 [00:56<00:12,  4.40it/s]*
*
Detecting Face:  82%|████████▏ | 244/299 [00:56<00:12,  4.40it/s]*
*
Detecting Face:  82%|████████▏ | 246/299 [00:56<00:12,  4.41it/s]*
*
Detecting Face:  83%|████████▎ | 248/299 [00:57<00:11,  4.43it/s]*
*
Detecting Face:  84%|████████▎ | 250/299 [00:57<00:11,  4.40it/s]*
Detecting Face:  84%|████████▍ | 251/299 [00:58<00:10,  4.42it/s]*
*
Detecting Face:  85%|████████▍ | 253/299 [00:58<00:10,  4.45it/s]*
*
Detecting Face:  85%|████████▌ | 255/299 [00:58<00:10,  4.39it/s]*
*
Detecting Face:  86%|████████▌ | 257/299 [00:59<00:09,  4.47it/s]*
Detecting Face:  86%|████████▋ | 258/299 [00:59<00:09,  4.41it/s]*
Detecting Face:  87%|████████▋ | 259/299 [00:59<00:08,  4.47it/s]*
*
Detecting Face:  87%|████████▋ | 261/299 [01:00<00:08,  4.44it/s]*
Detecting Face:  89%|████████▉ | 266/299 [01:01<00:07,  4.40it/s]*
*
Detecting Face:  90%|████████▉ | 268/299 [01:01<00:07,  4.34it/s]*
Detecting Face:  90%|█████████ | 270/299 [01:02<00:06,  4.36it/s]*
*
Detecting Face:  91%|█████████ | 272/299 [01:02<00:06,  4.41it/s]*
Detecting Face:  91%|█████████▏| 273/299 [01:03<00:05,  4.42it/s]*
*
Detecting Face:  92%|█████████▏| 276/299 [01:03<00:05,  4.37it/s]*
Detecting Face:  93%|█████████▎| 278/299 [01:04<00:04,  4.36it/s]*
Detecting Face:  94%|█████████▎| 280/299 [01:04<00:04,  4.40it/s]*
Detecting Face:  94%|█████████▍| 282/299 [01:05<00:03,  4.38it/s]*
Detecting Face:  95%|█████████▍| 283/299 [01:05<00:03,  4.35it/s]*
Detecting Face:  95%|█████████▍| 284/299 [01:05<00:03,  4.36it/s]*
Detecting Face:  95%|█████████▌| 285/299 [01:05<00:03,  4.37it/s]*
Detecting Face:  96%|█████████▌| 286/299 [01:06<00:02,  4.40it/s]*
*
Detecting Face:  97%|█████████▋| 290/299 [01:06<00:02,  4.41it/s]*
Detecting Face:  97%|█████████▋| 291/299 [01:07<00:01,  4.48it/s]*
Detecting Face:  98%|█████████▊| 292/299 [01:07<00:01,  4.47it/s]*
*
Detecting Face:  98%|█████████▊| 294/299 [01:07<00:01,  4.44it/s]*
*
Detecting Face:  99%|█████████▉| 296/299 [01:08<00:00,  4.41it/s]*
*
Detecting Face: 100%|█████████▉| 298/299 [01:08<00:00,  4.45it/s]*
Detecting Face: 100%|██████████| 299/299 [01:08<00:00,  4.33it/s]
Embed Signature   : 100%|██████████| 263120/263120 [00:10<00:00, 24797.37it/s]
Check for Signatures: 100%|██████████| 4784/4784 [00:00<00:00, 9461.33it/s]
Video name:mdfndlljvt.mp4 FC:299 Mismatch:3666 Match:1118 %Mismatch: 76.6304347826087%  FDC:133 time:82.05960392951965s
Video name : objgwnmscm.mp4 Frame count 299
Detecting Face: 100%|██████████| 299/299 [01:10<00:00,  4.23it/s]
Embed Signature   : 100%|██████████| 263120/263120 [00:10<00:00, 24851.38it/s]
Check for Signatures: 100%|██████████| 4784/4784 [00:00<00:00, 9435.23it/s]
Video name:maktypgsfl.mp4 FC:299 Mismatch:4152 Match:632 %Mismatch: 86.78929765886288%  FDC:0 time:84.08392930030823s
Video name : xrhqtmxlvx.mp4 Frame count 299
Detecting Face:   8%|▊         | 25/299 [00:05<00:57,  4.74it/s]*
Detecting Face:   9%|▉         | 28/299 [00:05<00:57,  4.68it/s]*
Detecting Face:  10%|█         | 30/299 [00:06<00:57,  4.65it/s]*
Detecting Face:  11%|█         | 32/299 [00:06<00:57,  4.64it/s]*
Detecting Face: 100%|██████████| 299/299 [01:04<00:00,  4.65it/s]
Embed Signature   : 100%|██████████| 263120/263120 [00:10<00:00, 24759.84it/s]
Check for Signatures: 100%|██████████| 4784/4784 [00:00<00:00, 9403.82it/s]
Video name:pleqihjpif.mp4 FC:299 Mismatch:4651 Match:133 %Mismatch: 97.21989966555184%  FDC:4 time:77.98052716255188s

Process finished with exit code 0
