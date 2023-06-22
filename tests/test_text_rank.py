from perke.unsupervised.graph_based import TextRank


def test_original_article_default(text: str) -> None:
    extractor = TextRank()
    extractor.load_text(input=text)
    extractor.weight_candidates(top_t_percent=0.33)
    keyphrases = [keyphrase for keyphrase, weight in extractor.get_n_best(n=3)]
    assert keyphrases == [
        'کاربردهای پردازش زبان طبیعی',
        'زمینه درک زبان طبیعی',
        'پردازش اطلاعات زبانی',
    ]


def test_with_candidate_selection(text: str) -> None:
    extractor = TextRank()
    extractor.load_text(input=text)
    extractor.select_candidates()
    extractor.weight_candidates()
    keyphrases = [keyphrase for keyphrase, weight in extractor.get_n_best(n=3)]
    assert keyphrases == [
        'کاربردهای متنوع پردازش زبان‌های طبیعی',
        'کاربردهای پردازش زبان طبیعی',
        'زمینه درک زبان طبیعی',
    ]
