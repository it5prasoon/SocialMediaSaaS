from random import randint
from time import sleep, time

import gc
from selenium.webdriver.common.by import By
from spawn_driver import start
from spawn_driver1 import start as start1
from selenium.webdriver.common.keys import Keys
import firebase_admin
from firebase_admin import db

cred_obj3 = firebase_admin.credentials.Certificate('scraped_data.json')
app3 = firebase_admin.initialize_app(cred_obj3,
                                     {'databaseURL': 'https://scraped-data-f193f-default-rtdb.firebaseio.com/'},
                                     name='app3')
ref3 = db.reference('/', app3)

# s=[]
s = ''


def convert_username_firebase(text):
    res = ''
    for x in text:
        res += str(ord(x)) + '-'
    return res[:-1]


def get_number_value(text):
    if (text[-1] == 'K'):
        number = float(text[:-1])
        return number * 1000
    elif (text[-1] == 'M'):
        number = float(text[:-1])
        return number * 1000000
    else:
        return float(text)


def start_driver(flag=0):
    if (flag):
        return start1()
    else:
        return start()


def get_creator_follower(url):
    driver = start_driver(1)
    driver.get(url)

    while True:
        try:
            followers_count = driver.find_element(by=By.XPATH, value='//strong[@data-e2e="followers-count"]').text
            break
        except:
            sleep(0.1)
    print(followers_count)
    return followers_count


def get_posts_metric(post_url_list, flag=0):
    flag = post_url_list[1]
    post_url_list = post_url_list[0]
    driver = start_driver(1)
    # try:
    #   if(driver.session_id): pass
    #  else: start_driver(1)
    # except: start_driver(1)

    for post_url in post_url_list:
        print(post_url)
        driver.execute_script(f"window.open('{post_url}','tab{post_url_list.index(post_url)}');")
        # driver.get(post_url)
    # driver.switch_to.window(driver.window_handles[0])

    '''if(type(post_url)==list):
        flag=post_url[1]
        post_url=post_url[0]
    #driver.switch_to.window("secondtab")
    driver.get(post_url)
    sleep(1)'''
    main_list = []
    for x in range(10):
        try:
            driver.switch_to.window(f'tab{x}')
            driver.execute_script("window.scrollBy(0, 500);")
            counter = 0
            caption = ''
            while counter < 30:
                try:
                    caption = driver.find_element(by=By.XPATH, value='//div[@data-e2e="browse-video-desc"]').text
                    break
                except:
                    sleep(0.1)
                    counter += 1
            mentions = []
            try:
                for x in caption.split(' '):
                    if (x[0] == "@"): mentions.append(x)
            except:
                pass
            try:
                like_count = driver.find_element(by=By.XPATH, value='//strong[@data-e2e="like-count"]').text
                like_count = get_number_value(like_count)
            except:
                like_count = 0

            try:
                comment_count = driver.find_element(by=By.XPATH, value='//strong[@data-e2e="comment-count"]').text
                comment_count = get_number_value(comment_count)
            except:
                comment_count = 0
            try:
                share_count = driver.find_element(by=By.XPATH, value='//strong[@data-e2e="share-count"]').text
                share_count = get_number_value(share_count)
            except:
                share_count = 0
            # music_url=driver.find_element(by=By.XPATH, value='//h4[@data-e2e="browse-music"]').find_element(by=By.TAG_NAME, value='a').get_attribute('href')
            hashtags = []
            for x in driver.find_elements(by=By.XPATH, value='//a[@class="tiktok-q3q1i1-StyledCommonLink ejg0rhn4"]'):
                hashtag_url = x.get_attribute('href')
                if ('/tag/' in hashtag_url): hashtags.append(hashtag_url[hashtag_url.index('/tag/') + 5:])

            print('------------------------------------------')
            # print(caption, like_count, comment_count, hashtags)
            if (flag):
                # creater_follower_count=get_creator_follower(driver.find_element(by=By.XPATH, value='//a[@class="tiktok-1b6v967-StyledLink e17fzhrb3"]').get_attribute('href'))
                # creater_follower_count=get_number_value(creater_follower_count)
                creater_follower_count = 100.00
                # driver.switch_to.window(driver.window_handles[0])
                main_list.append(
                    [caption, like_count, share_count, comment_count, hashtags, mentions, creater_follower_count])
            # driver.switch_to.window(driver.window_handles[0])
            main_list.append([caption, like_count, share_count, comment_count, hashtags, mentions])
        except:
            pass
    print(main_list)
    return main_list


