# Airlock
*This is a python implementation of **Project Airlock** using pygame. It contains code for a server, which can connect up to six clients via UDP, and a GUI to interpret and respond to server updates.*

### General functionality
- Server runs a game of airlock and communicates changes in game state to each client through UDP
- Server sends requests to client during play and waits for a response
- Client uses GUI to see changes in state and to answer requests for actions

### Existing problems
- Outlined in code with #TODO, #FIXME, or #BUG comments.

### Next steps
- Make server-client interaction more robust and account for loss of connection condition
- Improve usability by adding more gamestate updates for changes in player turn, ally selection, shuffling, and game win
- Add resetting functionality to client
- Overall improvements to GUI, including to graphics and animation

![image](https://user-images.githubusercontent.com/22649301/40291431-0cac2eb2-5c93-11e8-8fc0-d0cce5154761.png)
