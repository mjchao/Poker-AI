"""Contains logic for players at a poker table
"""

class Action(object):
  """Actions a player can take.
  """
  FOLD = 1
  CHECK = 2
  CALL = 3
  BET = 4
  RAISE = 5

  def __init__(self, action):
    if not (1 <= action and action <= 5):
      raise ValueError("Invalid action %d. Must be between 1 and 5 inclusive"
          %(action))
    self._action = action

  def GetActionType(self):
    return self._action


class Fold(Action):
  def __init__(self):
    super(Fold, self).__init__(Action.FOLD)


class Check(Action):
  def __init__(self):
    super(Check, self).__init__(Action.CHECK)


class Call(Action):
  def __init__(self):
    super(Call, self).__init__(Action.CALL)


class Bet(Action):
  def __init__(self, amount):
    super(Bet, self).__init__(Action.BET)
    self._amount = amount

  def GetBetAmount(self):
    return self._amount


class Raise(Action):
  def __init__(self, amount):
    super(Raise, self).__init__(Action.RAISE)
    self._amount = amount

  def GetRaiseAmount(self):
    return self._amount


class DealEndEvent(object):
  """Event that is broadcasted when the deal ends and someone wins.
  """

  def __init__(self, winner):
    """Creates an event describing who won the deal.

    Args:
      winner: (Player) The player who won. The state of the player is after
        the receive their chips.
    """
    pass


class PlayerEvent(object):
  """An event pertinent to a specific player that occurred during a deal.

  Typically, this is created for actions like FOLD or BET.
  """

  def __init__(self, player, curr_action):
    """Creates an event indicating the given player

    Args:
      player: (Player) The index of the player who caused this event
      curr_action: (Action) The action the player just made, e.g. FOLD
    """
    self._player = player
    self._curr_action = curr_action


class Player(object):
  """Base class representing a player:
    * The cards the player has.
    * The money the player has.
    * Hooks for events where another player folds, checks, calls, bets, raises,
      and for requesting the player to make a decision and for notifying when
      the deal is over.

    The player always folds.
  """

  def __init__(self, chips):
    self._hole_cards = []
    self._chips = chips

  def GetPublicView(self):
    """Returns a copy of this player's public data. The clone can be safely
    altered without affecting this player.

    Returns:
      (Player) A public, modifiable clone. The player's chips will be set, but
        their hole cards will not.
    """
    return Player(self._chips)

  def ModifyChips(self, delta):
    """Modifies the amount of cash this player has.

    Args:
      delta: (int) Positive or negative number of chips
    """
    self._chips += delta

  def SetHoleCards(self, hole_cards):
    """Sets the hole cards this player has.

      Must either be [] indicating no current deal, or must be a list of two
      cards.

    Args:
      (list of int) List of 0 or 2 cards. The ints are the deuces library
        representation of cards.
    """
    if len(hole_cards) != 0 and len(hole_cards) != 2:
      raise ValueError(
          "Invalid hole cards. Must be 0 or 2 hole cards. You provided %d hole "
          "cards." %(len(hole_cards)))

  def OnPlayerEvent(self, deal_data, event):
    """Callback for when another player makes an action.

    The deal data and player data represent the state of the game AFTER the
    action took place.

    Args:
      deal_data: (DealData) Details of the current deal.
      event: (PlayerEvent) The event that occurred.
    """
    pass

  def MakeDecision(self, deal_data, curr_bet, to_call, min_raise):
    """Callback for when it's time for the player to make a decision.

    Args:
      deal_data: (DealData) Details of the current deal.
      curr_bet: (int) Current bet in chips that you need to match.
      to_call: (int) Number of chips needed to call.
      min_raise: (int) Minimum number of chips to raise by. This is a delta
        above the current bet, so if you raise by x, the make the new bet
        curr_bet + x. This value is None if you are not allowed to raise (i.e.
        your raise would actually be a bet).

    Return:
      (Action) fold, call, check, bet, or raise.
        * You can fold at any time.
        * You can check any time to_call == 0
        * You can call any time to_call > 0, provided you have enough chips.
        * You can bet any time to_call == 0
        * You can raise by at least min_raise any time to_call > 0.
    """
    return Fold()

  def OnDealOver(self, deal_data, event):
    """Callback for when the deal is over.

    Args:
      deal_data: (Deal) Details of the current deal.
      event: (DealEndEvent) Details about the ending of the deal (i.e. who won)
    """
    pass

  def OnError(self, err):
    """Callback for an error.

    Args:
      err: (Exception) Any exception that occurred due to the player's faulty
        logic.
    """
    raise err

