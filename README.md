# Chess-AI-and-Implementation-to-Online-Chess-Game- 
DEMOS:

- https://www.youtube.com/watch?v=C83Q3hPqgCc - Online Mode and general features
- https://www.youtube.com/watch?v=CclX7bjWGGQ - AI Mode playthrough

Created Convolutional Neural Network (CNN) in TensorFlow and implemented it to add "Play Against AI" to my Chess Game project. 

-Used pandas and numpy to parse data and create "new_data.csv" to train the CNN. Data only included games of players with ratings of 2000 or greater.

-Trained CNN model by going through 10,000 games in "new_data.csv" and generating an input array of matrix board state representations and output array of consecutively perfomed moves in those games.  

-Created CNN using TensorFlow and trained it using data generated from "new_data.csv".

-Made enhancements to my "Online Chess Game", using the new chess AI stored in "CagnusMarlsen.keras" to play against user when game mode selected is "Play against AI".

    -AI would not always acknowledge a possible move and return None due to limited training. I added a check for other possible moves before returning None. 
    -added a cancel button when searching for connection in "online" mode.
    -fixed bug where the pawn promotion popup caused an error when user exited it instead of answering with promotion. 

Remarks: 
-Training the AI was limited due to hardware and data limitations. 
-There were only 15,000 games I had of 2000+ elo players which could of caused overfitting based on which moves were most common in this limited dataset. Due to this, the AI does not always make the best decisions.


