def get_default_profile(user, gold):
    return {
        'id': user.id,
        'gold': gold,
        'gold_stats': {},
        'butts': {
            'played': 0,
            'total': 0,
            'butt_count': {},  # How many of each number of butts
            'history': []
        },
    }


def get_blackjack_profile(user):
    return {
        'id': user.id,
        'gold_total': 0,
        'gold_won': 0,
        'gold_lost': 0,
        'played': 0,
        'wins': 0,
        'losses': 0,
        'dealt': 0,
        'blackjacks': 0,
        'busts': 0
    }


def get_slots_profile(user):
    return {
        'id': user.id,
        'gold_total': 0,
        'gold_won': 0,
        'gold_lost': 0,
        'played': 0,
        'played_normal': 0,
        'played_big': 0,
        'played_giant': 0,
        'highest_payout': 0
    }


def get_scratchcard_profile(user):
    return {
        'id': user.id,
        'gold_total': 0,
        'gold_won': 0,
        'gold_lost': 0,
        'played': 0,
        'won': 0,
        'lost': 0
    }


def get_hammerpot_profile(user):
    return {
        'id': user.id,
        'gold_total': 0,
        'gold_won': 0,
        'gold_lost': 0,
        'played': 0,
        'won': 0,
        'lost': 0
    }


def get_versushammer_profile(user):
    return {
        'id': user.id,
        'gold_total': 0,
        'gold_won': 0,
        'gold_lost': 0,
        'played': 0,
        'won': 0,
        'lost': 0,
        'highest_payout': 0,
        'highest_loss': 0
    }


def get_rollgames_profile(user):
    return {
        'id': user.id,
        'gold_total': 0,
        'gold_won': 0,
        'gold_lost': 0,
        'played': 0,
        'won': 0,
        'lost': 0,
        'most_rolls': 0,
        'least_rolls': 0
    }
