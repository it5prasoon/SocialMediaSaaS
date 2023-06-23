from selenium.webdriver.common.by import By
from spawn_driver import start
from spawn_driver1 import start as start1
import firebase_admin
from firebase_admin import db
from time import time
import gc

cred_obj4 = firebase_admin.credentials.Certificate('snapchat_database.json')
app4 = firebase_admin.initialize_app(cred_obj4, {'databaseURL': 'https://snapchat-23d13-default-rtdb.firebaseio.com/'},
                                     name='app4')
ref4 = db.reference('/', app4)


def start_driver(flag=0):
    if (flag):
        return start1()
    else:
        return start()


def convert_username_firebase(text):
    res = ''
    for x in text:
        res += str(ord(x)) + '-'
    return res[:-1]


def search_discover_page():
    start_driver(1)
    driver.get(f'https://www.snapchat.com/discover')
    posts = []
    while True:
        try:
            posts = [driver.find_element(by=By.XPATH,
                                         value='//div[@class="DiscoverFeed_storyFeedItemWrapper__Gz1yg DiscoverFeed_firstStoryFeedItem__gT_L2"]')]
            break
        except:
            pass
    print(len(posts))
    while len(posts) < 20:
        xx = 0
        print('HEYYYYYY')

        for post in driver.find_elements(by=By.XPATH, value='div[@class="DiscoverFeed_storyFeedItemWrapper__Gz1yg"]'):
            xx += 1
            print(xx)
            if (post not in posts): posts.append(post)

    print(len(posts))
    for post in posts:
        # post_url=post.find_element(by=By.XPATH, value='.//video[@class="StoryWebPlayer_videoPlayer__zfU4l StoryWebPlayer_media__SEsOE"]').get_attribute('src')
        post_author_name = post.find_element(by=By.XPATH,
                                             value='.//span[@class="CreatorContextCard_textColor__nLGUN"]').text
        post_profile_picture = post.find_element(by=By.XPATH, value='.//img[@alt="Profile Picture"]').get_attribute(
            'src')
        post_author_profile_url = post.find_element(by=By.XPATH,
                                                    value='.//a[@class="SuppressedDefaultActionLink_link__xPM2W"]').get_attribute(
            'href')
        print(post_author_name)
        driver.execute_script("window.scrollBy(0,500);")


def get_lens_page_info():
    driver = start_driver(1)
    url = f'https://lens.snapchat.com/'
    driver.get(url)
    while True:
        lenses = driver.find_elements(by=By.XPATH, value='//div[@class="LensGrid_item__Kxttt"]')
        if (len(lenses)): break
    print(len(lenses))
    c = 0
    main_dict = {}
    for lens in lenses:
        while True:
            try:
                lens_name = lens.find_element(by=By.XPATH,
                                              value='.//div[@class="LensTile_lensName__cOdmj LensTile_truncated__8TKmY LensTile_link__RSOey"]').text
                break
            except Exception as e:
                lens = driver.find_elements(by=By.XPATH, value='//div[@class="LensGrid_item__Kxttt"]')[c]
        while True:
            try:
                lens_author_name = lens.find_element(by=By.XPATH,
                                                     value='.//div[@class="LensTile_creatorName__7SbG7 LensTile_truncated__8TKmY"]').text
                lens_icon_img_url = lens.find_element(by=By.XPATH,
                                                      value='.//img[@class="LensTile_tileIcon__wSUDo"]').get_attribute(
                    'src')
                lens_thumbnail = lens.find_element(by=By.XPATH,
                                                   value='.//img[@class="ImageTile_tileMedia__EnPeo"]').get_attribute(
                    'src')
                lens_url = lens.find_element(by=By.XPATH, value='.//a[@class="LensTile_link__RSOey"]').get_attribute(
                    'href')
                lens_url = f'https://lens.snapchat.com/{lens_url[lens_url.index("&uuid=") + 6:lens_url.index("&metadata")]}'
                break
            except:
                lens = driver.find_elements(by=By.XPATH, value='//div[@class="LensGrid_item__Kxttt"]')[c]
        main_dict.update({c: {'lens_name': lens_name, 'lens_author_name': lens_author_name,
                              'lens_icon_img_url': lens_icon_img_url, 'lens_thumbnail': lens_thumbnail,
                              'lens_url': lens_url}})
        ref4.child(str(c)).update(
            {'lens_name': lens_name, 'lens_author_name': lens_author_name, 'lens_icon_img_url': lens_icon_img_url,
             'lens_thumbnail': lens_thumbnail, 'lens_url': lens_url})
        c += 1
    driver.quit()
    return main_dict


