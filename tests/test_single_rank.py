from perke.unsupervised.graph_based import SingleRank


def test_original_article_default(text: str) -> None:
    extractor = SingleRank()
    extractor.load_text(input=text)
    extractor.select_candidates()
    extractor.weight_candidates()
    keyphrases = [keyphrase for keyphrase, weight in extractor.get_n_best(n=3)]
    assert keyphrases == [
        'کاربردهای متنوع پردازش زبان‌های طبیعی',
        'کاربردهای پردازش زبان طبیعی',
        'پردازش زبان‌های طبیعی عبارت',
    ]
