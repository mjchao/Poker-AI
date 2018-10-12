import pokerai.game.player


class MockPlayer(pokerai.game.player.Player):
  """A mock player who will execute a sequence of predefined actions.
  """

  @staticmethod
  def FromActionList(action_list):
    """Creates a mock player who will execute the predefined sequence of
    actions.

      Args:
        action_list: (list of tuple/str) Each element of the list should be
          "fold", "check", "call", ("bet", <amount>), ("raise", amount)
          (case insensitive).

      Return:
        (MockPlayer) A mock player that will execute the given actions.
    """
    str_to_action = {
      "fold": pokerai.game.player.Fold,
      "check": pokerai.game.player.Check,
      "call": pokerai.game.player.Call,
      "bet": pokerai.game.player.Bet,
      "raise": pokerai.game.player.Raise,
    }
    return MockPlayer([(str_to_action[a]() if type(a) == str else
                        str_to_action[a[0]](*a[1:]))
                      for a in action_list])

  def __init__(self, predef_actions, chips=10):
    """Creates a mock player who will execute a predefined sequence of actions.

    Args:
      predef_actions: (list of Action) The actions the mock player should
        execute
    """
    super(MockPlayer, self).__init__(chips)
    self._predefined_actions = predef_actions
    self._curr_action_idx = 0

  def MakeDecision(self, deal_data, curr_bet, to_call, min_raise):
    action = self._predefined_actions[self._curr_action_idx]
    self._curr_action_idx += 1
    return action


def CreateMockPlayers(actions, chips=None):
  """Creates mock players that will perform the given actions.

    Args:
      actions: (list of list of tuple/str) actions[i] contains the list of
        actions ("fold", "check", "call", ("bet", <amount>), or
        ("raise", <amount>)

    Returns:
      (list of MockPlayer) list of mock players that will execute the specified
        actions.
  """
  if type(chips) == list:
    return [MockPlayer.FromActionList(a, c) for (a, c) in zip(actions, chips)]
  elif type(chips) == int:
    return [MockPlayer.FromActionList(a, chips) for a in actions]
  else:
    return [MockPlayer.FromActionList(a) for a in actions]