def get_user_profile(username):
    try:
        driver.quit()
        del driver
        gc.collect()
    except:
        pass
    t = time()
    url = f'https://www.tiktok.com/@{username}?lang=en'
    print('url is created')
    driver = start_driver(1)
    driver.get(url)

    # print(driver.title)

    if ('tiktok-verify-page' in driver.title):
        driver.find_element(by=By.TAG_NAME, value='body').send_keys(Keys.COMMAND + 'r')
    # profile_pic=driver.find_element(by=By.XPATH, value='//img[@class="tiktok-1zpj2q-ImgAvatar e1e9er4e1"]').get_attribute('src')
    while True:
        if (time() - t > 100):
            driver.quit()
            del driver
            gc.collect()
            return False
        try:
            following_count = driver.find_element(by=By.XPATH, value='//strong[@data-e2e="following-count"]').text
            break
        except:
            pass
    print(following_count)
    while True:
        try:

            followers_count = driver.find_element(by=By.XPATH, value='//strong[@data-e2e="followers-count"]').text
            followers_count = get_number_value(followers_count)
            break
        except:
            pass

    while True:
        try:
            likes_count = driver.find_element(by=By.XPATH, value='//strong[@data-e2e="likes-count"]').text
            break
        except:
            pass
    print(likes_count)
    try:
        user_bio = driver.find_element(by=By.XPATH, value='//h2[@data-e2e="user-bio"]').text
    except:
        user_bio = driver.find_element(by=By.XPATH, value='//h2[@data-e2e="user-bio"]').text
    print(user_bio)
    try:
        user_link = driver.find_element(by=By.XPATH, value='//a[@data-e2e="user-link"]').get_attribute('href')
    except:
        user_link = None
    print(user_link)

    posts = []
    p1 = []
    counter = 0
    total_views = float(0)
    post_views = float(0)
    while (len(posts) < 6 and counter < 30):
        try:
            for post in driver.find_elements(by=By.XPATH,
                                             value='//div[@class="tiktok-x6y88p-DivItemContainerV2 e19c29qe7"]'):
                sexxx = post.find_element(by=By.XPATH, value='.//div[@class="tiktok-yz6ijl-DivWrapper e1cg0wnj1"]')
                # sexxx=post.find_element(by=By.XPATH, value='.//a[@class="tiktok-1wrhn5c-AMetaCaptionLine eih2qak0"]')
                if (sexxx not in p1): p1.append(sexxx)
                post_url = post.find_element(by=By.XPATH,
                                             value='.//div[@class="tiktok-yz6ijl-DivWrapper e1cg0wnj1"]').find_element(
                    by=By.TAG_NAME, value='a').get_attribute('href')
                if (post_url not in posts):
                    posts.append(post_url)
                    post_views = post.find_element(by=By.XPATH, value='.//strong[@data-e2e="video-views"]').text
                    print(post_views, '-------------------')
                    post_views = get_number_value(post_views)
                    total_views += post_views
                if (len(posts) > 6): break
        except:
            sleep(0.05)
            counter += 1
        print(len(posts))
        if (len(posts) > 5): break
        driver.execute_script("window.scrollBy(0,250);")

        counter += 1
    print(total_views, post_views)

    # for x in range(5):
    #   driver.execute_script(f"window.open('{posts[x]}','tab{x}');")

    # posts=driver.find_elements(by=By.XPATH, value='//div[@class="tiktok-x6y88p-DivItemContainerV2 e19c29qe7"]')
    total_like_count, total_share_count, total_comment_count, hashtag_ranked_list, caption_ranked_list, mention_ranked_list = float(), float(), float(), [], [], []
    hashtag_blob, caption_blob, mention_blob = [], '', []
    for x in driver.find_elements(by=By.XPATH, value='//button[@type="button"]'):
        if (x.text == 'Accept all'):
            x.click()
    for post in posts[:min(5, len(posts))]:
        # print(posts[0])
        # posts[0].click()
        # sleep(5)
        if (time() - t > 50):
            driver.quit()
            del driver
            gc.collect()
            return False
        if True:
            driver.get(post)
        elif (posts.index(post) == 0):
            while True:
                if (time() - t > 30):
                    driver.quit()
                    del driver
                    gc.collect()
                    return False
                try:
                    # post.click()
                    # post.click()
                    driver.get(post)
                    print(driver.current_url)
                    break
                except Exception as e:
                    post = driver.find_element(by=By.XPATH, value='//div[@class="tiktok-yz6ijl-DivWrapper e1cg0wnj1"]')

            # sleep(randint(55,85)/100)
        else:
            try:
                driver.find_element(by=By.XPATH, value='//button[@data-e2e="arrow-right"]').click()
            except:
                while True:
                    if (time() - t > 30):
                        driver.quit()
                        del driver
                        gc.collect()
                        return False
                    try:
                        driver.find_element(by=By.XPATH,
                                            value='//div[@class="captcha_verify_bar--close sc-chPdSV dSiAYZ"]').click()
                        break
                    except:
                        sleep(0.05)
        # driver.switch_to.window(f'tab{posts.index(post)}')
        # sleep(0.5)
        # driver.execute_script("window.scrollBy(0, 500);")
        # print(driver.current_window_handle)
        # post_caption=post.find_element(by=By.XPATH, value='.//a[@class="tiktok-1wrhn5c-AMetaCaptionLine eih2qak0"]').get_attribute('title')
        # print(post_caption)
        counter = 0
        caption = ''
        while counter < 60:
            if (time() - t > 50):
                print('SLEEP')
                driver.quit()
                del driver
                gc.collect()
                return False
            try:
                caption = driver.find_element(by=By.XPATH, value='//div[@data-e2e="browse-video-desc"]').text
                break

            except Exception as e:
                if (counter > 20): print(e)
                # print('drag' in )
                sleep(0.05)
                counter += 1

        # if(counter<60): driver.quit()

        mentions = []
        hashtags = []
        try:
            for x in caption.split(' '):
                if (x[0] == "@"):
                    mentions.append(x)
                elif (x[0] == "#"):
                    hashtags.append(x)

        except:
            pass
        try:
            like_count = driver.find_element(by=By.XPATH, value='//strong[@data-e2e="browse-like-count"]').text
            # print(like_count)
            like_count = get_number_value(like_count)
            print(like_count)


        except Exception as e:

            try:
                like_count = driver.find_element(by=By.XPATH, value='//strong[@data-e2e="like-count"]').text
            except:
                like_count = driver.find_element(by=By.XPATH, value='//strong[@data-e2e="like-count"]').text
            like_count = get_number_value(like_count)
            print('like_count')

        try:
            comment_count = driver.find_element(by=By.XPATH, value='//strong[@data-e2e="browse-comment-count"]').text
            comment_count = get_number_value(comment_count)
        except:
            comment_count = driver.find_element(by=By.XPATH, value='//strong[@data-e2e="comment-count"]').text
            comment_count = get_number_value(comment_count)
            print('comcount')
        try:
            share_count = driver.find_element(by=By.XPATH, value='//strong[@data-e2e="share-count"]').text
            share_count = get_number_value(share_count)
            print(share_count)
        except:
            share_count = 0

        # music_url=driver.find_element(by=By.XPATH, value='//h4[@data-e2e="browse-music"]').find_element(by=By.TAG_NAME, value='a').get_attribute('href')
        # hashtags=[]
        # for x in driver.find_elements(by=By.XPATH, value='//a[@class="tiktok-q3q1i1-StyledCommonLink ejg0rhn4"]'):
        #   hashtag_url=x.get_attribute('href')
        #  if('/tag/' in hashtag_url): hashtags.append(hashtag_url[hashtag_url.index('/tag/')+5:].replace('?lang=en',''))

        total_like_count += like_count
        total_comment_count += comment_count
        total_share_count += share_count
        hashtag_blob.extend(hashtags)
        mention_blob.extend(mentions)
        caption_blob += caption
    # print(hashtag_blob)

    for x in list(set(hashtag_blob)):
        hashtag_ranked_list.append([x, hashtag_blob.count(x)])
    hashtag_ranked_list = sorted(hashtag_ranked_list, key=lambda l: l[1], reverse=True)
    for x in list(set(mention_blob)):
        mention_ranked_list.append([x, mention_blob.count(x)])
    mention_ranked_list = sorted(mention_ranked_list, key=lambda l: l[1], reverse=True)

    # hashtag_ranked_list=list(set(hashtag_ranked_list))
    for x in list(set(filter(lambda w: not w in s, caption_blob.split()))):
        if (x[0] != '#'):
            caption_ranked_list.append([x, caption_blob.count(x)])
    caption_ranked_list = sorted(caption_ranked_list, key=lambda l: l[1], reverse=True)
    caption_ranked_list = caption_ranked_list[:min(5, len(caption_ranked_list))]
    hashtag_ranked_list = hashtag_ranked_list[:min(5, len(hashtag_ranked_list))]
    mention_ranked_list = mention_ranked_list[:min(5, len(mention_ranked_list))]
    # caption_ranked_list=list(set(caption_ranked_list))
    # print(total_like_count, total_comment_count, hashtag_ranked_list[:5], caption_ranked_list[:5])
    engagement_rate = (total_like_count + total_comment_count) * 100 / (followers_count * 5)
    like_rate = total_like_count * 100 / (followers_count * 5)
    comment_rate = total_comment_count * 100 / (followers_count * 5)
    view_rate = total_views * 100 / (followers_count * 5)
    share_rate = total_share_count * 100 / (followers_count * 5)
    output_json = {
        # 'profile_pic': profile_pic,
        'following_count': following_count,
        'followers_count': followers_count,
        'total_likes_till_date': likes_count,
        'like_count_last50': total_like_count,
        'total_comment_count': total_comment_count,
        'total_share_count': total_share_count,
        'total_views': total_views,
        'engagement_rate': engagement_rate,
        'like_rate': like_rate,
        'comment_rate': comment_rate,
        'view_rate': view_rate,
        'share_rate': share_rate,
        'hashtag_ranked_list': hashtag_ranked_list,
        'caption_ranked_list': caption_ranked_list,
        'mention_ranked_list': mention_ranked_list,
        'user_bio': user_bio,
        'user_link': user_link
    }
    # print(time.time()-t)
    ref3.child(convert_username_firebase(username)).update(output_json)
    driver.quit()
    del driver
    gc.collect()
    ref3.child('call_counter').update(
        {'call_counter': ref3.child('call_counter').get('call_counter')[0].get('call_counter') + 1})
    return output_json


