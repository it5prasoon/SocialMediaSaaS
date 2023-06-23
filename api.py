from flask import Flask, redirect, request, render_template, session
import stripe
from login import register, sign_in

app = Flask(__name__, static_url_path="", static_folder="public")
app.secret_key = "<secret_key>"
# YOUR_DOMAIN='http://127.0.0.1:3000'
YOUR_DOMAIN = 'http://ec2-13-38-250-240.eu-west-3.compute.amazonaws.com'

stripe.api_key = "sk_test_51LUAXZSHmtYCXaFaBsM4MyH4LjCSdsYqW5jznLNFxTnLmkJV4SYBq2q91qVMEDnhth8LtdVNi4GsxlRebXyS6CA500H2j2W1Xn"
from tiktok import get_user_profile, get_hashtag_posts, get_music_posts, get_user_profile_detailed, search_user, \
    search_general
from snapchat import search_discover_page, get_lens_page_info, get_user_page_info, check_profile_exists
from send_mail import send_email
from twitter import get_profile_info as twitter_get_profile_info
from fetch_keyword import *
import string, random, json


def random_filename():
    res = ''.join(random.choices(string.ascii_uppercase, k=10))
    return res


@app.route('/')
def hello_world():
    return redirect(f'{YOUR_DOMAIN}/loginPage.html')


@app.route('/loginPage.html', methods=['POST'])
def loginpage():
    print(123)
    username = request.form.get("email")
    password = request.form.get("password")
    print(username, password)
    if (sign_in(username, password)):
        session["username"] = username
        session["flag"] = 1
        return redirect(f'{YOUR_DOMAIN}/search.html')
    else:
        return render_template(f'loginerror.html')


@app.route('/search.html')
def search_page():
    try:
        print(session)
        if (session["flag"] == 1):
            session["flag"] = 0
            return render_template(f'search.html')
        else:
            return redirect(f'{YOUR_DOMAIN}/loginPage.html')

    except:
        return redirect(f'{YOUR_DOMAIN}/loginPage.html')


@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    try:
        global email
        email = request.form.get("email")
        print(email)
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price': 'price_1LUAegSHmtYCXaFattbTMrof',
                    'quantity': 1
                }
            ],
            mode='subscription',
            success_url=YOUR_DOMAIN + '/success.html',
            cancel_url=YOUR_DOMAIN + '/cancel.html'
        )
    except Exception as e:
        return str(e)
    return redirect(checkout_session.url, code=303)


@app.route(f'/success.html')
def success():
    send_email(email)
    return redirect(YOUR_DOMAIN + '/mail_sent.html')


@app.route(f'/signupPage.html', methods=['POST'])
def signup():
    username = request.form.get('email')
    password = request.form.get('password')
    print(username, password)
    if (register(username, password)):
        status = [1]
        someTest = {''}
        return render_template('signupPage.html', someTest=True)
    else:
        someTest = False
        return render_template('signupPage.html', someTest=someTest)


@app.route(f'/profile_search_tiktok', methods=['POST'])
def profile_search_tiktok():
    profile_search_tiktok = request.form.get("profile_search_tiktok")
    temp = get_user_profile(profile_search_tiktok)
    while temp == False:
        temp = get_user_profile(profile_search_tiktok)

    return render_template('record.html', result=temp)


@app.route(f'/profile_search_tiktok_detailed', methods=['GET', 'POST'])
# @login_required
def profile_search_tiktok_detailed():
    profile_search_tiktok_detailed = request.form.get("profile_search_tiktok_detailed")
    detailed_stats, basic_stats, xaxis, values_g1, values_g2, values_g3, values_g4, values_g5, caption_ranked_list, mention_ranked_list, hashtag_ranked_list = get_user_profile_detailed(
        profile_search_tiktok_detailed, 10)
    while detailed_stats == False:
        detailed_stats, basic_stats, xaxis, values_g1, values_g2, values_g3, values_g4, values_g5, caption_ranked_list, mention_ranked_list, hashtag_ranked_list = get_user_profile_detailed(
            profile_search_tiktok_detailed, 10)

    return render_template('record.html', detailed_stats=detailed_stats, basic_stats=basic_stats, xaxis=xaxis,
                           values_g1=values_g1, values_g2=values_g2, values_g3=values_g3, values_g4=values_g4,
                           values_g5=values_g5, caption_ranked_list=caption_ranked_list,
                           mention_ranked_list=mention_ranked_list, hashtag_ranked_list=hashtag_ranked_list)


