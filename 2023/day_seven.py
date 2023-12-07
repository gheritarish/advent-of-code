import structlog
import sys

from utils import read_file

logger = structlog.get_logger()

sys.setrecursionlimit(1_000_000)


HAND_SCORES = {
    "five_of_a_kind": 600,
    "four_of_a_kind": 500,
    "full_house": 400,
    "three_of_a_kind": 300,
    "two_pairs": 200,
    "one_pair": 100,
    "highest_card": 0,
}

CARD_VALUES = {
    "A": 14,
    "K": 13,
    "Q": 12,
    "J": 11,
    "T": 10,
    "9": 9,
    "8": 8,
    "7": 7,
    "6": 6,
    "5": 5,
    "4": 4,
    "3": 3,
    "2": 2,
    "R": 1,
}


class Hand:
    def __init__(self, cards, bet):
        self.cards = cards
        self.bet = bet

    @property
    def scoring(self):
        return self.get_score()

    def update_card_types_joker(self, card_types: dict, yes: bool = False):
        if not yes:
            return card_types
        else:
            if "R" in card_types.keys():
                max_value = 0
                key_max = ""
                for key, value in card_types.items():
                    if key != "R":
                        if value > max_value:
                            max_value = value
                            key_max = key
                    else:
                        continue
                try:
                    card_types[key_max] += card_types["R"]
                except KeyError:
                    return card_types
                card_types.pop("R")

            return card_types


    def get_score(self):
        card_types = {}
        for card in self.cards:
            if card not in card_types.keys():
                card_types[card] = 1
            else:
                card_types[card] += 1

        self.update_card_types_joker(card_types, yes=True)
        if len(card_types.keys()) == 5:
            hand_scoring = HAND_SCORES["highest_card"]
        elif len(card_types.keys()) == 4:
            hand_scoring = HAND_SCORES["one_pair"]
        elif len(card_types.keys()) == 1:
            hand_scoring = HAND_SCORES["five_of_a_kind"]
        elif len(card_types.keys()) == 2:
            for _, value in card_types.items():
                if value in [1, 4]:
                    hand_scoring = HAND_SCORES["four_of_a_kind"]
                    break
                else:
                    hand_scoring = HAND_SCORES["full_house"]
                    break
        else:
            for _, value in card_types.items():
                if value == 3:
                    hand_scoring = HAND_SCORES["three_of_a_kind"]
                    break
                hand_scoring = HAND_SCORES["two_pairs"]

        return hand_scoring

    def compare_scores(self, other_hand) -> int:
        if self.scoring > other_hand.scoring:
            return 1
        elif self.scoring < other_hand.scoring:
            return 0
        else:
            for i in range(len(self.cards)):
                if CARD_VALUES[self.cards[i]] > CARD_VALUES[other_hand.cards[i]]:
                    return 1
                elif CARD_VALUES[self.cards[i]] < CARD_VALUES[other_hand.cards[i]]:
                    return 0
            return 2


def fusion(first_hands: list[Hand], second_hands: list[Hand]) -> list[Hand]:
    if first_hands is None or len(first_hands) == 0:
        return second_hands
    if second_hands is None or len(second_hands) == 0:
        return first_hands

    if first_hands[0].compare_scores(second_hands[0]) == 0:
        logger.info(
            "better_second_hand",
            first_hand=first_hands[0].cards,
            second_hand=second_hands[0].cards,
        )
        result = [first_hands[0]]
        result.extend(fusion(first_hands[1:], second_hands))
        return result
    elif first_hands[0].compare_scores(second_hands[0]) == 1:
        logger.info(
            "better_first_hand",
            first_hand=first_hands[0].cards,
            second_hand=second_hands[0].cards,
        )
        result = [second_hands[0]]
        result.extend(fusion(first_hands, second_hands[1:]))
        return result
    else:
        logger.info(
            "equality_found",
            first_hand=first_hands[0].cards,
            first_bet=first_hands[0].bet,
            second_hand=second_hands[0].cards,
            second_bet=second_hands[0].bet,
        )
        result = [first_hands[0], second_hands[0]]
        result.extend(fusion(first_hands[1:], second_hands[1:]))
        return result


def fusion_sort(hands: list[Hand]) -> list[Hand]:
    if len(hands) == 1:
        return hands
    middle = len(hands) // 2
    sorted_hands = fusion(fusion_sort(hands[:middle]), fusion_sort(hands[middle:]))
    return sorted_hands


def get_hands(lines: list[str]) -> list[Hand]:
    hands = []
    for line in lines:
        cards = line.split(" ")[0]
        bet = line.split(" ")[1].strip()
        hands.append(Hand(cards=cards, bet=int(bet)))
    return hands


def get_first_answer(sorted_cards: list[Hand]):
    result = 0
    for i in range(len(sorted_cards)):
        result += sorted_cards[i].bet * (i + 1)
    return result


def get_new_hands(hands: list[Hand]) -> list[Hand]:
    for hand in hands:
        cards = ""
        for card in hand.cards:
            if card == "J":
                cards += "R"
            else:
                cards += card
        hand.cards = cards
    return hands

def main():
    lines = read_file("input_seven.txt")
    hands = get_hands(lines)
    sorted_hands = fusion_sort(hands)
    first_answer = get_first_answer(sorted_hands)
    logger.info("first_question", answer=first_answer)

    new_hands = get_new_hands(hands)
    sorted_new_hands = fusion_sort(new_hands)
    second_answer = get_first_answer(sorted_new_hands)
    logger.info("second_question", answer=second_answer)


if __name__ == "__main__":
    main()