def get_hashtag_posts(hashtag):
    url = f'https://www.tiktok.com/tag/{hashtag}?lang=en'
    driver = start_driver(1)
    try:
        if (driver.session_id):
            pass
        else:
            start_driver()
    except:
        start_driver()

    driver.get(url)
    posts = []
    counter = 0
    while (len(posts) < 50 and counter < 5):
        try:
            for post in driver.find_elements(by=By.XPATH,
                                             value='//div[@class="tiktok-x6y88p-DivItemContainerV2 e19c29qe7"]'):
                post_url = post.find_element(by=By.XPATH,
                                             value='.//div[@class="tiktok-yz6ijl-DivWrapper e1cg0wnj1"]').find_element(
                    by=By.TAG_NAME, value='a').get_attribute('href')
                if (post_url not in posts): posts.append(post_url)
                if (len(posts) > 50): break
        except:
            pass
        print(len(posts))
        driver.execute_script("window.scrollBy(0, 500);")
        sleep(0.5)
        counter += 1
    print(len(posts))
    total_views = float()
    total_like_count, total_share_count, total_comment_count, hashtag_ranked_list, caption_ranked_list, mention_ranked_list, total_follower_count = float(), float(), float(), [], [], [], float()
    hashtag_blob, caption_blob, mention_blob = [], '', []
    url_list = []
    for x in range(0, len(posts), 10):
        # post_author=post.find_element(by=By.XPATH, value='.//h4[@data-e2e="challenge-item-username"]').text
        # print(post_author)
        # =post.find_element(by=By.XPATH, value='.//div[@class="tiktok-yz6ijl-DivWrapper e1cg0wnj1"]').find_element(by=By.TAG_NAME, value='a').get_attribute('href')
        # print(post_url)
        url_list.append([posts[x:x + 10], 1])

        # post_views=post.find_element(by=By.XPATH, value='.//strong[@data-e2e="video-views"]').text
        # print(post_views)
        # post_views=get_number_value(post_views)
        # total_views+=post_views

    # driver.quit()
    # pool = multiprocessing.Pool(processes = 5)
    # total_info=pool.map(get_posts_metric, url_list)
    total_info = get_posts_metric(url_list[0])
    print(total_info)
    for temposts in total_info:
        # temp=get_posts_metric(post_url, 1)
        for temp in temp1:
            total_like_count += temp[1]
            total_share_count += temp[2]
            total_comment_count += temp[3]
            hashtag_blob.extend(temp[4])
            mention_blob.extend(temp[5])
            caption_blob += temp[0]
            total_follower_count += temp[6]
    for x in range(len(caption_blob)):
        try:
            if (caption_blob[x] == '#'):
                caption_blob = caption_blob.replace(caption_blob[x:caption_blob[x:].index(' ') + x], '')
        except:
            pass

    while '  ' in caption_blob:
        caption_blob = caption_blob.replace('  ', ' ')
    caption_blob = caption_blob.strip()

    for x in list(set(hashtag_blob)):
        hashtag_ranked_list.append([x, hashtag_blob.count(x)])
    hashtag_ranked_list = sorted(hashtag_ranked_list, key=lambda l: l[1], reverse=True)
    for x in list(set(mention_blob)):
        mention_ranked_list.append([x, mention_blob.count(x)])
    mention_ranked_list = sorted(mention_ranked_list, key=lambda l: l[1], reverse=True)

    # hashtag_ranked_list=list(set(hashtag_ranked_list))
    for x in list(set(filter(lambda w: not w in s, caption_blob.split()))):
        caption_ranked_list.append([x, caption_blob.count(x)])
    caption_ranked_list = sorted(caption_ranked_list, key=lambda l: l[1], reverse=True)
    caption_ranked_list = caption_ranked_list[:5]
    hashtag_ranked_list = hashtag_ranked_list[:5]
    mention_ranked_list = mention_ranked_list[:5]

    # caption_ranked_list=list(set(caption_ranked_list))
    print(total_like_count, total_comment_count, hashtag_ranked_list[:5], caption_ranked_list[:5])
    engagement_rate = (total_like_count + total_comment_count) * 100 / (total_follower_count * 5)
    like_rate = total_like_count * 100 / (total_follower_count * 5)
    comment_rate = total_comment_count * 100 / (total_follower_count * 5)
    # view_rate=total_views*100/(total_follower_count*5)
    share_rate = total_share_count * 100 / (total_follower_count * 5)

    return {
        # 'profile_pic': profile_pic,
        # 'following_count':following_count,
        'follower_reach': total_follower_count,
        'follower_impressions': total_follower_count * 5,
        'total_like_count': total_like_count,
        'total_comment_count': total_comment_count,
        'hashtag_ranked_list': hashtag_ranked_list,
        'caption_ranked_list': caption_ranked_list,
        'mention_ranked_list': mention_ranked_list,
        'total_share_count': total_share_count,
        # 'total_views':total_views,
        'engagement_rate': engagement_rate,
        'like_rate': like_rate,
        'comment_rate': comment_rate,
        # 'view_rate':view_rate,
        'share_rate': share_rate
    }


