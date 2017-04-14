from MagicPointChecker import MagicPointChecker
from ValuableSeedNotifier import ValuableSeedNotifier

# notify valuable seeds
seedNotifier = ValuableSeedNotifier()
seeds = seedNotifier.crawl()
filteredSeeds = seedNotifier.filter(seeds)
seedNotifier.notify(filteredSeeds)

# notify if magic point is not high enough
checker = MagicPointChecker()
point = checker.crawl()
if point <= MagicPointChecker.POINT_THRESHOLD:
    checker.notify(point)
