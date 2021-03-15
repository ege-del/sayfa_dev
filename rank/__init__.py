from .rank_newest.main import rank as rank_newest
from .rank_shortest.main import rank as rank_shortest

algos = {
    'newest':rank_newest,
    'shortest_title':rank_shortest,
}