def get_music_posts(keyword):
    driver = start_driver(1)
    url = f'https://www.tiktok.com/discover/{keyword.replace(" ", "-")}?lang=en'
    try:
        if (driver.session_id):
            pass
        else:
            start_driver(1)
    except:
        start_driver(1)
    driver.get(url)
    temp = driver.find_element(by=By.XPATH, value='//li[@data-e2e="music-item"]')
    music_name = temp.find_element(by=By.XPATH, value='.//h4[@data-e2e="music-name"]').text
    singer_name = temp.find_element(by=By.XPATH, value='.//h4[@class="tiktok-144zzj7-H4MusicAuthor enosjlq5"]').text
    num_videos = temp.find_element(by=By.XPATH, value='.//span[@data-e2e="music-vv"]').text
    music_posts_url = temp.find_element(by=By.XPATH,
                                        value='.//a[@class="tiktok-gsh7eh-StyledLink evhd01a3"]').get_attribute('href')

    driver.get(music_posts_url)
    posts = driver.find_elements(by=By.XPATH, value='//div[@class="tiktok-x6y88p-DivItemContainerV2 e19c29qe7"]')
    total_views = float()
    total_like_count, total_share_count, total_comment_count, hashtag_ranked_list, caption_ranked_list, mention_ranked_list, total_follower_count = float(), float(), float(), [], [], [], float()
    hashtag_blob, caption_blob, mention_blob = [], '', []
    for post in posts[:5]:
        post_author = post.find_element(by=By.XPATH, value='.//h4[@data-e2e="challenge-item-username"]').text
        print(post_author)
        post_url = post.find_element(by=By.XPATH,
                                     value='.//div[@class="tiktok-yz6ijl-DivWrapper e1cg0wnj1"]').find_element(
            by=By.TAG_NAME, value='a').get_attribute('href')
        print(post_url)

        # post_views=post.find_element(by=By.XPATH, value='.//strong[@data-e2e="video-views"]').text
        # print(post_views)
        # post_views=get_number_value(post_views)
        # total_views+=post_views

        temp = get_posts_metric(post_url, 1)
        total_like_count += temp[1]
        total_share_count += temp[2]
        total_comment_count += temp[3]
        hashtag_blob.extend(temp[4])
        mention_blob.extend(temp[5])
        caption_blob += temp[0]
        total_follower_count += temp[6]
    for x in list(set(hashtag_blob)):
        hashtag_ranked_list.append([x, hashtag_blob.count(x)])
    hashtag_ranked_list = sorted(hashtag_ranked_list, key=lambda l: l[1], reverse=True)
    for x in list(set(mention_blob)):
        mention_ranked_list.append([x, mention_blob.count(x)])
    mention_ranked_list = sorted(mention_ranked_list, key=lambda l: l[1], reverse=True)

    # hashtag_ranked_list=list(set(hashtag_ranked_list))
    for x in list(set(filter(lambda w: not w in s, caption_blob.split()))):
        caption_ranked_list.append([x, caption_blob.count(x)])
    caption_ranked_list = sorted(caption_ranked_list, key=lambda l: l[1], reverse=True)
    caption_ranked_list = caption_ranked_list[:5]
    hashtag_ranked_list = hashtag_ranked_list[:5]
    mention_ranked_list = mention_ranked_list[:5]
    # caption_ranked_list=list(set(caption_ranked_list))
    print(total_like_count, total_comment_count, hashtag_ranked_list[:5], caption_ranked_list[:5])
    engagement_rate = (total_like_count + total_comment_count) * 100 / (total_follower_count * 5)
    like_rate = total_like_count * 100 / (total_follower_count * 5)
    comment_rate = total_comment_count * 100 / (total_follower_count * 5)
    # view_rate=total_views*100/(total_follower_count*5)
    share_rate = total_share_count * 100 / (total_follower_count * 5)
    return {
        # 'profile_pic': profile_pic,
        # 'following_count':following_count,
        'follower_reach': total_follower_count,
        'follower_impressions': total_follower_count * 5,
        'total_like_count': total_like_count,
        'total_comment_count': total_comment_count,
        'hashtag_ranked_list': hashtag_ranked_list,
        'caption_ranked_list': caption_ranked_list,
        'mention_ranked_list': mention_ranked_list,
        'total_share_count': total_share_count,
        # 'total_views':total_views,
        'engagement_rate': engagement_rate,
        'like_rate': like_rate,
        'comment_rate': comment_rate,
        # 'view_rate':view_rate,
        'share_rate': share_rate
    }