@app.route(f'/hashtag_search_tiktok', methods=['POST'])
def hashtag_search_tiktok():
    hashtag_search_tiktok = request.form.get("hashtag_search_tiktok")
    print(hashtag_search_tiktok)

    return test2(hashtag_search_tiktok)


@app.route(f'/music_search_tiktok', methods=['POST'])
def music_search_tiktok():
    music_search_tiktok = request.form.get("music_search_tiktok")
    return test3(music_search_tiktok)


@app.route(f'/user_search_tiktok', methods=['POST'])
def user_search_tiktok():
    user_search_tiktok = request.form.get("user_search_tiktok")

    return test4(user_search_tiktok)


@app.route(f'/general_search_tiktok', methods=['POST'])
def general_search_tiktok():
    general_search_tiktok = request.form.get("general_search_tiktok")

    return test5(general_search_tiktok)


@app.route(f'/profile_search_snapchat', methods=['POST'])
def profile_search_snapchat():
    profile_search_snapchat = request.form.get("profile_search_snapchat")
    temp = test8(profile_search_snapchat)

    return temp


@app.route(f'/check_profile_status', methods=['POST'])
def check_profile_status():
    check_profile_status = request.form.get("check_profile_status")
    temp = test9(check_profile_status)

    return temp


@app.route(f'/check_lens_page', methods=['POST'])
def check_lens_page():
    # check_profile_status = request.form.get("check_lens_page")
    # return test7()
    temp = test7()
    while temp == False:
        temp = test7()
    return temp


@app.route(f'/twitter_get_user_profile', methods=['GET', 'POST'])
def get_twitter_profile():
    get_twitter_profile = request.form.get('get_twitter_profile')
    profile_type, detailed_stats, basic_stats, xaxis, values_g1, values_g2, values_g3, values_g4, values_g5, text_ranked_list, hashtag_ranked_list = twitter_get_profile_info(
        get_twitter_profile)
    if (profile_type == 'Private'):
        return {'Profile_Type': "Private"}
    while detailed_stats == False:
        profile_type, detailed_stats, basic_stats, xaxis, values_g1, values_g2, values_g3, values_g4, values_g5, text_ranked_list, hashtag_ranked_list = twitter_get_profile_info(
            get_twitter_profile)
    return render_template('record_twitter.html', detailed_stats=detailed_stats, basic_stats=basic_stats, xaxis=xaxis,
                           values_g1=values_g1, values_g2=values_g2, values_g3=values_g3, values_g4=values_g4,
                           values_g5=values_g5, caption_ranked_list=text_ranked_list,
                           hashtag_ranked_list=hashtag_ranked_list)


#######################################################################################
#######################################################################################
#######################################################################################
@app.route(f'/tiktok/get_user_profile/<profile_name>')
def test1(profile_name):
    temp = get_user_profile(profile_name)
    while temp == False:
        temp = test1(profile_search_tiktok)
    return temp


@app.route(f'/tiktok/get_user_profile_detailed/<profile_name>/<number_of_posts>')
def test_detailed(profile_name, number_of_posts):
    content = request.json
    number_of_posts = int(number_of_posts)
    if (sign_in(content.get('username'), content.get('password'))):
        detailed_stats, basic_stats, xaxis, values_g1, values_g2, values_g3, values_g4, values_g5, caption_ranked_list, mention_ranked_list, hashtag_ranked_list = get_user_profile_detailed(
            profile_name, number_of_posts)
        while detailed_stats == False:
            detailed_stats, basic_stats, xaxis, values_g1, values_g2, values_g3, values_g4, values_g5, caption_ranked_list, mention_ranked_list, hashtag_ranked_list = get_user_profile_detailed(
                profile_name, number_of_posts)

        z = basic_stats | detailed_stats
        z.update({'weekday_views': values_g1, 'weekday_view_rate': values_g2, 'weekday_engagement_count': values_g3,
                  'weekday_engagement_rate': values_g4, 'weekday_posts': values_g5,
                  'caption_ranked_list': caption_ranked_list, 'mention_ranked_list': mention_ranked_list,
                  'hashtag_ranked_list': hashtag_ranked_list})
        return z
    else:
        return {'Verification_Status': "False"}


