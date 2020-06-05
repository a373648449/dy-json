import json
#f = open("json/company.json",'r',encoding='utf-8')
f = open("json/dy.json",'r',encoding='utf-8')
ln = 0
for line in f.readlines():
    ln += 1
    dic = json.loads(line)
    t = dic['aweme_list']
    f = open("out/data.txt",'a',encoding='utf-8')
    for aweme_list in t:
        video=aweme_list['video']['play_addr']['url_list'][0]
        f.writelines(str(video));f.write("\n")
    f.write(str(ln))
f.close()