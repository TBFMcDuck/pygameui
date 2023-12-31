import pygame

pygame.init()


VERSION = 1.12

class text():
    def __init__(self, position: tuple, content:str, color:tuple, **extra ):
        # Extras are addition arguments the user can input to further customize the text
        # The values in the array underneath are the values used if the user does not specify them
        self.e = {"font": "freesansbold.ttf", "fontSize": 20, "centerMode": True}
        for key in extra:
            if key in self.e:
                self.e[key] = extra[key]
            else: # Sends an error if the function has been passed a non recognizable argument
                extras_keys = []
                for extraKey in self.e:
                    extras_keys.append(extraKey)
                error = f"Argument error: Argument '{key}' not recognized. The extra arguments available are: {extras_keys}"
                raise Exception(error)
        # Pos
        self.x, self.y = position
        # Show
        self.show = True
        # Text
        self.font = pygame.font.SysFont(self.e["font"], self.e["fontSize"])  # Load font
        self.text = self.font.render(content, True, color) # Create surface object
        self.textRect = self.text.get_rect() # Get rect
        # centerMode
        self.textRect.topleft = (self.x - (self.textRect.width // 2), self.y - (self.textRect.height // 2)) if self.e["centerMode"] else (self.x, self.y)
        # Flowing
        self.flowing = False
        self.currentFlowPos = None
        self.otherFlowPos = None
        self.Xstep = 0
        self.Ystep = 0
        # Jumping
        self.jumping = False
        self.currentJumpPos = None
        self.otherJumpPos = None
        self.frames = 0
        self.frames_counter = 0
    
    def change_content(self, newContent, color):
        self.text = self.font.render(newContent, True, color) # Create surface object
        self.textRect = self.text.get_rect() # Get rect
        # centerMode
        self.textRect.topleft = (self.x - (self.textRect.width // 2), self.y - (self.textRect.height // 2)) if self.e["centerMode"] else (self.x, self.y)

    # Draws text on screen
    def draw(self, win):
        if self.show:
            win.blit(self.text, self.textRect)
    
    # Updates and moves the text if needed
    def update(self):
        if self.flowing: # If flowing
            # Check if flow has reached a flowpoint
            if self.e["centerMode"]: # If centermode is activated we will use the rects centerposition, if not the topleft
                if (self.Xstep == 0 or self.Ystep == 0):
                    if ((self.Xstep > 0) and (self.textRect.centerx > self.currentFlowPos[0])) or ((self.Xstep < 0) and (self.textRect.centerx < self.currentFlowPos[0])) or ((self.Ystep < 0) and (self.textRect.centery < self.currentFlowPos[1])) or ((self.Ystep > 0) and (self.textRect.centery > self.currentFlowPos[1])):
                        self.Xstep, self.Ystep = -self.Xstep, -self.Ystep # Switch direction
                        self.currentFlowPos, self.otherFlowPos = self.otherFlowPos, self.currentFlowPos
                else:
                    if (((self.Xstep > 0) and (self.textRect.centerx > self.currentFlowPos[0])) and ((self.Ystep > 0) and (self.textRect.centery > self.currentFlowPos[1]))) or (((self.Xstep > 0) and (self.textRect.centerx > self.currentFlowPos[0])) and ((self.Ystep < 0) and (self.textRect.centery < self.currentFlowPos[1]))) or (((self.Xstep < 0) and (self.textRect.centerx < self.currentFlowPos[0])) and ((self.Ystep > 0) and (self.textRect.centery > self.currentFlowPos[1])))or (((self.Xstep < 0) and (self.textRect.centerx < self.currentFlowPos[0])) and ((self.Ystep < 0) and (self.textRect.centery < self.currentFlowPos[1]))):
                        self.Xstep, self.Ystep = -self.Xstep, -self.Ystep # Switch direction
                        self.currentFlowPos, self.otherFlowPos = self.otherFlowPos, self.currentFlowPos
            else:
                if (self.Xstep == 0 or self.Ystep == 0):
                    if ((self.Xstep > 0) and (self.textRect.x > self.currentFlowPos[0])) or ((self.Xstep < 0) and (self.textRect.x < self.currentFlowPos[0])) or ((self.Ystep < 0) and (self.textRect.y < self.currentFlowPos[1])) or ((self.Ystep > 0) and (self.textRect.y > self.currentFlowPos[1])):
                        self.Xstep, self.Ystep = -self.Xstep, -self.Ystep # Switch direction
                        self.currentFlowPos, self.otherFlowPos = self.otherFlowPos, self.currentFlowPos
                else:
                    if (((self.Xstep > 0) and (self.textRect.x > self.currentFlowPos[0])) and ((self.Ystep > 0) and (self.textRect.y > self.currentFlowPos[1]))) or (((self.Xstep > 0) and (self.textRect.x > self.currentFlowPos[0])) and ((self.Ystep < 0) and (self.textRect.y < self.currentFlowPos[1]))) or (((self.Xstep < 0) and (self.textRect.x < self.currentFlowPos[0])) and ((self.Ystep > 0) and (self.textRect.y > self.currentFlowPos[1])))or (((self.Xstep < 0) and (self.textRect.x < self.currentFlowPos[0])) and ((self.Ystep < 0) and (self.textRect.y < self.currentFlowPos[1]))):
                        self.Xstep, self.Ystep = -self.Xstep, -self.Ystep # Switch direction
                        self.currentFlowPos, self.otherFlowPos = self.otherFlowPos, self.currentFlowPos

            self.move(self.Xstep, self.Ystep) # Apply movement
        
        elif self.jumping: # If jumping
            self.frames_counter += 1 # Increase frame counter
            if self.frames_counter >= self.frames: # If it has gone enough time to switch position
                self.move_to(self.otherJumpPos[0], self.otherJumpPos[1]) # Apply movement
                self.currentJumpPos, self.otherJumpPos = self.otherJumpPos, self.currentJumpPos
                self.frames_counter = 0 # Reset counter

    # Moves to specific cordinates
    def move_to(self, x: int, y: int):
        if self.e["centerMode"]:
            self.x = x - (self.textRect.width // 2)
            self.y = y - (self.textRect.height // 2)
            self.textRect.topleft = (self.x, self.y)
        else:
            self.x, self.y = x, y
            self.textRect.topleft = (self.x, self.y)
    
    # Moves in x and y direction
    def move(self, xMovement: float, yMovement: float):
        # Used to make small movements posible (self.x is a float, self.textRect.x is an int)
        self.x += xMovement
        self.y += yMovement
        self.textRect.x = self.x
        self.textRect.y = self.y

    def is_hovered(self):
        # Get mouse pos
        mouse_pos = pygame.mouse.get_pos()

        # Check mouse over and clicked conditions
        if self.textRect.collidepoint(mouse_pos):
            return True 

    # Flow lets the text flow between two points
    def flow(self, position1: tuple, position2: tuple, iterations: int):
        # Move to flowpoint
        self.move_to(position1[0], position1[1])
        # Set flowpostions
        self.otherFlowPos, self.currentFlowPos = position1, position2 
        # Get amount to move per iteration
        Xdistance, Ydistance = (position2[0] - position1[0]), (position2[1] - position1[1])
        self.Xstep = Xdistance / iterations
        self.Ystep = Ydistance / iterations
        # Activate flowing
        self.flowing = True
    
    # Jump lets the user toggle the text between two points on a userSpecified timer
    def jump(self, position1: tuple, position2: tuple, frames: int):
        # Move to jumppoint
        self.move_to(position1[0], position1[1])
        # Set jumpPostions
        self.otherJumpPos, self.currentJumpPos = position2, position1
        # Frames
        self.frames = frames
        # Activate jumping
        self.jumping = True

class element():
    def __init__(self, position: tuple, **extra ):
        # Extras are addition arguments the user can input to further customize the text
        # The values in the array underneath are the values used if the user does not specify them
        self.e = {"font": "freesansbold.ttf", "fontSize": 50, "content": None, "textColor": (231, 111, 81), "rectWidth": 200, "rectHeight": 75, "rectColor": (233, 196, 106), "rectBorderRadius": 10, "centerMode": True, "centerText": True}
        for key in extra:
            if key in self.e:
                self.e[key] = extra[key]
            else: # Sends an error if the function has been passed a non recognizable argument
                extras_keys = []
                for extraKey in self.e:
                    extras_keys.append(extraKey)
                error = f"Argument error: Argument '{key}' not recognized. The extra arguments available are: {extras_keys}"
                raise Exception(error)
        
        if isinstance(self.e["content"], str):
            # Pos
            self.x, self.y = (position[0] - (self.e["rectWidth"] // 2), position[1] - (self.e["rectHeight"] // 2)) if self.e["centerMode"] else (position[0], position[1])
            # Rect
            self.rect = pygame.rect.Rect(self.x, self.y, self.e["rectWidth"], self.e["rectHeight"])
            self.rectColor = self.e["rectColor"]
            self.borderRadius = self.e["rectBorderRadius"]
            # Text
            self.font = pygame.font.SysFont(self.e["font"], self.e["fontSize"])  # Load font
            self.text = self.font.render(self.e["content"], True, self.e["textColor"]) # Create surface object
            self.textRect = self.text.get_rect() # Get rect
            # centering the text
            if self.e["centerText"]:
                self.textRect.center = self.rect.center
            else:
                self.textRect.topleft = self.rect.topleft
        # If there is no text or image
        elif not self.e["content"]:
            # Pos
            self.x, self.y = (position[0] - (self.e["rectWidth"] // 2), position[1] - (self.e["rectHeight"] // 2)) if self.e["centerMode"] else (position[0], position[1])
            # Rect
            self.rect = pygame.rect.Rect(self.x, self.y, self.e["rectWidth"], self.e["rectHeight"])
            self.borderRadius = self.e["rectBorderRadius"]
            self.rectColor = self.e["rectColor"]
        # If there is an image
        else:
            self.image = self.e["content"]
            try:
                self.rect = self.image.get_rect()
            except:
                raise Exception(f"{self.image} is not a pygame image")
            if self.e["centerMode"]:
                self.rect.center = (position[0], position[1])
                # Pos
                self.x, self.y = self.rect.center
            else:
                self.rect.topleft = (position[0], position[1])
                self.x, self.y = self.rect.topleft

        # Show
        self.show = True
        # Flowing
        self.flowing = False
        self.currentFlowPos = None
        self.otherFlowPos = None
        self.Xstep = 0
        self.Ystep = 0
        # Jumping
        self.jumping = False
        self.currentJumpPos = None
        self.otherJumpPos = None
        self.frames = 0
        self.frames_counter = 0
        # Clicking
        self.clicked = True

    def draw(self, win):
        if self.show:
            # If the element has text
            if isinstance(self.e["content"], str):
                # Draw text
                pygame.draw.rect(win, self.rectColor, self.rect, border_radius = self.borderRadius)
                win.blit(self.text, self.textRect)
            # If there is no text or image
            elif not self.e["content"]:
                pygame.draw.rect(win, self.rectColor, self.rect, border_radius = self.borderRadius)
            # If the element has an image
            else:
                # Draw img
                win.blit(self.image, self.rect)

    def is_hovered(self):
        # Get mouse pos
        mouse_pos = pygame.mouse.get_pos()

        # Check mouse over and clicked conditions
        if self.rect.collidepoint(mouse_pos):
            return True 

    def is_clicked(self, button_elements: list):
        # Get mouse pos
        mouse_pos = pygame.mouse.get_pos()

        # Check mouse over and clicked conditions
        if self.rect.collidepoint(mouse_pos):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            if pygame.mouse.get_pressed()[0] == 1: # == 1 is left click
                return True
        else:
            for element in button_elements: # Checks if user is howering any other buttons
                if element.rect.collidepoint(mouse_pos):
                    break
            else: # If not howering any other buttons: set cursor to arrow
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def was_clicked(self, button_elements: list):
        action = False

        # Get mouse pos
        mouse_pos = pygame.mouse.get_pos()

        # Check mouse over and clicked conditions
        if self.rect.collidepoint(mouse_pos):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False: # == 1 is left click
                self.clicked = True
                action = True
        else:
            for element in button_elements:
                if element.rect.collidepoint(mouse_pos):
                    break
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        
        if pygame.mouse.get_pressed()[0] == 0: #  No mousebuttons down
            self.clicked = False

        return action

    # Updates and moves the text if needed
    def update(self):
        if self.flowing: # If flowing
            # Check if flow has reached a flowpoint
            if self.e["centerMode"]: # If centermode is activated we will use the rects centerposition, if not the topleft
                if (self.Xstep == 0 or self.Ystep == 0):
                    if ((self.Xstep > 0) and (self.rect.centerx > self.currentFlowPos[0])) or ((self.Xstep < 0) and (self.rect.centerx < self.currentFlowPos[0])) or ((self.Ystep < 0) and (self.rect.centery < self.currentFlowPos[1])) or ((self.Ystep > 0) and (self.rect.centery > self.currentFlowPos[1])):
                        self.Xstep, self.Ystep = -self.Xstep, -self.Ystep # Switch direction
                        self.currentFlowPos, self.otherFlowPos = self.otherFlowPos, self.currentFlowPos
                else:
                    if (((self.Xstep > 0) and (self.rect.centerx > self.currentFlowPos[0])) and ((self.Ystep > 0) and (self.rect.centery > self.currentFlowPos[1]))) or (((self.Xstep > 0) and (self.rect.centerx > self.currentFlowPos[0])) and ((self.Ystep < 0) and (self.rect.centery < self.currentFlowPos[1]))) or (((self.Xstep < 0) and (self.rect.centerx < self.currentFlowPos[0])) and ((self.Ystep > 0) and (self.rect.centery > self.currentFlowPos[1])))or (((self.Xstep < 0) and (self.rect.centerx < self.currentFlowPos[0])) and ((self.Ystep < 0) and (self.rect.centery < self.currentFlowPos[1]))):
                        self.Xstep, self.Ystep = -self.Xstep, -self.Ystep # Switch direction
                        self.currentFlowPos, self.otherFlowPos = self.otherFlowPos, self.currentFlowPos
            else:
                if (self.Xstep == 0 or self.Ystep == 0):
                    if ((self.Xstep > 0) and (self.rect.x > self.currentFlowPos[0])) or ((self.Xstep < 0) and (self.rect.x < self.currentFlowPos[0])) or ((self.Ystep < 0) and (self.rect.y < self.currentFlowPos[1])) or ((self.Ystep > 0) and (self.rect.y > self.currentFlowPos[1])):
                        self.Xstep, self.Ystep = -self.Xstep, -self.Ystep # Switch direction
                        self.currentFlowPos, self.otherFlowPos = self.otherFlowPos, self.currentFlowPos
                else:
                    if (((self.Xstep > 0) and (self.rect.x > self.currentFlowPos[0])) and ((self.Ystep > 0) and (self.rect.y > self.currentFlowPos[1]))) or (((self.Xstep > 0) and (self.rect.x > self.currentFlowPos[0])) and ((self.Ystep < 0) and (self.rect.y < self.currentFlowPos[1]))) or (((self.Xstep < 0) and (self.rect.x < self.currentFlowPos[0])) and ((self.Ystep > 0) and (self.rect.y > self.currentFlowPos[1])))or (((self.Xstep < 0) and (self.rect.x < self.currentFlowPos[0])) and ((self.Ystep < 0) and (self.rect.y < self.currentFlowPos[1]))):
                        self.Xstep, self.Ystep = -self.Xstep, -self.Ystep # Switch direction
                        self.currentFlowPos, self.otherFlowPos = self.otherFlowPos, self.currentFlowPos

            self.move(self.Xstep, self.Ystep) # Apply movement
        
        elif self.jumping: # If jumping
            self.frames_counter += 1 # Increase frame counter
            if self.frames_counter >= self.frames: # If it has gone enough time to switch position
                self.move_to(self.otherJumpPos[0], self.otherJumpPos[1]) # Apply movement
                self.currentJumpPos, self.otherJumpPos = self.otherJumpPos, self.currentJumpPos
                self.frames_counter = 0 # Reset counter

    # Moves to specific cordinates
    def move_to(self, x: int, y:  int):
        if self.e["centerMode"]:
            self.rect.center = (x, y)
            self.x, self.y = self.rect.center
            if isinstance(self.e["content"], str): # Only affect the textRect if there is text
                if self.e["centerText"]:
                    self.textRect.center = self.rect.center
                else:
                    self.textRect.topleft = self.rect.topleft
        else:
            self.rect.topleft = (x, y)
            self.x, self.y = self.rect.topleft
            if isinstance(self.e["content"], str): # Only affect the textRect if there is text
                if self.e["centerText"]:
                    self.textRect.center = self.rect.center
                else:
                    self.textRect.topleft = self.rect.topleft
    
    # Moves in x and y direction
    def move(self, xMovement: float, yMovement: float):
        # Used to make small movements posible (self.x is a float, self.textRect.x is an int)
        self.x += xMovement
        self.y += yMovement
        if self.e["centerMode"]:
            self.rect.center = (self.x, self.y)
            if isinstance(self.e["content"], str): # Only affect the textRect if there is text
                if self.e["centerText"]:
                    self.textRect.center = self.rect.center
                else:
                    self.textRect.topleft = self.rect.topleft
        else:
            self.rect.topleft = (self.x, self.y)
            if isinstance(self.e["content"], str): # Only affect the textRect if there is text
                if self.e["centerText"]:
                    self.textRect.center = self.rect.center
                else:
                    self.textRect.topleft = self.rect.topleft

    # Flow lets the text flow between two points
    def flow(self, position1: tuple, position2: tuple, iterations: int):
        # Move to flowpoint
        self.move_to(position1[0], position1[1])
        # Set flowpostions
        self.otherFlowPos, self.currentFlowPos = position1, position2 
        # Get amount to move per iteration
        Xdistance, Ydistance = (position2[0] - position1[0]), (position2[1] - position1[1])
        self.Xstep = Xdistance / iterations
        self.Ystep = Ydistance / iterations
        # Activate flowing
        self.flowing = True
    
    # Jump lets the user toggle the text between two points on a userSpecified timer
    def jump(self, position1: tuple, position2: tuple, frames: int):
        # Move to jumppoint
        self.move_to(position1[0], position1[1])
        # Set jumpPostions
        self.otherJumpPos, self.currentJumpPos = position2, position1
        # Frames
        self.frames = frames
        # Activate jumping
        self.jumping = True

class input():
    def __init__(self, position: tuple, **extra ):
        pygame.scrap.init()
        pygame.scrap.set_mode(pygame.SCRAP_CLIPBOARD)
        
        # Extras are addition arguments the user can input to further customize the text
        # The values in the array underneath are the values used if the user does not specify them
        self.e = {"font": "freesansbold.ttf", "fontSize": 30, "exampleContent": "Click me to input!", "prefilledContent": "", "characterLimit": 100, "normalTextColor": (231, 111, 81), "exampleTextColor": (100, 100, 100), "rectWidth": 200, "rectHeight": 50, "rectColorActive": (233, 196, 106), "rectColorPassive": (200, 200, 200), "rectBorderRadius": 1, "rectBorderWidth": 5, "centerMode": True}
        for key in extra:
            if key in self.e:
                self.e[key] = extra[key]
            else: # Sends an error if the function has been passed a non recognizable argument
                extras_keys = []
                for extraKey in self.e:
                    extras_keys.append(extraKey)
                error = f"Argument error: Argument '{key}' not recognized. The extra arguments available are: {extras_keys}"
                raise Exception(error)
        
        # Create position variables and font
        # Pos
        self.x, self.y = (position[0] - (self.e["rectWidth"] // 2), position[1] - (self.e["rectHeight"] // 2)) if self.e["centerMode"] else (position[0], position[1])
        # Rect
        self.rect = pygame.rect.Rect(self.x, self.y, self.e["rectWidth"], self.e["rectHeight"])
        self.borderRadius = self.e["rectBorderRadius"]
        self.rectBorderWidth = self.e["rectBorderWidth"]
        self.rectColorPassive = self.e["rectColorPassive"]
        self.rectColorActive = self.e["rectColorActive"]
        # Text
        self.normalTextColor = self.e["normalTextColor"]
        self.exampleTextColor = self.e["exampleTextColor"]
        self.characterLimit = self.e["characterLimit"]
        self.font = pygame.font.SysFont(self.e["font"], self.e["fontSize"])  # Load font
        self.userText = self.e["prefilledContent"]
        self.exampleContent = self.e["exampleContent"]
        self.userTextSurface = self.font.render(self.userText, True, self.normalTextColor) # Create surface object for the userText
        self.exampleTextSurface = self.font.render(self.exampleContent, True, self.exampleTextColor) # Create surface object the exampleText

        self.userTextRect = self.userTextSurface.get_rect() # Get rect
        self.exampleTextRect = self.exampleTextSurface.get_rect() # Get rect
        # centering the text
        self.userTextRect.center = self.rect.center
        self.exampleTextRect.center = self.rect.center
        
        # Show
        self.show = True
        # Flowing
        self.flowing = False
        self.currentFlowPos = None
        self.otherFlowPos = None
        self.Xstep = 0
        self.Ystep = 0
        # Jumping
        self.jumping = False
        self.currentJumpPos = None
        self.otherJumpPos = None
        self.frames = 0
        self.frames_counter = 0
        # Clicking
        self.clicked = False
        self.active = False

    def draw(self, win):
        if self.show:
            if self.userText != "":
                win.blit(self.userTextSurface, self.userTextRect)
            else:
                if not self.active:
                    win.blit(self.exampleTextSurface, self.exampleTextRect)
                    
            if self.active:
                pygame.draw.rect(win, self.rectColorActive, self.rect, self.rectBorderWidth, border_radius = self.borderRadius)
            else:
                pygame.draw.rect(win, self.rectColorPassive, self.rect, self.rectBorderWidth, border_radius = self.borderRadius)

    def work(self, events: list, clickable_elements: list):
        # Make activating work
        # Get mouse pos
        mouse_pos = pygame.mouse.get_pos()

        # Check mouse over and clicked conditions
        if self.rect.collidepoint(mouse_pos):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False: # == 1 is left click
                self.active = True
                self.clicked = True
        else:
            if pygame.mouse.get_pressed()[0]: # == 1 is left click
                self.active = False
            for element in clickable_elements:
                if element.rect.collidepoint(mouse_pos):
                    break
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        
        if pygame.mouse.get_pressed()[0] == 0: #  No mousebuttons down
            self.clicked = False

        # Make writing work
        for event in events:
            if event.type == pygame.KEYDOWN:
                if self.active:
                    if event.key == pygame.K_v and event.mod & pygame.KMOD_CTRL:
                        self.userText = pygame.scrap.get("text/plain;charset=utf-8").decode()
                        self.userText = self.userText.replace("\x00", "")
                    elif event.key == pygame.K_BACKSPACE:
                        self.userText = self.userText[0: -1] # Removes last character
                    elif (len(self.userText) <= self.characterLimit) and event.key != pygame.K_RETURN: # Keep text under character limit and don't enterperate enter as a key
                        self.userText += event.unicode # Adds the userinput to the text
                    self.userTextSurface = self.font.render(self.userText, True, self.normalTextColor) # Create surface object for the userText
                    self.userTextRect = self.userTextSurface.get_rect() # Get rect
                    self.userTextRect.center = self.rect.center

    # Updates and moves the text if needed
    def update(self):
        if self.flowing: # If flowing
            # Check if flow has reached a flowpoint
            if self.e["centerMode"]: # If centermode is activated we will use the rects centerposition, if not the topleft
                if (self.Xstep == 0 or self.Ystep == 0):
                    if ((self.Xstep > 0) and (self.rect.centerx > self.currentFlowPos[0])) or ((self.Xstep < 0) and (self.rect.centerx < self.currentFlowPos[0])) or ((self.Ystep < 0) and (self.rect.centery < self.currentFlowPos[1])) or ((self.Ystep > 0) and (self.rect.centery > self.currentFlowPos[1])):
                        self.Xstep, self.Ystep = -self.Xstep, -self.Ystep # Switch direction
                        self.currentFlowPos, self.otherFlowPos = self.otherFlowPos, self.currentFlowPos
                else:
                    if (((self.Xstep > 0) and (self.rect.centerx > self.currentFlowPos[0])) and ((self.Ystep > 0) and (self.rect.centery > self.currentFlowPos[1]))) or (((self.Xstep > 0) and (self.rect.centerx > self.currentFlowPos[0])) and ((self.Ystep < 0) and (self.rect.centery < self.currentFlowPos[1]))) or (((self.Xstep < 0) and (self.rect.centerx < self.currentFlowPos[0])) and ((self.Ystep > 0) and (self.rect.centery > self.currentFlowPos[1])))or (((self.Xstep < 0) and (self.rect.centerx < self.currentFlowPos[0])) and ((self.Ystep < 0) and (self.rect.centery < self.currentFlowPos[1]))):
                        self.Xstep, self.Ystep = -self.Xstep, -self.Ystep # Switch direction
                        self.currentFlowPos, self.otherFlowPos = self.otherFlowPos, self.currentFlowPos
            else:
                if (self.Xstep == 0 or self.Ystep == 0):
                    if ((self.Xstep > 0) and (self.rect.x > self.currentFlowPos[0])) or ((self.Xstep < 0) and (self.rect.x < self.currentFlowPos[0])) or ((self.Ystep < 0) and (self.rect.y < self.currentFlowPos[1])) or ((self.Ystep > 0) and (self.rect.y > self.currentFlowPos[1])):
                        self.Xstep, self.Ystep = -self.Xstep, -self.Ystep # Switch direction
                        self.currentFlowPos, self.otherFlowPos = self.otherFlowPos, self.currentFlowPos
                else:
                    if (((self.Xstep > 0) and (self.rect.x > self.currentFlowPos[0])) and ((self.Ystep > 0) and (self.rect.y > self.currentFlowPos[1]))) or (((self.Xstep > 0) and (self.rect.x > self.currentFlowPos[0])) and ((self.Ystep < 0) and (self.rect.y < self.currentFlowPos[1]))) or (((self.Xstep < 0) and (self.rect.x < self.currentFlowPos[0])) and ((self.Ystep > 0) and (self.rect.y > self.currentFlowPos[1])))or (((self.Xstep < 0) and (self.rect.x < self.currentFlowPos[0])) and ((self.Ystep < 0) and (self.rect.y < self.currentFlowPos[1]))):
                        self.Xstep, self.Ystep = -self.Xstep, -self.Ystep # Switch direction
                        self.currentFlowPos, self.otherFlowPos = self.otherFlowPos, self.currentFlowPos

            self.move(self.Xstep, self.Ystep) # Apply movement
        
        elif self.jumping: # If jumping
            self.frames_counter += 1 # Increase frame counter
            if self.frames_counter >= self.frames: # If it has gone enough time to switch position
                self.move_to(self.otherJumpPos[0], self.otherJumpPos[1]) # Apply movement
                self.currentJumpPos, self.otherJumpPos = self.otherJumpPos, self.currentJumpPos
                self.frames_counter = 0 # Reset counter

    # Moves to specific cordinates
    def move_to(self, x: int, y:  int):
        if self.e["centerMode"]:
            self.rect.center = (x, y)
            self.x, self.y = self.rect.center
            self.userTextRect.center = (x, y)
            self.exampleTextRect.center = (x, y)
        else:
            self.rect.topleft = (x, y)
            self.x, self.y = self.rect.topleft
            self.userTextRect.topleft = (self.x, self.y)
            self.exampleTextRect.topleft = (self.x, self.y)
    
    # Moves in x and y direction
    def move(self, xMovement: float, yMovement: float):
        # Used to make small movements posible (self.x is a float, self.textRect.x is an int)
        self.x += xMovement
        self.y += yMovement
        if self.e["centerMode"]:
            self.rect.center = (self.x, self.y)
            self.userTextRect.center = (self.x, self.y)
            self.exampleTextRect.center = (self.x, self.y)
        else:
            self.rect.topleft = (self.x, self.y)
            self.userTextRect.topleft = (self.x, self.y)
            self.exampleTextRect.topleft = (self.x, self.y)
    
    def is_hovered(self):
        # Get mouse pos
        mouse_pos = pygame.mouse.get_pos()

        # Check mouse over and clicked conditions
        if self.rect.collidepoint(mouse_pos):
            return True 

    # Flow lets the text flow between two points
    def flow(self, position1: tuple, position2: tuple, iterations: int):
        # Move to flowpoint
        self.move_to(position1[0], position1[1])
        # Set flowpostions
        self.otherFlowPos, self.currentFlowPos = position1, position2 
        # Get amount to move per iteration
        Xdistance, Ydistance = (position2[0] - position1[0]), (position2[1] - position1[1])
        self.Xstep = Xdistance / iterations
        self.Ystep = Ydistance / iterations
        # Activate flowing
        self.flowing = True
    
    # Jump lets the user toggle the text between two points on a userSpecified timer
    def jump(self, position1: tuple, position2: tuple, frames: int):
        # Move to jumppoint
        self.move_to(position1[0], position1[1])
        # Set jumpPostions
        self.otherJumpPos, self.currentJumpPos = position2, position1
        # Frames
        self.frames = frames
        # Activate jumping
        self.jumping = True
