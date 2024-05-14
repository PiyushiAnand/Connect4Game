# Connect4Game

This is a self project for the Python implementation of the Connect4 game.

## Step by Step Explanation:

### Single Player Version

1. **Basic Game Setup**: 
   - Make the basic UI using the pygame library.
   - Write code for animating the drop of coins into slots.

2. **Build Game Logic**: 
   - Write the logic of the game that will be used to determine the score.

3. **Add Everything Together**: 
   - Integrate everything, and we have our single-player game ready.
   - Basically, two players can sit together and play this game.

Note: Score system has not been added yet in this version.

### Multiplayer Version

1. **Extend the Game for Multiplayer**:
   - Implement network communication using sockets to allow multiple players to connect.
   - Update the game logic to handle multiplayer interactions.
   
2. **Synchronize Game State**:
   - Ensure that the game state (board, scores, current player) is synchronized between all connected players using threads.
   
3. **Handle Turn-Based Gameplay**:
   - Implement turn-based gameplay so that each player takes turns dropping their pieces.

4. **Update Scores**:
   - Implement score tracking and update mechanisms to reflect the scores of both players accurately.

5. **Enhance UI for Multiplayer**:
   - Update the UI to display information about the current state of the game (e.g., whose turn it is, scores).
