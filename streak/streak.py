import redis

class Streak(object):
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

  def __init__(self, default_options = DEFAULTS):
    self.options = Streak.DEFAULTS.copy()
    self.options.update(default_options)
    self.redis = redis.StrictRedis(host = 'localhost', port = 6379, db = 0)

  def aggregate(self, id, count):
    '''
    Aggregate streaks for a given +id+. If +count+ is greater than 0, it will increment +Streak.positive_key+ and 
    +Streak.positive_total_key+ by the absolute value of count. It will zero out +Streak.negative_key+. Finally, it 
    will add the absolute value of count to +Streak.total_key+. If the current positive streak is greater than 
    the value of +Streak.positive_streak_key+, its value will be replaced. 
    If +count+ is less than than 0, it will increment +Streak.negative_key+ and 
    +Streak.negative_total_key+ by the absolute value of count. It will zero out +Streak.positive_key+. Finally, it 
    will add the absolute value of count to +Streak.total_key+. If the current negative streak is greater than 
    the value of +Streak.negative_streak_key+, its value will be replaced.
    
    @param id [String] ID of the item being monitored for a streak.
    @param count [Integer] Streak count, which can be positive or negative.
    '''
    if count >= 0:
      pipe = self.redis.pipeline()
      pipe.get('%s:%s:%s' \
        % (self.options['namespace'], self.options['positive_key'], id))
      pipe.get('%s:%s:%s' \
        % (self.options['namespace'], self.options['positive_streak_key'], id))
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
        % (self.options['namespace'], self.options['positive_streak_key'], id), max([previous_wins + abs(count), previous_streak]))
      pipe.incr('%s:%s:%s' \
        % (self.options['namespace'], self.options['positive_key'], id), abs(count))
      pipe.incr('%s:%s:%s' \
        % (self.options['namespace'], self.options['positive_total_key'], id), abs(count))
      pipe.set('%s:%s:%s' \
        % (self.options['namespace'], self.options['negative_key'], id), 0)
      pipe.incr('%s:%s:%s' \
        % (self.options['namespace'], self.options['total_key'], id), abs(count))

      pipe.execute()
    else:
      pipe = self.redis.pipeline()
      pipe.get('%s:%s:%s' \
        % (self.options['namespace'], self.options['negative_key'], id))
      pipe.get('%s:%s:%s' \
        % (self.options['namespace'], self.options['negative_streak_key'], id))
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
        % (self.options['namespace'], self.options['negative_streak_key'], id), max([previous_losses + abs(count), previous_streak]))
      pipe.incr('%s:%s:%s' \
        % (self.options['namespace'], self.options['negative_key'], id), abs(count))
      pipe.incr('%s:%s:%s' \
        % (self.options['namespace'], self.options['negative_total_key'], id), abs(count))
      pipe.set('%s:%s:%s' \
        % (self.options['namespace'], self.options['positive_key'], id), 0)
      pipe.incr('%s:%s:%s' \
        % (self.options['namespace'], self.options['total_key'], id), abs(count))
      
      pipe.execute()

  def statistics(self, id, keys = []):
    '''
    Retrieve all (or some) of the streak statistics collected. By default, without a second parameter, this 
    method will return a +dict+ of: +Streak.positive_key+, +Streak.positive_total_key+, +Streak.positive_streak_key+, 
    +Streak.negative_key+, +Streak.negative_total_key+, +Streak.negative_streak_key+, and +Streak.total_key+ with
    their corresponding values. If you want a subset of that list, pass in an array with the keys you want
    returned.
    
    @param id [String] ID.
    @param keys [Array, optional]. Optional list of streak statistic keys to be retrieved.
    
    @return +dict+ of streak statistics and their corresponding values for a given +id+.
    '''
    if len(keys) == 0:
      keys = self.slicedict(self.options, 'namespace').values()

    pipe = self.redis.pipeline()
    for key in keys:
      pipe.get('%s:%s:%s' % (self.options['namespace'], key, id))
    values = pipe.execute()

    for index, value in enumerate(values):
      if value == None:
        values[index] = 0

    return dict(zip(keys, map(int, values)))

  def reset_statistics(self, id):
    '''
    Reset all the statistics for a given +id+ to 0.
    
    @param id [String] ID.
    '''
    keys = keys = self.slicedict(self.options, 'namespace').values()

    pipe = self.redis.pipeline()
    for key in keys:
      pipe.set('%s:%s:%s' % (self.options['namespace'], key, id), 0)
    pipe.execute()

  def slicedict(self, userdict, substring):
    return { key:value for key,value in userdict.iteritems() if not key.startswith(substring) }
