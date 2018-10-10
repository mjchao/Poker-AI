import pokerai.game.player


class MockPlayer(pokerai.game.player.Player):
  """A mock player who will execute a sequence of predefined actions.
  """

  def __init__(self, predef_actions):
    """Creates a mock player who will execute a predefined sequence of actions.

    Args:
      predef_actions: (list of Action) The actions the mock player should
        execute
    """
    self._predefined_actions = predef_actions
    self._curr_action_idx = 0

  def MakeDecision(self, round_data):
    action = self._predefined_actions[self._curr_action_idx]
    self._curr_action_idx += 1
    return action

