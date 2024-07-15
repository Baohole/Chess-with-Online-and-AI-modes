import pygame
import os







width=360
height=360


#load images
w_pawn=pygame.image.load(os.path.join("img","white_pawn.png"))
w_knight=pygame.image.load(os.path.join("img","white_knight.png"))
w_bishop=pygame.image.load(os.path.join("img","white_bishop.png"))
w_rook=pygame.image.load(os.path.join("img","white_rook.png"))
w_queen=pygame.image.load(os.path.join("img","white_queen.png"))
w_king=pygame.image.load(os.path.join("img","white_king.png"))

b_pawn=pygame.image.load(os.path.join("img","black_pawn.png"))
b_knight=pygame.image.load(os.path.join("img","black_knight.png"))
b_bishop=pygame.image.load(os.path.join("img","black_bishop.png"))
b_rook=pygame.image.load(os.path.join("img","black_rook.png"))
b_queen=pygame.image.load(os.path.join("img","black_queen.png"))
b_king=pygame.image.load(os.path.join("img","black_king.png"))

board=pygame.image.load(os.path.join("img","board.png"))

#scale images
black=[b_bishop,b_king,b_knight,b_pawn,b_queen,b_rook]
white=[w_bishop,w_king,w_knight,w_pawn,w_queen,w_rook]
B=[]
W=[]


for img in black:
    B.append(pygame.transform.scale(img,(35,35)))
for img in white:
    W.append(pygame.transform.scale(img,(35,35)))



