      MODE 21
      ORIGIN 800,600
      COLOUR 2,20,100,20
      VDU 23,23,2|
      COLOUR 128+2

      DIM Pieces{(18) l%,x%,y%}  :REM Contains location on board (or not) of each piece
      FOR x%=0 TO 17
        Pieces{(x%)}.l%=-1     :REM Initially location is not on board
        PROCPiecePos(x%)
      NEXT x%

      DIM Brd%(23),Pcs%(17) :REM Will store the pieces at each board location, and location of each piece!

      DIM Board{(24) occ%,con%(4),nc%,x%,y%} :REM Each of the 24 locations has an occupancy (-1=free, or the piece number), and up to 4 connections
      FOR x%=0 TO 23
        PROCPointPos(x%)
        Board{(x%)}.occ%=-1
      NEXT x%
      REM Set up links between points (construct a directed graph!)
      PROCDrawBoard
      FOR x%=1 TO 32
        READ a%,b%
        Board{(a%)}.con%(Board{(a%)}.nc%)=b%
        Board{(a%)}.nc%+=1
        Board{(b%)}.con%(Board{(b%)}.nc%)=a%
        Board{(b%)}.nc%+=1
      NEXT x%
      REM Here's the data for the links, each of which is bidirectional
      DATA 0,1,0,9,1,2,1,4,2,14,3,4,3,10,4,5,4,7,5,13,6,7,6,11,7,8,8,12,9,10,9,21
      DATA 10,11,10,18,11,15,12,13,12,17,13,14,13,20,14,23,15,16,16,17,16,19,18,19,19,20,19,22
      DATA 21,22,22,23
      OFF

      DIM Movestruct{sp%,sl%,d%,s}         :REM Structure for returning moves - contains piece number, location to move to, possibly a deleted opposition counter, and the score

      DIM Playertype%(1) :REM computer player (1) or human (0)?
      Playertype%(0)=1

      nblack%=9
      nred%=9
      NextPlayer%=0
      moves%=0

      REM Main game loop
      REPEAT
        moved%=FALSE
        PROCRefillLocArrays:REM Set up arrays needed for AI
        IF moves%<18 THEN
          phase%=1
        ELSE
          IF nblack%>3 AND nred%>3 THEN phase%=2 ELSE phase%=3
        ENDIF
        IF NextPlayer%=0 THEN c$="Black" ELSE c$="RED"
        IF Playertype%(NextPlayer%)=1 THEN
          PROCFindMove(Brd%(),Pcs%(),NextPlayer%,moves%,3,Movestruct{})
          sl%=Movestruct.sl%
          sp%=Movestruct.sp%
          IF phase%=2 THEN
            PRINT" Back from the dead!"
            q$=GET$
          ENDIF
        ELSE
          PRINT TAB(0,0);c$+" to play: Eval for "+c$+": ";FNEvaluate(Brd%(),Pcs%(),NextPlayer%,phase%);" phase ";phase%
          PRINT"Params for black were ";Movestruct.s,sp%,sl%
          REPEAT
            MOUSE x%,y%,z%
            WAIT 1
          UNTIL z%>0
          REM Clicked down: identify counter
          sp%=FNFindPiece(x%,y%)
          IF sp%>-1 AND FNColFromPiece(sp%)=NextPlayer% THEN
            REM We found a counter! Drag it....
            GCOL 4,2+(sp% DIV 9)
            CIRCLE x%,y%,50
            REPEAT
              MOUSE px%,py%,z%
              WAIT 1
              CIRCLE x%,y%,50
              CIRCLE px%,py%,50
              x%=px%:y%=py%
            UNTIL z%=0
            CIRCLE x%,y%,50
            REM Find the board location closest (within 50) to the mouse pointer
            sl%=FNFindLocation(x%,y%)
          ENDIF
        ENDIF
        REM Re-entry point for AI move suggestion
  
        IF sl%>-1 AND sp%>-1 THEN
          REM Found a location
          IF Board{(sl%)}.occ%=-1 AND FNlinked(sl%,Pieces{(sp%)}.l%) THEN
            REM The space is vacant, and can be reached from where the counter started
            Board{(sl%)}.occ%=sp%
            Pieces{(sp%)}.x%=Board{(sl%)}.x%
            Pieces{(sp%)}.y%=Board{(sl%)}.y%
            IF Pieces{(sp%)}.l%>-1 THEN Board{(Pieces{(sp%)}.l%)}.occ% =-1  :REM Mark the space it has come from as empty
            Pieces{(sp%)}.l%=sl%
            PROCDrawBoard
            PROCRefillLocArrays:REM Set up arrays needed for AI (and FNIsInMill!)
            IF Playertype%(NextPlayer%)=1 THEN
              IF Movestruct.d%>-1 THEN
                REM Computer made a mill and deleted a piece!
                PRINT"Computer made a mill and deletes piece on ";Pieces{(Movestruct.d%)}.l%
                WAIT 200
                PROCKillPiece(Movestruct.d%)
              ENDIF
            ELSE
              IF FNIsInMill(Brd%(),sl%) THEN PROCRemoveCounter(sp%)
            ENDIF
            moved%=TRUE
            moves%+=1
          ENDIF
        ENDIF
        IF moved% THEN NextPlayer%=(NextPlayer%+1) MOD 2
      UNTIL FALSE
      END



      DEFPROCDrawBoard
      LOCAL n%,x%,y%,n1%,n2%
      *REFRESH OFF
      GCOL 128+2
      GCOL 15
      CLG
      RECTANGLE -150,-150,300,300
      RECTANGLE -300,-300,600,600
      RECTANGLE -450,-450,900,900
      LINE -450,0,-150,0
      LINE 150,0,450,0
      LINE 0,-450,0,-150
      LINE 0,150,0,450
      FOR n%=0 TO 17
        REM PROCPos(n%,x%,y%)
        IF n%<9 THEN GCOL 0 ELSE GCOL 1
        CIRCLE FILL Pieces{(n%)}.x%,Pieces{(n%)}.y%,50
      NEXT n%
      *REFRESH ON
      ENDPROC
      :
      DEFPROCPiecePos(p%)
      LOCAL l%,x%,y%,n1%,n2%
      l%=Pieces{(x%)}.l%
      IF l%=-1 THEN
        IF p%<9 THEN
          x%=-700:y%=(4-p%)*120
        ELSE
          x%=700:y%=(13-p%)*120
        ENDIF
      ELSE
        n1%=l% DIV 3
        n2%=l% MOD 3
        CASE l% OF
          WHEN 0,1,2,3,4,5,6,7,8: x%=-150*(3-n1%)+n2%*150*(3-n1%):y%=-150*(3-n1%)
          WHEN 9,10,11: x%=-450+n2%*150:y%=0
          WHEN 12,13,14:x%=150+n2%*150:y%=0
          WHEN 15,16,17,18,19,20,21,22,23: x%=-150*(n1%-4)+n2%*150*(n1%-4):y%=150*(n1%-4)
        ENDCASE
      ENDIF
      Pieces{(p%)}.x%=x%
      Pieces{(p%)}.y%=y%
      ENDPROC
      :
      DEFPROCPointPos(l%)
      LOCAL x%,y%,n1%,n2%
      n1%=l% DIV 3
      n2%=l% MOD 3
      CASE l% OF
        WHEN 0,1,2,3,4,5,6,7,8: x%=-150*(3-n1%)+n2%*150*(3-n1%):y%=-150*(3-n1%)
        WHEN 9,10,11: x%=-450+n2%*150:y%=0
        WHEN 12,13,14:x%=150+n2%*150:y%=0
        WHEN 15,16,17,18,19,20,21,22,23: x%=-150*(n1%-4)+n2%*150*(n1%-4):y%=150*(n1%-4)
      ENDCASE
      Board{(l%)}.x%=x%
      Board{(l%)}.y%=y%
      ENDPROC
      :
      DEFFNFindPiece(x%,y%)
      LOCAL p%
      FOR p%=0 TO 17
        IF SQR((x%-Pieces{(p%)}.x%)^2+(y%-Pieces{(p%)}.y%)^2)<50 THEN =p%
      NEXT p%
      =-1
      :
      DEFFNFindLocation(x%,y%)
      LOCAL p%
      REM IF SQR((x%)^2+(y%)^2)<50 THEN =-2   Think this is a hangover from dumping them in the middle..
      FOR p%=0 TO 23
        IF SQR((x%-Board{(p%)}.x%)^2+(y%-Board{(p%)}.y%)^2)<50 THEN =p%
      NEXT p%
      =-1
      :
      DEFFNlinked(l1%,l2%)
      LOCAL x%
      IF l2%=-1 THEN =TRUE     :REM Piece to be moved is still off the board (phase 1)
      CASE FNColFromPlace(Brd%(),l2%) OF
        WHEN 0:IF nblack%=3 THEN =TRUE
        WHEN 1: IF nred%=3 THEN =TRUE
      ENDCASE
      FOR x%=0 TO 3
        IF Board{(l1%)}.con%(x%)=l2% THEN =TRUE
      NEXT x%
      =FALSE
      :
      DEFFNIsInMill(Brd%(),l%)
      LOCAL c%,r%
      IF l%<0 THEN =FALSE  :REM Would only apply if originated from a counter not yet been placed
      IF Brd%(l%)=-1 THEN =FALSE :REM This point isn't occupied!
      c%=Brd%(l%) DIV 9
      r%=3*(l% DIV 3)
      IF FNColFromPlace(Brd%(),r%)=c%  AND FNColFromPlace(Brd%(),r%+1)=c%  AND FNColFromPlace(Brd%(),r%+2)=c% THEN =TRUE
      CASE l% OF
        WHEN 0,9,21: IF FNColFromPlace(Brd%(),0)=c% AND FNColFromPlace(Brd%(),9)=c% AND FNColFromPlace(Brd%(),21)=c% THEN =TRUE
        WHEN 3,10,18: IF FNColFromPlace(Brd%(),3)=c% AND FNColFromPlace(Brd%(),10)=c% AND FNColFromPlace(Brd%(),18)=c% THEN =TRUE
        WHEN 6,11,15: IF FNColFromPlace(Brd%(),6)=c% AND FNColFromPlace(Brd%(),11)=c% AND FNColFromPlace(Brd%(),15)=c% THEN =TRUE
        WHEN 1,4,7: IF FNColFromPlace(Brd%(),1)=c% AND FNColFromPlace(Brd%(),4)=c% AND FNColFromPlace(Brd%(),7)=c% THEN =TRUE
        WHEN 16,19,22: IF FNColFromPlace(Brd%(),16)=c% AND FNColFromPlace(Brd%(),19)=c% AND FNColFromPlace(Brd%(),22)=c% THEN =TRUE
        WHEN 8,12,17: IF FNColFromPlace(Brd%(),8)=c% AND FNColFromPlace(Brd%(),12)=c% AND FNColFromPlace(Brd%(),17)=c% THEN =TRUE
        WHEN 5,13,20: IF FNColFromPlace(Brd%(),5)=c% AND FNColFromPlace(Brd%(),13)=c% AND FNColFromPlace(Brd%(),20)=c% THEN =TRUE
        WHEN 2,14,23: IF FNColFromPlace(Brd%(),2)=c% AND FNColFromPlace(Brd%(),14)=c% AND FNColFromPlace(Brd%(),23)=c% THEN =TRUE
      ENDCASE
      =FALSE
      :
      DEFFNColFromPlace(Brd%(),l%)
      IF Brd%(l%)=-1 THEN =-1
      = Brd%(l%) DIV 9
      :
      DEFFNColFromPiece(p%)
      =p% DIV 9
      :
      DEFPROCRemoveCounter(c%)
      LOCAL x%,y%,z%,sp%,c1$,c2$
      c1$="Black"
      c2$="Red"
      IF FNColFromPiece(c%)=1 THEN SWAP c1$,c2$
      PRINT TAB(0,0);c1$" mill completed! Click a "+c2$+" piece to remove it"
      REPEAT
        REPEAT
          MOUSE x%,y%,z%
          WAIT 1
        UNTIL z%>0
        REM Clicked: identify counter
        sp%=FNFindPiece(x%,y%)
        REM Clear mouse buffer
        REPEAT
          MOUSE x%,y%,z%
          WAIT 1
        UNTIL z%=0
      UNTIL Pieces{(sp%)}.l%>-1 AND (FNColFromPiece(sp%)=(FNColFromPiece(c%)+1) MOD 2) AND FNMillsOk(Brd%(),Pcs%(),sp%)
      PROCKillPiece(sp%)
      REM Board{(Pieces{(sp%)}.l%)}.occ%=-1
      REM Pieces{(sp%)}.x%=-2000
      REM Pieces{(sp%)}.y%=0
      REM Pieces{(sp%)}.l% =-2  :REM May be better not to do this?
      REM IF c% DIV 9=0 THEN nred%-=1 ELSE nblack%-=1
      REM PROCDrawBoard
      REM IF nblack%<3 THEN PRINT"Black only has two pieces, and has lost!":END
      REM IF nred%<3 THEN PRINT"Red only has two pieces, and has lost!":END
      ENDPROC
      :
      DEFPROCKillPiece(sp%)
      Board{(Pieces{(sp%)}.l%)}.occ%=-1
      Pieces{(sp%)}.x%=-2000
      Pieces{(sp%)}.y%=0
      Pieces{(sp%)}.l% =-2  :REM May be better not to do this?
      IF c% DIV 9=0 THEN nred%-=1 ELSE nblack%-=1
      PROCDrawBoard
      IF nblack%<3 THEN PRINT"Black only has two pieces, and has lost!":END
      IF nred%<3 THEN PRINT"Red only has two pieces, and has lost!":END
      ENDPROC

      :
      DEFPROCAIRemCounter(Brd%(),Pcs%(),p%) :REM Remove counter from arrays being processed for AI Not permanent!
      Brd%(Pcs%(p%))=-1
      Pcs%(p%)=-2
      ENDPROC
      :
      DEFFNMillsOk(Brd%(),Pcs%(),p%)
      IF p%<0 THEN =TRUE :REM Should never be true!
      IF NOT FNIsInMill(Brd%(),Pcs%(p%)) THEN =TRUE
      LOCAL x%,c%
      c%=FNColFromPiece(p%)
      FOR x%=0 TO 8
        IF (NOT FNIsInMill(Brd%(),Pcs%(c%*9+x%))) AND Pcs%(c%*9+x%)>-1 THEN =FALSE
      NEXT x%
      =TRUE
      :
      DEFFNEvaluate(Brd%(),Pcs%(),p%,phase%):REM Takes arrays with board pieces and piece locations, and a player ID, and evaluates the value of this position
      LOCAL x%,y%,c%,c2%,n%(),m%(),premill%(),freemoves%()
      DIM n%(1),m%(1),premill%(1),freemoves%(1)
      FOR x%=0 TO 23
        IF Brd%(x%)>-1 THEN
          c%=Brd%(x%) DIV 9
          n%(c%)+=1
          IF FNIsInMill(Brd%(),x%) THEN m%(c%)+=1
          FOR y%=0 TO Board{(x%)}.nc%-1
            IF Brd%(Board{(x%)}.con%(y%))=-1 THEN freemoves%(c%)+=1
          NEXT y%
        ELSE
          Brd%(x%)=0
          IF FNIsInMill(Brd%(),x%) THEN premill%(0)+=1
          Brd%(x%)=9
          IF FNIsInMill(Brd%(),x%) THEN premill%(1)+=1
          Brd%(x%)=-1
        ENDIF
      NEXT x%
      REM Weightings
      CASE phase% OF
        WHEN 1:
          pieceweight=1
          millweight=.1
          premillweight=.2
          movesweight=.1
        WHEN 2:
          pieceweight=1
          millweight=.1
          premillweight=.2
          movesweight=.001
          IF n%(c%)<3 THEN =-100
          IF n%(c2%)<3 THEN =100
        WHEN 3:
          pieceweight=1
          millweight=.1
          premillweight=1.5
          movesweight=.001
          IF n%(c%)<3 THEN =-100
          IF n%(c2%)<3 THEN =100
      ENDCASE
      c%=p%
      c2%=(c%+1) MOD 2
      =pieceweight*n%(c%)+millweight*m%(c%)+premillweight*premill%(c%)+movesweight*freemoves%(c%)-(pieceweight*n%(c2%)+millweight*m%(c2%)+premillweight*premill%(c2%)+movesweight*freemoves%(c2%))
      :
      DEFPROCRefillLocArrays
      LOCAL x%
      FOR x%=0 TO 23
        Brd%(x%)=Board{(x%)}.occ%
      NEXT x%
      FOR x%=0 TO 17
        Pcs%(x%)=Pieces{(x%)}.l%
      NEXT x%
      ENDPROC
      :
      DEFPROCFindMove(Bord%(),Peeces%(),p%,m%,d%,RETURN MoveStruct{}) :REM Passes in (a copy of) the board and pieces arrays, which player is  making the move (0 or 1), number of moves completed, and depth to go to
      REM Returns the piece to move and its (new) location, possibly a piece to delete, and the evaluation score in MoveStruct
      LOCAL p2%,x%,y%,z%,Brd%(),Pcs%(),pn%,ts,tm,minimax,best%,delp%,tdp%
      LOCAL bestmove{}
      DIM bestmove{}=Movestruct{}
      DIM Brd%(23),Pcs%(17)
      Brd%()=Bord%()
      Pcs%()=Peeces%()
      p2%=(p%+1) MOD 2
      delp%=-1
      IF d% MOD 2=1 THEN minimax=-150 ELSE minimax=150
      IF m%<18 THEN
        REM Still in phase 1: only need to consider possible placements of 1 counter. Try it in each space on the board
        REM PRINT "moves ";m%;" player ";p%
        pn%=p%*9+(m% DIV 2)
        FOR x%=0 TO 23
          IF Bord%(x%)=-1 THEN
            Brd%(x%)=pn%
            Pcs%(pn%)=x%
            IF FNIsInMill(Brd%(),x%) THEN
              REM We've made a mill! Need to remove an opposition piece
              FOR y%=0 TO (m% DIV 2)
                REM Brd%()=Bord%()
                REM Pcs%()=Peeces%()
                REM Brd%(x%)=pn%
                REM Pcs%(pn%)=x%
                tdp%=p2%*9+y%
                IF Pcs%(tdp%)>-1 THEN
                  Brd%(Pcs%(tdp%))=-1
                  IF d% MOD 2=0 THEN
                    PROCFindMove(Brd%(),Pcs%(),p2%,m%+1,d%-1,MoveStruct{})
                    IF MoveStruct.s<minimax THEN minimax=MoveStruct.s:bestmove.sl%=x%:bestmove.sp%=pn%:bestmove.d%=tdp%
                  ELSE
                    IF d%= 1 THEN
                      MoveStruct.s=FNEvaluate(Brd%(),Pcs%(),p%,1)
                    ELSE
                      PROCFindMove(Brd%(),Pcs%(),p2%,m%+1,d%-1,MoveStruct{})
                    ENDIF
                    IF MoveStruct.s>minimax THEN minimax=MoveStruct.s:bestmove.sl%=x%:bestmove.sp%=pn%:bestmove.d%=tdp%
                  ENDIF
                ENDIF
                Brd%(x%)=-1
                Pcs%(pn%)=-1
          
              NEXT y%
            ELSE
              IF d% MOD 2=0 THEN
                PROCFindMove(Brd%(),Pcs%(),p2%,m%+1,d%-1,MoveStruct{})
                IF MoveStruct.s<minimax THEN minimax=MoveStruct.s:bestmove.sl%=x%:bestmove.sp%=pn%:bestmove.d%=-1
              ELSE
                IF d%= 1 THEN
                  MoveStruct.s=FNEvaluate(Brd%(),Pcs%(),p%,1)
                ELSE
                  PROCFindMove(Brd%(),Pcs%(),p2%,m%+1,d%-1,MoveStruct{})
                ENDIF
                IF MoveStruct.s>minimax THEN minimax=MoveStruct.s:bestmove.sl%=x%:bestmove.sp%=pn%:bestmove.d%=-1
              ENDIF
            ENDIF
          ENDIF
          Brd%()=Bord%()
        NEXT x%
        bestmove.s=minimax
        MoveStruct{}=bestmove{}
        ENDPROC
      ELSE
        REM We're in phase 2 or 3: need to consider each point: if it's our peice, what moves are possible?
        FOR x%=0 TO 23
          pn%=Bord%(x%)
          IF pn% DIV 9=p% AND pn%>-1 THEN
            REM it's our piece: see if it can move
            FOR y%=0 TO Board{(x%)}.nc%
              tm%=Board{(x%)}.con%(y%)
              IF Bord%(tm%)=-1 THEN
                REM this move is possible!
                Brd%(tm%)=pn%
                Pcs%(pn%)=tm%
                Brd%(x%)=-1
                IF FNIsInMill(Brd%(),x%) THEN
                  REM We've made a mill! Need to remove an opposition piece
                  FOR z%=0 TO 8
                    tdp%=p2%*9+y%
                    IF Pcs%(tdp%)>-1 THEN
                      Brd%(Pcs%(tdp%))=-1
                      IF d%>1 THEN
                        PROCFindMove(Brd%(),Pcs%(),p2%,m%+1,d%-1,MoveStruct{})
                        IF MoveStruct.s<minimax THEN minimax=MoveStruct.s:bestmove.sl%=x%:bestmove.sp%=pn%:bestmove.d%=tdp%
                      ELSE
                        MoveStruct.s=FNEvaluate(Brd%(),Pcs%(),p%,1)
                        IF MoveStruct.s>minimax THEN minimax=MoveStruct.s:bestmove.sl%=x%:bestmove.sp%=pn%:bestmove.d%=tdp%
                      ENDIF
                      Brd%(Pcs%(tdp%))=tdp%
                    ENDIF
                  NEXT z%
                ELSE
                  REM No mill: simply evaluate the positions
                  IF d%>1 THEN
                    PROCFindMove(Brd%(),Pcs%(),p2%,m%+1,d%-1,MoveStruct{})
                    IF MoveStruct.s<minimax THEN minimax=MoveStruct.s:bestmove.sl%=x%:bestmove.sp%=pn%:bestmove.d%=-1
                  ELSE
                    MoveStruct.s=FNEvaluate(Brd%(),Pcs%(),p%,1)
                    IF MoveStruct.s>minimax THEN minimax=MoveStruct.s:bestmove.sl%=x%:bestmove.sp%=pn%:bestmove.d%=-1
                  ENDIF
                ENDIF
          
              ENDIF
              Brd%()=Bord%()
              Pcs%()=Peeces%()
        
            NEXT y%
          ENDIF
        NEXT x%
      ENDIF
      bestmove.s=minimax
      MoveStruct{}=bestmove{}
      ENDPROC