def get_user_page_info(username):
    driver = start_driver(1)
    url = f'https://www.snapchat.com/add/{username}'
    driver.get(url)
    t = time()
    while time() - t < 10:
        try:
            profile_display_name = driver.find_element(by=By.XPATH,
                                                       value='//span[@class="PublicProfileDetailsCard_displayNameText__xA50x PublicProfileDetailsCard_textColor__wIKUa PublicProfileDetailsCard_oneLineTruncation__SeuMy"]').text
            break
        except:
            pass
    if (time() - t > 100):
        driver.quit()
        del driver
        gc.collect()
        return False

    try:
        profile_subscriber_count = driver.find_element(by=By.XPATH,
                                                       value='//div[@class="PublicProfileDetailsCard_desktopSubscriberText__wQcXg PublicProfileDetailsCard_subscribersDesktop__Lgnmt"]').text
    except:
        profile_subscriber_count = None
    try:
        profile_snapcode_image = driver.find_element(by=By.XPATH,
                                                     value='//img[@data-test="snapCodeImage"]').get_attribute('src')
    except:
        profile_snapcode_image = None
    try:
        profile_bio = driver.find_element(by=By.XPATH,
                                          value='//div[@class="PublicProfileCard_desktopTitle__9ik6D PublicProfileCard_desktopText__IYnRg"]').text
    except:
        profile_bio = None
    try:
        profile_location = driver.find_element(by=By.XPATH, value='//div[@data-test="secondaryDetailsAddress"]').text
    except:
        profile_location = None
    try:
        profile_additional_website_url = driver.find_element(by=By.XPATH,
                                                             value='//div[@data-test="secondaryDetailsWebSiteUrl"]').find_element(
            by=By.TAG_NAME, value='a').get_attribute('href')
    except:
        profile_additional_website_url = None
    stories = driver.find_elements(by=By.XPATH,
                                   value='//div[@class="StoryHighlightTile_highlightWrapperDesktop__G6Kox StoryHighlightTile_highlightWrapper__R_GvA"]')
    story_dict = {}
    for story in stories:
        try:
            story_caption = story.find_element(by=By.XPATH,
                                               value='.//span[@class="StoryHighlightTile_storyTitle__HKy8l"]').text
        except:
            story_caption = None
        try:
            story_thumbnail = story.find_element(by=By.XPATH,
                                                 value='.//img[@class="ImageTile_tileMedia__JCUC0"]').get_attribute(
                'src')
        except:
            story_thumbnail = None
        story_dict.update({stories.index(story): {'story_caption': story_caption, 'story_thumbnail': story_thumbnail}})
    spotlights = driver.find_elements(by=By.XPATH,
                                      value='//div[@class="StoryHighlightTile_highlightWrapperDesktop__G6Kox StoryHighlightTile_highlightWrapper__R_GvA"]')
    spotlight_dict = {}
    for spotlight in spotlights:
        try:
            spotlight_thumbnail = spotlight.find_element(by=By.XPATH,
                                                         value='.//img[@class="ImageTile_tileMedia__JCUC0"]').get_attribute(
                'src')
        except:
            spotlight_thumbnail = None
        spotlight_dict.update({spotlights.index(spotlight): {'spotlight_thumbnail': spotlight_thumbnail}})
    lenses = driver.find_elements(by=By.XPATH, value='//div[@class="LensList_desktopItemContainer__aJcMH"]')
    lens_dict = {}
    for lens in lenses:
        try:
            lens_name = lens.find_element(by=By.XPATH,
                                          value='.//span[@class="LensTile_lensName__61_dk LensTile_truncated__5qXd6 LensTile_link__HTic6"]').text
        except:
            lens_name = None
        try:
            lens_icon_img_url = lens.find_element(by=By.XPATH,
                                                  value='.//img[@class="LensTile_tileIcon__SWyAT"]').get_attribute(
                'src')
        except:
            lens_icon_img_url = None
        try:
            lens_thumbnail = lens.find_element(by=By.XPATH,
                                               value='.//img[@class="ImageTile_tileMedia__JCUC0"]').get_attribute('src')
        except:
            lens_thumbnail = None
        try:
            lens_url = lens.find_element(by=By.XPATH, value='.//a[@class="LensTile_link__HTic6"]').get_attribute('href')
            lens_url = f'https://lens.snapchat.com/{lens_url[lens_url.index("&uuid=") + 6:lens_url.index("&metadata")]}'
        except:
            lens_url = None
        lens_dict.update({lenses.index(lens): {'lens_name': lens_name, 'lens_icon_img_url': lens_icon_img_url,
                                               'lens_thumbnail': lens_thumbnail, 'lens_url': lens_url}})

    if (time() - t > 15):
        driver.quit()
        del driver
        gc.collect()
        return False
    ref4.child(convert_username_firebase(username)).update({
        'profile_display_name': profile_display_name,
        'profile_subscriber_count': profile_subscriber_count,
        'profile_snapcode_image': profile_snapcode_image,
        'profile_bio': profile_bio,
        'profile_location': profile_location,
        'profile_additional_website_url': profile_additional_website_url,
        'stories': story_dict,
        'spotlights': spotlight_dict,
        'lenses': lens_dict
    })
    driver.quit()
    del driver
    gc.collect()
    return {
        'username': username,
        'profile_display_name': profile_display_name,
        'profile_subscriber_count': profile_subscriber_count,
        'profile_snapcode_image': profile_snapcode_image,
        'profile_bio': profile_bio,
        'profile_location': profile_location,
        'profile_additional_website_url': profile_additional_website_url,
        'stories': story_dict,
        'spotlights': spotlight_dict,
        'lenses': lens_dict
    }

    {
        'profile_display_name': profile_display_name,
        'profile_subscriber_count': profile_subscriber_count,
        'profile_snapcode_image': profile_snapcode_image,
        'profile_bio': profile_bio,
        'profile_location': profile_location,
        'profile_additional_website_url': profile_additional_website_url,
        'story_caption': story_caption,
        'story_thumbnail': story_thumbnail,
        'spotlight_thumbnail': spotlight_thumbnail,
        'lens_name': lens_name,
        'lens_icon_img_url': lens_icon_img_url,
        'lens_thumbnail': lens_thumbnail,
        'lens_url': lens_url
    }


def check_profile_exists(username):
    driver = start_driver(1)
    driver.get(f'https://www.snapchat.com/add/{username}')
    # t=time()
    while True:  # time()-t>100:
        try:
            driver.find_element(by=By.XPATH, value='//div[@class="PageFrame_navContainer__QR3yv"]')
            break
        except:
            pass
    try:
        if ('This content was not found' in driver.find_element(by=By.XPATH,
                                                                value='//span[@class="NoContent_subtitle__15G7T"]').text):
            print("KUN")
            driver.quit()
            return {'Username Entered': username, 'Account Status': False}
    except:
        print('SAA')
        driver.quit()
        return {'Username Entered': username, 'Account Status': True}

    return True
