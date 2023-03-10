from perke.unsupervised.graph_based import PositionRank


def test_original_article_default(text: str) -> None:
    extractor = PositionRank()
    extractor.load_text(input=text)
    extractor.select_candidates()
    extractor.weight_candidates()
    keyphrases = [keyphrase for keyphrase, weight in extractor.get_n_best(n=3)]
    assert keyphrases == [
        'پردازش زبان‌های طبیعی',
        'پردازش زبان طبیعی',
        'پردازش زبان گفتاری',
    ]
