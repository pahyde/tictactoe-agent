board = [
    [' ',' ',' '],
    [' ',' ',' '],
    [' ',' ',' ']
]

def print_board(b):
    print()
    for i,row in enumerate(b):
        print(' ', end='')
        print((' | ').join(row), end='')
        print(' ')
        if i < 2:
            print('-----------')
    print()



def run_game():
    
    print('Pick one. X\'s or O\'s: ', end='')
    if input().lower() == 'x': moves, i = ['x','o'], 0
    else:                      moves, i = ['o','x'], 1
    
    winner = None
    while winner == None:
        if i % 2 == 0:  user_move(moves[0])
        else:          agent_move(moves[1],i)
        winner = get_winner_status(board)
        i += 1

    if winner != 'tie': print(winner, 'wins!')
    else:               print('tie game!')

def user_move(c):
    print('User turn: use b,m,t (bottom,middle,top) and l,m,r (left,middle,right) to specify move..')
    idx = {'b':2,'m':1,'t':0,'l':0,'r':2}
    i,j = [idx[p] for p in list(input())]
    board[i][j] = c
    print_board(board)

def agent_move(c,idx):
    if c == 'x' and idx == 1:
       board[0][0] = c
       print_board(board) 
       return
    max_win_prob = -100
    i,j = 0,0
    for row in range(3):
        for col in range(3):
            if board[row][col] == ' ':
                score, games = win_prob(row,col,c,board,c)
                w = score / games
                print(row,col, w)
                if w > max_win_prob:
                    max_win_prob = w
                    i,j = row, col
    board[i][j] = c
    print_board(board)

def win_prob(row,col,c,b,agent):
    
    state = [r[:] for r in b[:]]
    state[row][col] = c
    winner = get_winner_status(state)

    if winner != None:
        if winner == agent:   outcome = 1
        elif winner == 'tie': outcome = 0
        else:                 outcome = -1
        return (outcome, 1)
    
    score, games = 0, 0
    
    #game winning moves
    for i in range(3):
        for j in range(3):
            if state[i][j] == ' ':
                potent = [r[:] for r in state[:]]
                opponent = 'x' if c == 'o' else 'o'
                potent[i][j] = opponent
                if get_winner_status(potent) == opponent:
                    ds, dg = win_prob(i,j,'x' if c == 'o' else 'o',state,agent)
                    score += ds
                    games += dg
                    return score, games

    #defensive moves
    for i in range(3):
        for j in range(3):
            if state[i][j] == ' ':
                potent = [r[:] for r in state[:]]
                potent[i][j] = c
                if get_winner_status(potent) == c:
                    ds, dg = win_prob(i,j,'x' if c == 'o' else 'o',state,agent)
                    score += ds
                    games += dg
                    return score, games

    for i in range(3):
        for j in range(3):
            if state[i][j] == ' ':
                ds, dg = win_prob(i,j,'x' if c == 'o' else 'o',state,agent)
                score += ds
                games += dg
    return (score, games)



def get_winner_status(board):
    for i in range(3):
        if board[i][0] != ' ' and all(board[i][j+1] == board[i][0] for j in range(2)):
            return board[i][0]
        if board[0][i] != ' ' and all(board[j+1][i] == board[0][i] for j in range(2)):
            return board[0][i]
    if board[0][0] != ' ' and board[0][0] == board[1][1] and board[0][0] == board[2][2]:
        return board[0][0]
    if board[2][0] != ' ' and board[2][0] == board[1][1] and board[2][0] == board[0][2]:
        return board[2][0]
    return 'tie' if all(board[i][j] != ' ' for i in range(3) for j in range(3)) else None

run_game()