def search_user(keyword):
    driver = start_driver(1)
    url = f'https://www.tiktok.com/search/user?q={keyword.replace(" ", "%20")}'
    try:
        if (driver.session_id):
            pass
        else:
            start_driver(1)
    except:
        start_driver(1)
    driver.get(url)
    users = driver.find_elements(by=By.XPATH, value='//div[@data-e2e="search-user-container"]')
    for user in users:
        profile_pic = user.find_element(by=By.XPATH,
                                        value='.//img[@class="tiktok-1zpj2q-ImgAvatar e1e9er4e1"]').get_attribute('src')
        profile_username = user.find_element(by=By.XPATH, value='.//p[@data-e2e="search-user-unique-id"]').text
        profile_follower_count = user.find_element(by=By.XPATH,
                                                   value='.//div[@class="tiktok-1av3vif-DivSubTitleWrapper e10wilco5"]').find_element(
            by=By.TAG_NAME, value='strong').text
        profile_bio = user.find_element(by=By.XPATH, value='.//p[@class="tiktok-1jq7d8a-PDesc e10wilco7"]').text


def search_general(keyword):
    driver = start_driver(1)
    url = f'https://www.tiktok.com/discover/{keyword.replace(" ", "-")}?lang=en'
    try:
        if (driver.session_id):
            pass
        else:
            start_driver(1)
    except:
        start_driver(1)
    driver.get(url)
    posts = driver.find_elements(by=By.XPATH, value='//div[@data-e2e="video-item"]')
    total_views = float()
    total_like_count, total_share_count, total_comment_count, hashtag_ranked_list, caption_ranked_list, mention_ranked_list, total_follower_count = float(), float(), float(), [], [], [], float()
    hashtag_blob, caption_blob, mention_blob = [], '', []
    for post in posts[:5]:
        post_author = post.find_element(by=By.XPATH, value='.//h4[@data-e2e="challenge-item-username"]').text
        print(post_author)
        post_url = post.find_element(by=By.XPATH,
                                     value='.//div[@class="tiktok-yz6ijl-DivWrapper e1cg0wnj1"]').find_element(
            by=By.TAG_NAME, value='a').get_attribute('href')
        print(post_url)

        # post_views=post.find_element(by=By.XPATH, value='.//strong[@data-e2e="video-views"]').text
        # print(post_views)
        # post_views=get_number_value(post_views)
        # total_views+=post_views
        temp = get_posts_metric(post_url, 1)
        total_like_count += temp[1]
        total_share_count += temp[2]
        total_comment_count += temp[3]
        hashtag_blob.extend(temp[4])
        mention_blob.extend(temp[5])
        caption_blob += temp[0]
        total_follower_count += temp[6]
    for x in list(set(hashtag_blob)):
        hashtag_ranked_list.append([x, hashtag_blob.count(x)])
    hashtag_ranked_list = sorted(hashtag_ranked_list, key=lambda l: l[1], reverse=True)
    for x in list(set(mention_blob)):
        mention_ranked_list.append([x, mention_blob.count(x)])
    mention_ranked_list = sorted(mention_ranked_list, key=lambda l: l[1], reverse=True)

    # hashtag_ranked_list=list(set(hashtag_ranked_list))
    for x in list(set(filter(lambda w: not w in s, caption_blob.split()))):
        caption_ranked_list.append([x, caption_blob.count(x)])
    caption_ranked_list = sorted(caption_ranked_list, key=lambda l: l[1], reverse=True)
    caption_ranked_list = caption_ranked_list[:5]
    hashtag_ranked_list = hashtag_ranked_list[:5]
    mention_ranked_list = mention_ranked_list[:5]
    # caption_ranked_list=list(set(caption_ranked_list))
    print(total_like_count, total_comment_count, hashtag_ranked_list[:5], caption_ranked_list[:5])
    engagement_rate = (total_like_count + total_comment_count) * 100 / (total_follower_count * 5)
    like_rate = total_like_count * 100 / (total_follower_count * 5)
    comment_rate = total_comment_count * 100 / (total_follower_count * 5)
    # view_rate=total_views*100/(total_follower_count*5)
    share_rate = total_share_count * 100 / (total_follower_count * 5)
    return {
        # 'profile_pic': profile_pic,
        # 'following_count':following_count,
        'follower_reach': total_follower_count,
        'follower_impressions': total_follower_count * 5,
        'total_like_count': total_like_count,
        'total_comment_count': total_comment_count,
        'hashtag_ranked_list': hashtag_ranked_list,
        'caption_ranked_list': caption_ranked_list,
        'mention_ranked_list': mention_ranked_list,
        'total_share_count': total_share_count,
        # 'total_views':total_views,
        'engagement_rate': engagement_rate,
        'like_rate': like_rate,
        'comment_rate': comment_rate,
        # 'view_rate':view_rate,
        'share_rate': share_rate
    }


