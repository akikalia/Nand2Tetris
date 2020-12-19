// The game of life world consists of 2D grid 16x32, the grid is mapped in memory:
// RAM[100] == grid(0, 0)
// RAM[132] == grid(1, 0)
// RAM[611] == grid(16, 31)
//
// RAM[99] contains number of generations to iterate over the Game of life world (aka grid)
//
// Iteration rules:
// For a space that is 'populated':
// * Each cell with one or no neighbors dies, as if by solitude.
// * Each cell with four or more neighbors dies, as if by overpopulation.
// * Each cell with two or three neighbors survives.
//
// For a space that is 'empty' or 'unpopulated'
// * Each cell with three neighbors becomes populated.
//
// initial values are set by test. The are only two values allowed:
// 1 -- the cell is populated
// 0 -- the cell is empty

(MAIN)
    @99
    D=M
    @gens
    M=D
    @100
    D=A
    @grid
    M=D
    @612
    D=A
    @backup
    M=D
    @32
    D=A
    @width
    M=D
    @16
    D=A
    @height
    M=D
    @cube_size
    M=D
    @512
    D=A
    @board_width
    M=D
    @GENERATIONS
    0;JMP


(UNFILL)
    @addr_cube_cur
    D=M
    A=D
    M=0
    @DRAW_CUBE_LOOP
    0;JMP   
(FILL)
    @addr_cube_cur
    D=M
    A=D
    M=-1
    @DRAW_CUBE_LOOP
    0;JMP
    
(DRAW_LINE)
    @fill
    D=M
    @FILL
    D;JGT
    @UNFILL
    0;JMP

(DRAW_CUBE_LOOP)
    @width
    D=M
    @addr_cube_cur
    M=D+M
    
    //until y equals height draw line
    @cube_y
    D=M+1
    M=D
    @cube_size
    D=M-D
    @DRAW_LINE
    D;JGT
    @DRAW_BOARD_X
    0;JMP

(DRAW_CUBE)
    @cube_y
    M=0
    M=M-1

    @addr_grid_cur
    D=M
    @board_x
    D=D+M
    A=D
    D=M
    @fill
    M=D

    @addr_board_cur
    D=M
    @width
    D=D-M
    @board_x
    D=D+M
    @addr_cube_cur
    M=D

    @DRAW_CUBE_LOOP
    0;JMP

(DRAW_BOARD_X)
    @board_x
    M=M+1
    D=M
    @width
    D=M-D

    @DRAW_CUBE
    D;JGT
    @DRAW_BOARD_LOOP
    0;JMP

(DRAW_BOARD_LOOP)
    @width
    D=M
    @addr_grid_cur
    M=D+M

    @512
    D=A
    @addr_board_cur
    M=M+D
    
    @board_x
    M=0
    M=M-1
    //until y equals height draw line
    @board_y
    M=M+1
    D=M
    @height
    D=M-D
    @DRAW_BOARD_X
    D;JGT
    @GENERATIONS
    0;JMP

(DRAW_BOARD)
    //y=-1
    @board_y
    M=0
    M=M-1

    //addr_board_cur = screen - 1 line
    @SCREEN
    D=A
    @512
    D=D-A
    @addr_board_cur
    M=D

    //addr_grid = grid - 1 line
    @grid
    D=M
    @width
    D=D-M
    @addr_grid_cur
    M=D

    @DRAW_BOARD_LOOP
    0;JMP






(COPY_CELL)
    @gridoffs
    M=M-1
    @offset
    M=M-1
    @backupoffs
    M=M-1

    //check memory
    @offset
    D=M
    @DRAW_BOARD
    D;JLT
    
    @backupoffs
    //copy backup to original
    A=M
    D=M
    @gridoffs
    A=M
    M=D
    
    @COPY_CELL
    0;JMP

(COPY_ARR)
    //initialize backupoffs and gridoffs
    @offset
    D=M
    @gridoffs
    M=D
    @backupoffs
    M=D
    @grid
    D=M
    @gridoffs
    M=M+D
    @backup
    D=M
    @backupoffs
    M=M+D
    
    @COPY_CELL
    0;JMP

















