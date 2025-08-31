import tkinter as tk
import random
import time
import threading

card_values = {
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
    'J': 10, 'Q': 10, 'K': 10, 'A': 11
}

def create_deck():
    deck = []
    for suit in ['Hearts', 'Diamonds', 'Clubs', 'Spades']:
        for value in card_values.keys():
            deck.append((value, suit))
    random.shuffle(deck)
    return deck

def calculate_hand_value(hand):
    value = sum(card_values[card[0]] for card in hand)
    num_aces = sum(1 for card in hand if card[0] == 'A')
    while value > 21 and num_aces:
        value -= 10
        num_aces -= 1
    return value

class BlackjackApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Blackjack")
        self.resizable(False, False)
        self.deck = []
        self.player_hand = []
        self.dealer_hand = []
        self.setup_ui()
        self.start_game()

    def animate_card_flip(self, card_label):
        current_text = card_label.cget("text")
        card_label.config(text="Flipping...")
        self.update()
        time.sleep(0.5)
        card_label.config(text=current_text)
        self.update()

    def setup_ui(self):
        self.title_label = tk.Label(self, text="Blackjack", font=("Arial", 16))
        self.title_label.grid(row=0, columnspan=3, pady=10)

        self.player_hand_label = tk.Label(self, text="Player's Hand:", font=("Arial", 12))
        self.player_hand_label.grid(row=1, column=0, sticky="w", padx=10)

        self.player_cards = tk.Label(self, text="")
        self.player_cards.grid(row=1, column=1, sticky="w", padx=10)

        self.player_total = tk.Label(self, text="Player Total: 0", font=("Arial", 12))
        self.player_total.grid(row=1, column=2, sticky="w", padx=10)

        self.dealer_hand_label = tk.Label(self, text="Dealer's Hand:", font=("Arial", 12))
        self.dealer_hand_label.grid(row=2, column=0, sticky="w", padx=10)

        self.dealer_cards = tk.Label(self, text="")
        self.dealer_cards.grid(row=2, column=1, sticky="w", padx=10)

        self.dealer_total = tk.Label(self, text="Dealer Total: ??", font=("Arial", 12))
        self.dealer_total.grid(row=2, column=2, sticky="w", padx=10)

        self.hit_button = tk.Button(self, text="Hit", command=self.hit, font=("Arial", 12))
        self.hit_button.grid(row=3, column=0, pady=10, padx=10)

        self.stand_button = tk.Button(self, text="Stand", command=self.stand, font=("Arial", 12))
        self.stand_button.grid(row=3, column=1, pady=10, padx=10)

        self.play_again_button = tk.Button(self, text="Play Again", command=self.new_game, font=("Arial", 12), state=tk.DISABLED)
        self.play_again_button.grid(row=4, column=0, pady=10, padx=10)

        self.result_label = tk.Label(self, text="", font=("Arial", 12), fg="red")
        self.result_label.grid(row=4, column=1, pady=10, padx=10)

    def start_game(self):
        self.deck = create_deck()
        self.player_hand = [self.deck.pop(), self.deck.pop()]
        self.dealer_hand = [self.deck.pop(), self.deck.pop()]
        
        self.update_player_display()
        self.update_dealer_display(reveal=False)
        
        player_total = calculate_hand_value(self.player_hand)
        self.player_total.config(text=f"Player Total: {player_total}")
        
        self.hit_button.config(state=tk.NORMAL)
        self.stand_button.config(state=tk.NORMAL)
        self.play_again_button.config(state=tk.DISABLED)
        self.result_label.config(text="")
        self.dealer_total.config(text="Dealer Total: ??")

    def update_player_display(self):
        cards = [f"{card[0]} of {card[1]}" for card in self.player_hand]
        self.player_cards.config(text=", ".join(cards))

    def update_dealer_display(self, reveal=False):
        if reveal:
            cards = [f"{card[0]} of {card[1]}" for card in self.dealer_hand]
        else:
            if len(self.dealer_hand) == 0:
                cards = []
            else:
                cards = [f"{self.dealer_hand[0][0]} of {self.dealer_hand[0][1]}"]
                remaining = len(self.dealer_hand) - 1
                cards += ["Hidden Card"] * remaining
        self.dealer_cards.config(text=", ".join(cards))

    def hit(self):
        new_card = self.deck.pop()
        self.player_hand.append(new_card)
        
        threading.Thread(target=self.animate_card_flip, args=(self.player_cards,)).start()
        self.update_player_display()
        
        player_total = calculate_hand_value(self.player_hand)
        self.player_total.config(text=f"Player Total: {player_total}")
        
        if player_total > 21:
            self.end_game()

    def stand(self):
        self.reveal_dealer_hand()
        dealer_total = calculate_hand_value(self.dealer_hand)
        while dealer_total < 17:
            new_card = self.deck.pop()
            self.dealer_hand.append(new_card)
            threading.Thread(target=self.animate_card_flip, args=(self.dealer_cards,)).start()
            self.update_dealer_display(reveal=True)
            dealer_total = calculate_hand_value(self.dealer_hand)
        self.end_game()

    def reveal_dealer_hand(self):
        self.update_dealer_display(reveal=True)
        dealer_total = calculate_hand_value(self.dealer_hand)
        self.dealer_total.config(text=f"Dealer Total: {dealer_total}")

    def end_game(self):
        player_total = calculate_hand_value(self.player_hand)
        dealer_total = calculate_hand_value(self.dealer_hand)
        
        self.reveal_dealer_hand()
        
        self.player_total.config(text=f"Player Total: {player_total}")
        
        result = ""
        if player_total > 21:
            result = "You bust! Dealer wins."
        elif dealer_total > 21:
            result = "Dealer busts! You win."
        elif player_total > dealer_total:
            result = "You win!"
        elif player_total < dealer_total:
            result = "Dealer wins!"
        else:
            result = "It's a tie!"
        
        self.result_label.config(text=result)
        self.hit_button.config(state=tk.DISABLED)
        self.stand_button.config(state=tk.DISABLED)
        self.play_again_button.config(state=tk.NORMAL)

    def new_game(self):
        self.start_game()
        self.result_label.config(text="")

if __name__ == "__main__":
    app = BlackjackApp()
    app.mainloop()
