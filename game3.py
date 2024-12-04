import pygame
import math

# Initialize Pygame
pygame.init()

# Initialize Pygame mixer
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=4096)

# Function to generate a beep sound
def generate_beep(frequency=1000, duration=0.1):
    sample_rate = 22050  # Standard audio sample rate
    n_samples = int(sample_rate * duration)
    
    # Generate the sine wave samples for the beep
    samples = []
    for t in range(n_samples):
        sample = int(32767.0 * math.sin(2 * math.pi * frequency * t / sample_rate))
        samples.append(sample)

    # Convert to byte data (need to be in a format that Pygame can play)
    sound_data = pygame.sndarray.array(samples)
    
    # Convert to pygame sound
    beep_sound = pygame.mixer.Sound(sound_data)
    
    return beep_sound

# Create different beep sounds with varying frequencies and durations
beep_400hz = generate_beep(frequency=400, duration=0.3)  # Low note
beep_600hz = generate_beep(frequency=600, duration=0.3)  # Slightly higher
beep_800hz = generate_beep(frequency=800, duration=0.3)  # Mid note
beep_1000hz = generate_beep(frequency=1000, duration=0.3)  # Mid-high note
beep_1200hz = generate_beep(frequency=1200, duration=0.3)  # High note
beep_1500hz = generate_beep(frequency=1500, duration=0.3)  # Very high note

# Function to create the melody sequence
def play_game_theme():
    melody = [
        beep_400hz, beep_600hz, beep_800hz, beep_1000hz, beep_1200hz,
        beep_1000hz, beep_800hz, beep_600hz, beep_400hz, beep_1200hz,
        beep_1000hz, beep_1500hz, beep_1200hz, beep_800hz, beep_600hz,
        beep_400hz, beep_800hz, beep_1000hz, beep_1200hz
    ]
    
    return melody

# Pygame screen setup for testing
monitor = pygame.display.set_mode((640, 480))
pygame.display.set_caption("This game is ass")

# Initialize variables to track song playback
song_playing = False
melody = []
note_index = 0  # Track the current note in the melody
note_timer = 0  # Timer to track when to play the next note

# Start the song automatically when the game starts
melody = play_game_theme()  # Generate the melody
song_playing = True
melody[note_index].play()  # Play the first note
note_timer = pygame.time.get_ticks()  # Start timer

# Create the player character surface (human-like)
def draw_player(x, y):
    body_color = (0, 128, 255)  # Blue for the body
    head_color = (255, 220, 185)  # Skin color for the head
    leg_color = (0, 0, 0)  # Black for legs (representing pants)
    arm_color = (0, 128, 255)  # Same as body color for arms
    shoe_color = (50, 50, 50)  # Dark color for shoes
    eye_color = (0, 0, 0)  # Black for eyes
    
    # Head (oval)
    head_width = 40
    head_height = 50
    pygame.draw.ellipse(monitor, head_color, (x + 10, y, head_width, head_height))

    # Eyes (two small circles)
    eye_radius = 5
    pygame.draw.circle(monitor, eye_color, (x + 20, y + 20), eye_radius)  # Left eye
    pygame.draw.circle(monitor, eye_color, (x + 30, y + 20), eye_radius)  # Right eye

    # Body (rectangle)
    body_width = 30
    body_height = 60
    pygame.draw.rect(monitor, body_color, (x + 5, y + head_height, body_width, body_height))

    # Arms (rectangles)
    arm_width = 10
    arm_height = 40
    pygame.draw.rect(monitor, arm_color, (x - arm_width + 5, y + head_height + 10, arm_width, arm_height))  # Left arm
    pygame.draw.rect(monitor, arm_color, (x + body_width + 5, y + head_height + 10, arm_width, arm_height))  # Right arm

    # Legs (rectangles)
    leg_width = 12
    leg_height = 40
    pygame.draw.rect(monitor, leg_color, (x + 5, y + head_height + body_height, leg_width, leg_height))  # Left leg
    pygame.draw.rect(monitor, leg_color, (x + 18, y + head_height + body_height, leg_width, leg_height))  # Right leg

    # Shoes (small rectangles at the bottom of the legs)
    shoe_width = 15
    shoe_height = 5
    pygame.draw.rect(monitor, shoe_color, (x + 5, y + head_height + body_height + leg_height, shoe_width, shoe_height))  # Left shoe
    pygame.draw.rect(monitor, shoe_color, (x + 18, y + head_height + body_height + leg_height, shoe_width, shoe_height))  # Right shoe

