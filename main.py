import pygame
import os
import sys

pygame.init()

TILE_SIZE = 16
VIRTUAL_WIDTH = 320
VIRTUAL_HEIGHT = 180
virtual_screen = pygame.Surface((VIRTUAL_WIDTH, VIRTUAL_HEIGHT))

WINDOW_WIDTH = 960
WINDOW_HEIGHT = 540
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Warping-Zone")
clock = pygame.time.Clock()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LevelMusic = os.path.join(BASE_DIR, "assets", "Music", "LevelMusic.wav")
VictorySound = os.path.join(BASE_DIR, "assets", "Music", "Victory.wav")
icon_img_path = os.path.join(BASE_DIR, "assets", "Images", "icon.ico")

try:
    import GameOverSound
except ImportError as e:
    print(f"Script Import Error: {e}")
    sys.exit()

try:
    victory_track = pygame.mixer.Sound(VictorySound)
    pygame.mixer.music.load(LevelMusic)
    pygame.mixer.music.play(-1)
except pygame.error as e:
    print(f"Audio Error: {e}")
    sys.exit()

try:
    game_icon = pygame.image.load(icon_img_path)
    pygame.display.set_icon(game_icon)
except pygame.error as e:
    print(f"Icon Loading Warning: {e}")

player_img_path = os.path.join(BASE_DIR, "assets", "Images", "Boy.png")

try:
    player_sprite = pygame.image.load(player_img_path).convert_alpha()
    player_sprite = pygame.transform.scale(player_sprite, (14, 14))
except pygame.error as e:
    print(f"Image Loading Error: {e}")
    sys.exit()

MAP_WIDTH = 1000
MAP_HEIGHT = 1000

level1data = {
    0:  "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
    1:  "W..............................................................W",
    2:  "W..WWWW......WWWW..............................................W",
    3:  "W....W........W.............................................V..W",
    4:  "W....P........W.......HHHH..................O..................W",
    5:  "W....W........W................................................W",
    6:  "W..WWWW......WWWW..............................................W",
    7:  "W..............................................................W",
    8:  "W..............................................................W",
    9:  "W..............................................................W",
    10: "W..............................................................W",
    11: "W..............................................................W",
    12: "W..............................................................W",
    13: "W..............................................................W",
    14: "W..............................................................W",
    15: "W..............................................................W",
    16: "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW"
}

walls = []
hazards = []
portals = []
victory_tiles = []
player = pygame.Rect(0, 0, 14, 14)
player_speed = 2
game_over_triggered = False
victory_triggered = False

for row_index, row_string in level1data.items():
    for col_index, char in enumerate(row_string):
        pixel_x = col_index * TILE_SIZE
        pixel_y = row_index * TILE_SIZE
        if char == "W":
            wall_block = pygame.Rect(pixel_x, pixel_y, TILE_SIZE, TILE_SIZE)
            walls.append(wall_block)
        elif char == "H":
            hazard_block = pygame.Rect(pixel_x, pixel_y, TILE_SIZE, TILE_SIZE)
            hazards.append(hazard_block)
        elif char == "O":
            portal_block = pygame.Rect(pixel_x, pixel_y, TILE_SIZE, TILE_SIZE)
            portals.append(portal_block)
        elif char == "V":
            victory_block = pygame.Rect(pixel_x, pixel_y, TILE_SIZE, TILE_SIZE)
            victory_tiles.append(victory_block)
        elif char == "P":
            player.x = pixel_x + 1
            player.y = pixel_y + 1

def trigger_game_over():
    global game_over_triggered, running
    if game_over_triggered or victory_triggered:
        return
    game_over_triggered = True

    pygame.mixer.music.stop()

    virtual_screen.fill((50, 0, 0))
    scaled_surface = pygame.transform.scale(virtual_screen, (WINDOW_WIDTH, WINDOW_HEIGHT))
    window.blit(scaled_surface, (0, 0))
    pygame.display.flip()
    
    GameOverSound.play_game_over()
    
    running = False

def trigger_victory():
    global victory_triggered, running
    if victory_triggered or game_over_triggered:
        return
    victory_triggered = True

    pygame.mixer.music.stop()

    virtual_screen.fill((0, 50, 0))
    scaled_surface = pygame.transform.scale(virtual_screen, (WINDOW_WIDTH, WINDOW_HEIGHT))
    window.blit(scaled_surface, (0, 0))
    pygame.display.flip()

    victory_track.play()
    track_duration = int(victory_track.get_length() * 1000)
    pygame.time.wait(track_duration)

    running = False

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    old_x, old_y = player.x, player.y
    
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player.x -= player_speed
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player.x += player_speed
        
    if player.x < 0:
        player.x = 0
    if player.x > MAP_WIDTH - player.width:
        player.x = MAP_WIDTH - player.width

    for wall in walls:
        if player.colliderect(wall):
            player.x = old_x
            
    for hazard in hazards:
        if player.colliderect(hazard):
            trigger_game_over()

    for portal in portals:
        if player.colliderect(portal):
            player.x = 50
            player.y = 50
            
    for vic in victory_tiles:
        if player.colliderect(vic):
            trigger_victory()
        
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        player.y -= player_speed
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        player.y += player_speed
        
    if player.y < 0:
        player.y = 0
    if player.y > MAP_HEIGHT - player.height:
        player.y = MAP_HEIGHT - player.height

    for wall in walls:
        if player.colliderect(wall):
            player.y = old_y
            
    for hazard in hazards:
        if player.colliderect(hazard):
            trigger_game_over()

    for portal in portals:
        if player.colliderect(portal):
            player.x = 50
            player.y = 50

    for vic in victory_tiles:
        if player.colliderect(vic):
            trigger_victory()

    camera_x = player.x - (VIRTUAL_WIDTH // 2)
    camera_y = player.y - (VIRTUAL_HEIGHT // 2)

    if camera_x < 0:
        camera_x = 0
    if camera_x > MAP_WIDTH - VIRTUAL_WIDTH:
        camera_x = MAP_WIDTH - VIRTUAL_WIDTH

    if camera_y < 0:
        camera_y = 0
    if camera_y > MAP_HEIGHT - VIRTUAL_HEIGHT:
        camera_y = MAP_HEIGHT - VIRTUAL_HEIGHT

    if running:
        virtual_screen.fill((20, 20, 30))
        
        for wall in walls:
            pygame.draw.rect(virtual_screen, (70, 70, 90), (wall.x - camera_x, wall.y - camera_y, wall.width, wall.height))
            
        for hazard in hazards:
            pygame.draw.rect(virtual_screen, (255, 60, 60), (hazard.x - camera_x, hazard.y - camera_y, hazard.width, hazard.height))

        for portal in portals:
            pygame.draw.rect(virtual_screen, (60, 120, 255), (portal.x - camera_x, portal.y - camera_y, portal.width, portal.height))

        for vic in victory_tiles:
            pygame.draw.rect(virtual_screen, (255, 215, 0), (vic.x - camera_x, vic.y - camera_y, vic.width, vic.height))
            
        virtual_screen.blit(player_sprite, (player.x - camera_x, player.y - camera_y))
        
        scaled_surface = pygame.transform.scale(virtual_screen, (WINDOW_WIDTH, WINDOW_HEIGHT))
        window.blit(scaled_surface, (0, 0))
        pygame.display.flip()
        clock.tick(60)

pygame.quit()
sys.exit()
