
## Contract Whist

For now a command line implementation of the game contract whist

### Rules

Contract whist (_aka bid whist_) is a standard variation on whist trick taking games. There are quite a few minor variations of this game, this implementation is the version I've always played.

#### Game play

Each round the players are dealt a different number of cards, with values descending in steps of 2 from the second highest possible down to 1 card, then back up in steps of 2 to the maximum possible number of cards. With 4 players this is 12, 10, 8, ... 1, 3, ..., 11, 13. The **trump** suit for each round cycles through ♣➡♦➡♥➡♠➡NT (no trumps).

In each round the players lay one card in turn into the pile in the middle of the table. **If you can follow the suit of the first card laid you must**. If you have several of that suit you can choose which one to lay. If you cannot follow suit any card can be played, but it can't win unless it is a trump. The highest value card in the pile wins. With real cards, that pile of cards is turned over in front of whoever laid the highest card, who will then lead the next card. Each of these piles is called a **trick**.

The skill in the game is calling how many tricks you will make once you have looked at your cards, but before any have been laid. This is your **contract**. If you make your contract, you get a 10 point bonus, plus one point for every trick you made. If you missed your contract you still get one point for every trick made. As one final twist, the total of everyone's bids cannot add up to the total number of tricks available. As the dealer calls last it is their bid that is limited by this caveat.

Points are scored cumulatively across all of the rounds, with the winner being the person with the highest total at the end.