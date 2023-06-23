from keybert import KeyBERT
from image_to_text import get_text
from vid_to_text import vid_to_text
import os


def fetch_keyword(doc, keyphrase_ngram_range, stop_words, top_n, min_df, use_maxsum, use_mmr, diversity, nr_candidates):
    kw_model = KeyBERT()
    # keywords=kw_model.extract_keywords(doc, keyphrase_ngram_range=keyphrase_ngram_range, stop_words=stop_words, candidates=candidates)
    keywords = kw_model.extract_keywords(doc,
                                         keyphrase_ngram_range=keyphrase_ngram_range,  # length of extracted keywords
                                         stop_words=stop_words,
                                         # candidates=candidates,
                                         top_n=top_n,  # return top n keywords
                                         min_df=min_df,
                                         # min document frequency of a keyword. Prefer setting it to >1 only for big blob
                                         use_maxsum=use_maxsum,
                                         use_mmr=use_mmr,  # use Maximal Marginal Relevance
                                         diversity=diversity,  # diversity between results if MMR is set to true
                                         nr_candidates=nr_candidates)  # number of candidates to consider if maxsum isTrue
    # vectorizer=vectorizer,
    # highlight=highlight)
    # seed_keywords=seed_keywords,                     #pass a bunch of keywords to guide the algo towards these keywords
    # doc_embeddings=doc_embeddings,
    # word_embeddings=word_embeddings)
    return keywords


def fetch_keyword_from_image(img, keyphrase_ngram_range, stop_words, top_n, min_df, use_maxsum, use_mmr, diversity,
                             nr_candidates):
    doc = get_text(img, 1)
    os.remove(img)
    return fetch_keyword(doc, keyphrase_ngram_range, stop_words, top_n, min_df, use_maxsum, use_mmr, diversity,
                         nr_candidates)


def fetch_keyword_from_video(vid, keyphrase_ngram_range, stop_words, top_n, min_df, use_maxsum, use_mmr, diversity,
                             nr_candidates):
    doc = vid_to_text(vid)
    os.remove(vid)
    return fetch_keyword(doc, keyphrase_ngram_range, stop_words, top_n, min_df, use_maxsum, use_mmr, diversity,
                         nr_candidates)
