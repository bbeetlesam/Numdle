# This game is created fully in Python with Pygame module.
# Also, this is my first game project using "real" programming languages (since I've made some games in Fancade within the name "Sams"), so I'm sorry if the code is so messy and unsorted. T_T
# I use some external assets that are free-to-use, so I concern there will be no problems by using them.
# This game still have some things to fix, so stay tune with the updates.

import pygame, random, math, webbrowser, os, sys, pickle

pygame.init()
pygame.mixer.init()

# All variables (inits)
screen_height, screen_width = 800, 1000
row, column = 5, 6
set_digit = column

# Game data (saved in bin file)
game_data = {
   "win": False,
   "lose": False,

   "game_played": 0,
   "winrate": 0,
   "game_won": 0,
   "game_lost": 0,
   "winstreak": 0,

   "gamehard_played": 0,
   "gamehard_won": 0,
   "gamehard_lost": 0,
   "winratehard": 0,

   "answer_num": None,
   "input_list": [None] * row,
   "gridcheck_list": [[-1] * column for _ in range(row)],
   "numbercheck_list": [[-1] * 5 for _ in range(2)],
   "guess_count": 0,

   "answers": [], # (answer, last guess, guess count, hardmode)
   "guess_dis": [0]*5,

   "hard-mode": False,
   "dark-mode": True,
   "keyboard-mode": True,
}

# Data file's name
datafile: str = "data.bin"

# Load game data (if not exist, then make the file)
try:
   with open(datafile, 'rb') as gamedata:
      game_data = pickle.load(gamedata)
except:
   with open(datafile, 'wb') as gamedata:
      pickle.dump(game_data, gamedata)

scene = 1 # start from Menu scene
frame = 0 # for debugging
is_fullscreen = False

game_loop = True
checking = False
open_howto = open_stat = open_set = open_windowAny = False
win, lose = game_data["win"], game_data["lose"]

input_num = ""
input_list = game_data["input_list"] #list that contains all the previous guessed number
gridcheck_list = game_data["gridcheck_list"] #row*column list that represents the status of each grid that has been filled (-1defaultcolor 0lgrey 1green 2yellow)
numbercheck_list = game_data["numbercheck_list"] #5*2 list that represents the status of the number (0-9)
guess_count = game_data["guess_count"]

credit_linkTap = []
number_tap = [False]*10

# Color variables (RGB)
WINDOW: tuple[int] = (27, 27, 27)
GREY: tuple[int] = (18, 18, 19)
LGREY: tuple[int] = (58, 58, 60)
L2GREY: tuple[int] = (86, 87, 88)
L3GREY: tuple[int] = (129, 131, 132)
GREEN: tuple[int] = (83, 141, 78)
YELLOW: tuple[int] = (181, 159, 59)
WHITE: tuple[int] = (248, 248, 248)

size_playx, size_playy = 300, 100
size_quitx, size_quity = 300, 100
addhow = addback = addstat = adddel = addetr = addrest = addset = 0
id = 0
tapArrU = tapArrD = False
tap_hard = tap_theme = tap_keyboard = False

# Take external assets from temp directory
def resource_path(relative_path):
   if hasattr(sys, '_MEIPASS'):
      return os.path.join(sys._MEIPASS, relative_path)
   return os.path.join(os.path.abspath("."), relative_path)

# Set the fonts
def bungee_font(size):
   return pygame.font.Font(resource_path(os.path.join("assets", "font", "Bungee-Regular.ttf")), size)
def jetbrains_font(size):
   return pygame.font.Font(resource_path(os.path.join("assets", "font", "JetBrainsMono-ExtraBold.ttf")), size)

# Sfx dictionary
sfx = {
   "click": pygame.mixer.Sound(resource_path(os.path.join("assets", "sfx", "clicked.wav"))),
   "flip": pygame.mixer.Sound(resource_path(os.path.join("assets", "sfx", "enter-flipped.wav"))),
   "denied": pygame.mixer.Sound(resource_path(os.path.join("assets", "sfx", "denied.wav"))),
   "correct": pygame.mixer.Sound(resource_path(os.path.join("assets", "sfx", "correct.wav"))),
   "incorrect": pygame.mixer.Sound(resource_path(os.path.join("assets", "sfx", "incorrect.wav"))),
   "restart": pygame.mixer.Sound(resource_path(os.path.join("assets", "sfx", "restart.wav")))
}

# Img dictionary
img = {
   "game-icon": pygame.image.load(resource_path(os.path.join("assets", "img", "512px-Wordle_Logo.svg.png"))),
   "info-full": pygame.image.load(resource_path(os.path.join("assets", "img", "info_80dp_F8F8F8_FILL1_wght700_GRAD200_opsz40.png"))),
   "info-hollow": pygame.image.load(resource_path(os.path.join("assets", "img", "info_80dp_F8F8F8_FILL0_wght700_GRAD200_opsz40.png"))),
   "arrow-up": pygame.image.load(resource_path(os.path.join("assets", "img", "arrow_upward_70dp_F8F8F8_FILL0_wght700_GRAD200_opsz24.png"))),
   "arrow-down": pygame.image.load(resource_path(os.path.join("assets", "img", "arrow_downward_70dp_F8F8F8_FILL0_wght700_GRAD200_opsz24.png"))),
   "backspace": pygame.image.load(resource_path(os.path.join("assets", "img", "backspace_80dp_F8F8F8_FILL0_wght700_GRAD0_opsz48.png"))),
   "enter": pygame.image.load(resource_path(os.path.join("assets", "img", "subdirectory_arrow_left_80dp_F8F8F8_FILL0_wght700_GRAD0_opsz48.png"))),
   "back": pygame.image.load(resource_path(os.path.join("assets", "img", "home_80dp_121313_FILL1_wght700_GRAD-25_opsz48.png"))),
   "statistic": pygame.image.load(resource_path(os.path.join("assets", "img", "leaderboard_80dp_121313_FILL1_wght700_GRAD200_opsz48.png"))),
   "restart": pygame.image.load(resource_path(os.path.join("assets", "img", "fiber_new_80dp_121313_FILL1_wght700_GRAD200_opsz48.png"))),
   "arrowp": pygame.image.load(resource_path(os.path.join("assets", "img", "keyboard_arrow_up_40dp_F8F8F8_FILL0_wght700_GRAD200_opsz24.png"))),
   "arrowd": pygame.image.load(resource_path(os.path.join("assets", "img", "keyboard_arrow_down_40dp_F8F8F8_FILL0_wght700_GRAD200_opsz24.png"))),
   "setting": pygame.image.load(resource_path(os.path.join("assets", "img", "settings_80dp_121313_FILL1_wght700_GRAD200_opsz48.png"))),
   "turn-on": pygame.image.load(resource_path(os.path.join("assets", "img", "toggle_on_40dp_538D4E_FILL1_wght700_GRAD200_opsz24.png"))),
   "turn-off": pygame.image.load(resource_path(os.path.join("assets", "img", "toggle_off_40dp_878A8C_FILL1_wght700_GRAD200_opsz24.png"))),

   "statistic_white": pygame.image.load(resource_path(os.path.join("assets", "img", "leaderboard_80dp_F8F8F8_FILL1_wght700_GRAD200_opsz48.png"))),
   "back_white": pygame.image.load(resource_path(os.path.join("assets", "img", "home_80dp_F8F8F8_FILL1_wght700_GRAD200_opsz48.png"))),
   "setting_white": pygame.image.load(resource_path(os.path.join("assets", "img", "settings_80dp_F8F8F8_FILL1_wght700_GRAD200_opsz48.png"))),
   "restart_white": pygame.image.load(resource_path(os.path.join("assets", "img", "fiber_new_80dp_F8F8F8_FILL1_wght700_GRAD200_opsz48.png"))),

   "arrowp-black": pygame.image.load(resource_path(os.path.join("assets", "img", "keyboard_arrow_up_40dp_121313_FILL1_wght700_GRAD200_opsz24.png"))),
   "arrowd-black": pygame.image.load(resource_path(os.path.join("assets", "img", "keyboard_arrow_down_40dp_121313_FILL1_wght700_GRAD200_opsz24.png"))),

   "info-full-black": pygame.image.load(resource_path(os.path.join("assets", "img", "info_80dp_121313_FILL1_wght700_GRAD200_opsz40.png"))),
   "info-hollow-black": pygame.image.load(resource_path(os.path.join("assets", "img", "info_80dp_121313_FILL0_wght700_GRAD200_opsz40.png")))
}

