# December 7, 2022

from graphics import *
import time
from random import randint as rnd

WIN_RESOLUTION = (1280, 800)

BOARD_DIMENSIONS = (1024, 730)

'''
The Board, Disk, and Button classes for all the graphics elements.

The Board class creates the board and has logic for detecting mouse clicks
and drawing the disks on the board.
'''

class Board:
    def __init__(self, window, disk_radius):
        self.window = window
        self.radius = disk_radius
        
        self.disks = {}
        self.slot_buffer = 10
        self.board = 0
        
    def create_slot_points(self):
        starting_point = (WIN_RESOLUTION[0] - BOARD_DIMENSIONS[0], WIN_RESOLUTION[1] - BOARD_DIMENSIONS[1])
        
        current_column = starting_point[0] + self.slot_buffer + self.radius
        
        # Loops over all of the columns on the board
        for i in range(7):
            row_coord = starting_point[1] + self.slot_buffer + self.radius
            
            # Loops over all of the rows in each column
            for k in range(6):
                '''
                For each disk center point on the board, a new Disk object is created and stored in a dictionary
                with a key that is the board coordinates. The first number in the key tuple is the column and the 
                second is the row number.For example: self.disks[(1, 1)] would reference the disk in the top
                left corner of the board. 
                '''
                self.disks[(i + 1, k + 1)] = Disk([current_column, row_coord], "white", self.radius, self.window)
                
                row_coord += self.slot_buffer + self.radius*2
            
            current_column += self.slot_buffer + self.radius*2
        
        
        # Remove these later. These are just to print all the points for debugging.
        print(self.disks)
            
        return self.disks
        
    def create(self):
        starting_point = (WIN_RESOLUTION[0] - BOARD_DIMENSIONS[0], WIN_RESOLUTION[1] - BOARD_DIMENSIONS[1])
    
        # Drawing the bg of the board.
        board_p1 = Point(starting_point[0], starting_point[1])
        board_p2 = Point(BOARD_DIMENSIONS[0], BOARD_DIMENSIONS[1])
        
        self.board = Rectangle(board_p1, board_p2)
        
        self.board.setWidth(5)
        self.board.setOutline("black")
        self.board.setFill(color_rgb(66, 142, 255))
        
        self.board.draw(self.window)
        
        self.create_slot_points()
        
        # Drawing all the empty slots using the point dictionary
        for key in self.disks.keys():
            self.disks[key].update_color("white")
            
            # Delete later
            print(self.disks[key])  

        return

    # Destroys the board
    def destroy(self):
        self.board.undraw()
        for key in self.disks.keys():
            self.disks[key].destroy()
        return
    
    def lowest_disk(self, column):
        disk_dict = self.disks
        lowest_point = 0
        
        # Loops over all the rows in the column to find which is the lowest disk without a color.
        for i in range(1, 7):
            
            if disk_dict[(column, i)].get_color() != "white":
                lowest_point = (column, i - 1)
                break
            
            elif i == 6:
                lowest_point = (column, 6)
            
        return lowest_point
    
    def dropping_animation(self, color, lowest_disk):
        # Loops over all the rows before the lowest disk in the column.
        for i in range(1, lowest_disk[1]):
            # Sets the disk to the target color, waits 0.125 seconds, and then sets the color back to white.
            self.disks[(lowest_disk[0], i)].update_color(color)
            time.sleep(0.125)
            self.disks[(lowest_disk[0], i)].update_color("white")

        # Finally, sets the color of the lowest disk to the target color.
        self.disks[lowest_disk].update_color(color)
            
        return
    
    def is_full_column(self, column):
        disk_count = 0
        
        for i in range(1, 7):
            if column != 0 and self.disks[(column, i)].get_color() != "white":
                disk_count += 1
        
        if disk_count == 6 or column == 0:
            return True
        else:
            return False
        
    def is_full_board(self):
        full_columns = 0
        for i in range(1, 8):
            if self.is_full_column(i):
                full_columns += 1
        
        if full_columns == 7:
            return True
        else:
            return False
            
    
    def check_row(self, position, color):
        current_column = 1
        color_streak = 0
        
        while current_column <= 7:
            if(position != 0 and self.disks[(current_column, position)].get_color() == color):
                 color_streak += 1
                 if color_streak == 4:
                     return color_streak
            else:
                if color_streak > 0:
                    color_streak = 0
                 
            current_column += 1
            
        return color_streak
    
    def check_column(self, position, color):
        current_row = 1
        color_streak = 0
        
        while current_row <= 6:
            if(position != 0 and self.disks[(position, current_row)].get_color() == color):
                 color_streak += 1
                 if color_streak == 4:
                     return color_streak
            else:
                if color_streak > 0:
                    color_streak = 0
                 
            current_row += 1
            
        return color_streak
    
    def check_forward_diagonal(self, color):
        for current_row in range(1, 4):
            for current_column in range(1, 5):
                if((self.disks[(current_column, current_row)].get_color() == color) and (self.disks[(current_column + 1, current_row + 1)].get_color() == color)):
                    if((self.disks[(current_column + 2, current_row + 2)].get_color() == color) and (self.disks[(current_column + 3, current_row + 3)].get_color() == color)):
                       return True
        return False
    
    def check_backwards_diagonal(self, color):
        for current_row in range(6, 3, -1):
            for current_column in range(1, 5):
                if((self.disks[(current_column, current_row)].get_color() == color) and (self.disks[(current_column + 1, current_row - 1)].get_color() == color)):
                    if((self.disks[(current_column + 2, current_row - 2)].get_color() == color) and (self.disks[(current_column + 3, current_row - 3)].get_color() == color)):
                       return True
        return False
    
    def get_column_from_mouse(self, mouse_x, mouse_y):
        # Calculates the step size to use later on in the loop
        column_step_size = self.radius*2 + self.slot_buffer
        column_count = 1
        
        disk_to_change = ()
        
        # Loops over all the columns
        for i in range(WIN_RESOLUTION[0] - BOARD_DIMENSIONS[0], BOARD_DIMENSIONS[0], column_step_size):
            # Detects which column the mouse is in and whether the board was actually clicked.
            if mouse_x < (i + column_step_size) and mouse_x > i and column_count <= 7:
                if mouse_y < BOARD_DIMENSIONS[1] and mouse_y > (WIN_RESOLUTION[1] - BOARD_DIMENSIONS[1]):
                    # Finds the lowest point in the column that doesn't have a colored disk.
                    disk_to_change = self.lowest_disk(column_count)
                    break
            
            column_count += 1
            
        return disk_to_change
    
    def clicked(self, mouse_point, color):
        mouse_x = mouse_point.getX()
        mouse_y = mouse_point.getY()
        
        disk_to_change = self.get_column_from_mouse(mouse_x, mouse_y)
        
        # If the disk_to_change point is a valid point for the dictionary, it draws the new disk at the lowest point in the column.
        if len(disk_to_change) > 0 and disk_to_change[1] > 0:
            #self.disks[disk_to_change].update_color(color)
            self.dropping_animation(color, disk_to_change)
            print(self.disks[disk_to_change])
            
        game_won = False
        
        if self.check_row(disk_to_change[1], color) == 4:
            game_won = True
        elif self.check_column(disk_to_change[0], color) == 4:
            game_won = True
        elif self.check_backwards_diagonal(color):
            game_won = True
        elif self.check_forward_diagonal(color):
            game_won = True
        elif self.is_full_board():
            game_won = "Draw"
        
        return game_won
    
    def draw_with_coord(self, column):
        disk_to_change = self.lowest_disk(column)
        game_won = False
        
        self.dropping_animation("yellow", disk_to_change)
        
        if self.check_row(disk_to_change[1], "yellow") == 4:
            game_won = True
        elif self.check_column(disk_to_change[0], "yellow") == 4:
            game_won = True
        elif self.check_backwards_diagonal("yellow"):
            game_won = True
        elif self.check_forward_diagonal("yellow"):
            game_won = True
        elif self.is_full_board():
            game_won = "Draw"
        
        return game_won
    
    def was_clicked(self, mouse_point):
        mouse_x = mouse_point.getX()
        mouse_y = mouse_point.getY()
        
        clicked = False
        
        if mouse_x < BOARD_DIMENSIONS[0] and mouse_x > WIN_RESOLUTION[0] - BOARD_DIMENSIONS[0]:
            if mouse_y < BOARD_DIMENSIONS[1] and mouse_y > WIN_RESOLUTION[1] - BOARD_DIMENSIONS[1]:
                clicked = True
        
        return clicked