//maybe grid and backup switch locations each time to make it faster
(GENERATIONS)
    @gens
    M=M-1
    D=M
    
    @MUTATE
    D;JGE
    @END
    0;JMP

(MUTATE)
    @y
    M=0
    M=M-1 // y = -1
    @offset
    M=0 // offset = 0
    @LOOP_Y
    0;JMP
    
(LOOP_Y)
    //x = -1
    @x
    M=0
    M=M-1
    @offset
    M=M-1
    //y++
    @y
    M=M+1
    D=M
    @height
    D=M-D
    @COPY_ARR
    D;JLE
    //if (y < height) LOOP_WIDTH
    @LOOP_X
    0;JMP

(LOOP_X)
    @offset
    M=M+1

    //x++
    @x
    M=M+1
    D=M
    @width
    D=M-D
    //if (x >= 0) CHECK
    @CHECK
    D;JGT
    @LOOP_Y
    0;JMP

(CHECK)
    //y_minus = y-2
    @y
    D=M
    @y_minus
    M=D-1
    M=M-1

    //y_nbrs = 3
    @3
    D=A
    @y_nbrs
    M=D

    @total_nbrs
    M=0

    @offset
    D=M    
    @width
    D=D-M
    D=D-M
    @nbr_offs
    M=D+1
    M=M+1
    @Y_NEIGHBORS
    0;JMP

(Y_NEIGHBORS)
    @width
    D=M
    @nbr_offs
    M=M+D
    @y_nbrs
    M=M-1
    D=M
    //if all neighbors checked populate
    @POPULATE
    D;JLT
    @y_minus
    M=M+1
    @x
    D=M
    @x_minus
    M=D-1
    M=M-1
    @3
    D=A
    @x_nbrs
    M=D
    @nbr_offs
    M=M-D
    M=M-1
    @X_NEIGHBORS
    0;JMP

(X_NEIGHBORS)
    @nbr_offs
    M=M+1
    @x_nbrs
    M=M-1
    D=M
    //if all neighbors checked in this line, check next line
    @Y_NEIGHBORS
    D;JLT
    @x_minus
    M=M+1
    @CHECK_NEIGHBOR
    0;JMP

(CHECK_NEIGHBOR)
    //check x y axis boundry
    @y_minus
    D=M
    @X_NEIGHBORS
    D;JLT
    @height
    D=M-D
    @X_NEIGHBORS
    D;JLE
    @x_minus
    D=M
    @X_NEIGHBORS
    D;JLT
    @width
    D=M-D
    @X_NEIGHBORS
    D;JLE
    //add neighbor to total_nbrs
    @grid
    D=M
    @nbr_offs
    D=D+M
    A=D
    D=M
    @total_nbrs
    M=M+D
    @X_NEIGHBORS
    0;JMP

(POPULATE)
//if (grid + offset) POPULATED else EMPTY 
    @offset
    D=M
    @grid
    D=D+M
    A=D
    D=M
    @POPULATED
    D;JGT
    @EMPTY
    0;JMP

(EMPTY)
    @total_nbrs
    D=M
    @3
    D=D-A
    @SET_ZERO
    D;JNE
    @SET_ONE
    0;JMP

(POPULATED)
//if not-empty self was included as a neighbor
    @total_nbrs
    M=M-1
    D=M
    @2
    D=D-A
    //if total_nbrs == 2 or 3 set populated/ else empty
    @SET_ONE
    D;JEQ
    D=D-1
    @SET_ONE
    D;JEQ
    @SET_ZERO
    0;JMP

(SET_ONE)
    @backup
    D=M
    @offset
    D=D+M
    A=D
    M=1
    @LOOP_X
    0;JMP
(SET_ZERO)
    @backup
    D=M
    @offset
    D=D+M
    A=D
    M=0
    @LOOP_X
    0;JMP

(END)
    @END
    0;JMP