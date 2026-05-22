const CONCLUDED_STATUSES = ['Win', 'Forfeit', 'Suspensions']

export function hasRecordedScore(score, game) {
  const scoringType = game?.scoring_type

  if (scoringType === 'Component Score') {
    return (
      (Array.isArray(score?.score_components)
        && score.score_components.length > 0)
      || Number(score?.total_score) > 0
    )
  }

  if (scoringType === 'Threshold Incremental') {
    return (
      score?.sets_won != null
      || (Array.isArray(score?.set_scores)
        && score.set_scores.length > 0)
    )
  }

  return Number(score?.total_score) > 0
}

export function isFinalizedGame(game) {
  if (!game) {
    return false
  }

  if (game.is_finalized === true) {
    return true
  }

  if (CONCLUDED_STATUSES.includes(game.game_status)) {
    return true
  }

  if (
    Array.isArray(game.scores)
    && game.scores.some(score => hasRecordedScore(score, game))
  ) {
    return true
  }

  return false
}

export function isScheduledGame(game) {
  return !isFinalizedGame(game)
}