@app.route(f'/general/get_keywords')
def get_keywords():
    # content=request.json
    json_data = request.files['json_data']
    content = json.load(json_data)

    if (sign_in(content.get('username'), content.get('password'))):
        try:
            doc = content.get('doc')
        except:
            doc = ""
        try:
            keyphrase_ngram_range = tuple(content.get('keyphrase_ngram_range'))
        except:
            keyphrase_ngram_range = (1, 1)
        try:
            stop_words = content.get('stop_words')
        except:
            stop_words = 'english'
        # candidates=list(content.get('candidates'))
        # except: candidates=None
        try:
            top_n = int(content.get('top_n'))
        except:
            top_n = 5
        try:
            min_df = int(content.get('min_df'))
        except:
            min_df = 1
        try:
            use_maxsum = bool(content.get('use_maxsum'))
        except:
            use_maxsum = False
        try:
            use_mmr = bool(content.get('use_mmr'))
        except:
            use_mmr = False
        try:
            diversity = float(content.get('diversity'))
        except:
            diversity = 0.6
        try:
            nr_candidates = int(content.get('nr_candidates'))
        except:
            nr_candidates = 20
        # try: vectorizer=content.get('vectorizer')
        # except: vectorizer=None
        # try: highlight=bool(content.get('highlight'))
        # except: highlight=None
        # try: seed_keywords=list(content.get('seed_keywords'))
        # except: seed_keywords=None
        # try: doc_embeddings=content.get('doc_embeddings')
        # except: doc_embeddings=None
        # try: word_embeddings=content.get('word_embeddings')
        # except: word_embeddings=None
        # try: 
        #     uploaded_img = request.files['image']
        #     uploaded_img.save('savedImage.png')
        #     print(type(uploaded_img))
        #     img='savedImage.png'
        #     print(img)
        # except Exception as e:
        #     print(e) 

        #     img=None
        # try: 
        #     uploaded_vid = request.files['video']
        #     uploaded_vid.save('savedvid.mp4')
        #     vid="savedvid.mp4"
        # except: vid=None

        # print(img)

        return {"Keywords": fetch_keyword(doc, keyphrase_ngram_range, stop_words, top_n, min_df, use_maxsum, use_mmr,
                                          diversity, nr_candidates)}
    else:
        return {'Processing_Status': "Failed"}


@app.route(f'/general/get_keywords_from_image')
def get_keywords_from_image():
    json_data = request.files['json_data']
    content = json.load(json_data)
    if (sign_in(content.get('username'), content.get('password'))):
        try:
            keyphrase_ngram_range = tuple(content.get('keyphrase_ngram_range'))
        except:
            keyphrase_ngram_range = (1, 1)
        try:
            stop_words = content.get('stop_words')
        except:
            stop_words = 'english'
        # candidates=list(content.get('candidates'))
        # except: candidates=None
        try:
            top_n = int(content.get('top_n'))
        except:
            top_n = 5
        try:
            min_df = int(content.get('min_df'))
        except:
            min_df = 1
        try:
            use_maxsum = bool(content.get('use_maxsum'))
        except:
            use_maxsum = False
        try:
            use_mmr = bool(content.get('use_mmr'))
        except:
            use_mmr = False
        try:
            diversity = float(content.get('diversity'))
        except:
            diversity = 0.6
        try:
            nr_candidates = int(content.get('nr_candidates'))
        except:
            nr_candidates = 20
        # try: vectorizer=content.get('vectorizer')
        # except: vectorizer=None
        # try: highlight=bool(content.get('highlight'))
        # except: highlight=None
        # try: seed_keywords=list(content.get('seed_keywords'))
        # except: seed_keywords=None
        # try: doc_embeddings=content.get('doc_embeddings')
        # except: doc_embeddings=None
        # try: word_embeddings=content.get('word_embeddings')
        # except: word_embeddings=None
        try:
            uploaded_img = request.files['image']
            img = f'{random_filename()}.png'
            uploaded_img.save(img)

        except Exception as e:
            print(e)
            img = None
        return {"Keywords": fetch_keyword_from_image(img, keyphrase_ngram_range, stop_words, top_n, min_df, use_maxsum,
                                                     use_mmr, diversity, nr_candidates)}
    else:
        return {'Processing_Status': "Failed"}


