import pygame, sys, random 

def draw_floor():
	screen.blit(floor_surface,(floor_x_pos,450))
	screen.blit(floor_surface,(floor_x_pos + 288,450))

def create_pipe():
	random_pipe_pos = random.choice(pipe_height)
	bottom_pipe = pipe_surface.get_rect(midtop = (350,random_pipe_pos))
	top_pipe = pipe_surface.get_rect(midbottom = (350,random_pipe_pos - 150))
	return bottom_pipe,top_pipe

def move_pipes(pipes):
	for pipe in pipes:
		pipe.centerx -= 2.5
	return pipes

def draw_pipes(pipes):
	for pipe in pipes:
		if pipe.bottom >= 512:
			screen.blit(pipe_surface,pipe)
		else:
			flip_pipe = pygame.transform.flip(pipe_surface,False,True)
			screen.blit(flip_pipe,pipe)
def remove_pipes(pipes):
	for pipe in pipes:
		if pipe.centerx == -300:
			pipes.remove(pipe)
	return pipes
def check_collision(pipes):
	global can_score
	for pipe in pipes:
		if bird_rect.colliderect(pipe):
			death_sound.play()
			can_score = True
			return False

	if bird_rect.top <= -50 or bird_rect.bottom >= 450:
		can_score = True
		return False

	return True

def rotate_bird(bird):
	new_bird = pygame.transform.rotozoom(bird,-bird_movement * 1.5,0.5)
	return new_bird

def bird_animation():
	new_bird = bird_frames[bird_index]
	new_bird_rect = new_bird.get_rect(center = (50,bird_rect.centery))
	return new_bird,new_bird_rect

def score_display(game_state):
	if game_state == 'main_game':
		score_surface = game_font.render(str(int(score)),True,(127.5,127.5,127.5))
		score_rect = score_surface.get_rect(center = (144,50))
		screen.blit(score_surface,score_rect)
	if game_state == 'game_over':
		score_surface = game_font.render(f'Score: {int(score)}' ,True,(127.5,127.5,127.5))
		score_rect = score_surface.get_rect(center = (144,50))
		screen.blit(score_surface,score_rect)

		high_score_surface = game_font.render(f'High score: {int(high_score)}',True,(127.5,127.5,127.5))
		high_score_rect = high_score_surface.get_rect(center = (144,425))
		screen.blit(high_score_surface,high_score_rect)

def update_score(score, high_score):
	if score > high_score:
		high_score = score
	return high_score


def pipe_score_check():
	global score, can_score 
	
	if pipe_list:
		for pipe in pipe_list:
			if 47.5 < pipe.centerx < 52.5 and can_score:
				score += 1
				score_sound.play()
				can_score = False
			if pipe.centerx < 0:
				can_score = True


pygame.mixer.pre_init(frequency = 44100, size = 16, channels = 1, buffer = 512)
pygame.init()
screen = pygame.display.set_mode((288,512))
clock = pygame.time.Clock()
game_font = pygame.font.SysFont('04B_19.TTF',20)

# Game Variables
gravity = 0.125
bird_movement = 0
game_active = True
score = 0
high_score = 0
can_score = True

bg_surface = pygame.image.load('assets/background-day.png').convert()

floor_surface = pygame.image.load('assets/base.png').convert()
floor_x_pos = 0

bird_downflap = pygame.image.load('assets/bluebird-downflap.png').convert_alpha()
bird_midflap = pygame.image.load('assets/bluebird-midflap.png').convert_alpha()
bird_upflap = pygame.image.load('assets/bluebird-upflap.png').convert_alpha()
bird_frames = [bird_downflap,bird_midflap,bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center = (50,256))

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP,200)

pipe_surface = pygame.image.load('assets/pipe-green.png')
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE,1200)
pipe_height = [200,300,400]

game_over_surface = pygame.image.load('assets/message.png').convert_alpha()
game_over_rect = game_over_surface.get_rect(center = (144,256))

flap_sound = pygame.mixer.Sound('audio/wing.wav')
death_sound = pygame.mixer.Sound('audio/hit.wav')
score_sound = pygame.mixer.Sound('audio/point.wav')
score_sound_countdown = 100

# Event Loop

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE and game_active:
				bird_movement = 0
				bird_movement -= 6
				flap_sound.play()
			if event.key == pygame.K_SPACE and game_active == False:
				game_active = True
				pipe_list.clear()
				bird_rect.center = (50,256)
				bird_movement = 0
				score = 0

		if event.type == SPAWNPIPE:
			pipe_list.extend(create_pipe())

		if event.type == BIRDFLAP:
			if bird_index < 2:
				bird_index += 1
			else:
				bird_index = 0

			bird_surface,bird_rect = bird_animation()

	screen.blit(bg_surface,(0,0))

	if game_active:
		# Bird
		bird_movement += gravity
		rotated_bird = rotate_bird(bird_surface)
		bird_rect.centery += bird_movement
		screen.blit(rotated_bird,bird_rect)
		game_active = check_collision(pipe_list)

		# Pipes
		pipe_list = move_pipes(pipe_list)
		pipe_list = remove_pipes(pipe_list)
		draw_pipes(pipe_list)
		
		# Score
		pipe_score_check()
		score_display('main_game')
	else:
		screen.blit(game_over_surface,game_over_rect)
		high_score = update_score(score,high_score)
		score_display('game_over')


	# Floor
	floor_x_pos -= 1
	draw_floor()
	if floor_x_pos <= -288:
		floor_x_pos = 0
	

	pygame.display.update()
	clock.tick(120)