from perke.unsupervised.graph_based import TextRank


def test_original_article_default(text):
    extractor = TextRank()
    extractor.load_text(input=text)
    extractor.weight_candidates(top_t_percent=0.33)
    keyphrases = [keyphrase for keyphrase, weight in
                  extractor.get_n_best(n=3)]
    assert keyphrases == ['کاربردهای پردازش زبان طبیعی',
                          'کاربردهای گفتاری پردازش زبان',
                          'زمینه درک زبان طبیعی']


def test_with_candidate_selection(text):
    extractor = TextRank()
    extractor.load_text(input=text)
    extractor.select_candidates()
    extractor.weight_candidates()
    keyphrases = [keyphrase for keyphrase, weight in
                  extractor.get_n_best(n=3)]
    assert keyphrases == ['کاربردهای متنوع پردازش زبان‌های طبیعی',
                          'کاربردهای پردازش زبان طبیعی',
                          'کاربردهای گفتاری پردازش زبان']
