__all__ = [
    'TextRank',
    'SingleRank',
    'PositionRank',
    'TopicRank',
    'MultipartiteRank',
]

import os
import sys

from perke.unsupervised.graph_based.multipartite_rank import MultipartiteRank
from perke.unsupervised.graph_based.position_rank import PositionRank
from perke.unsupervised.graph_based.single_rank import SingleRank
from perke.unsupervised.graph_based.text_rank import TextRank
from perke.unsupervised.graph_based.topic_rank import TopicRank

# Fix sphinx links
if os.path.basename(sys.argv[0]) in ['sphinx-build', 'sphinx-build.exe']:
    for model in __all__:
        globals()[model].__module__ = __name__
