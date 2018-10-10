"""Contains logic for players at a poker table
"""

class Action(object):
  """Enum for actions a player can make.
  """
  FOLD = 1
  CHECK = 2
  CALL = 3
  BET = 4
  RAISE = 5


class Player(object):
  """Base class representing a player:
    * The cards the player has.
    * The money the player has.
    * Hooks for events where another player folds, checks, calls, bets, raises,
      and for requesting the player to make a decision and for notifying when
      the deal is over.

    The player always folds.
  """

  def __init__(self):
    pass

  def OnFolded(self, deal_data, event):
    """Callback for when another player folds.

    Args:
      deal_data: (Deal) Details of the current deal after the player
        folded.
      event: (Event) Details about the fold.
    """
    pass

  def OnChecked(self, deal_data, event):
    """Callback for when another player checks.

    Args:
      deal_data: (Deal) Details of the current deal after the player
        checked.
      event: (Event) Details about the check.
    """
    pass

  def OnCalled(self, deal_data, event):
    """Callback for when another player calls.

    Args:
      deal_data: (Deal) Details of the current deal after the player
        called.
      event: (Event) Details about the call.
    """
    pass

  def OnBet(self, deal_data, event):
    """Callback for when another player bet.

    Args:
      deal_data: (Deal) Details of the current deal after the player
        bet.
      event: (Event) Details about the bet.
    """
    pass

  def OnRaised(self, deal_data, event):
    """Callback for when another player makes a decision.

    Args:
      deal_data: (Deal) Details of the current deal after the player
        raised.
      event: (Event) Details about the raise.
    """
    pass

  def MakeDecision(self, deal_data):
    """Callback for when it's time for the player to make a decision.

    Args:
      deal_data: (Deal) Details of the current deal.

    Return:
      (Action) FOLD, CALL, CHECK, BET, or RAISE.
    """
    return Action.FOLD

  def OndealOver(self, deal_data, event):
    """Callback for when the deal is over.

    Args:
      deal_data: (Deal) Details of the current deal.
      event: (Event) Details about the ending of the deal (i.e. who won)
    """
    pass

