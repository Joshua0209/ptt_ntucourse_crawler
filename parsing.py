import pttcrawler as cr
import pandas as pd
import re

searches = ['張小虹', '廖彥棻', '黃馨瑩', '黃恆綜', '楊乃冬', '張嘉倩']  # 欲搜尋的內容
title = "大一英文"  # 儲存檔名
numPages = 1  # 每個搜尋對象要爬的頁數

# =========================================================
# crawling content or reading content
content = cr.crawl_pages(searches=searches, title=title, numPages=numPages)

# with open(title+".txt", 'r', encoding="utf-8") as file:
#     content = file.read()
# =========================================================
INDEX = ["學年度", "授課教師", "開課系所與授課對象", "課程大概內容", "私心推薦指數",
         "上課用書", "上課方式", "評分方式", "考題型式、作業方式", "其它", "總結"]
KEYS = "ψ|λ|δ|Ω|η|μ|σ|ρ|ω|Ψ|--\n※"
REPLACE = [
    "授課教師 (若為多人合授請寫開課教師，以方便收錄)",
    "開課系所與授課對象 (是否為必修或通識課 / 內容是否與某些背景相關)",
    "課程大概內容",
    "私心推薦指數(以五分計) ★★★★★",
    "上課用書(影印講義或是指定教科書)",
    "上課方式(投影片、團體討論、老師教學風格)",
    "評分方式(給分甜嗎？是紮實分？)",
    "考題型式、作業方式",
    "其它(是否注重出席率？如果為外系選修，需先有什麼基礎較好嗎？老師個性？\n加簽習慣？嚴禁遲到等…)",
    "總結"]
# =========================================================


def find_title(soup):
    x = soup.find("]")
    y = soup.find("時間")
    z = soup.find("哪一學年度修課：")
    return soup[x+1:y].strip(" "), [soup[z:].replace("哪一學年度修課：", "").strip(" \n")]


data = pd.DataFrame(index=INDEX)

content = content.strip(
    "\n\n\n\n************************下一篇************************\n\n\n\n\n")
posts = content.split("************************下一篇************************")

for post in posts:
    post = re.split(KEYS, post)
    try:
        post.remove("")
    except:
        pass
    finally:
        if (len(post) <= 12) & ((post[0].find('[通識]') != -1) or post[0].find('[評價]') != -1):
            name, details = find_title(post[0])
            x = 1
            for i in range(len(REPLACE)):
                for j in range(x, len(post)-1):
                    if post[j].find(REPLACE[i]) != -1:
                        details.append(post[j].replace(
                            REPLACE[i], "").strip(" \n "))
                        x += 1
                        break
                else:
                    details.append(None)
            data[name] = details

        else:
            x = post[0].find('[')
            y = post[0].find(']')
            print(post[0][x:y+1])


data.to_csv(f"{title}.csv", encoding="utf-8")
