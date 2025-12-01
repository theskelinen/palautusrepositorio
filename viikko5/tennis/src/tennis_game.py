class TennisGame:
    scores = ["Love", "Fifteen", "Thirty", "Forty"]

    def __init__(self, player1_name, player2_name):
        self.player1_name = player1_name
        self.player2_name = player2_name
        self.player1_score = 0
        self.player2_score = 0

    def won_point(self, player_name):
        if player_name == self.player1_name:
            self.player1_score += 1
        else:
            self.player2_score += 1

    def get_score(self):
        if self._is_tied():
            return self._tied_score()
        if self._is_endgame():
            return self._endgame_score()
        return self._regular_score()

    def _is_tied(self):
        return self.player1_score == self.player2_score

    def _is_endgame(self):
        return self.player1_score >= 4 or self.player2_score >= 4

    def _tied_score(self):
        if self.player1_score <= 2:
            return f"{self._score_name(self.player1_score)}-All"
        return "Deuce"

    def _endgame_score(self):
        difference = self.player1_score - self.player2_score
        if difference == 1:
            return f"Advantage {self.player1_name}"
        if difference == -1:
            return f"Advantage {self.player2_name}"
        if difference >= 2:
            return f"Win for {self.player1_name}"
        return f"Win for {self.player2_name}"

    def _regular_score(self):
        player1_score = self._score_name(self.player1_score)
        player2_score = self._score_name(self.player2_score)
        return f"{player1_score}-{player2_score }"

    def _score_name(self, score_value):
        return self.scores[score_value]
