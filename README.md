# streak

streak is a library for calculating win/loss streaks. It uses Redis as its backend for collecting the data. 
This is a Python port of the original [streak](https://github.com/czarneckid/streak) Ruby gem.

## Installation

## Usage

```python
>>> from streak import Streak
>>> streak = Streak()
>>> streak.aggregate('david', 3)
>>> streak.aggregate('david', -2)
>>> streak.aggregate('david', 5)
>>> streak.aggregate('david', -1)
>>> statistics = streak.statistics('david')
>>> print statistics
{'losses_streak': 2, 'wins_streak': 5, 'wins': 0, 'losses_total': 3, 'losses': 1, 'wins_total': 8, 'total': 11}
>>> streak.reset_statistics('david')
>>> statistics = streak.statistics('david')
>>> print statistics
{'losses_streak': 0, 'wins_streak': 0, 'wins': 0, 'losses_total': 0, 'losses': 0, 'wins_total': 0, 'total': 0}
>>> 
```

## Contributing

1. Fork it
2. Create your feature branch (`git checkout -b my-new-feature`)
3. Commit your changes (`git commit -am 'Added some feature'`)
4. Push to the branch (`git push origin my-new-feature`)
5. Create new Pull Request

## Copyright

Copyright (c) 2012 David Czarnecki. See LICENSE for further details.