class Piece():
    def __init__(self, x, y, color):
        self.x=x
        self.y=y
        self.color=color
        self.selected=False

        


    def move(self):
        pass
    #check if when the piece moves, will it reveal a check. If it will, do not let piece move there (can't be a valid move)
    def finalvalidMoves(self, bo, black, white):
        ycoord = self.y
        xcoord = self.x
        
        indexesToRemove = []
        CaptureChecker = False
        SecondHolder = self
        
        for m in range(8):
            for n in range(8):
                if type(bo.board[m][n]) == King and bo.board[m][n].color == self.color:
                    king = bo.board[m][n]
                    
                    CheckKeeper = king.InCheck
                    
                    thePiecesMoves, AmountOfMoves = self.validMoves(bo, black, white)
                    
                    for p in range(AmountOfMoves):
                        theirX, theirY = thePiecesMoves[p]
                        Holder = bo.board[theirY][theirX]
                        
                        bo.board[theirY][theirX] = SecondHolder
                        SecondHolder.x = theirX
                        SecondHolder.y = theirY
                        bo.board[ycoord][xcoord] = None
                        king.validMoves(bo, black, white)
                        if bo.board[m][n] is not None:
                            bo.board[m][n].selected = False
                        if king.InCheck == True:
                            indexesToRemove.append(p)
                        
                        king.InCheck = CheckKeeper
                        bo.board[theirY][theirX] = Holder
                        bo.board[ycoord][xcoord] = SecondHolder
                        SecondHolder.x = xcoord
                        SecondHolder.y = ycoord
        
        returnedlist = [thePiecesMoves[i] for i in range(AmountOfMoves) if i not in indexesToRemove]
        
        return returnedlist, len(returnedlist)

    def validMoves(self, bo, black, white):
        
        from board import Board

        size=0
        possiblemoves=self.movement()
      
        validMoves=[]
        
        
        
        if type(self)==Pawn:
            
            if self.color=='w':
                if self.x-1>=0 and self.x-1<=7 and self.y-1>=0 and self.y-1<=7:
                    if type(bo.board[self.y][self.x-1])==Pawn and bo.board[self.y][self.x-1].turn==1 and bo.board[self.y][self.x-1].UsedMove==1 and bo.board[self.y-1][self.x-1]==None:
                        validMoves.append((self.x-1, self.y-1))
                        size+=1
                if self.x+1>=0 and self.x+1<=7 and self.y-1>=0 and self.y-1<=7:
                    if type(bo.board[self.y][self.x+1])==Pawn and bo.board[self.y][self.x+1].turn==1 and bo.board[self.y][self.x+1].UsedMove==1 and bo.board[self.y-1][self.x+1]==None:
                        validMoves.append((self.x+1, self.y-1))
                        size+=1
            elif self.color=='b':
                if self.x-1>=0 and self.x-1<=7 and self.y+1>=0 and self.y+1<=7:
                    if type(bo.board[self.y][self.x-1])==Pawn and bo.board[self.y][self.x-1].turn==1 and bo.board[self.y][self.x-1].UsedMove==1 and bo.board[self.y+1][self.x-1]==None:
                        validMoves.append((self.x-1, self.y+1))
                        size+=1
                if self.x+1>=0 and self.x+1<=7 and self.y+1>=0 and self.y+1<=7:
                    if type(bo.board[self.y][self.x+1])==Pawn and bo.board[self.y][self.x+1].turn==1 and bo.board[self.y][self.x+1].UsedMove==1 and bo.board[self.y+1][self.x+1]==None:
                        validMoves.append((self.x+1, self.y+1))
                        size+=1
            for i in range(self.arraySize):
                tempX, tempY=possiblemoves[i]
                if tempX>=0 and tempX<=7 and tempY>=0 and tempY<=7:
                    if tempY==self.y-2 and tempX==self.x and self.color=='w'and bo.board[tempY][tempX]==None and bo.board[self.y-1][tempX]==None and self.turn==0:
                            validMoves.append(possiblemoves[i])
                            #self.turn=1           #Update this when the user moves the pawn for the first time 
                            size+=1
                    
                    elif tempY==self.y+2 and tempX==self.x and self.color=='b'and bo.board[tempY][tempX]==None and bo.board[self.y+1][tempX]==None and self.turn==0:
                            validMoves.append(possiblemoves[i])
                            #self.turn=1            #Update this when the user moves the pawn for the first time
                            size+=1
                    elif self.color=='w' and bo.board[tempY][tempX]==None and tempY==self.y-1 and tempX==self.x:
                        validMoves.append(possiblemoves[i])
                        size+=1
                    elif self.color=='b' and bo.board[tempY][tempX]==None and tempY==self.y+1 and tempX==self.x:
                        validMoves.append(possiblemoves[i])
                        size+=1
                    elif bo.board[tempY][tempX]!=None and bo.board[tempY][tempX].color!=self.color and (tempX==self.x+1 or tempX==self.x-1):
                        validMoves.append(possiblemoves[i])
                        size+=1
                    
                    
                    
        elif type(self)==Knight:
            for i in range(self.arraySize):
                tempX,tempY=possiblemoves[i]
                if tempX>=0 and tempX<=7 and tempY>=0 and tempY<=7:
                    if bo.board[tempY][tempX] == None or bo.board[tempY][tempX].color != self.color:
                        validMoves.append(possiblemoves[i])
                        #bo.board[tempY][tempX]=1
                        size += 1
                    
        elif type(self)==Bishop:
            topright=True
            topleft=True
            bottomright=True
            bottomleft=True
    
            for i in range(self.arraySize):
                
                tempX,tempY=possiblemoves[i]
                if tempX>=0 and tempX<=7 and tempY>=0 and tempY<=7:
                    if tempY<self.y and tempX>self.x and topright==True:

                        if bo.board[tempY][tempX] == None:
                            validMoves.append(possiblemoves[i])
                            size += 1
                        elif bo.board[tempY][tempX].color != self.color:
                            validMoves.append(possiblemoves[i])
                            size += 1
                            topright=False
                        elif bo.board[tempY][tempX].color == self.color:
                            topright=False

                    if tempY<self.y and tempX<self.x and topleft==True:
                        if bo.board[tempY][tempX] == None:
                            validMoves.append(possiblemoves[i])
                            size += 1
                        elif bo.board[tempY][tempX].color != self.color:
                            validMoves.append(possiblemoves[i])
                            size += 1
                            topleft=False
                        elif bo.board[tempY][tempX].color == self.color:
                            topleft=False

                    if tempY>self.y and tempX>self.x and bottomright==True:
                        if bo.board[tempY][tempX] == None:
                            validMoves.append(possiblemoves[i])
                            size += 1
                        elif bo.board[tempY][tempX].color != self.color:
                            validMoves.append(possiblemoves[i])
                            size += 1
                            bottomright=False
                        elif bo.board[tempY][tempX].color == self.color:
                            bottomright=False

                    if tempY>self.y and tempX<self.x and bottomleft==True:
                        if bo.board[tempY][tempX] == None:
                            validMoves.append(possiblemoves[i])
                            size += 1
                        elif bo.board[tempY][tempX].color != self.color:
                            validMoves.append(possiblemoves[i])
                            size += 1
                            bottomleft=False
                        elif bo.board[tempY][tempX].color == self.color:
                            bottomleft=False
        elif type(self)==Rook:
            up=True
            down=True
            right=True
            left=True
    
            for i in range(self.arraySize):
                tempX,tempY=possiblemoves[i]
                if tempX>=0 and tempX<=7 and tempY>=0 and tempY<=7:

                    if tempY<self.y and tempX==self.x and up==True:
                        if bo.board[tempY][tempX] == None:
                            validMoves.append(possiblemoves[i])
                            size += 1
                        elif bo.board[tempY][tempX].color != self.color:
                            validMoves.append(possiblemoves[i])
                            size += 1
                            up=False
                        elif bo.board[tempY][tempX].color == self.color:
                            up=False

                    if tempY>self.y and tempX==self.x and down==True:
                        if bo.board[tempY][tempX] == None:
                            validMoves.append(possiblemoves[i])
                            size += 1
                        elif bo.board[tempY][tempX].color != self.color:
                            validMoves.append(possiblemoves[i])
                            size += 1
                            down=False
                        elif bo.board[tempY][tempX].color == self.color:
                            down=False

                    if tempY==self.y and tempX>self.x and right==True:
                        if bo.board[tempY][tempX] == None:
                            validMoves.append(possiblemoves[i])
                            size += 1
                        elif bo.board[tempY][tempX].color != self.color:
                            validMoves.append(possiblemoves[i])
                            size += 1
                            right=False
                        elif bo.board[tempY][tempX].color == self.color:
                            right=False

                    if tempY==self.y and tempX<self.x and left==True:
                        if bo.board[tempY][tempX] == None:
                            validMoves.append(possiblemoves[i])
                            size += 1
                        elif bo.board[tempY][tempX].color != self.color:
                            validMoves.append(possiblemoves[i])
                            size += 1
                            left=False
                        elif bo.board[tempY][tempX].color == self.color:
                            left=False   

        elif type(self)==King:
            
            notallowed=[]
            counter=0
            
            #makes it possible to see if there is check beyond king
            bo.board[self.y][self.x]=None
            self.InCheck=False
            self.howManyCheck=0
            

            for i in range(self.arraySize):
                checkmove=False
                tempX,tempY=possiblemoves[i]
                if tempX>=0 and tempX<=7 and tempY>=0 and tempY<=7:
                    for x in range(8):
                        for y in range(8):
                            if bo.board[x][y]!= None:
                                if bo.board[x][y].color != self.color and type(bo.board[x][y])!=King:
                                   
                                    PieceMoves, MovesSize=bo.board[x][y].validMoves(bo, black, white)
                                    
                                        
                                                                               

                                    if type(bo.board[x][y])==Pawn and MovesSize==0:
                                        if bo.board[x][y].color=='w' and (bo.board[x][y].x+1==tempX or bo.board[x][y].x-1==tempX) and (bo.board[x][y].y-1==tempY):
                                            notallowed.append(possiblemoves[i])
                                            counter+=1
                                        
                                        if bo.board[x][y].color=='w' and (bo.board[x][y].x+1==self.x or bo.board[x][y].x-1==self.x) and (bo.board[x][y].y-1==self.y):
                                            self.InCheck=True
                                            self.checkingPiece=bo.board[x][y]

                                        if bo.board[x][y].color=='w' and (bo.board[x][y].x+1==3 or bo.board[x][y].x-1==3) and (bo.board[x][y].y-1==0):
                                            notallowed.append((3,0))
                                            counter+=1

                                        if bo.board[x][y].color=='w' and (bo.board[x][y].x+1==2 or bo.board[x][y].x-1==2) and (bo.board[x][y].y-1==0):
                                            notallowed.append((2,0))
                                            counter+=1

                                        if bo.board[x][y].color=='w' and (bo.board[x][y].x+1==5 or bo.board[x][y].x-1==5) and (bo.board[x][y].y-1==0):
                                            notallowed.append((5,0))
                                            counter+=1

                                        if bo.board[x][y].color=='w' and (bo.board[x][y].x+1==6 or bo.board[x][y].x-1==6) and (bo.board[x][y].y-1==0):
                                            notallowed.append((6,0))
                                            counter+=1
                                            
                                            
                                            
                                            
                                        if bo.board[x][y].color=='b' and (bo.board[x][y].x+1==tempX or bo.board[x][y].x-1==tempX) and (bo.board[x][y].y+1==tempY):
                                            notallowed.append(possiblemoves[i])
                                            counter+=1

                                        if bo.board[x][y].color=='b' and (bo.board[x][y].x+1==6 or bo.board[x][y].x-1==6) and (bo.board[x][y].y+1==7):
                                            notallowed.append((6,7))
                                            counter+=1
                                            
                                        if bo.board[x][y].color=='b' and (bo.board[x][y].x+1==5 or bo.board[x][y].x-1==5) and (bo.board[x][y].y+1==7):
                                            notallowed.append((5,7))
                                            counter+=1
                                        
                                        if bo.board[x][y].color=='b' and (bo.board[x][y].x+1==3 or bo.board[x][y].x-1==3) and (bo.board[x][y].y+1==7):
                                            notallowed.append((3,7))
                                            counter+=1
                                            
                                        if bo.board[x][y].color=='b' and (bo.board[x][y].x+1==2 or bo.board[x][y].x-1==2) and (bo.board[x][y].y+1==7):
                                            notallowed.append((2,7))
                                            counter+=1
                                        if bo.board[x][y].color=='b' and (bo.board[x][y].x+1==self.x or bo.board[x][y].x-1==self.x) and (bo.board[x][y].y+1==self.y):
                                            self.InCheck=True
                                            self.checkingPiece=bo.board[x][y]

                                       
                                               
                                            
                                        
                                    elif(MovesSize!=0):
                                        
                                        for move in range(MovesSize):
                                            moveX, moveY=PieceMoves[move]
                                           
                                            if self.color=='w':
                                                if (moveX==2 or moveX==6) and moveY==7:
                                                    notallowed.append((moveX,7)) 
                                                    counter+=1
                                            if self.color=='b':
                                                if (moveX==2 or moveX==6) and moveY==0:
                                                    notallowed.append((moveX,0)) 
                                                    counter+=1

                                            if moveX==self.x and moveY==self.y and type(bo.board[x][y])!=Pawn:
                                                self.InCheck=True
                                                self.checkingPiece=bo.board[x][y]
                                                
                                            
                                            if type(bo.board[x][y])!= Pawn and tempY==moveY and tempX==moveX :
                                                notallowed.append(possiblemoves[i]) 
                                                counter+=1

                                                
                                            elif type(bo.board[x][y])==Pawn:
                                                

                                                    
                                               
                                                if bo.board[x][y].color=='b' and tempY==bo.board[x][y].y+1 and (tempX==bo.board[x][y].x+1 or tempX==bo.board[x][y].x-1):
                                                    notallowed.append(possiblemoves[i]) 
                                                    counter=+1
                                                
                                                if bo.board[x][y].color=='b' and (bo.board[x][y].x+1==6 or bo.board[x][y].x-1==6) and (bo.board[x][y].y+1==7):
                                                    notallowed.append((6,7))
                                                    counter+=1
                                                    
                                                if bo.board[x][y].color=='b' and (bo.board[x][y].x+1==5 or bo.board[x][y].x-1==5) and (bo.board[x][y].y+1==7):
                                                    notallowed.append((5,7))
                                                    counter+=1
                                                
                                                if bo.board[x][y].color=='b' and (bo.board[x][y].x+1==3 or bo.board[x][y].x-1==3) and (bo.board[x][y].y+1==7):
                                                    notallowed.append((3,7))
                                                    counter+=1
                                                    
                                                if bo.board[x][y].color=='b' and (bo.board[x][y].x+1==2 or bo.board[x][y].x-1==2) and (bo.board[x][y].y+1==7):
                                                    notallowed.append((2,7))
                                                    counter+=1

                                                
                                                    
                                                        
                                                
                                                if  bo.board[x][y].color=='w' and tempY==bo.board[x][y].y-1 and (tempX==bo.board[x][y].x+1 or tempX==bo.board[x][y].x-1):
                                                    notallowed.append(possiblemoves[i]) 
                        
                                                    counter+=1

                                                if bo.board[x][y].color=='w' and (bo.board[x][y].x+1==3 or bo.board[x][y].x-1==3) and (bo.board[x][y].y-1==0):
                                                    notallowed.append((3,0))
                                                    counter+=1

                                                if bo.board[x][y].color=='w' and (bo.board[x][y].x+1==2 or bo.board[x][y].x-1==2) and (bo.board[x][y].y-1==0):
                                                    notallowed.append((2,0))
                                                    counter+=1

                                                if bo.board[x][y].color=='w' and (bo.board[x][y].x+1==5 or bo.board[x][y].x-1==5) and (bo.board[x][y].y-1==0):
                                                    notallowed.append((5,0))
                                                    counter+=1

                                                if bo.board[x][y].color=='w' and (bo.board[x][y].x+1==6 or bo.board[x][y].x-1==6) and (bo.board[x][y].y-1==0):
                                                    notallowed.append((6,0))
                                                    counter+=1
                                                
                                                if (bo.board[x][y].x+1==self.x or bo.board[x][y].x-1==self.x) and (bo.board[x][y].y+1==self.y)and bo.board[x][y].color=='b':
                                                    
                                                    self.InCheck=True
                                                    self.checkingPiece=bo.board[x][y]
                                                    

                                                if (bo.board[x][y].x+1==self.x or bo.board[x][y].x-1==self.x) and (bo.board[x][y].y-1==self.y) and bo.board[x][y].color=='w':
                                                   
                                                    self.InCheck=True
                                                    self.checkingPiece=bo.board[x][y]
                                                  
                                            
                                            
                                                  
                                        
                                        
            bo.board[self.y][self.x]=King(self.x, self.y, self.color)
            bo.board[self.y][self.x].selected=True
            
                                    
                                        
                                                        
                                           
                        
            for j in range(self.arraySize):
                checkmove=False
                Xmove,Ymove=possiblemoves[j]
                if Xmove>=0 and Xmove<=7 and Ymove>=0 and Ymove<=7:                            
                    if bo.board[Ymove][Xmove]!=None and bo.board[Ymove][Xmove].color!=self.color and ((Xmove, Ymove) not in notallowed):
                        Piece=bo.board[Ymove][Xmove]
                        color=bo.board[Ymove][Xmove].color
                        xcoord=bo.board[Ymove][Xmove].x
                        ycoord=bo.board[Ymove][Xmove].y
                        
                        bo.board[Ymove][Xmove]=None

                        flag=False
                        for q in range(8):
                            if flag:
                                break
                            for w in range(8):
                                if flag:
                                    break
                                if bo.board[q][w]!= None:
                                    if bo.board[q][w].color == color  and type(bo.board[q][w])!=King and type(bo.board[q][w])!=Pawn:#type(Piece)!=type(bo.board[q][w] #why did I do this, know it lets king capture protected pieces
                                        Moves, movesize =bo.board[q][w].validMoves(bo, black, white)

                                        for t in range(movesize):
                                            thisX, thisY=Moves[t]
                                            if thisX==xcoord and thisY==ycoord:
                                                notallowed.append(possiblemoves[j])
                                                counter+=1
                                                checkmove=True
                                                flag=True
                                                
                                                
                                                break   
                        bo.board[Ymove][Xmove]=Piece
                        if(checkmove==False):
                            validMoves.append(possiblemoves[j])
                            size+=1
                        



                               
                    elif bo.board[Ymove][Xmove]==None and ((Xmove, Ymove) not in notallowed):
                        validMoves.append(possiblemoves[j])
                        size += 1
                    
            if self.CanCastle==True:
                
                
                if self.color=='b'and black==True:
                    if type(bo.board[0][0])==Rook and bo.board[0][0].CanCastle==True:
                        
                        if (((3,0)not in notallowed) and ((2,0)not in notallowed) and (bo.board[0][3]==None) and (bo.board[0][2]==None)and (bo.board[0][1]==None) ):
                            validMoves.append((2,0))
                            size+=1
                    if type(bo.board[0][7])==Rook and bo.board[0][7].CanCastle==True:
                        
                        if (((5,0)not in notallowed) and ((6,0)not in notallowed)and (bo.board[0][6]==None) and (bo.board[0][5]==None)):
                            validMoves.append((6,0))
                            size+=1
                elif self.color=='w' and white==True:
                    
                    if type(bo.board[7][7])==Rook and bo.board[7][7].CanCastle==True:
                        
                        
                            
                        if (bo.board[7][5] is None) and ((5,7)not in notallowed) and  (bo.board[7][6] is None) and ((6,7)not in notallowed):
                            
                            validMoves.append((6,7))
                            size+=1
                    if type(bo.board[7][0])==Rook and bo.board[7][0].CanCastle==True:
                        
                        if (((3,7)not in notallowed) and ((2,7)not in notallowed)and (bo.board[7][3]==None) and (bo.board[7][2]==None)and (bo.board[7][1]==None)):
                            validMoves.append((2,7))
                            size+=1
        
                       



            


        elif type(self)==Queen:

            topright=True
            topleft=True
            bottomright=True
            bottomleft=True
            up=True
            down=True
            right=True
            left=True
    
            for i in range(self.arraySize):
                
                tempX,tempY=possiblemoves[i]
                if tempX>=0 and tempX<=7 and tempY>=0 and tempY<=7:
                    if tempY<self.y and tempX>self.x and topright==True:

                        if bo.board[tempY][tempX] == None:
                            validMoves.append(possiblemoves[i])
                            size += 1
                        elif bo.board[tempY][tempX].color != self.color:
                            validMoves.append(possiblemoves[i])
                            size += 1
                            topright=False
                        elif bo.board[tempY][tempX].color == self.color:
                            topright=False

                    if tempY<self.y and tempX<self.x and topleft==True:
                        if bo.board[tempY][tempX] == None:
                            validMoves.append(possiblemoves[i])
                            size += 1
                        elif bo.board[tempY][tempX].color != self.color:
                            validMoves.append(possiblemoves[i])
                            size += 1
                            topleft=False
                        elif bo.board[tempY][tempX].color == self.color:
                            topleft=False

                    if tempY>self.y and tempX>self.x and bottomright==True:
                        if bo.board[tempY][tempX] == None:
                            validMoves.append(possiblemoves[i])
                            size += 1
                        elif bo.board[tempY][tempX].color != self.color:
                            validMoves.append(possiblemoves[i])
                            size += 1
                            bottomright=False
                        elif bo.board[tempY][tempX].color == self.color:
                            bottomright=False

                    if tempY>self.y and tempX<self.x and bottomleft==True:
                        if bo.board[tempY][tempX] == None:
                            validMoves.append(possiblemoves[i])
                            size += 1
                        elif bo.board[tempY][tempX].color != self.color:
                            validMoves.append(possiblemoves[i])
                            size += 1
                            bottomleft=False
                        elif bo.board[tempY][tempX].color == self.color:
                            bottomleft=False
                    
                    

                    if tempY<self.y and tempX==self.x and up==True:
                        if bo.board[tempY][tempX] == None:
                            validMoves.append(possiblemoves[i])
                            size += 1
                        elif bo.board[tempY][tempX].color != self.color:
                            validMoves.append(possiblemoves[i])
                            size += 1
                            up=False
                        elif bo.board[tempY][tempX].color == self.color:
                            up=False

                    if tempY>self.y and tempX==self.x and down==True:
                        if bo.board[tempY][tempX] == None:
                            validMoves.append(possiblemoves[i])
                            size += 1
                        elif bo.board[tempY][tempX].color != self.color:
                            validMoves.append(possiblemoves[i])
                            size += 1
                            down=False
                        elif bo.board[tempY][tempX].color == self.color:
                            down=False

                    if tempY==self.y and tempX>self.x and right==True:
                        if bo.board[tempY][tempX] == None:
                            validMoves.append(possiblemoves[i])
                            size += 1
                        elif bo.board[tempY][tempX].color != self.color:
                            validMoves.append(possiblemoves[i])
                            size += 1
                            right=False
                        elif bo.board[tempY][tempX].color == self.color:
                            right=False

                    if tempY==self.y and tempX<self.x and left==True:
                        if bo.board[tempY][tempX] == None:
                            validMoves.append(possiblemoves[i])
                            size += 1
                        elif bo.board[tempY][tempX].color != self.color:
                            validMoves.append(possiblemoves[i])
                            size += 1
                            left=False
                        elif bo.board[tempY][tempX].color == self.color:
                            left=False   
                        
        return validMoves, size  

        
    

        
    def draw(self, screen):
        col=self.x*((352-4)/8)+8
        row=self.y*((352-4)/8)+8
       
        if self.color=="w":
            figure=W[self.img]

        else:
            figure=B[self.img]
        
        

        screen.blit(figure, (col, row))
        
    def draw_selected(self, screen,bo, black, white):
        col=self.x*((352-4)/8)+8
        row=self.y*((352-4)/8)+8
        if self.selected:
            pygame.draw.rect(screen, (255,0,0), pygame.Rect(col, row, 38, 38), 2)
            
            
            '''rect = pygame.Surface((38, 38))
            rect.fill((255, 0, 0))
            screen.blit(rect, (col, row))'''
            
          
            if type(self)!=King:
                
                Moves, size= self.finalvalidMoves(bo, black, white)     #validMoves()
               
                
            else:
                
                Moves, size= self.validMoves(bo, black, white)     #validMoves()
            

            for i in range(size):

                x, y=Moves[i]
                colValue=x*((352-4)/8)+8+20
                rowValue=y*((352-4)/8)+8+20
                
                
                pygame.draw.circle(screen, (255, 0, 0), (colValue, rowValue), 5)
                
            
        
                


   
    
