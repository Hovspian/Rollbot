def get_default_profile(user, gold):
    return {
        'id': user.id,
        'gold': gold,
        'gold_stats': {},
        'butts': {
            'played': 0,
            'total': 0,
            'ones': 0,
            'twenties': 0,
            'history': []  # Last 5 butts
        },
        'blackjack': {
            'gold_total': 0,
            'gold_won': 0,
            'gold_lost': 0,
            'played': 0,
            'wins': 0,
            'losses': 0,
            'dealt': 0,
            'blackjacks': 0
        },
        'slots': {
            'gold_total': 0,
            'gold_won': 0,
            'gold_lost': 0,
            'played': 0,
            'played_normal': 0,
            'played_big': 0,
            'played_giant': 0,
            'highest_payout': 0,
        },
        'scratchcard': {
            'gold_total': 0,
            'gold_won': 0,
            'gold_lost': 0,
            'played': 0,
            'won': 0,
            'lost': 0
        },
        'hammerpot': {
            'gold_total': 0,
            'gold_won': 0,
            'gold_lost': 0,
            'played': 0,
            'won': 0,
            'lost': 0
        },
        'versushammer': {
            'gold_total': 0,
            'gold_won': 0,
            'gold_lost': 0,
            'played': 0,
            'won': 0,
            'lost': 0,
            'highest_payout': 0,
            'highest_loss': 0
        },
        'rollgames': {
            'gold_total': 0,
            'gold_won': 0,
            'gold_lost': 0,
            'played': 0,
            'won': 0,
            'lost': 0,
            'most_rolls': 0,
            'least_rolls': 0
        }
    }