# Every disk on the board uses this class. The position and color of each disk can be retrieved and the color 
# can be updated by referencing the methods in this class.
class Disk:
    def __init__(self, position, color, radius, window):
        self.position = position
        self.color = color
        self.radius = radius
        self.window = window
        
        self.pos_point = Point(position[0], position[1])
        self.disk = 0
        
    def __str__(self):
        str_var = "Disk(" + str(self.position) + ", \"" + self.color + "\", " + str(self.radius) + ", window)"
        return str_var
        
    # Updates the color attribute and draws the disk on the board.
    def update_color(self, color):
        if(self.disk != 0):
            self.destroy()

        self.color = color
        self.disk = Circle(self.pos_point, self.radius)
        
        self.disk.setFill(color)
        self.disk.setWidth(2)
        
        self.disk.draw(self.window)
        return

    # Destroys the disk
    def destroy(self):
        self.disk.undraw()
        return
    
    # Functions to retrieve certain attributes that might be useful
    def get_position(self):
        pos = self.position
        return pos
    
    def get_pos_point(self):
        pos_point = self.pos_point
        return pos_point
    
    def get_color(self):
        color = self.color
        return color
    
# Creating the buttons for use in the UI such as in the menus or win screens.
class Button:
    def __init__(self, btn_position, btn_width, btn_height, btn_bg_color, btn_text, btn_text_size, btn_text_color, window):
        self.position = btn_position
        self.width = btn_width
        self.height = btn_height
        self.bg_color = btn_bg_color
        self.text = btn_text
        self.text_size = btn_text_size
        self.text_color = btn_text_color
        self.window = window
        
        self.center_point = Point(btn_position[0], btn_position[1])
        self.border = 0
        self.btn_text = 0
    
    def create(self):
        self.border = Rectangle(Point(self.position[0] - self.width//2, self.position[1] - self.height//2), Point(self.position[0] + self.width//2, self.position[1] + self.height//2))
        
        self.border.setFill(self.bg_color)
        self.border.setWidth(2)
        
        self.btn_text = Text(self.center_point, self.text)
        
        self.btn_text.setSize(self.text_size)
        self.btn_text.setFace("arial")
        self.btn_text.setSize(self.text_size)
        self.btn_text.setTextColor(self.text_color)
        
        self.border.draw(self.window)
        self.btn_text.draw(self.window)
        
        return   

    def destroy(self):
        self.border.undraw()
        self.btn_text.undraw()
        return
    
    def clicked(self, click_pos):
        clicked = False
        
        mouse = click_pos
        mouse_x = mouse.getX()
        mouse_y = mouse.getY()
        
        # If the point that was clicked is inside the boundaries of the button, the method returns true, otherwise false
        if mouse_x < (self.position[0] + self.width//2) and mouse_x > (self.position[0] - self.width//2):
            if mouse_y < (self.position[1] + self.height//2) and mouse_y > (self.position[1] - self.height//2):
                clicked = True
        
        return clicked
    
'''
All the normal functions for running the game.
'''
    
def create_window():
    win = GraphWin("Connect 4", WIN_RESOLUTION[0], WIN_RESOLUTION[1])
    return win

# Random moves with some intelligence
def calculate_move(board, blocked_moves):
    column = [rnd(1, 7), False]
    will_win = False
    
    while board.is_full_column(column[0]):
        column = [rnd(1,7), False]
        
    # Checks columns to see if there is a column where the computer placed 3 disks. If it has, it will make the winning move
    for i in range(1, 8):
        current_column = board.check_column(i, "yellow")
        
        if current_column == 3 and not board.is_full_column(i):
            column = [i, False]
            will_win = True
            print("will win")
    
    # Checks each column to see if the player has stacked at least 2 disks
    for i in range(1, 8):
        current_column = board.check_column(i, "red")
        
        # 70% chance the computer will block a move if the player has stacked more than 2 disks 
        if current_column >= 2 and i not in blocked_moves and not board.is_full_column(i) and not will_win:
            if rnd(1, 10) < 7:
                column = [i, True]
                print("blocking player")
    
    return column

def normal_mode(window):
    game_over = False
    board_clickable = True
    player_turn = "red"
    
    # Creating UI elements
    quit_btn = Button([60, 35], 80, 40, "gray", "Quit", 14, "white", window)
    quit_btn.create()
    
    board = Board(window, 49)
    board.create()
    
    # Creating win condition announcements
    red_win_txt = Text(Point(WIN_RESOLUTION[0]//2, (WIN_RESOLUTION[1] - BOARD_DIMENSIONS[1])//2), "Red Wins!")
    red_win_txt.setFace("courier")
    red_win_txt.setSize(36)
    
    yellow_win_txt = Text(Point(WIN_RESOLUTION[0]//2, (WIN_RESOLUTION[1] - BOARD_DIMENSIONS[1])//2), "Yellow Wins!")
    yellow_win_txt.setFace("courier")
    yellow_win_txt.setSize(36)
    
    draw_txt = Text(Point(WIN_RESOLUTION[0]//2, (WIN_RESOLUTION[1] - BOARD_DIMENSIONS[1])//2), "It's a Draw!")
    draw_txt.setFace("courier")
    draw_txt.setSize(36)
    
    # Player turn box
    turn_box_border = Rectangle(Point((WIN_RESOLUTION[0]//2 - 200), WIN_RESOLUTION[1] - 60), Point((WIN_RESOLUTION[0]//2 + 200), WIN_RESOLUTION[1] - 10))
    turn_box_border.setWidth(3)
    
    turn_box_border.setFill("red")
    turn_box_border.draw(window)
    
    turn_text = Text(Point(WIN_RESOLUTION[0]//2, WIN_RESOLUTION[1] - 35), "Red's Turn")
    turn_text.setFace("courier")
    turn_text.setSize(34)
    turn_text.setTextColor("white")
    turn_text.draw(window)
    
    # Main game loop
    while game_over == False:
        # Captures point that the mouse clicked
        mouse = window.getMouse()
        
        # If it determines the board was clicked and the board is clickable, it runs through placing a disk
        if board.was_clicked(mouse) and board_clickable:
            # Checks if the column that the player just clicked is full. If not, it goes along with the move.
            if((len(board.get_column_from_mouse(mouse.getX(), mouse.getY())) != 0) and not board.is_full_column(board.get_column_from_mouse(mouse.getX(), mouse.getY())[0])):
                # If the player turn is red, it places a red disk in the column clicked, otherwise, it places a yellow disk
                if player_turn == "red":
                    game_won = board.clicked(mouse, player_turn)
                    
                    # If red won the game, it displays the "Red Wins!" text
                    if game_won == True:
                        red_win_txt.draw(window)
                        
                        board_clickable = False
                    # If the game is a draw, it displays the draw text
                    elif game_won == "Draw":
                        draw_txt.draw(window)
                        
                        board_clickable = False
                    # Otherwise, it makes makes the player turn yellow     
                    else:
                        player_turn = "yellow"
                        
                        turn_text.undraw()
                        turn_text.setText("Yellow's Turn")
                        turn_text.setSize(30)
                        turn_text.setTextColor("black")
                        
                        turn_box_border.undraw()
                        turn_box_border.setFill("yellow")
                        
                        turn_box_border.draw(window)            
                        turn_text.draw(window)
                        
                # Same as red's turn, but with a yellow disk
                else:
                    game_won = board.clicked(mouse, player_turn)
                    
                    if game_won == True:
                        yellow_win_txt.draw(window)
                        
                        board_clickable = False
                    elif game_won == "Draw":
                        draw_txt.draw(window)
                        
                        board_clickable = False
                    else:
                        player_turn = "red"
                        
                        turn_text.undraw()
                        turn_text.setText("Red's Turn")
                        turn_text.setTextColor("white")
                        
                        turn_box_border.undraw()
                        turn_box_border.setFill("red")
                        
                        turn_box_border.draw(window)            
                        turn_text.draw(window) 
        
        # If the quit button is clicked, all the UI elements are destroyed and the game goes back to the main menu
        elif quit_btn.clicked(mouse):
            game_over = True
            board.destroy()
            quit_btn.destroy()
            
            yellow_win_txt.undraw()
            red_win_txt.undraw()
            draw_txt.undraw()
            turn_box_border.undraw()
            turn_text.undraw()
            
            main_menu(window)
    return

def computer_mode(window):
    game_over = False
    game_won = False
    board_clickable = True
    quit_clickable = False
    turn = "player"
    blocked_moves = []
    
    # Creating all UI elements
    quit_btn = Button([60, 35], 80, 40, "gray", "Quit", 14, "white", window)
    quit_btn.create()
    
    board = Board(window, 49)
    board.create()
    
    # Creating win condition announcements
    red_win_txt = Text(Point(WIN_RESOLUTION[0]//2, (WIN_RESOLUTION[1] - BOARD_DIMENSIONS[1])//2), "Red Wins!")
    red_win_txt.setFace("courier")
    red_win_txt.setSize(36)
    
    yellow_win_txt = Text(Point(WIN_RESOLUTION[0]//2, (WIN_RESOLUTION[1] - BOARD_DIMENSIONS[1])//2), "Yellow Wins!")
    yellow_win_txt.setFace("courier")
    yellow_win_txt.setSize(36)
    
    draw_txt = Text(Point(WIN_RESOLUTION[0]//2, (WIN_RESOLUTION[1] - BOARD_DIMENSIONS[1])//2), "It's a Draw!")
    draw_txt.setFace("courier")
    draw_txt.setSize(36)    
    
    # Player turn box
    turn_box_border = Rectangle(Point((WIN_RESOLUTION[0]//2 - 200), WIN_RESOLUTION[1] - 60), Point((WIN_RESOLUTION[0]//2 + 200), WIN_RESOLUTION[1] - 10))
    turn_box_border.setWidth(3)
    
    turn_box_border.setFill("red")
    turn_box_border.draw(window)
    
    turn_text = Text(Point(WIN_RESOLUTION[0]//2, WIN_RESOLUTION[1] - 35), "Player's Turn")
    turn_text.setFace("courier")
    turn_text.setSize(34)
    turn_text.setTextColor("white")
    turn_text.draw(window)
    
    # Main game loop
    while game_over == False:
        
        # If it's the computer's turn, the computer places a disk
        if turn == "computer" and game_won == False:                        
            # waits one second
            time.sleep(1)
            
            # Calculates the computer's move for if it's the computer's turn
            calculated_column = calculate_move(board, blocked_moves)
            
            rand_column = calculated_column[0]
            
            # Appends the blocked move to the blocked moves list so that the computer doesn't to to block that same move later
            if calculated_column[1] == True:
                blocked_moves.append(calculated_column[0])
            
            # Places the computer's disk and checks to see if the game has been won
            game_won = board.draw_with_coord(rand_column)                    
            
            # Draws the win text if the computer won
            if game_won == True:
                yellow_win_txt.draw(window)
                
                board_clickable = False
                quit_clickable = True
            elif game_won == "Draw":
                draw_txt.draw(window)
                
                board_clickable = False
                quit_clickable = True
            else:
                turn = "player"
            
                # Draw's the player turn text
                turn_text.undraw()
                turn_text.setText("Player's Turn")
                turn_text.setTextColor("white")
                
                turn_box_border.undraw()
                turn_box_border.setFill("red")
                
                turn_box_border.draw(window)            
                turn_text.draw(window)  
                
        elif turn == "player" or quit_clickable:
            # Gets the position that the mouse clicked
            mouse = window.getMouse()   
           
            # If it's determined the board was clicked and the board is clickable, it runs through placing a disk
            if board.was_clicked(mouse) and board_clickable:
                # Checks to see if the column that was just clicked is full. If not, it goes along with the move
                if((len(board.get_column_from_mouse(mouse.getX(), mouse.getY())) != 0) and not board.is_full_column(board.get_column_from_mouse(mouse.getX(), mouse.getY())[0])):
                    # It places the players disk and checks if the game has been won through the clicked method
                    game_won = board.clicked(mouse, "red")
                                        
                    # If the game has been won, it draws the win text
                    if game_won == True:
                        red_win_txt.draw(window)
                        
                        board_clickable = False
                        quit_clickable = True
                    elif game_won == "Draw":
                        draw_txt.draw(window)
                        
                        board_clickable = False
                        quit_clickable = True
                    else:
                        # Draws the turn text
                        turn_text.undraw()
                        turn_text.setText("Computer's Turn")
                        turn_text.setSize(30)
                        turn_text.setTextColor("black")
                        
                        turn_box_border.undraw()
                        turn_box_border.setFill("yellow")
                        
                        turn_box_border.draw(window)            
                        turn_text.draw(window)   
                        turn = "computer"
            
            # Goes back to the main menu if the quit button is clicked     
            elif quit_btn.clicked(mouse):
                game_over = True
                board.destroy()
                quit_btn.destroy()
                
                yellow_win_txt.undraw()
                red_win_txt.undraw()
                turn_box_border.undraw()
                turn_text.undraw()
                
                main_menu(window)
    return

def main_menu(window):
    title_text_point = Point(WIN_RESOLUTION[0]//2, 150)
    btn_clicked = False
    
    # Drawing the title    
    title = Text(title_text_point, "Connect 4")
    title.setFace("courier")
    title.setSize(36)
    
    title.draw(window)
    
    # Creating the game mode buttons
    normal_btn = Button([WIN_RESOLUTION[0]//2, WIN_RESOLUTION[1] - 400], 400, 150, color_rgb(132, 156, 194), "Normal", 26, "white", window)
    comp_btn = Button([WIN_RESOLUTION[0]//2, WIN_RESOLUTION[1] - 200], 400, 150, color_rgb(132, 156, 194), "Computer", 26, "white", window)
    quit_btn = Button([60, 35], 80, 40, "gray", "Quit", 14, "white", window)
    
    normal_btn.create()
    comp_btn.create()
    quit_btn.create()
    
    # Repeatedly checks for mouse clicks until one of the buttons are clicked.
    while btn_clicked == False:
        mouse = window.getMouse()
        
        if normal_btn.clicked(mouse):
            btn_clicked = True
            
            normal_btn.destroy()
            comp_btn.destroy()
            title.undraw()
            
            normal_mode(window)
            
        elif comp_btn.clicked(mouse):
            btn_clicked = True
            
            comp_btn.destroy()
            normal_btn.destroy()
            title.undraw()
            
            # Replace with bot mode later
            computer_mode(window)
            
        elif quit_btn.clicked(mouse):
            btn_clicked = True
            window.close()
        
    return

win = create_window()

main_menu(win)