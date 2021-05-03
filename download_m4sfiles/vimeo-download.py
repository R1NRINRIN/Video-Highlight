import requests
import base64
from tqdm import tqdm


master_json_url = 'https://174vod-adaptive.akamaized.net/exp=1620039047~acl=%2F183749173%2F%2A~hmac=f7e0125974f6a165693b7bcfcb2a90136fa9b7988de80f8b2e526159ece31727/183749173/sep/video/605418808,605418800,605418803/master.json?base64_init=1'
base_url = master_json_url[:master_json_url.rfind('/', 0, -26) + 1]
print("base_url", base_url)

resp = requests.get(master_json_url)
content = resp.json()

heights = [(i, d['height']) for (i, d) in enumerate(content['video'])]
#idx, _ = max(heights, key=lambda h: (_, h))
idx, _ = max(heights, key=lambda x:x[1])
video = content['video'][idx]
# video_base_url = base_url + video['base_url']
video_base_url = '%s%s/chop/'%(base_url, video['id'])
print("video_base_url", video_base_url)

# print ('base url:', video_base_url)

filename = 'video_%d.mp4' % int(video['id'])
print ('saving to %s' % filename)

video_file = open(filename, 'wb')

init_segment = base64.b64decode(video['init_segment'])
video_file.write(init_segment)

####
initsegfile = open('init.m4s', 'wb')
initsegfile.write(init_segment)
initsegfile.flush()
initsegfile.close()
####
i = 1
for segment in tqdm(video['segments']):
    segment_url = video_base_url + segment['url']
    # print("segment_url = ", segment_url)

    ###
    segname = '%d.m4s' % i
    segfile = open(segname, 'wb')
    ###

    resp = requests.get(segment_url, stream=True)
    if resp.status_code != 200:
        print ('not 200!')
        print (resp)
        print (segment_url)
        break
    for chunk in resp:
        video_file.write(chunk)
        ###
        segfile.write(chunk)
        ###
    ###
    segfile.flush()
    segfile.close()
    i += 1
    ###

video_file.flush()
video_file.close()