def get_user_profile_detailed(username, number_of_posts=10):
    try:
        driver.quit()
        del driver
        gc.collect()
    except:
        pass
    t = time()
    url = f'https://www.tiktok.com/@{username}?lang=en'
    print('url is created')
    driver = start_driver(1)
    driver.get(url)

    # print(driver.title)

    if ('tiktok-verify-page' in driver.title):
        driver.find_element(by=By.TAG_NAME, value='body').send_keys(Keys.COMMAND + 'r')
    # profile_pic=driver.find_element(by=By.XPATH, value='//img[@class="tiktok-1zpj2q-ImgAvatar e1e9er4e1"]').get_attribute('src')
    while True:
        if (time() - t > 100):
            driver.quit()
            del driver
            gc.collect()
            return False, False, False, False, False, False, False, False, False, False, False
        try:
            following_count = driver.find_element(by=By.XPATH, value='//strong[@data-e2e="following-count"]').text
            break
        except:
            pass
    print(following_count)
    while True:
        try:

            followers_count = driver.find_element(by=By.XPATH, value='//strong[@data-e2e="followers-count"]').text
            followers_count = get_number_value(followers_count)
            break
        except:
            pass

    while True:
        try:
            likes_count = driver.find_element(by=By.XPATH, value='//strong[@data-e2e="likes-count"]').text
            break
        except:
            pass
    print(likes_count)
    try:
        user_bio = driver.find_element(by=By.XPATH, value='//h2[@data-e2e="user-bio"]').text
    except:
        user_bio = driver.find_element(by=By.XPATH, value='//h2[@data-e2e="user-bio"]').text
    print(user_bio)
    try:
        user_link = driver.find_element(by=By.XPATH, value='//a[@data-e2e="user-link"]').get_attribute('href')
    except:
        user_link = None
    print(user_link)

    posts = []
    p1 = []
    counter = 0
    total_views = float(0)
    post_views = float(0)
    post_view_list = []
    while (len(posts) < number_of_posts and counter < 30):
        try:
            for post in driver.find_elements(by=By.XPATH,
                                             value='//div[@class="tiktok-x6y88p-DivItemContainerV2 e19c29qe7"]'):
                sexxx = post.find_element(by=By.XPATH, value='.//div[@class="tiktok-yz6ijl-DivWrapper e1cg0wnj1"]')
                # sexxx=post.find_element(by=By.XPATH, value='.//a[@class="tiktok-1wrhn5c-AMetaCaptionLine eih2qak0"]')
                if (sexxx not in p1): p1.append(sexxx)
                post_url = post.find_element(by=By.XPATH,
                                             value='.//div[@class="tiktok-yz6ijl-DivWrapper e1cg0wnj1"]').find_element(
                    by=By.TAG_NAME, value='a').get_attribute('href')
                if (post_url not in posts):
                    posts.append(post_url)
                    post_views = post.find_element(by=By.XPATH, value='.//strong[@data-e2e="video-views"]').text
                    print(post_views, '-------------------')
                    post_views = get_number_value(post_views)
                    total_views += post_views
                    post_view_list.append(post_views)
                if (len(posts) > number_of_posts): break
        except:
            sleep(0.05)
            counter += 1
        print(len(posts))
        if (len(posts) > number_of_posts): break
        driver.execute_script("window.scrollBy(0,250);")

        counter += 1
    print('len is ', len(posts))
    print(total_views, post_views)

    # for x in range(5):
    #   driver.execute_script(f"window.open('{posts[x]}','tab{x}');")

    # posts=driver.find_elements(by=By.XPATH, value='//div[@class="tiktok-x6y88p-DivItemContainerV2 e19c29qe7"]')
    total_like_count, total_share_count, total_comment_count, hashtag_ranked_list, caption_ranked_list, mention_ranked_list = float(), float(), float(), [], [], []
    hashtag_blob, caption_blob, mention_blob = [], '', []
    weekday_views, weekday_posts, weekday_engagement_rate, weekday_engagement_count, weekday_view_rate, weekday_post_rate = [
        0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0,
                                                                                                    0], [0, 0, 0, 0, 0,
                                                                                                         0, 0]
    for x in driver.find_elements(by=By.XPATH, value='//button[@type="button"]'):
        if (x.text == 'Accept all'):
            x.click()
    for post in posts[:min(number_of_posts, len(posts))]:
        # print(posts[0])
        # posts[0].click()
        # sleep(5)
        if (time() - t > 100):
            driver.quit()
            del driver
            gc.collect()
            return False, False, False, False, False, False, False, False, False, False, False
        if True: driver.get(post)
        counter = 0
        caption = ''
        while counter < 60:
            if (time() - t > 100):
                print('SLEEP')
                driver.quit()
                del driver
                gc.collect()
                return False, False, False, False, False, False, False, False, False, False, False
            try:
                caption = driver.find_element(by=By.XPATH, value='//div[@data-e2e="browse-video-desc"]').text
                break

            except Exception as e:
                if (counter > 20): print(e)
                # print('drag' in )
                sleep(0.05)
                counter += 1

        # if(counter<60): driver.quit()

        mentions = []
        hashtags = []
        try:
            for x in caption.split(' '):
                if (x[0] == "@"):
                    mentions.append(x)
                elif (x[0] == "#"):
                    hashtags.append(x)

        except:
            pass
        try:
            like_count = driver.find_element(by=By.XPATH, value='//strong[@data-e2e="browse-like-count"]').text
            # print(like_count)
            like_count = get_number_value(like_count)
            print(like_count)


        except Exception as e:

            try:
                like_count = driver.find_element(by=By.XPATH, value='//strong[@data-e2e="like-count"]').text
            except:
                try:
                    like_count = driver.find_element(by=By.XPATH, value='//strong[@data-e2e="like-count"]').text
                except:
                    like_count = '0'
            like_count = get_number_value(like_count)
            print('like_count')

        try:
            comment_count = driver.find_element(by=By.XPATH, value='//strong[@data-e2e="browse-comment-count"]').text
        except:
            try:
                comment_count = driver.find_element(by=By.XPATH, value='//strong[@data-e2e="comment-count"]').text
            except:
                comment_count = '0'
        comment_count = get_number_value(comment_count)
        print('comcount')
        try:
            share_count = driver.find_element(by=By.XPATH, value='//strong[@data-e2e="share-count"]').text
            share_count = get_number_value(share_count)
            print(share_count)
        except:
            share_count = 0

        try:
            driver.execute_script("window.scrollBy(0,500);")
            counter = 0
            while counter < 60:
                try:
                    post_date = driver.find_element(by=By.XPATH,
                                                    value='//span[@data-e2e="browser-nickname"]//span[2]').text
                    break
                except:
                    sleep(0.05)
                    counter += 1
            print(f'post_date is {post_date}')
            post_date = get_date(post_date)
            post_day = post_date.weekday()

            weekday_views[post_day] += post_view_list[posts.index(post)]
            weekday_posts[post_day] += 1
            weekday_engagement_count[post_day] += like_count + comment_count

        except Exception as e:
            print(e)
            exit()

        total_like_count += like_count
        total_comment_count += comment_count
        total_share_count += share_count
        hashtag_blob.extend(hashtags)
        mention_blob.extend(mentions)
        caption_blob += caption
    # print(hashtag_blob)

    for x in list(set(hashtag_blob)):
        hashtag_ranked_list.append([x, hashtag_blob.count(x)])
    hashtag_ranked_list = sorted(hashtag_ranked_list, key=lambda l: l[1], reverse=True)
    for x in list(set(mention_blob)):
        mention_ranked_list.append([x, mention_blob.count(x)])
    mention_ranked_list = sorted(mention_ranked_list, key=lambda l: l[1], reverse=True)

    # hashtag_ranked_list=list(set(hashtag_ranked_list))
    for x in list(set(filter(lambda w: not w in s, caption_blob.split()))):
        if (x[0] != '#'):
            caption_ranked_list.append([x, caption_blob.count(x)])
    caption_ranked_list = sorted(caption_ranked_list, key=lambda l: l[1], reverse=True)
    caption_ranked_list = caption_ranked_list[:min(5, len(caption_ranked_list))]
    hashtag_ranked_list = hashtag_ranked_list[:min(5, len(hashtag_ranked_list))]
    mention_ranked_list = mention_ranked_list[:min(5, len(mention_ranked_list))]
    # caption_ranked_list=list(set(caption_ranked_list))
    # print(total_like_count, total_comment_count, hashtag_ranked_list[:5], caption_ranked_list[:5])
    engagement_rate = (total_like_count + total_comment_count) * 100 / (
                followers_count * min(number_of_posts, len(caption_ranked_list)))
    like_rate = total_like_count * 100 / (followers_count * min(number_of_posts, len(caption_ranked_list)))
    comment_rate = total_comment_count * 100 / (followers_count * min(number_of_posts, len(caption_ranked_list)))
    view_rate = total_views * 100 / (followers_count * min(number_of_posts, len(caption_ranked_list)))
    share_rate = total_share_count * 100 / (followers_count * min(number_of_posts, len(caption_ranked_list)))

    for x in weekday_views:
        weekday_view_rate[weekday_views.index(x)] = x * 100 / (
                    followers_count * min(number_of_posts, len(caption_ranked_list)))

    for x in weekday_engagement_count:
        weekday_engagement_rate[weekday_engagement_count.index(x)] = x * 100 / (
                    followers_count * min(number_of_posts, len(caption_ranked_list)))

    for x in weekday_posts:
        weekday_post_rate[weekday_posts.index(x)] = x / min(number_of_posts, len(caption_ranked_list))

    basic_stats = {
        'Username': username,
        'User Bio': user_bio,
        # 'User Link':user_link,
        'Following Count': following_count,
        'Followers Count': followers_count
    }
    detailed_stats = {
        # 'profile_pic': profile_pic,
        # 'total_likes_till_date':likes_count,
        'Total Like Count': total_like_count,
        'Total Comment Count': total_comment_count,
        # 'Hashtag Ranked List':hashtag_ranked_list,
        # 'Caption Ranked List':caption_ranked_list,
        # 'Mention Ranked List': mention_ranked_list,
        'Total Share Count': total_share_count,
        'Total Views': total_views,
        'Engagement Rate': round(engagement_rate, 3),
        'Like Rate': round(like_rate, 3),
        'Comment Rate': round(comment_rate, 3),
        'View Rate': round(view_rate, 3),
        'Share Rate': round(share_rate, 3)
        # 'Weekday Views':weekday_views,
        # 'Weekday Posts':weekday_posts,
        # 'Weekday Engagement Count':weekday_engagement_count,
        # 'Weekday View Rate':weekday_view_rate,
        # 'Weekday Engagement Rate':weekday_engagement_rate,

    }

    xaxis = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    values_g1 = weekday_views
    values_g2 = weekday_view_rate
    values_g3 = weekday_engagement_count
    values_g4 = weekday_engagement_rate
    values_g5 = weekday_posts

    # print(time.time()-t)
    output_json = {
        # 'profile_pic': profile_pic,
        'following_count': following_count,
        'followers_count': followers_count,
        'total_likes_till_date': likes_count,
        'user_bio': user_bio,
        'user_link': user_link,
        'like_count_last50': total_like_count,
        'total_comment_count': total_comment_count,
        'hashtag_ranked_list': hashtag_ranked_list,
        'caption_ranked_list': caption_ranked_list,
        'mention_ranked_list': mention_ranked_list,
        'total_share_count': total_share_count,
        'total_views': total_views,
        'engagement_rate': engagement_rate,
        'like_rate': like_rate,
        'comment_rate': comment_rate,
        'view_rate': view_rate,
        'share_rate': share_rate,
        'weekday_views': weekday_views,
        'weekday_posts': weekday_posts,
        'weekday_engagement_count': weekday_engagement_count,
        'weekday_view_rate': weekday_view_rate,
        'weekday_engagement_rate': weekday_engagement_rate,

    }
    ref3.child(convert_username_firebase(username)).update(output_json)
    driver.quit()
    del driver
    gc.collect()
    ref3.child('call_counter').update(
        {'call_counter': ref3.child('call_counter').get('call_counter')[0].get('call_counter') + 1})
    return detailed_stats, basic_stats, xaxis, values_g1, values_g2, values_g3, values_g4, values_g5, caption_ranked_list, mention_ranked_list, hashtag_ranked_list


# get_user_profile_detailed('f1')
import datetime


def get_date(temp):
    if ('d ago' in temp):
        temp = int(temp.replace('d ago', ''))
        return (datetime.datetime.today() - datetime.timedelta(days=temp)).date()
    elif (temp.count('-') == 2):
        if (temp[6] == '-'):
            temp = temp[:5] + '0' + temp[5:]
        if (len(temp) == 9):
            temp = temp[:-1] + '0' + temp[-1]
        return datetime.datetime.strptime(temp.replace('-', ''), "%Y%m%d").date()
    elif (temp.count('-') == 1):
        if (temp[1] == '-'):
            temp = '0' + temp
        if (len(temp) == 4):
            temp = temp[:-1] + '0' + temp[-1]
        return datetime.datetime.strptime(f'{datetime.date.today().year}-{temp}'.replace('-', ''), "%Y%m%d").date()
    return datetime.date.today()
