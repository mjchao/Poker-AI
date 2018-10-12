"""Contains logic for a deal, i.e. the entire sequence of four betting rounds.
"""
import deuces.deck
import pokerai.game.player

class DealData(object):
  """Contains details about the current deal of poker.
  """

  def __init__(self, dealer_idx, pot):
    self.dealer_idx = dealer_idx
    self.pot = pot

class Deal(object):
  """Contains logic about one deal of poker.
  """

  def __init__(self, players, dealer_idx, blind=1):
    self._players = players
    self._is_folded = [False for _ in range(len(self._players))]
    self._dealer_idx = dealer_idx
    self._deck = deuces.deck.Deck()
    self._blind = blind
    self._pot = 0

  def GetDealData(self):
    """Packages the current deal information into an object.
    """
    return DealData(self._dealer_idx, self._pot)

  def NotifyPlayersOfAction(self, action):
    """Notifies all players of an action that took place.
    """
    pass

  def GetNormalizedIdx(self, idx):
    """Converts the given index to a value from 0..len(self._players) - 1
    """
    return idx % len(self._players)

  def GetPlayer(self, idx):
    """Gets the player at the given index

    Args:
      idx: (int) A player index, which may exceed len(self._players). The
        index will automatically wrap around

    Returns:
      (Player) The player at corresponding to the given index
    """
    return self._players[self.GetNormalizedIdx(idx)]

  def DoBettingRound(self, start_idx, is_preflop):
    """Completes an entire round of betting - until everyone has matched
    the bet or raise, or folded. Excludes preflop betting which is slightly
    different.

    Afterwards, the players bets are cleared and the pot is updated with the
    total bets.

    Args:
      start_idx: (int) Index of the player who starts
      is_preflop: (bool) If this round is the preflop round. The preflop round
        is special because the big blind is technically the one who initiates
        the betting to 2*blinds, but has the option to check or raise
        at the end. If preflop, the start_idx-1 is assumed to be the big blind.
    """
    bets = [0 for _ in range(len(self._players))]
    bet_to_match = 0

    # Compute min amount needed to stay in the round
    if is_preflop:
      # for preflop, small blind and big blind have already bet money via the
      # blinds
      bets[self.GetNormalizedIdx(start_idx - 1)] = 2 * self._blind
      bets[self.GetNormalizedIdx(start_idx - 2)] = 1 * self._blind
      bet_to_match = 2 * self._blind

    last_to_act_idx = self.GetNormalizedIdx(start_idx - 1)
    curr_player_idx = self.GetNormalizedIdx(start_idx)
    curr_player = self.GetPlayer(start_idx)
    while True:
      if not self._is_folded[curr_player_idx]:
        to_call = (bet_to_match - bets[curr_player_idx])
        # you have to at least double the current bet if you choose to raise
        if to_call == 0:
          min_raise = None
        else:
          min_raise = max(1, bet_to_match)

        # process player's decision
        is_action_valid = False
        while not is_action_valid:
          player_action = curr_player.MakeDecision(self.GetDealData(),
              bet_to_match, to_call, min_raise)

          # allowed to fold anytime
          if player_action.GetActionType() == pokerai.game.player.Action.FOLD:
            is_action_valid = True
            self._is_folded[curr_player_idx] = True

          # allowed to check whenever to_call == 0. Nothing needs to be updated.
          elif (player_action.GetActionType() ==
                  pokerai.game.player.Action.CHECK):
            is_action_valid = (to_call == 0)
            if not is_action_valid:
              err_msg = ("You cannot check because someone has already bet %d "
                          "more than you." %(to_call))

          # allowed to call whenever to_call > 0. Have to update the player's
          # total bet
          elif (player_action.GetActionType() ==
                  pokerai.game.player.Action.CALL):
            is_action_valid = (to_call > 0)
            if is_action_valid:
              bets[curr_player_idx] += to_call
            else:
              err_msg = ("You cannot call because nobody has bet anything. "
                          "You should check instead.")

          # allowed to bet whenever to_call == 0. Update the bet to match and
          # the player's total bet. The previous player becomes the last one
          # to act.
          elif (player_action.GetActionType() ==
                  pokerai.game.player.Action.BET):
            bet_amount = player_action.GetBetAmount()
            is_action_valid = (to_call == 0 and bet_amount > 0)
            if is_action_valid:
              bets[curr_player_idx] += bet_amount
              bet_to_match = bet_amount
              last_to_act_idx = self.GetNormalizedIdx(curr_player_idx - 1)
            else:
              if to_call == 0:
                err_msg = ("You cannot bet when there is another outstanding "
                            "bet to match. You should either call or raise")
              else: # bet_amount <= 0
                err_msg = ("Your bet, %d, is invalid. It must be positive."
                            %(bet_amount))

          # allowed to raise to at least twice the current outstanding bet if
          # to_call != 0. Have to update the player's bet and the current
          # outstanding bet. The previous player becomes the last one to act.
          elif (player_action.GetActionType() ==
                  pokerai.game.player.Action.RAISE):
            raise_amount = player_action.GetRaiseAmount()

            is_action_valid = (to_call != 0 and raise_amount >= min_raise)
            if is_action_valid:
              # to_call matches the current outstanding bet, raise_amount then
              # raises the current outstanding bet
              bets[curr_player_idx] += (to_call + raise_amount)
              bet_to_match = bet_to_match + raise_amount
              last_to_act_idx = self.GetNormalizedIdx(curr_player_idx - 1)
            else:
              if to_call == 0:
                err_msg = ("You cannot raise when nobody else has bet. "
                            "You should bet instead.")
              else: # raise_amount < min_raise
                err_msg = ("Your raise of %d is too low. It needs to be at "
                            "least %d" %(raise_amount, min_raise))

          else:
            is_action_valid = False
            err_msg = ("Invalid action of type %d. Please return FOLD, CHECK, "
                        "CALL, BET, or RAISE in your player implementation."
                        %(player_action.GetActionType()))

          # if action wasn't valid, throw an exception and try again
          if not is_action_valid:
            curr_player.OnError(ValueError(err_msg))
            continue


      # We're done with the betting round if the current player is the last
      # one to act and has either folded or matched the bet
      if (curr_player_idx == last_to_act_idx and
          (self._is_folded[curr_player_idx] or
            bets[curr_player_idx] == bet_to_match)):
        break

      # if we're not done with the betting round, then move on to the next
      # person
      curr_player_idx = self.GetNormalizedIdx(curr_player_idx + 1)
      curr_player = self.GetPlayer(curr_player_idx)


  def Execute(self):
    """Executes the deal by dealing hole cards, requesting bets, dealing the
    flop, requesting bets, and so on, until somebody wins.
    """
    # get the blinds
    # in 2 player heads up, dealer is small blind and other player is big blind
    if len(self._players) == 2:
      self.GetPlayer(self._dealer_idx).ModifyChips(-1 * self._blind)
      self.GetPlayer(self._dealer_idx + 1).ModifyChips(-2 * self._blind)
      big_blind_idx = self._dealer_idx + 1

    # if more than 2 players, small blind and big blind are the two players
    # directly after the dealer
    else:
      self.GetPlayer(self._dealer_idx + 1).ModifyChips(-1 * self._blind)
      self.GetPlayer(self._dealer_idx + 2).ModifyChips(-2 * self._blind)
      big_blind_idx = self._dealer_idx + 2

    # deal out hole cards
    for p in self._players:
      p.SetHoleCards(self._deck.draw(2))

    self.DoBettingRound(big_blind_idx + 1, True)

    # TODO