# Create a surface for the yellow player square
surf = pygame.Surface((30, 30))
surf.fill("yellow")
surf_rect = surf.get_rect(topleft=(1, 1))  # Start at top-left corner

# Movement speed and direction for the yellow player surface
yellow_speed = 100
yellow_movement_surf = pygame.math.Vector2(-1, 1)

# Create a surface for the yellow player square
surf2 = pygame.Surface((30, 30))
surf2.fill("red")
surf_rect2 = surf2.get_rect(topright=(599, 1))  # Start at top-left corner

# Movement speed and direction for the yellow player surface
yellow_speed2 = 150
yellow_movement_surf2 = pygame.math.Vector2(-1, -1)

# Movement speed and direction for the character
player_x = 300
player_y = 200
player_speed = 100

# Initialize clock and game status
clock = pygame.time.Clock()
game_over = False

score = 0

# Event loop to keep the program running
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Reset the game when spacebar is pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_over:
                # Reset positions and flags
                player_x = 300
                player_y = 200
                surf_rect.topleft = (1, 1)  # Reset yellow surface position
                surf_rect2.topright = (590, 1)
                game_over = False
                note_index = 0
                melody[note_index].play()  # Restart the melody
                note_timer = pygame.time.get_ticks()  # Reset timer
                score = 0 #reset score

    # Check if the current note has finished playing and time has passed
    if not game_over:
        current_time = pygame.time.get_ticks()  # Get the current time
        note_duration = melody[note_index].get_length() * 1000  # Duration of the current note in milliseconds

        if current_time - note_timer > note_duration:  # Time to play the next note
            note_index += 1
            if note_index < len(melody):
                melody[note_index].play()  # Play the next note
                note_timer = pygame.time.get_ticks()  # Reset the timer for the next note
            else:
                # Reset to loop the song
                note_index = 0
                melody[note_index].play()
                note_timer = pygame.time.get_ticks()  # Reset timer for looping

        # Handle key presses for movement of the player character
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_x -= player_speed * 0.01
        if keys[pygame.K_RIGHT]:
            player_x += player_speed * 0.01
        if keys[pygame.K_UP]:
            player_y -= player_speed * 0.01
        if keys[pygame.K_DOWN]:
            player_y += player_speed * 0.01

        # Ensure the player doesn't move out of bounds
        player_x = max(0, min(player_x, 640 - 40))  # Player width is 40
        player_y = max(0, min(player_y, 480 - 100))  # Player height is 100

        # Moving the yellow surface
        if surf_rect.x >= 640 - 30 or surf_rect.x <= 0 or surf_rect.colliderect(surf_rect2):
            yellow_movement_surf.x *= -1
        if surf_rect.y >= 480 - 30 or surf_rect.y <= 0:
            yellow_movement_surf.y *= -1
        surf_rect.center += yellow_movement_surf * yellow_speed * (clock.get_time() / 1000)  # Use delta_time for smooth movement

        # Moving the red surface
        if surf_rect2.x >= 640 - 30 or surf_rect2.x <= 0 or surf_rect2.colliderect(surf_rect):
            yellow_movement_surf2.x *= -1
        if surf_rect2.y >= 480 - 30 or surf_rect2.y <= 0:
            yellow_movement_surf2.y *= -1
        surf_rect2.center += yellow_movement_surf2 * yellow_speed2 * (clock.get_time() / 1000)  # Use delta_time for smooth movement

        # Check for collision (if the player's rect intersects the yellow surface)
        player_rect = pygame.Rect(player_x, player_y, 40, 100)  # Player rect
        if player_rect.colliderect(surf_rect) or player_rect.colliderect(surf_rect2):
            game_over = True  # Set game over when collision happens
        score += 1

        # White background
        monitor.fill("darkgrey")

        # Draw player character
        draw_player(player_x, player_y)

        # Draw the yellow surface
        monitor.blit(surf, surf_rect)
        monitor.blit(surf2, surf_rect2)

        pygame.display.flip()

    else:
        # Display game over message
        font = pygame.font.SysFont(None, 55)
        game_over_text = font.render(f"GAME OVER! score: {score}", True, (255, 0, 0))
        monitor.blit(game_over_text, (100, 150))
        pygame.display.flip()

    # Frame rate control
    
    clock.tick(60)

pygame.quit()
