from perke.unsupervised.graph_based import PositionRank


def test_original_article_default(text: str) -> None:
    extractor = PositionRank()
    extractor.load_text(input=text, universal_pos_tags=False)
    extractor.select_candidates()
    extractor.weight_candidates()
    keyphrases = [keyphrase for keyphrase, weight in extractor.get_n_best(n=3)]
    assert keyphrases == [
        'کاربردهای پردازش زبان',
        'پردازش زبان‌های',
        'کاربردهای گفتاری پردازش',
    ]
