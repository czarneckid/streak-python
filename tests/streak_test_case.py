import os
import redis
import unittest

from streak import Streak

class StreakTestCase(unittest.TestCase):

  def setUp(self):
    self.redis = redis.StrictRedis(host = 'localhost', port = 6379, db = 15)    
    self.redis.flushdb()

  def test_streak_default_values(self):
    self.assertEquals('streak', Streak.DEFAULTS['namespace'])
    self.assertEquals('wins', Streak.DEFAULTS['positive_key'])
    self.assertEquals('wins_total', Streak.DEFAULTS['positive_total_key'])
    self.assertEquals('wins_streak', Streak.DEFAULTS['positive_streak_key'])
    self.assertEquals('losses', Streak.DEFAULTS['negative_key'])
    self.assertEquals('losses_total', Streak.DEFAULTS['negative_total_key'])
    self.assertEquals('losses_streak', Streak.DEFAULTS['negative_streak_key'])
    self.assertEquals('total', Streak.DEFAULTS['total_key'])

  def test_can_retrieve_statistics_without_data(self):
    streak = Streak()
    statistics = streak.statistics('david')

    self.assertEquals(7, len(statistics))
    self.assertEquals(0, statistics['wins'])
    self.assertEquals(0, statistics['wins_total'])
    self.assertEquals(0, statistics['wins_streak'])
    self.assertEquals(0, statistics['losses'])
    self.assertEquals(0, statistics['losses_total'])
    self.assertEquals(0, statistics['losses_streak'])
    self.assertEquals(0, statistics['total'])

  def test_default_options_in_initializer(self):
    streak = Streak(dict(
      positive_key = 'kills',
      positive_total_key = 'kills_total',
      positive_streak_key = 'kills_streak',
      negative_key = 'deaths',
      negative_total_key = 'deaths_total',
      negative_streak_key = 'deaths_streak'
    ))

    streak.redis = self.redis

    options = streak.options
    self.assertEquals('streak', options['namespace'])
    self.assertEquals('kills', options['positive_key'])
    self.assertEquals('kills_total', options['positive_total_key'])
    self.assertEquals('kills_streak', options['positive_streak_key'])
    self.assertEquals('deaths', options['negative_key'])
    self.assertEquals('deaths_total', options['negative_total_key'])
    self.assertEquals('deaths_streak', options['negative_streak_key'])
    self.assertEquals('total', options['total_key'])

  def test_aggregate_statistics_and_reset_statistics(self):
    streak = Streak()
    streak.redis = self.redis

    streak.aggregate('david', 3)
    streak.aggregate('david', -2)
    streak.aggregate('david', 5)
    streak.aggregate('david', -1)
    
    statistics = streak.statistics('david')
    self.assertEquals(7, len(statistics))
    self.assertEquals(0, statistics['wins'])
    self.assertEquals(8, statistics['wins_total'])
    self.assertEquals(5, statistics['wins_streak'])
    self.assertEquals(1, statistics['losses'])
    self.assertEquals(3, statistics['losses_total'])
    self.assertEquals(2, statistics['losses_streak'])
    self.assertEquals(11, statistics['total'])

    statistics = streak.statistics('david', [Streak.DEFAULTS['positive_streak_key'], Streak.DEFAULTS['negative_streak_key']])
    self.assertEquals(2, len(statistics))
    self.assertEquals(5, statistics['wins_streak'])
    self.assertEquals(2, statistics['losses_streak'])

    streak.reset_statistics('david')
    statistics = streak.statistics('david')
    self.assertEquals(0, statistics['wins'])
    self.assertEquals(0, statistics['wins_total'])
    self.assertEquals(0, statistics['wins_streak'])
    self.assertEquals(0, statistics['losses'])
    self.assertEquals(0, statistics['losses_total'])
    self.assertEquals(0, statistics['losses_streak'])
    self.assertEquals(0, statistics['total'])