import gc
from time import sleep, time

import firebase_admin
from firebase_admin import firestore
from nltk.corpus import stopwords
from selenium.webdriver.common.by import By

from spawn_driver import start
from spawn_driver1 import start as start1

cred_obj5 = firebase_admin.credentials.Certificate('twitter_database.json')
firebase_admin.initialize_app(cred_obj5)
db = firestore.client()
# ref5=db.reference('/', app5)
import datetime

s = set(stopwords.words('english'))


def get_number_value(text):
    text = text.replace(',', '')
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


def get_date(temp):
    print(temp)
    if (temp.count(',') == 1):
        if (temp[0].isalpha()):
            return datetime.datetime.strptime(temp, '%b %d, %Y')
        else:
            return datetime.datetime.strptime(temp, '%d %b, %Y')
    elif (' ' in temp):
        temp = f'{temp}, {datetime.date.today().year}'
        if (temp[0].isalpha()):
            return datetime.datetime.strptime(temp, '%b %d, %Y')
        else:
            return datetime.datetime.strptime(temp, '%d %b, %Y')
    return datetime.date.today()


def get_profile_info(username, limit=50):
    try:
        driver.quit()
        del driver
        gc.collect()
    except:
        pass
    driver = start_driver(1)
    t = time()
    url = f'https://twitter.com/{username}'
    driver.get(url)
    count = 0
    while True:
        if (time() - t > limit * 10):
            driver.quit()
            del driver
            gc.collect()
            return 'Public', False, False, False, False, False, False, False, False, False, False
        try:
            if (count > 20):
                driver.refresh()
                count = -10000000
            account_name = driver.find_element(by=By.XPATH,
                                               value='//div[@class="css-901oao r-1awozwy r-18jsvk2 r-6koalj r-37j5jr r-adyw6z r-1vr29t4 r-135wba7 r-bcqeeo r-1udh08x r-qvutc0"]').text
            break
        except:
            count += 1
            sleep(0.1)

    if (len(driver.find_elements(by=By.XPATH, value='//div[@aria-label="Provides details about verified accounts."]'))):
        verified_account = True
    else:
        verified_account = False
    try:
        user_bio = driver.find_element(by=By.XPATH, value='//div[@data-testid="UserDescription"]').text
    except:
        user_bio = None
    account_dob = driver.find_element(by=By.XPATH, value='//span[@data-testid="UserJoinDate"]').text.replace('Joined ',
                                                                                                             '')
    following_count = int(get_number_value(
        driver.find_element(by=By.XPATH, value=f'//a[@href="/{username}/following"]').text.replace(' Following', '')))
    followers_count = int(get_number_value(
        driver.find_element(by=By.XPATH, value=f'//a[@href="/{username}/followers"]').text.replace(' Followers', '')))
    total_tweet_count = driver.find_element(by=By.XPATH,
                                            value='//div[@class="css-901oao css-1hf3ou5 r-14j79pv r-37j5jr r-n6v787 r-16dba41 r-1cwl3u0 r-bcqeeo r-qvutc0"]').text.replace(
        ' Tweets', '')
    total_tweet_count = int(get_number_value(total_tweet_count))
    # return account_name, account_dob, user_bio, followers_count, following_count, total_tweet_count

    tweets = []
    total_reply_count, total_retweet_count, total_like_count = 0, 0, 0
    weekday_likes, weekday_posts, weekday_engagement_rate, weekday_engagement_count, weekday_like_rate, weekday_post_rate = [
        0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0,
                                                                                                    0], [0, 0, 0, 0, 0,
                                                                                                         0, 0]
    text_blob = ''
    hashtag_blob = []
    while len(tweets) < limit:
        if (time() - t > limit * 10):
            driver.quit()
            del driver
            gc.collect()
            return 'Public', False, False, False, False, False, False, False, False, False, False
        try:
            for tweet in driver.find_elements(by=By.XPATH,
                                              value='//div[@class="css-1dbjc4n r-1iusvr4 r-16y2uox r-1777fci r-kzbkwu"]'):
                if (len(driver.find_elements(by=By.XPATH, value='//div[@data-testid="sheetDialog"]'))):
                    driver.refresh()
                    # while True:
                    #     try: 
                    #         tweet_date=tweet.find_element(by=By.XPATH, value='.//div[@class="css-1dbjc4n r-18u37iz r-1q142lx"]').text
                    #         break
                    #     except: 
                    #         driver.execute_script("window.scrollBy(0,2500);")
                if (len(driver.find_elements(by=By.XPATH, value='//div[@data-testid="emptyState"]'))):
                    return 'Private', False, False, False, False, False, False, False, False, False, False
                if (tweet not in tweets):
                    tweets.append(tweet)
                    tweet_date = tweet.find_element(by=By.XPATH,
                                                    value='.//div[@class="css-1dbjc4n r-18u37iz r-1q142lx"]').text
                    tweet_text = tweet.find_element(by=By.XPATH, value='.//div[@data-testid="tweetText"]').text
                    if (len(tweet.find_elements(by=By.XPATH, value='.//div[@data-testid="tweetPhoto"]'))):
                        media_flag = True
                    else:
                        media_flag = False
                    reply_count = int(
                        get_number_value(tweet.find_element(by=By.XPATH, value='.//div[@data-testid="reply"]').text))
                    retweet_count = int(
                        get_number_value(tweet.find_element(by=By.XPATH, value='.//div[@data-testid="retweet"]').text))
                    like_count = int(
                        get_number_value(tweet.find_element(by=By.XPATH, value='.//div[@data-testid="like"]').text))

                    # print(tweet_date)
                    # print(tweet_text)
                    # print(reply_count)
                    # print(retweet_count)
                    # print(like_count)
                    # print(media_flag)
                    total_reply_count += reply_count
                    total_retweet_count += retweet_count
                    total_like_count += like_count
                    tweet_text = tweet_text.replace('\n', ' ')
                    tweet_text = tweet_text.replace('.', ' ')
                    while '  ' in tweet_text:
                        tweet_text = tweet_text.replace('  ', ' ')

                    # tweet_text=tweet_text.strip()
                    text_blob += tweet_text + ' '

                    tweet_date = get_date(tweet_date)
                    tweet_day = tweet_date.weekday()
                    print(tweet_day, '-----------')
                    weekday_likes[tweet_day] += like_count
                    weekday_engagement_count[tweet_day] += like_count + retweet_count + reply_count
                    weekday_posts[tweet_day] += 1
                    if (tweet_day in [0]): print('HELLO')
                    # print(weekday_engagement_count)

                if (len(tweets) > limit): break
        except Exception as e:
            print(e)
        driver.execute_script("window.scrollBy(0,350);")
    driver.quit()
    del driver
    gc.collect()
    print('DONEEEEEEEEE')

    # print(total_reply_count, total_retweet_count, total_like_count)

    while '  ' in text_blob:
        text_blob = text_blob.replace('  ', ' ')
    text_blob.strip(' ')
    for word in text_blob.split(' '):
        try:
            if (word[0] == '#'):
                hashtag_blob.append(word)
        except:
            pass

    text_ranked_list, hashtag_ranked_list = [], []
    for x in list(set(filter(lambda w: not w in s, text_blob.split()))):
        if (x[0] != '#' and len(x) > 1 and x.isnumeric() == False):
            text_ranked_list.append([x, text_blob.count(x)])
    text_ranked_list = sorted(text_ranked_list, key=lambda l: l[1], reverse=True)
    text_ranked_list = text_ranked_list[:min(5, len(text_ranked_list))]

    for x in list(set(hashtag_blob)):
        hashtag_ranked_list.append([x, hashtag_blob.count(x)])
    hashtag_ranked_list = sorted(hashtag_ranked_list, key=lambda l: l[1], reverse=True)

    # print(text_ranked_list, hashtag_ranked_list)

    engagement_rate = (total_like_count + total_reply_count + total_retweet_count) * 100 / (
            followers_count * min(limit, total_tweet_count))
    like_rate = total_like_count * 100 / (followers_count * min(limit, total_tweet_count))
    reply_rate = total_reply_count * 100 / (followers_count * min(limit, total_tweet_count))
    retweet_rate = total_retweet_count * 100 / (followers_count * min(limit, total_tweet_count))

    for x in weekday_likes:
        weekday_like_rate[weekday_likes.index(x)] = x * 100 / (followers_count * min(limit, total_tweet_count))
    for x in weekday_engagement_count:
        weekday_engagement_rate[weekday_engagement_count.index(x)] = x * 100 / (
                followers_count * min(limit, total_tweet_count))
    for x in weekday_posts:
        weekday_post_rate[weekday_posts.index(x)] = x * 100 / (followers_count * min(limit, total_tweet_count))

    basic_stats = {
        'Account Name': account_name,
        'User Bio': user_bio,
        'Verfied Account': verified_account,
        'Following Count': following_count,
        'Followers Count': followers_count,
        'Account Since': account_dob,
        'Total Tweet Count': total_tweet_count
    }

    detailed_stats = {
        'Total Like Count': total_like_count,
        'Total Reply Count': total_reply_count,
        'Total Retweet Count': total_retweet_count,
        'Total Engagement': total_like_count + total_reply_count + total_retweet_count,
        'Like Rate': round(like_rate, 3),
        'Reply Rate': round(reply_rate, 3),
        'Retweet Rate': round(retweet_rate, 3),
        'Engagement Rate': round(engagement_rate, 3)
    }

    xaxis = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    values_g1 = weekday_likes
    values_g2 = weekday_like_rate
    values_g3 = weekday_engagement_count
    values_g4 = weekday_engagement_rate
    values_g5 = weekday_posts

    database_json = {
        'Account Name': account_name,
        'User Bio': user_bio,
        'Verfied Account': verified_account,
        'Following Count': following_count,
        'Followers Count': followers_count,
        'Account Since': account_dob,
        'Total Tweet Count': total_tweet_count,
        'Total Like Count': total_like_count,
        'Total Reply Count': total_reply_count,
        'Total Retweet Count': total_retweet_count,
        'Total Engagement': total_like_count + total_reply_count + total_retweet_count,
        'Like Rate': round(like_rate, 3),
        'Reply Rate': round(reply_rate, 3),
        'Retweet Rate': round(retweet_rate, 3),
        'Engagement Rate': round(engagement_rate, 3),
        'weekday_likes': weekday_likes,
        'weekday_like_rate': weekday_like_rate,
        'weekday_engagement_count': weekday_engagement_count,
        'weekday_engagement_rate': weekday_engagement_rate,
        'weekday_posts': weekday_posts,
        'weekday_post_rate': weekday_post_rate

    }

    db.collection('accounts').document(username).set(database_json)

    return 'Public', detailed_stats, basic_stats, xaxis, values_g1, values_g2, values_g3, values_g4, values_g5, text_ranked_list, hashtag_ranked_list
