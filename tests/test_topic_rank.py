from perke.unsupervised.graph_based import TopicRank


def test_original_paper_default(text):
    extractor = TopicRank()
    extractor.load_text(input=text)
    extractor.select_candidates()
    extractor.weight_candidates()
    keyphrases = [keyphrase for keyphrase, weight in
                  extractor.get_n_best(n=3)]
    assert keyphrases == ['طبیعی',
                          'رایانه',
                          'پردازش زبان گفتاری']