@app.route(f'/general/get_keywords_from_video')
def get_keywords_from_video():
    json_data = request.files['json_data']
    content = json.load(json_data)
    if (sign_in(content.get('username'), content.get('password'))):
        try:
            keyphrase_ngram_range = tuple(content.get('keyphrase_ngram_range'))
        except:
            keyphrase_ngram_range = (1, 1)
        try:
            stop_words = content.get('stop_words')
        except:
            stop_words = 'english'
        # candidates=list(content.get('candidates'))
        # except: candidates=None
        try:
            top_n = int(content.get('top_n'))
        except:
            top_n = 5
        try:
            min_df = int(content.get('min_df'))
        except:
            min_df = 1
        try:
            use_maxsum = bool(content.get('use_maxsum'))
        except:
            use_maxsum = False
        try:
            use_mmr = bool(content.get('use_mmr'))
        except:
            use_mmr = False
        try:
            diversity = float(content.get('diversity'))
        except:
            diversity = 0.6
        try:
            nr_candidates = int(content.get('nr_candidates'))
        except:
            nr_candidates = 20
        # try: vectorizer=content.get('vectorizer')
        # except: vectorizer=None
        # try: highlight=bool(content.get('highlight'))
        # except: highlight=None
        # try: seed_keywords=list(content.get('seed_keywords'))
        # except: seed_keywords=None
        # try: doc_embeddings=content.get('doc_embeddings')
        # except: doc_embeddings=None
        # try: word_embeddings=content.get('word_embeddings')
        # except: word_embeddings=None
        try:
            uploaded_vid = request.files['video']
            vid = f'{random_filename()}.mp4'
            uploaded_vid.save(vid)
            print(vid)
        except Exception as e:
            print(e)
            vid = None
        return {"Keywords": fetch_keyword_from_video(vid, keyphrase_ngram_range, stop_words, top_n, min_df, use_maxsum,
                                                     use_mmr, diversity, nr_candidates)}
    else:
        return {'Processing_Status': "Failed"}


@app.route(f'/tiktok/get_hashtag_posts/<hashtag>')
def test2(hashtag):
    return get_hashtag_posts(hashtag)


@app.route(f'/tiktok/get_music_posts/<keyword>')
def test3(keyword):
    return get_music_posts(keyword)


@app.route(f'/tiktok/search_user/<keyword>')
def test4(keyword):
    return search_user(keyword)


@app.route(f'/tiktok/search_general/<keyword>')
def test5(keyword):
    return search_general(keyword)


@app.route('/snapchat/search_discover_page')
def test6():
    return search_discover_page()


@app.route('/snapchat/get_lens_page_info')
def test7():
    return get_lens_page_info()


@app.route('/snapchat/get_user_page_info/<username>')
def test8(username):
    return get_user_page_info(username)


@app.route('/snapchat/check_profile_exists/<username>')
def test9(username):
    return check_profile_exists(username)


@app.route(f'/twitter/get_user_profile/<profile_name>/<number_of_tweets>')
def test_detailed_twitter(profile_name, number_of_tweets):
    content = request.json
    number_of_tweets = int(number_of_tweets)
    if (sign_in(content.get('username'), content.get('password'))):
        profile_type, detailed_stats, basic_stats, xaxis, values_g1, values_g2, values_g3, values_g4, values_g5, text_ranked_list, hashtag_ranked_list = twitter_get_profile_info(
            profile_name, number_of_tweets)
        while detailed_stats == False:
            profile_type, detailed_stats, basic_stats, xaxis, values_g1, values_g2, values_g3, values_g4, values_g5, text_ranked_list, hashtag_ranked_list = twitter_get_profile_info(
                profile_name, number_of_tweets)

        z = basic_stats | detailed_stats
        z.update({'weekday_views': values_g1, 'weekday_view_rate': values_g2, 'weekday_engagement_count': values_g3,
                  'weekday_engagement_rate': values_g4, 'weekday_posts': values_g5,
                  'text_ranked_list': text_ranked_list, 'hashtag_ranked_list': hashtag_ranked_list})
        return z
    else:
        return {'Verification_Status': "False"}


if (__name__ == '__main__'):
    app.run(host='0.0.0.0', port=3000, threaded=True, debug=True)