class Bishop(Piece):
    img=0
    arraySize=28
    def movement(self):
        possibleMoves=[]
        if self.color:
            for i in range(1,8):
                possibleMoves.append((self.x+i, self.y+i))
                possibleMoves.append((self.x-i, self.y-i))
                possibleMoves.append((self.x-i, self.y+i))
                possibleMoves.append((self.x+i, self.y-i))
            return possibleMoves
        
    
class King(Piece):
    
    CanCastle=True
    checkingPiece=None
    img=1
    arraySize=8
    InCheck=False
    def movement(self):
        possibleMoves=[]
        possibleMoves.append((self.x+1, self.y+1))
        possibleMoves.append((self.x+1, self.y-1))
        possibleMoves.append((self.x-1, self.y+1))
        possibleMoves.append((self.x+1, self.y))
        possibleMoves.append((self.x-1, self.y))
        possibleMoves.append((self.x-1, self.y-1))
        possibleMoves.append((self.x, self.y+1))
        possibleMoves.append((self.x, self.y-1))
        return possibleMoves
        

class Knight(Piece):
    
    
    img=2
   
    arraySize=8
    def movement(self):
        possibleMoves=[]
        possibleMoves.append((self.x+2,self.y+1 ))
        possibleMoves.append((self.x+2, self.y-1))
        possibleMoves.append((self.x-2,self.y+1 ))
        possibleMoves.append((self.x-2, self.y-1))
        possibleMoves.append((self.x-1,self.y+2 ))
        possibleMoves.append((self.x+1, self.y+2))
        possibleMoves.append((self.x-1,self.y-2 ))
        possibleMoves.append((self.x+1, self.y-2))
        
        
        return possibleMoves
