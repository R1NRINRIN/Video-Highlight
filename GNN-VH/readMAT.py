from scipy import io
import pandas as pd

import sys
import numpy as np
np.set_printoptions(threshold=sys.maxsize)


mat_file = io.loadmat('./data/SumMe/GT/Air_Force_One.mat')
print(mat_file.keys())   # 'all_userIDs', 'segments', 'nFrames', 'video_duration', 'FPS', 'gt_score', 'user_score'
# dtype='<U2' : 문자형
# dtype='<U18' : 
# dtype='<U31' : 
df = pd.DataFrame()
# df['segments'] = mat_file.get('segments')
# print(df)
print(mat_file.get('user_score'))
print(len(mat_file.get('user_score')))