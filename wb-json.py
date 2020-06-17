import json
# f = open("json/company.json",'r',encoding='utf-8')
f = open("json/company.json", 'r', encoding='utf-8')
ln = 0
for line in f.readlines():
    ln += 1
    dic = json.loads(line)
    t = dic['cards']
    f = open("out/data.txt", 'a', encoding='utf-8')
    for cards in t:
        img = cards['card_group']
        for pics in img:
            for pic in pics['pics']:
                dd = pic['pic_big']
                f.writelines(str(dd))
                f.write("\n")
        f.write(str(ln))
f.close()