infof_img = pygame.transform.smoothscale(img["info-full"], (35,35))
infoh_img = pygame.transform.smoothscale(img["info-hollow"], (35,35))
backspace_img = pygame.transform.smoothscale(img["backspace"], (65,65))
enter_img = pygame.transform.smoothscale(img["enter"], (65,65))
back_img = pygame.transform.smoothscale(img["back"], (75,75))
stat_img = pygame.transform.smoothscale(img["statistic"], (65,65))
restart_img = pygame.transform.smoothscale(img["restart"], (65,65))
setting_img = pygame.transform.smoothscale(img["setting"], (70,70))

credit_font3 = bungee_font(50)
credit_font3.set_underline(True)
info_font = bungee_font(60)

# Tuples
misc_words = ("Instagram", "Youtube", "Repository", "Thanks for playing!", "[ESC] to back",  "Luckiest", "Genius", "Clever", "Great", "Phew", "Oh No",  "?",
              "- Each guess must be a 6-digit number.", "- Each guess cannot start with 0.", "- Tiles' color will show how close your guess was to the answer.", "Examples",
              "1 is in the number and in the correct spot.", "3 is not in the number in any spot.", "5 is in the number but in the wrong spot.",
              "Upward arrow tells that the correct number in that spot is > 5.", "Statistics",
              "Played", "Won", "Lost", "Win Distribution", "Game History", "Winrate", "Succeed", "Failed", "Winstreak")
credit_links = ("https://www.instagram.com/jstsams?igsh=dGRtdnBkejZleDEy",
                "https://www.youtube.com/@rilsams",
                "https://github.com/bbeetlesam/Numdle")

# Set the main window called Numdle and the window's icon
screen = pygame.display.set_mode((screen_width, screen_height), pygame.SCALED | pygame.RESIZABLE)
pygame.display.set_caption("Numdle")
pygame.display.set_icon(img["game-icon"])

clock = pygame.time.Clock()
mouse_clicked = pygame.mouse.get_pressed()

# Toggle fullscreen
def toggle_fullscreen():
   global is_fullscreen, screen
   if is_fullscreen:
      screen = pygame.display.set_mode((1000, 800), pygame.RESIZABLE)
      is_fullscreen = False
   else:
      screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
      is_fullscreen = True

# Make data.txt read-only (Windows)
# def set_read_only_Win(filename):
#    if os.name == 'nt':
#       os.system(f'attrib +r {filename}')

# Un-read-only to change data (Windows)
# def remove_read_only_Win(filename):
#    if os.name == 'nt':
#       os.system(f'attrib -r {filename}')