class Pawn(Piece):

    img=3
    arraySize=4
    turn=0
    UsedMove=0
    def movement(self):
        possibleMoves=[]
        if self.color=='w':
            if self.turn==0:
                possibleMoves.append((self.x, self.y-2))
                self.arraySize=4
            elif self.turn>=1:
                self.arraySize=3
            

            possibleMoves.append((self.x+1, self.y-1))
            possibleMoves.append((self.x-1, self.y-1))
            possibleMoves.append((self.x, self.y-1))
           
        else:
            if self.turn==0:
                possibleMoves.append((self.x, self.y+2))
                self.arraySize=4
            elif self.turn>=1:
                self.arraySize=3
            
            possibleMoves.append((self.x+1, self.y+1))
            possibleMoves.append((self.x-1, self.y+1))
            possibleMoves.append((self.x, self.y+1))
            
        return possibleMoves

        
class Queen(Piece):
    img=4
    arraySize=56
    def movement(self):
        possibleMoves=[]
        for i in range(1,8):
            possibleMoves.append((self.x+i, self.y+i))
            possibleMoves.append((self.x-i, self.y-i))
            possibleMoves.append((self.x-i, self.y+i))
            possibleMoves.append((self.x+i, self.y-i))
        for i in range(1,8):
            possibleMoves.append((self.x+i, self.y))
            possibleMoves.append((self.x-i, self.y))
            possibleMoves.append((self.x, self.y+i))
            possibleMoves.append((self.x, self.y-i))
        return possibleMoves
class Rook(Piece):
    CanCastle=True
    img=5
    arraySize=28
    def movement(self):
        possibleMoves=[]
        for i in range(1,8):
            possibleMoves.append((self.x+i, self.y))
            possibleMoves.append((self.x-i, self.y))
            possibleMoves.append((self.x, self.y+i))
            possibleMoves.append((self.x, self.y-i))
        return possibleMoves




