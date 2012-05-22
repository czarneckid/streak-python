__version__ = "0.0.1"

import redis

class Streak:
  DEFAULTS = dict(
    namespace = 'streak',
    positive_key = 'wins',
    positive_total_key = 'wins_total',
    positive_streak_key = 'wins_streak',
    negative_key = 'losses',
    negative_total_key = 'losses_total',
    negative_streak_key = 'losses_streak',
    total_key = 'total'
  )

  def __init__(self):
    self.redis = redis.StrictRedis(host = 'localhost', port = 6379, db = 0)

  def aggregate(self, id, count):
    if count >= 0:
      pipe = self.redis.pipeline()
      pipe.get('%s:%s:%s' \
        % (Streak.DEFAULTS['namespace'], Streak.DEFAULTS['positive_key'], id))
      pipe.get('%s:%s:%s' \
        % (Streak.DEFAULTS['namespace'], Streak.DEFAULTS['positive_streak_key'], id))
      previous_data = pipe.execute()

      previous_wins = previous_data[0]
      previous_streak = previous_data[1]

      if previous_wins == None:
        previous_wins = 0
      if previous_streak == None:
        previous_streak = 0

      previous_wins = int(previous_wins)
      previous_streak = int(previous_streak)

      pipe = self.redis.pipeline()
      pipe.set('%s:%s:%s' \
        % (Streak.DEFAULTS['namespace'], Streak.DEFAULTS['positive_streak_key'], id), max([previous_wins + abs(count), previous_streak]))
      pipe.incr('%s:%s:%s' \
        % (Streak.DEFAULTS['namespace'], Streak.DEFAULTS['positive_key'], id), abs(count))
      pipe.incr('%s:%s:%s' \
        % (Streak.DEFAULTS['namespace'], Streak.DEFAULTS['positive_total_key'], id), abs(count))
      pipe.set('%s:%s:%s' \
        % (Streak.DEFAULTS['namespace'], Streak.DEFAULTS['negative_key'], id), 0)
      pipe.incr('%s:%s:%s' \
        % (Streak.DEFAULTS['namespace'], Streak.DEFAULTS['total_key'], id), abs(count))

      pipe.execute()
    else:

      pipe = self.redis.pipeline()
      pipe.get('%s:%s:%s' \
        % (Streak.DEFAULTS['namespace'], Streak.DEFAULTS['negative_key'], id))
      pipe.get('%s:%s:%s' \
        % (Streak.DEFAULTS['namespace'], Streak.DEFAULTS['negative_streak_key'], id))
      previous_data = pipe.execute()

      previous_losses = previous_data[0]
      previous_streak = previous_data[1]

      if previous_losses == None:
        previous_losses = 0
      if previous_streak == None:
        previous_streak = 0

      previous_losses = int(previous_losses)
      previous_streak = int(previous_streak)

      pipe = self.redis.pipeline()
      pipe.set('%s:%s:%s' \
        % (Streak.DEFAULTS['namespace'], Streak.DEFAULTS['negative_streak_key'], id), max([previous_losses + abs(count), previous_streak]))
      pipe.incr('%s:%s:%s' \
        % (Streak.DEFAULTS['namespace'], Streak.DEFAULTS['negative_key'], id), abs(count))
      pipe.incr('%s:%s:%s' \
        % (Streak.DEFAULTS['namespace'], Streak.DEFAULTS['negative_total_key'], id), abs(count))
      pipe.set('%s:%s:%s' \
        % (Streak.DEFAULTS['namespace'], Streak.DEFAULTS['positive_key'], id), 0)
      pipe.incr('%s:%s:%s' \
        % (Streak.DEFAULTS['namespace'], Streak.DEFAULTS['total_key'], id), abs(count))
      
      pipe.execute()

  def statistics(self, id, keys = [DEFAULTS['positive_key'], DEFAULTS['positive_total_key'], DEFAULTS['positive_streak_key'],
      DEFAULTS['negative_key'], DEFAULTS['negative_total_key'], DEFAULTS['negative_streak_key'],
      DEFAULTS['total_key']]):
    pipe = self.redis.pipeline()
    for key in keys:
      pipe.get('%s:%s:%s' % (Streak.DEFAULTS['namespace'], key, id))
    values = pipe.execute()
    return dict(zip(keys, map(lambda value: int(value), values)))

  def reset_statistics(self, id):
    keys = [Streak.DEFAULTS['positive_key'], Streak.DEFAULTS['positive_total_key'], Streak.DEFAULTS['positive_streak_key'],
      Streak.DEFAULTS['negative_key'], Streak.DEFAULTS['negative_total_key'], Streak.DEFAULTS['negative_streak_key'],
      Streak.DEFAULTS['total_key']]

    pipe = self.redis.pipeline()
    for key in keys:
      pipe.set('%s:%s:%s' % (Streak.DEFAULTS['namespace'], key, id), 0)
    pipe.execute()