# All scenes in a class
class Scene_Controller():
   def image(img, x, y, size, center=True) -> object:
      image = pygame.transform.smoothscale(img, (size, size))
      if center:
         imagepos = image.get_rect(center=(x, y))
      else:
         imagepos = (x, y)
      screen.blit(image, imagepos)
      return image
   def rect(x, y, width, height) -> bool:
      rect = pygame.Rect(0, 0, width, height)
      rect.center = (x, y)
      return rect.collidepoint(mouse_pos)
   def point(x, y, color=WHITE):
      pygame.draw.circle(screen, color, (x ,y), 5)
   def message_center(word, color, x, y, func):
      message = screen.blit(func.render(word, True, color), func.render(word, True, color).get_rect(center = (x, y)))
   def message_midleft(word, color, x, y, func, outer=False, color_outer=WHITE, alignx=0, aligny=0):
      if outer:
         pygame.draw.rect(screen, color_outer, (x-alignx/2+0.5, y-(func.render(word, True, color_outer).get_height()+aligny)/2, func.render(word, True, color_outer).get_width()+alignx, func.render(word, True, color_outer).get_height()+aligny), border_radius=1)
      message = screen.blit(func.render(word, True, color), func.render(word, True, color).get_rect(midleft = (x, y)))
   def animate_move(start, end):
      frame0 = 0

      dx, dy = start[0] - end[0], start[1] - end[1]
      dis = math.sqrt(dx**2 + dy**2)
      dx /= dis
      dy /= dis

      frame0 += 1
   def end_message():
      if win:
         message = misc_words[guess_count+5-1]
      elif lose:
         message = answer_num
      else:
         message = None

      # Print the end messages 500
      word = bungee_font(45).render(message, True, (GREY if dark_theme else WHITE) if not hard_mode else (255, 0, 0))
      rect = word.get_rect(center=(screen_width/2, screen_height/6))
      x, y = rect.x, rect.y
      pygame.draw.rect(screen, WHITE if dark_theme else GREY, (x-15/2, y-3, word.get_width()+15, word.get_height()+6), border_radius=3)
      screen.blit(word, rect)
   def credit():
      # Draw circles (as a decor bg)
      pygame.draw.circle(screen, LGREY, (screen_width/2, 0), screen_width/2)
      pygame.draw.circle(screen, LGREY, (screen_width/2, screen_height), screen_width/2)

      credit = bungee_font(130).render("ABOUT", True, WHITE)
      credit_rect = credit.get_rect(center = (screen_width/2, screen_height/2-80-160))

      screen.blit(credit, credit_rect)

      credit2_rect = None
      link_tapped = [False] * 3
      for index, word in enumerate(misc_words[0:5]):
         if index >= 3:
            spacing = index*60 + 115
         else:
            spacing = index*80

         # Render and blit for normal words
         credit2 = bungee_font(50).render(word, True, WHITE)
         credit2_rect = credit2.get_rect(center = (screen_width/2, screen_height/2-80+spacing))
         screen.blit(credit2, credit2_rect)

         # Render for underlined words
         credit3 = credit_font3.render(word, True, WHITE)
         credit3_rect = credit3.get_rect(center = (screen_width/2, screen_height/2-80+spacing))

         if index < 3:
            link_tapped[index] = credit2_rect.collidepoint(mouse_pos)

            if link_tapped[index]:
               screen.blit(credit3, credit3_rect)

      return link_tapped
   def menu():
      global size_playx, size_playy, size_quitx, size_quity

      # Title
      scenes.message_center("NUMDLE", numdle_color, screen_width / 2, screen_height / 2 - 170, bungee_font(150))
      pygame.draw.line(screen, numdle_color, (screen_width/2-350, screen_height/2-170-70), (screen_width/2+350, screen_height/2-170-70), width=10)
      pygame.draw.line(screen, numdle_color, (screen_width/2-350, screen_height/2-170+70), (screen_width/2+350, screen_height/2-170+70), width=10)

      # Create Play and Quit buttons
      button_play = pygame.draw.rect(screen, button_color, (screen_width/2-size_playx/2, screen_height/2+30-size_playy/2, size_playx, size_playy), border_radius=10)
      button_quit = pygame.draw.rect(screen, button_color, (screen_width/2-size_quitx/2, screen_height/2+200-size_quity/2, size_quitx, size_quity), border_radius=10)

      # Put the words on the surface
      scenes.message_center("Play", text_color, screen_width / 2, screen_height / 2 + 30, bungee_font(80))
      scenes.message_center("Quit", text_color, screen_width / 2, screen_height / 2 + 200, bungee_font(80))

      # Interactions with the buttons
      if button_play.collidepoint(mouse_pos):
         size_playx = 325
         size_playy = 125
      else:
         size_playx = 300
         size_playy = 100

      if button_quit.collidepoint(mouse_pos):
         size_quitx = 325
         size_quity = 125
      else:
         size_quitx = 300
         size_quity = 100

      # Hover in Credit (About)
      infof_rect = infof_img.get_rect(topleft=(3,3))
      if infof_rect.collidepoint(mouse_pos):
         screen.blit(infof_img, (3, 3)) if dark_theme else scenes.image(img["info-full-black"], 3+35/2, 3+35/2, 35)
      else:
         screen.blit(infoh_img, (3, 3))  if dark_theme else scenes.image(img["info-hollow-black"], 3+35/2, 3+35/2, 35)

      return button_play.collidepoint(mouse_pos), button_quit.collidepoint(mouse_pos), infof_rect.collidepoint(mouse_pos)
   def play():
      global open_windowAny, number_tap
      block_size = 100
      block_disx, block_disy = 8, 8
      anchor_x, anchor_y = screen_width/2-100-50, screen_height/2-100-8
      num_size = 60

      open_windowAny = open_howto or open_stat or open_set

      # Create grids
      for i in range(row):
         if not row%2 == 0:
            pos_y = anchor_y-(block_size/2)-((block_size+block_disy)*int(row/2))+i*(block_size+block_disy)
         else:
            pos_y = anchor_y-(block_size/2)+(block_size/2+block_disy/2)-((block_size+block_disy)*(row/2))+i*(block_size+block_disy)

         for a, status in enumerate(gridcheck_list[i]):
            if not column%2 == 0:
               pos_x = anchor_x-(block_size/2)-((block_size+block_disx)*int(column/2))+a*(block_size+block_disx)
            else:
               pos_x = anchor_x-(block_size/2)+(block_size/2+block_disx/2)-((block_size+block_disx)*(column/2))+a*(block_size+block_disx)

            # Coloring the inner block
            color_inner = color_list[status+1]

            # Default outer blocks' color
            if status == -1:
               color_outer = (LGREY if dark_theme else L3GREY) if not hard_mode else ((255, 100, 100) if not dark_theme else (255, 130, 130))

            # Coloring the outer block
            if i == guess_count: # Only on the current row
               if a < len(input_num):
                  color_outer = L2GREY if not hard_mode else ((255, 0, 0) if not dark_theme else (255, 90, 90))
            elif i < guess_count:
               color_outer = color_list[status+1]
            else: # Other than the current rrow
               color_outer = (LGREY if dark_theme else L3GREY) if not hard_mode else ((255, 100, 100) if not dark_theme else (255, 130, 130))

            pygame.draw.rect(screen, color_outer, (pos_x, pos_y, block_size, block_size), border_radius=2) # Outer blocks
            pygame.draw.rect(screen, color_inner, (pos_x+4, pos_y+4, block_size-8, block_size-8), border_radius=2) # Inner blocks

      # Create number buttons in below
      for i in range(2):
         for a, status in enumerate(numbercheck_list[i]):
            # Blocks' color
            match status:
               case -1: color = L3GREY
               case 0: color = LGREY
               case 1: color = GREEN
               case 2: color = YELLOW

            # Number buttons
            num_button = (pygame.draw.rect(screen, color, ((screen_width/2-50)-108*2+108*a, ((anchor_y-266+block_size*5+block_disy*4)+(screen_height-(anchor_y-266+block_size*5+block_disy*4))/2-(block_size+block_disy/2))+108*i, block_size, block_size), border_radius=15))

            if not (game_ends and guess_count == column):
               number_tap[a+i*5] = num_button.collidepoint(mouse_pos)

               if num_button.collidepoint(mouse_pos):
                  if len(input_num) < column and not (len(input_num) == 0 and number_tap[0] == True) and not game_ends and not open_windowAny:
                     num_size = 70
               else:
                  num_size = 60

            # Button numbers
            num_text = jetbrains_font(num_size).render(str(a+i*5), True, WHITE)
            num_rect = num_text.get_rect(center = ((screen_width/2)-108*2+108*a, ((anchor_y-266+block_size*5+block_disy*4)+(screen_height-(anchor_y-266+block_size*5+block_disy*4))/2-(block_size+block_disy/2))+54+108*i-5))

            screen.blit(num_text, num_rect)

      # Create other buttons (and the fonts)
      global addhow, addback, addstat, adddel, addetr, addrest, addset
      button_how = pygame.draw.rect(screen, button_color, ((anchor_x+320+330/2-100)-15-addhow/2, anchor_y-266-addhow/2, block_size+addhow, block_size+addhow), border_radius=2)
      button_back = pygame.draw.rect(screen, button_color, (anchor_x+320+330/2+15-addback/2, anchor_y-266-addback/2, block_size+addback, block_size+addback), border_radius=2)
      button_stat = pygame.draw.rect(screen, button_color, ((anchor_x+320+330/2-100)-15-addstat/2, anchor_y-266-addstat/2+130, block_size+addstat, block_size+addstat), border_radius=2)

      if not game_ends:
         restart_color = L2GREY
      else:
         restart_color = WHITE if dark_theme else GREY

      button_restart = pygame.draw.rect(screen, restart_color, ((anchor_x+320+330/2-100)-15-addrest/2, anchor_y-266-addrest/2+260, block_size+addrest, block_size+addrest), border_radius=2)

      button_delete = pygame.draw.rect(screen, L3GREY, (screen_width/2-50+324-adddel/2, ((anchor_y-266+block_size*5+block_disy*4)+(screen_height-(anchor_y-266+block_size*5+block_disy*4))/2-(block_size+block_disy/2))-adddel/2, block_size+adddel, block_size+adddel), border_radius=15)
      button_enter = pygame.draw.rect(screen, L3GREY, (screen_width/2-50-324-addetr/2, ((anchor_y-266+block_size*5+block_disy*4)+(screen_height-(anchor_y-266+block_size*5+block_disy*4))/2-(block_size+block_disy/2))-addetr/2, block_size+addetr, block_size+addetr), border_radius=15)

      # Settings
      button_set = pygame.draw.rect(screen, button_color, ((anchor_x + 320 + 330 / 2 + 15) - addset / 2, anchor_y - 266 - addset / 2 + 130, block_size + addset, block_size + addset), border_radius=2)

      if dark_theme:
         scenes.image(img["setting"], anchor_x + 320 + 330 / 2 + 15 + 50 - 70 / 2, anchor_y - 266 + 50 - 70 / 2 + 130, 70, False)
      else:
         scenes.image(img["setting_white"], anchor_x + 320 + 330 / 2 + 15 + 50 - 70 / 2, anchor_y - 266 + 50 - 70 / 2 + 130, 70, False)

      if not open_windowAny:
         if button_how.collidepoint(mouse_pos): addhow = 10
         else: addhow = 0
         if button_back.collidepoint(mouse_pos): addback = 10
         else: addback = 0
         if button_stat.collidepoint(mouse_pos): addstat = 10
         else: addstat = 0
         if button_delete.collidepoint(mouse_pos) and not len(input_num) == 0: adddel = 10
         else: adddel = 0
         if button_enter.collidepoint(mouse_pos) and len(input_num) == column: addetr = 10
         else: addetr = 0
         if button_set.collidepoint(mouse_pos): addset = 10
         else: addset = 0
         if game_ends and button_restart.collidepoint(mouse_pos): addrest = 10
         else: addrest = 0
      else:
         addhow = addback = addstat = adddel = addetr = addrest = addset = 0

      # ? symbol
      scenes.message_center(misc_words[11], text_color, anchor_x+320+330/2-50-15, anchor_y-266+50, bungee_font(70))

      # Other button symbols
      screen.blit(backspace_img, (screen_width/2-65/2+324, ((anchor_y-266+block_size*5+block_disy*4)+(screen_height-(anchor_y-266+block_size*5+block_disy*4))/2-(block_size+block_disy/2))+65/4))
      screen.blit(enter_img, (screen_width/2-65/2-324, ((anchor_y-266+block_size*5+block_disy*4)+(screen_height-(anchor_y-266+block_size*5+block_disy*4))/2-(block_size+block_disy/2))+65/4))

      if dark_theme:
         screen.blit(back_img, (anchor_x+320+330/2+15+50-75/2, anchor_y-266+50-75/2))
         screen.blit(stat_img, (anchor_x+320+330/2-100-15-65/2+50, anchor_y-266+50-65/2+130))
         screen.blit(restart_img, (anchor_x+320+330/2+15-65-15-65/2, anchor_y-266+50-65/2+260))
      else:
         scenes.image(img["back_white"], anchor_x+320+330/2+15+50-75/2+75/2, anchor_y-266+50-75/2+75/2, 75)
         scenes.image(img["statistic_white"], anchor_x+320+330/2-100-15-65/2+50+ 65/2, anchor_y-266+50-65/2+130 + 65/2, 65)
         scenes.image(img["restart_white"], anchor_x+320+330/2+15-65-15-65/2+65/2, anchor_y-266+50-65/2+260+65/2, 65)

      # Hard-mode color edge (EXPERIMENTAL) red
      # if hard_mode:
      #    pygame.draw.line(screen, (150, 35, 35), (0, 0), (screen_width, 0), width=10)
      #    pygame.draw.line(screen, (150, 35, 35), (0, screen_height), (screen_width, screen_height), width=10)
      #    pygame.draw.line(screen, (150, 35, 35), (0, 0), (0, screen_height), width=10)
      #    pygame.draw.line(screen, (150, 35, 35), (screen_width, 0), (screen_width, screen_height), width=10)

      # #line between back&how
      # pygame.draw.line(screen, GREEN, (anchor_x+320+330/2, 0), (anchor_x+320+330/2, screen_height), width=7) #670+330/2=835
      # #line beside how an back
      # pygame.draw.line(screen, GREEN, (anchor_x+320+330/2-115, 0), (anchor_x+320+330/2-115, screen_height), width=1)
      # pygame.draw.line(screen, GREEN, (anchor_x+320+330/2+15+100, 0), (anchor_x+320+330/2+115, screen_height), width=1)
      # #y-line for anchor of grids
      # pygame.draw.line(screen, GREEN, (0, anchor_y), (screen_width, anchor_y), width=7)
      # #y-line for anchor of number buttons
      # pygame.draw.line(screen, GREEN, (0, screen_height-243+243/2), (screen_width, screen_height-243+243/2), width=7)
      # #grid anchor point
      # pygame.draw.circle(screen, GREEN, (anchor_x, anchor_y), 10)
      # #top and right edge of grid
      # pygame.draw.line(screen, GREEN, (anchor_x+320, 0), (anchor_x+320, screen_height), width=7) #anchor_x = screen_width/2-100-50 = 350
      # pygame.draw.line(screen, GREEN, (0, anchor_y-266), (screen_width, anchor_y-266), width=7) #anchor_y = screen_height/2-100-8 = 292
      # pygame.draw.line(screen, GREEN, (0, anchor_y-266+block_size*5+block_disy*4), (screen_width, anchor_y-266+block_size*5+block_disy*4), width=7) #anchor_y = screen_height/2-100-8 = 292
      # pygame.draw.circle(screen, GREEN, ((screen_width/2-50)-108*2, (screen_height-243+243/2-50+block_size+4)-54), 10)

      # pygame.draw.circle(screen, GREEN, ((screen_width/2-50)-108*2, ((anchor_y-266+block_size*5+block_disy*4)+(screen_height-(anchor_y-266+block_size*5+block_disy*4))/2-(block_size+block_disy/2))), 10)

      return button_how.collidepoint(mouse_pos), button_back.collidepoint(mouse_pos), button_stat.collidepoint(mouse_pos), button_delete.collidepoint(mouse_pos), button_enter.collidepoint(mouse_pos), button_restart.collidepoint(mouse_pos), button_set.collidepoint(mouse_pos)
   def howtoplay():
      # Make an overlay (for blur effect behind window)
      overlay = pygame.Surface((screen_width, screen_height))
      overlay.set_alpha(150)
      overlay.fill(GREY)
      screen.blit(overlay, (0, 0))

      # Make the window
      pygame.draw.rect(screen, L2GREY if dark_theme else WHITE, (screen_width/2-452, screen_height/2-377, 904, 754), border_radius=10)
      pygame.draw.rect(screen, WINDOW if dark_theme else WHITE, (screen_width/2-450, screen_height/2-375, 900, 750), border_radius=10)

      # Print the words
      howtoplay = bungee_font(70).render("how to play", True, WHITE if dark_theme else GREY)
      get_rect = howtoplay.get_rect(center = (screen_width/2, screen_height/2-310))
      esc = bungee_font(30).render(misc_words[4], True, WHITE if dark_theme else GREY)
      esc_rect = esc.get_rect(center = (screen_width/2, screen_height/2+310))

      screen.blit(howtoplay, get_rect)
      screen.blit(esc, esc_rect)

      # All words (aligned to left)
      for i, wrd in enumerate(misc_words[12:15]):
         word = jetbrains_font(20).render(wrd, True, WHITE if dark_theme else GREY)
         word_rect = word.get_rect(midleft = (screen_width/2-435, screen_height/2-240+i*25))

         screen.blit(word, word_rect)

      ex = bungee_font(20).render(misc_words[15], True, WHITE if dark_theme else GREY) #Example
      ex_rect = ex.get_rect(midleft = (screen_width/2-435, screen_height/2-240+2*25+50))
      screen.blit(ex, ex_rect)

      # Make tiles in How To Play + explanations below them
      block_size = 80
      block_disx, block_disy = 6, 45 #15
      anchor_x, anchor_y = screen_width/2-435, screen_height/2-240+2*25+50+20

      arrimg = img["arrow-up"]
      arrimg = pygame.transform.smoothscale(arrimg, (25, 25))

      for i in range(3):
         pos_y = anchor_y + i*(block_size+block_disy)
         for a in range(6):
            pos_x = anchor_x + a*(block_size+block_disx)

            #Create tiles and its color
            if i == 0 and a == 0:
               outer = inner = GREEN
               numbercolor = WHITE
            elif i == 1 and a == 2:
               outer = inner = LGREY
               numbercolor = WHITE
            elif i == 2 and a == 4:
               outer = inner = YELLOW
               numbercolor = WHITE
            else:
               outer = L3GREY if dark_theme else L2GREY
               inner = WINDOW if dark_theme else WHITE
               numbercolor = WHITE if dark_theme else GREY

            pygame.draw.rect(screen, outer, (pos_x, pos_y, block_size, block_size)) #Outer blocks
            pygame.draw.rect(screen, inner, (pos_x+4, pos_y+4, block_size-8, block_size-8)) #Inner blocks

            if i == 2 and a == 4:
               arrimgr = arrimg.get_rect(center=(pos_x+block_size-15, pos_y+15))
               screen.blit(arrimg, arrimgr)

            # Print numbers inside tiles
            scenes.message_center(str(a+1), numbercolor, anchor_x+block_size/2+a*(block_size+block_disx), anchor_y+block_size/2+i*(block_size+block_disy)-2.5, jetbrains_font(45))

         # Print explanations below tiles
         anu = jetbrains_font(20).render(misc_words[i+16], True, WHITE if dark_theme else GREY) #Explanation
         anu_rect = anu.get_rect(midleft = (anchor_x, anchor_y+block_size+block_disy/3+i*(block_disy+block_size)))
         screen.blit(anu, anu_rect)

      # Print add explanation for Yellow
      anu = jetbrains_font(20).render(misc_words[19], True, WHITE if dark_theme else GREY) #Last explanation (yellow tile)
      anu_rect = anu.get_rect(midleft = (anchor_x, anchor_y+block_size+2*(block_disy+block_size)+block_disy/3*2.5))
      screen.blit(anu, anu_rect)
   def statistic():
      global id

      overlay = pygame.Surface((screen_width, screen_height))
      overlay.set_alpha(150)
      overlay.fill(GREY)
      screen.blit(overlay, (0, 0))

      # Make the block
      pygame.draw.rect(screen, L2GREY if dark_theme else WHITE, (screen_width/2-954/2, screen_height/2-377, 954, 754), border_radius=10)
      pygame.draw.rect(screen, WINDOW if dark_theme else WHITE, (screen_width/2-950/2, screen_height/2-375, 950, 750), border_radius=10)

      # Print STATISTICS and ESC TO BACK
      statword = bungee_font(70).render("statistics", True, WHITE if dark_theme else GREY)
      stat_rect = statword.get_rect(center = (screen_width/2, screen_height/2-310))
      esc = bungee_font(30).render(misc_words[4], True, WHITE if dark_theme else GREY)
      esc_rect = esc.get_rect(center = (screen_width/2, screen_height/2+295))

      screen.blit(statword, stat_rect)
      screen.blit(esc, esc_rect)

      # Print words
      word = bungee_font(25).render(misc_words[20], True, WHITE if dark_theme else GREY) #Statistics (small)
      wrect = word.get_rect(midleft = (screen_width/2-950/2+20, screen_height/2-310+80))
      screen.blit(word, wrect)

      for i in range(2): #Guess Distribution & Game History
         scenes.message_midleft(misc_words[i+24], WHITE if dark_theme else GREY, screen_width/2-950/2+20+(950/2-20+20)*i, screen_height/2-155+55+70, bungee_font(25))

      statValue = list(game_data.values())
      for i, data in enumerate(statValue[3:7]): #statistics section
         anu = f"{data}%" if i == 0 else f"{data}"

         played = jetbrains_font(75).render(anu, True, WHITE if dark_theme else GREY) #statistic data
         played_rect = played.get_rect(center=(screen_width/2-450+900/5*(i+1), screen_height/2-155))
         screen.blit(played, played_rect)

         word = jetbrains_font(20).render(misc_words[i+26], True, WHITE if dark_theme else GREY) #indicator
         wrect = word.get_rect(center = (screen_width/2-450+900/5*(i+1), screen_height/2-155+55))
         screen.blit(word, wrect)

      # Guess Distribution data
      for i in range(5):
         word = bungee_font(25).render(f"{i+1}", True, WHITE if dark_theme else GREY) #1-6 number
         wrect = word.get_rect(midleft = (screen_width/2-950/2+20, screen_height/2-155+55+70+45*(i+1)))
         screen.blit(word, wrect)

         length = max(screen_width/2-950/2+20+25+35, screen_width/2-950/2+20+25+410*(game_data["guess_dis"][i]/max(game_data["game_won"], 1))) #100% = 385 px long (now 410 ig)
         pygame.draw.line(screen, LGREY if dark_theme else L3GREY, (screen_width/2-950/2+20+25, screen_height/2-155+55+70+45*(i+1)), (length, screen_height/2-155+55+70+45*(i+1)), width=35)

         scenes.message_center(f"{game_data["guess_dis"][i]}", WHITE, length-35/2, screen_height/2-155+55+70+45*(i+1), bungee_font(25)) #guess distrib data

      # Game History data and tiles
      size, d = 68, 5
      answers = list(game_data["answers"])
      for i, (ans, gss, cnt, hardmode) in enumerate(answers[-1-id:-4-id:-1]):
         for a in range(6):
            if ans == gss:
               color = GREEN
            else:
               if gss[a] == ans[a]:
                  color = GREEN
               elif gss[a] in ans:
                  color = YELLOW
               else:
                  color = LGREY

            pygame.draw.rect(screen, color, (screen_width/2+20+(size+d)*a, screen_height/2-155+55+70+30+73*i, size, size))

            scenes.message_center(gss[a], WHITE, screen_width/2+20+32.5+(size+d)*a, screen_height/2-155+55+70+73*(i)+62.5, jetbrains_font(40))

            if not ans == gss: #show answers for failed guesses
               scenes.message_center(ans[a], WHITE, screen_width/2+20+32.5+(size+d)*a+25, screen_height/2-155+55+70+73*(i)+62.5-20, jetbrains_font(20))

         # Shows the guess history's count (upleft)
         if hardmode:
            scenes.message_midleft(f"{len(answers) - i - id}", WHITE, screen_width / 2 + 20 + 5, screen_height / 2 - 155 + 55 + 70 + 73 * (i) + 62.5 - 22.5, jetbrains_font(10), True, (240, 35, 35), 5, (-1))
         else:
            scenes.message_midleft(f"{len(answers)-i-id}", WHITE, screen_width/2+20+5, screen_height/2-155+55+70+73*(i)+62.5-22.5, jetbrains_font(10))

         # Shows the guess count on Win match (downleft)
         if ans == gss:
            scenes.message_midleft(f"{cnt}", WHITE, screen_width/2+20+5, screen_height/2-155+55+70+73*(i)+62.5-22.5+47.5, jetbrains_font(10))

         # Make Arrow Up and Down
         try:
            if len(game_data["answers"]) > 3:
               if not id == 0: #arrow up
                  if ifArrUp:
                     ifArrUp = scenes.rect(screen_width/2+20+size*6+d*5-15, screen_height/2-155+55+70+30-15, 35, 35)
                     scenes.image(img["arrowp"] if dark_theme else img["arrowp-black"], screen_width/2+20+size*6+d*5-15, screen_height/2-155+55+70+30-18, 65)
                  else:
                     ifArrUp = scenes.rect(screen_width/2+20+size*6+d*5-15, screen_height/2-155+55+70+30-15, 25, 25)
                     scenes.image(img["arrowp"] if dark_theme else img["arrowp-black"], screen_width/2+20+size*6+d*5-15, screen_height/2-155+55+70+30-18, 50)

               if not id == len(game_data["answers"])-3:
                  if ifArrDown: #arrow down
                     ifArrDown = scenes.rect(screen_width/2+20+size*6+d*5-15, screen_height/2-155+55+70+30+size*3+d*2+19, 35, 35)
                     scenes.image(img["arrowd"] if dark_theme else img["arrowd-black"], screen_width/2+20+size*6+d*5-15, screen_height/2-155+55+70+30+size*3+d*2+19, 65)
                  else:
                     ifArrDown = scenes.rect(screen_width/2+20+size*6+d*5-15, screen_height/2-155+55+70+30+size*3+d*2+19, 25, 25)
                     scenes.image(img["arrowd"] if dark_theme else img["arrowd-black"], screen_width/2+20+size*6+d*5-15, screen_height/2-155+55+70+30+size*3+d*2+19, 50)
         except:
            ifArrUp = scenes.rect(screen_width/2+20+size*6+d*5-15, screen_height/2-155+55+70+30-15, 25, 25)
            ifArrDown = scenes.rect(screen_width/2+20+size*6+d*5-15, screen_height/2-155+55+70+30+size*3+d*2+19, 25, 25)

      # pygame.draw.line(screen, GREEN, (screen_width/2, screen_height/2-750/2), (screen_width/2, screen_height/2+750/2), width=3)
      # pygame.draw.circle(screen, GREEN, (screen_width/2+20+size*6+d*5-15, screen_height/2-155+55+70+30+size*3+d*2+19), 5)
      # pygame.draw.line(screen, GREEN, (screen_width/2-450, screen_height/2-155+55+70+30), (screen_width/2+450, screen_height/2-155+55+70+30), width=3)
      # pygame.draw.line(screen, GREEN, (screen_width/2-450, screen_height/2-155+55+70+30+35*5+10*4), (screen_width/2+450, screen_height/2-155+55+70+30+35*5+10*4), width=3)

      try:
         return ifArrUp, ifArrDown
      except:
         return False, False
   def settings():
      # Make an overlay (for blur effect behind window)
      overlay = pygame.Surface((screen_width, screen_height))
      overlay.set_alpha(150)
      overlay.fill(GREY)
      screen.blit(overlay, (0, 0))

      # Make the window
      pygame.draw.rect(screen, L2GREY if dark_theme else WHITE, (screen_width / 2 - 854/2, screen_height / 2 - 604/2, 854, 604), border_radius=10)
      pygame.draw.rect(screen, WINDOW if dark_theme else WHITE, (screen_width / 2 - 850/2, screen_height / 2 - 600/2, 850, 600), border_radius=10)

      # Print the words
      scenes.message_center("settings", WHITE if dark_theme else GREY, screen_width / 2, screen_height / 2-235, bungee_font(70))
      scenes.message_center(misc_words[4], WHITE if dark_theme else GREY, screen_width / 2, screen_height / 2+160+(screen_height/2+600/2-(screen_height/2+160))/2, bungee_font(30))

      # Informations
      scenes.message_midleft("Hard Mode", (240, 35, 35), screen_width / 2-850/2+20, screen_height / 2-125, bungee_font(35))
      scenes.message_midleft("Remove arrow hints on yellow tiles", WHITE if dark_theme else GREY, screen_width / 2-850/2+20, screen_height / 2+27.5-125, jetbrains_font(18))

      pygame.draw.line(screen, WHITE if dark_theme else GREY, (screen_width / 2-850/2+20, screen_height / 2+27.5-125+37.5),(screen_width / 2+850/2-20, screen_height / 2+27.5-125+37.5), width=1)

      scenes.message_midleft("Dark Theme", WHITE if dark_theme else GREY, screen_width / 2 - 850 / 2 + 20, screen_height / 2 - 125+110*1, bungee_font(35))
      scenes.message_midleft("Choose your own preference", WHITE if dark_theme else GREY, screen_width / 2 - 850 / 2 + 20, screen_height / 2 + 27.5 - 125+110*1, jetbrains_font(18))

      pygame.draw.line(screen, WHITE if dark_theme else GREY, (screen_width / 2-850/2+20, screen_height / 2+27.5-125+37.5+110*1),(screen_width / 2+850/2-20, screen_height / 2+27.5-125+37.5+110*1), width=1)

      scenes.message_midleft("Keyboard Input", WHITE if dark_theme else GREY, screen_width / 2 - 850 / 2 + 20, screen_height / 2 - 125 + 110 * 2, bungee_font(35))
      scenes.message_midleft("Allow key input from user's keyboard", WHITE if dark_theme else GREY, screen_width / 2 - 850 / 2 + 20, screen_height / 2 + 27.5 - 125 + 110 * 2, jetbrains_font(18))

      # Toggle indicators
      scenes.image(img["turn-on"], screen_width / 2+850/2-20-70/2, screen_height / 2-110-5, 70) if hard_mode else scenes.image(img["turn-off"], screen_width / 2+850/2-20-70/2, screen_height / 2-110-5, 70)
      scenes.image(img["turn-on"], screen_width / 2+850/2-20-70/2, screen_height / 2-5, 70) if dark_theme else scenes.image(img["turn-off"], screen_width / 2+850/2-20-70/2, screen_height / 2-5, 70)
      scenes.image(img["turn-on"], screen_width / 2+850/2-20-70/2, screen_height / 2+110-5, 70) if keyboard_mode else scenes.image(img["turn-off"], screen_width / 2+850/2-20-70/2, screen_height / 2+110-5, 70)

      hard = scenes.rect(screen_width / 2 + 850 / 2 - 20 - 70 / 2, screen_height / 2 - 110 - 5, 70, 40)
      theme = scenes.rect(screen_width / 2 + 850 / 2 - 20 - 70 / 2, screen_height / 2 - 5, 70, 40)
      keyboard = scenes.rect(screen_width / 2 + 850 / 2 - 20 - 70 / 2, screen_height / 2 - 5+110, 70, 40)

      # pygame.draw.line(screen, GREEN, (screen_width / 2, screen_height / 2 - 600 / 2),(screen_width / 2, screen_height / 2 + 600 / 2), width=3)
      # pygame.draw.line(screen, GREEN, (screen_width / 2-850/2+20, screen_height / 2-170 ),(screen_width / 2+850/2-20, screen_height / 2-170), width=1)
      # pygame.draw.line(screen, GREEN, (screen_width / 2-850/2+20, screen_height / 2+27.5-125+37.5+110*2),(screen_width / 2+850/2-20, screen_height / 2+27.5-125+37.5+110*2), width=1)

      return hard, theme, keyboard

