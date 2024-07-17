# Chess-AI-and-Implementation-to-Online-Chess-Game-
Created Convolutional Neural Network (CNN) in TensorFlow and implemented it to add "Play Against AI" to my Chess Game project. 

-Used pandas and numpy to parse data and create "new_data.csv" to train the CNN. Data only included games of players with ratings of 2000 or greater.

-Trained CNN model by going through 10,000 games in "new_data.csv" and generating and input array of matrix board state representations and output array of consecutively perfomed moves in those games.  another with performed moves. 

-Created CNN using TensorFlow and trained it using data generated from "new_data.csv".

-Made enhancements to my "Online Chess Game", using the new chess AI stored in "CagnusMarlsen.keras" to play against user when game mode selected is "Play against AI".

    -AI would not always acknowledge a possible move and return None due to limited training. I added a check for other possible moves before returning None. 
    -added a cancel button when searching for connection in "online" mode.
    -fixed bug where the pawn promotion popup caused an error when user exited it instead of answering with promotion. 

Remarks: 
-Training the AI was limited due to hardware and data limitations. 
-There were only 15,000 games I had of 2000+ elo players which could of caused overfitting and training the model took long.
-Due to this, the AI, does not always make the best decisions, hence the satirical name "Cagnus Marlsen".

Chess AI Demo:
-Download the ChessAIDemo.mkv file to view a game with the AI and the Cancel feature. As you can probably notice the AI does not make the best decisions due to training limitations. 
