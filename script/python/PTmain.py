from biz.MagicPointChecker import MagicPointChecker
from biz.ValuableSeedNotifier import ValuableSeedNotifier

# notify valuable seeds
ValuableSeedNotifier().check()

# notify if magic point is not high enough
MagicPointChecker().check()