# Set the initial answer
if not game_data["answer_num"] == None:
   answer_num = game_data["answer_num"]
else:
   answer_num = str(random.randint(10**(set_digit-1), 10**(set_digit)))
   game_data["answer_num"] = answer_num

game_restart = False

# Game loop comes here!
while game_loop:
   hard_mode: bool = game_data["hard-mode"]
   dark_theme: bool = game_data["dark-mode"]
   keyboard_mode: bool = game_data["keyboard-mode"]

   # To simplify the coloring code in Play scene
   color_list = [(GREY if dark_theme else WHITE), LGREY, GREEN, YELLOW]

   # Set color for each theme (dark and light)
   if dark_theme:
      bg_color = GREY
      button_color = WHITE
      text_color = GREY
      numdle_color = WHITE
   else:
      bg_color = WHITE
      button_color = GREY
      text_color = WHITE
      numdle_color = GREY

   screen.fill(bg_color)

   # Update the variables based on current window's size
   screen_width, screen_height = pygame.display.get_surface().get_size()

   mouse_pos = pygame.mouse.get_pos()
   keys = pygame.key.get_pressed()
   screen_width, screen_height = screen.get_size()
   scenes = Scene_Controller

   game_ends = win or lose

   # Switch case for each scene
   match scene:
      case 0: #credit
         credit_linkTap = scenes.credit()
      case 1: #mainmenu
         tap_play, tap_quit, tap_credit = scenes.menu()
      case 2: #playing
         tap_how, tap_back, tap_stat, tap_del, tap_enter, tap_restart, tap_setting = scenes.play()

   # Cek kumpulan event (hover cursor, tapped key, clicked mouse, etc)
   for event in pygame.event.get():
      if event.type == pygame.QUIT: #keluar program lewat X
         game_loop = False

      elif event.type == pygame.VIDEORESIZE and not is_fullscreen: #resize window
         screen_width, screen_height = event.size
         screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)

      elif event.type == pygame.KEYUP and keys[pygame.K_F11]: #toggle fullscreen with F11
         toggle_fullscreen()

      # In menu screen
      if scene == 1:
         if tap_play and event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            sfx["click"].play()
            scene = 2
         elif tap_credit and event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            scene = 0
         elif tap_quit and event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            sfx["click"].play()
            pygame.time.delay(int(sfx["click"].get_length()*750)) # delay for 750ms before quitting
            game_loop = False

      # In credit scene
      if scene == 0:
         if keys[pygame.K_ESCAPE] or (event.type == pygame.MOUSEBUTTONUP and event.button == 3):
            scene = 1

         for index, link in enumerate(credit_linkTap):
            if link and event.type == pygame.MOUSEBUTTONUP and event.button == 1:
               credit_linkTap[index] = False
               sfx["click"].play()
               webbrowser.open(credit_links[index])
      else:
         credit_linkTap = [False] * 3

      # In play scene
      if scene == 2:
         if not open_windowAny: # If not shown other window (howtoplay/statistic)
            # Tap How, Back, Stat, Delete, Setting, or NumButtons button
            if tap_how and event.type == pygame.MOUSEBUTTONUP and event.button == 1: #how
               sfx["click"].play()
               open_howto = True
            elif tap_stat and event.type == pygame.MOUSEBUTTONUP and event.button == 1: #stats
               sfx["click"].play()
               open_stat = True
            elif tap_back and event.type == pygame.MOUSEBUTTONUP and event.button == 1: #back
               sfx["click"].play()
               scene = 1
            elif tap_setting and event.type == pygame.MOUSEBUTTONUP and event.button == 1: #setting
               sfx["click"].play()
               open_set = True
            elif tap_del and event.type == pygame.MOUSEBUTTONUP and not len(input_num) == 0 and event.button == 1: #backspace
               sfx["click"].play()
               input_num = input_num[0:-1]
            elif True in number_tap and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not game_ends: #number buttons
               if len(input_num) < column and not (len(input_num) == 0 and number_tap.index(True) == 0):
                  input_num += str(number_tap.index(True))
                  sfx["click"].play()

            if not game_ends:
               # Insert/delete the number
               if event.type == pygame.KEYDOWN and keyboard_mode:
                  if (event.unicode).isdigit() and len(input_num) < column and not (len(input_num) == 0 and event.unicode == '0'):
                     input_num += event.unicode

               if event.type == pygame.KEYUP and keyboard_mode:
                  if keys[pygame.K_BACKSPACE]:
                     input_num = input_num[0:-1]

               # ENTER submitted number only if digit is 6 (Keyboard or Ingame button)
               if len(input_num) == column and keys[pygame.K_RETURN] and keyboard_mode or (tap_enter and event.type == pygame.MOUSEBUTTONUP and len(input_num) == column and event.button == 1):
                  # Insert the guessed numbers to a list
                  input_list[guess_count] = input_num

                  input_num = ""
                  guess_count += 1
                  checking = True

                  sfx["flip"].play()
            else:
               # If click Restart/New
               if tap_restart and event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                  game_restart = True

         else: # In other window
            if open_howto:
               if keys[pygame.K_ESCAPE] or (event.type == pygame.MOUSEBUTTONUP and event.button == 3):
                  open_howto = False
            elif open_stat:
               if keys[pygame.K_ESCAPE] or (event.type == pygame.MOUSEBUTTONUP and event.button == 3):
                  open_stat = False
            elif open_set: # Save settings when exit setting
               if keys[pygame.K_ESCAPE] or (event.type == pygame.MOUSEBUTTONUP and event.button == 3):
                  #remove_read_only_Win(datafile)

                  with open(datafile, 'r+b') as savegame:
                     savegame.truncate(0)
                     pickle.dump(game_data, savegame)

                  #set_read_only_Win(datafile)
                  open_set = False
      else:
         tap_how = tap_back = tap_stat = tap_del = tap_enter = tap_restart = tap_setting = False

      # In Statistic scene
      if open_stat:
         if tapArrU and event.type == pygame.MOUSEBUTTONUP and event.button == 1 and not id == 0:
            sfx["flip"].play()
            id -= 1
         if tapArrD and event.type == pygame.MOUSEBUTTONUP and event.button == 1 and not id == len(game_data["answers"])-3:
            sfx["flip"].play()
            id += 1

      # In Settings scene
      if open_set:
         if tap_hard and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and guess_count == 0:
            sfx["restart"].play()
            game_data["hard-mode"] = not game_data["hard-mode"]
         if tap_theme and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            sfx["flip"].play()
            game_data["dark-mode"] = not game_data["dark-mode"]
         if tap_keyboard and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            sfx["flip"].play()
            game_data["keyboard-mode"] = not game_data["keyboard-mode"]

   # Checking current submitted guess
   if checking:
      correct = 0
      for index, num in enumerate(input_list[guess_count-1]):
         if num == answer_num[index]:
            gridcheck_list[guess_count-1][index] = 1
            correct += 1
            numbercheck_list[int(int(num)/5)][int(num)-int(int(num)/5)*5] = 1
         elif num in answer_num:
            gridcheck_list[guess_count-1][index] = 2
            if not numbercheck_list[int(int(num)/5)][int(num)-int(int(num)/5)*5] == 1:
               numbercheck_list[int(int(num)/5)][int(num)-int(int(num)/5)*5] = 2
         else:
            gridcheck_list[guess_count-1][index] = 0
            if not numbercheck_list[int(int(num)/5)][int(num)-int(int(num)/5)*5] == 1:
               numbercheck_list[int(int(num)/5)][int(num)-int(int(num)/5)*5] = 0

      # If all correct, then Win
      if correct == set_digit:
         sfx["correct"].play()
         win = True
         game_data["win"] = win
      else:
         if guess_count == row:
            sfx["incorrect"].play()
            lose = True
            game_data["lose"] = lose
         correct = 0

      game_data["answer_num"] = answer_num
      game_data["gridcheck_list"] = gridcheck_list
      game_data["numbercheck_list"] = numbercheck_list
      game_data["guess_count"] = guess_count

      # remove_read_only_Win(datafile)

      with open(datafile, 'r+b') as savegame:
         savegame.truncate(0)
         pickle.dump(game_data, savegame)

      # set_read_only_Win(datafile)

      checking = False

   # In Play scene
   if scene == 2:
      # Print current input numbers
      x_dif = 0
      for char in input_num:
         num_text = jetbrains_font(60).render(char, True, button_color)
         num_rect = num_text.get_rect(center = (screen_width/2-432+108-100+4 + x_dif, screen_height/2-324+ guess_count*108))

         screen.blit(num_text, num_rect)
         x_dif += num_text.get_width() + 72

      # Print all the previous guessed numbers on grids
      for index in range(guess_count):
         x_dif = 0
         for i, char in enumerate(input_list[index]):
            num_text = jetbrains_font(60).render(char, True, WHITE)
            num_rect = num_text.get_rect(center = (screen_width/2-432+108-100+4 + x_dif, screen_height/2-324+ index*108))

            screen.blit(num_text, num_rect)
            x_dif += num_text.get_width() + 72

            # If Yellow, gives arrow indicator (if the correct answer is higher/lower)
            if gridcheck_list[index][i] == 2 and not hard_mode:
               if int(char) > int(answer_num[i]):
                  arrow_img = img["arrow-down"]
               else:
                  arrow_img = img["arrow-up"]

               arrow_img = pygame.transform.smoothscale(arrow_img, (25,25))
               arrow_rect = arrow_img.get_rect(center=(screen_width/2-432+108-100+4+108*i+35, screen_height/2-324+ index*108-35))

               screen.blit(arrow_img, arrow_rect)

      # If game ends
      if game_ends:
         scenes.end_message()

         # If Restart game (reset variables)
         if game_restart:
            sfx["restart"].play()

            game_data["answers"].append((answer_num, input_list[guess_count-1], guess_count, hard_mode)) # Append answer and last guess to data

            if win:
               game_data["game_won"] += 1
               game_data["guess_dis"][guess_count-1] += 1
               game_data["winstreak"] += 1
            elif lose:
               game_data["game_lost"] += 1
               game_data["winstreak"] = 0

            game_restart = game_ends = win = lose = False

            game_data["game_played"] = game_data["game_won"]+game_data["game_lost"]
            game_data["winrate"] = int(game_data["game_won"]/game_data["game_played"]*100)

            answer_num = str(random.randint(10**(set_digit-1), 10**(set_digit)))
            gridcheck_list = [[-1] * column for _ in range(row)]
            numbercheck_list = [[-1] * 5 for _ in range(2)]
            input_list = [None] * row
            guess_count = 0

            game_data["answer_num"] = answer_num
            game_data["input_list"] = input_list
            game_data["gridcheck_list"] = gridcheck_list
            game_data["numbercheck_list"] = numbercheck_list
            game_data["guess_count"] = guess_count
            game_data["answer_num"] = answer_num
            game_data["win"] = win
            game_data["lose"] = lose
            game_data["hard-mode"] = False

            # remove_read_only_Win(datafile)

            with open(datafile, 'r+b') as savegame:
               savegame.truncate(0)
               pickle.dump(game_data, savegame)

            # set_read_only_Win(datafile)

      # Open Howtoplay window
      if open_howto:
         scenes.howtoplay()

      # Open Statistic window
      if open_stat:
         tapArrU, tapArrD = scenes.statistic()
      else:
         tapArrU = tapArrD = False

      # Open Settings window
      if open_set:
         tap_hard, tap_theme, tap_keyboard = scenes.settings()

   frame += 1
   print(len((game_data["answers"])), game_data["answer_num"], guess_count, dark_theme)

   pygame.display.flip()

   # Set the FPS
   clock.tick(60)

pygame.quit()

# WIP:
# - Set the animation for end-message
