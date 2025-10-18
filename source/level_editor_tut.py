# Echoes of Ruin
# Rhein, Corbeil, Magnaudeix, Godin
import pygame as pg
import csv
import os

from usefull_fonctions import get_files_in_directory


class SLRButton():
    def __init__(self, x, y, image, scale, enabled=True):
        width = image.get_width()
        height = image.get_height()
        self.original_image = pg.transform.scale(image, (int(width * scale), int(height * scale)))
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.clicked = False
        self.enabled = enabled

    def draw(self, surface):
        action = False
        pos = pg.mouse.get_pos()

        if self.enabled:
            # Effet de survol (légère réduction de luminosité)
            if self.rect.collidepoint(pos):
                self.image.set_alpha(100)  # Rendre un peu transparent
                if pg.mouse.get_pressed()[0] == 1 and not self.clicked:
                    action = True
                    self.clicked = True
            else:
                self.image.set_alpha(255)  # Opacité normale

            if pg.mouse.get_pressed()[0] == 0:
                self.clicked = False
        else:
            self.image.set_alpha(100)  # Rendre le bouton plus transparent si désactivé

        surface.blit(self.image, self.rect.topleft)
        return action

    def set_enabled(self, enabled):
        self.enabled = enabled

# === INIT PG ===
def level_editor_loop():
	# === INIT PG ===
	pg.init()

	clock = pg.time.Clock()
	FPS = 60
	info_object = pg.display.Info()

	WIDTH,HEIGHT = info_object.current_w, info_object.current_h  # Taille de la fenetre

	# Fenêtre du jeu
	SCREEN_HEIGHT = 640
	LOWER_MARGIN = 200
	SIDE_MARGIN = 600

	#screen = pg.display.set_mode((SCREEN_WIDTH + SIDE_MARGIN, SCREEN_HEIGHT + LOWER_MARGIN))
	screen = pg.display.set_mode((WIDTH,HEIGHT),flags=pg.FULLSCREEN,vsync=1)
	pg.display.set_caption('editeur de pièce')


	# Définition des variables du jeu
	mode = "level_editor"
	ROWS = 32
	MAX_COLS = 244
	TILE_SIZE = HEIGHT // ROWS
	room = 0
	current_tile = 0
	scroll_left = False
	scroll_right = False
	scroll = 0
	scroll_speed = 1

	# initialisation de la varible TILE_TYPES
	folder='stone'
	TILE_TYPES = get_files_in_directory(f'assets/images/basic/{folder}')

	# Charger les images
	pine1_img = pg.image.load(r'assets/images/background/pine1.png').convert_alpha()
	pine2_img = pg.image.load(r'assets/images/background/pine2.png').convert_alpha()
	mountain_img = pg.image.load(r'assets/images/background/mountain.png').convert_alpha()
	sky_img = pg.image.load(r'assets/images/background/sky_cloud.png').convert_alpha()

	# Stocker les tuiles dans une liste
	img_list = []
	for x in TILE_TYPES:
		img = pg.image.load(f'assets/images/basic/{folder}/{x}').convert_alpha()
		img = pg.transform.scale(img, (TILE_SIZE, TILE_SIZE))
		img_list.append(img)
  
	# initialise des images pour les boutons
	save_img = pg.image.load(r'assets/images/usefull/save_btn.png').convert_alpha()
	load_img = pg.image.load(r'assets/images/usefull/load_btn.png').convert_alpha()
	exit_img = pg.image.load(r'assets/images/usefull/exit_btn.png').convert_alpha()


	# Définition des couleurs
	rgb_gray_nb=32
	GRAY = (rgb_gray_nb, rgb_gray_nb, rgb_gray_nb)
	WHITE = (255, 255, 255)
	RED = (200, 25, 25)

	# Définition de la police
	font = pg.font.SysFont('Futura', 30)

	# Créer une liste vide pour le niveau
	def world_data_create():
		world_data = []
		for row in range(ROWS):
			r = [-1] * MAX_COLS
			world_data.append(r)
		return world_data
	world_data=world_data_create()

	# Fonction pour afficher du texte à l'écran

	def draw_text(text, font, text_col, x, y):
		img = font.render(text, True, text_col)
		screen.blit(img, (x, y))
	
	# Fonction pour changer le format de la save
	# Permet d'éléminer les éléments inutils dans la variable world_data
	def change_format(world_data:list):# dixit la fonction du diable (4 heures de travaille et de tourmente)

		template = [world_data[i].copy() for i in range(len(world_data))]
		empty_list_row = [-1 for i in range(len(world_data[0]))]

		for i_row in range(len(world_data)-1, -1, -1):
			if world_data[i_row] == empty_list_row :
				template.pop(i_row)
	
		empty_list_col = [-1 for i in range(len(template))]   
		for col in range(len(template[0])-1, -1, -1):
			if [template[i][col] for i in range(len(template))] == empty_list_col:
				for i in range(len(template)):
					template[i].pop(col)
		return template

	# Remplace les nombres par les noms des blocs avec la même indentation
	def creator_list_tile_clear(folder:str=f'assets/images/basic/stone'):
		tile_list = get_files_in_directory(f'{folder}')
		new_tile_list = []
		for elt in tile_list:
			new_tile_list.append(elt.replace(".png", ""))
		return new_tile_list

	# Remplace les nombres par les noms des blocs dans le template final
	def template_replace_name(template:list,list_nom_tile:list):
		if template == []:
			return []
		for x in range(len(template)):
			for y in range(len(template[0])):
				if template[x][y] == -1:
					template[x][y] = 0
				else:
					template[x][y] = list_nom_tile[template[x][y]]
		return template
	# fonction pour ajouter 0,1,2,.. au début de la liste
	def add_nb_template(template:list):
		list_add = [i for i in range(len(template[0]))]
		template.insert(0,list_add)
		return template
	
 
	# Créer une fonction pour dessiner l'arrière-plan
	def draw_bg():
		screen.fill(GRAY)
		width = sky_img.get_width()
		for x in range(4):
			screen.blit(sky_img, ((x * width) - scroll * 0.5, 0))
			screen.blit(mountain_img, ((x * width) - scroll * 0.6, HEIGHT - mountain_img.get_height() - 300))
			screen.blit(pine1_img, ((x * width) - scroll * 0.7, HEIGHT - pine1_img.get_height() - 150))
			screen.blit(pine2_img, ((x * width) - scroll * 0.8, HEIGHT - pine2_img.get_height()))


	# Dessiner la grille
	def draw_grid():
		# Lignes verticales
		for c in range(MAX_COLS + 1):
			pg.draw.line(screen, WHITE, (c * TILE_SIZE - scroll, 0), (c * TILE_SIZE - scroll, HEIGHT-LOWER_MARGIN))
		# Lignes horizontales
		for c in range(ROWS + 1):
			pg.draw.line(screen, WHITE, (0, c * TILE_SIZE), (WIDTH-SIDE_MARGIN, c * TILE_SIZE))


	# Fonction pour dessiner les tuiles du monde
	def draw_world():
		for y, row in enumerate(world_data):
			for x, tile in enumerate(row):
				if tile >= 0:
					screen.blit(img_list[tile], (x * TILE_SIZE - scroll, y * TILE_SIZE))


	# Créer des boutons en t'en que class PS:width des exit,save et load button 80px

	save_button = SLRButton(WIDTH // 2 -160 - WIDTH // 16, HEIGHT//2 +  HEIGHT//3, save_img, 1)
	load_button = SLRButton(WIDTH // 2 -240 + WIDTH // 16, HEIGHT//2 +  HEIGHT//3, load_img, 1)
	exit_button = SLRButton(WIDTH // 2 + 80 + WIDTH // 16, HEIGHT//2 +  HEIGHT//3, exit_img, 1)
 
	# Créer une liste de boutons tile_list,à droite
	button_list = []
	button_col = 0
	button_row = 0
	for i in range(len(img_list)):
		tile_button = SLRButton(WIDTH + (75 * button_col)-600, 75 * button_row + 50, img_list[i], 1)
		button_list.append(tile_button)
		button_col += 1
		if button_col == 6: #nb de colonne
			button_row += 1
			button_col = 0

	# change de display
	def change_display(WIDTH, HEIGHT, is_window_fullscreen: bool):
		global screen
		if is_window_fullscreen:
			screen = pg.display.set_mode((WIDTH, HEIGHT - 60), flags=pg.RESIZABLE, vsync=1)
		else:
			screen = pg.display.set_mode((WIDTH, HEIGHT), flags=pg.FULLSCREEN, vsync=1)

	run = True
	while run:

		clock.tick(FPS)

		draw_bg()
		draw_grid()
		draw_world()
	
		# Dessiner l'espace pour la sélection des tuilles (l'espace à droite)
		pg.draw.rect(screen, GRAY, (WIDTH-SIDE_MARGIN-TILE_SIZE, 0, SIDE_MARGIN+TILE_SIZE,HEIGHT))
	
		# Dessiner l'espace pour boutons/mots (l'espace en bas)
		pg.draw.rect(screen, GRAY, (0, HEIGHT-LOWER_MARGIN, WIDTH, LOWER_MARGIN))
	
		# Surligner la tuile sélectionnée
		pg.draw.rect(screen, RED, button_list[current_tile].rect, 3)
	
		draw_text(f'Room: {room}', font, WHITE, 10,HEIGHT- 90)
		draw_text('Appuyez sur HAUT ou BAS pour changer de niveau', font, WHITE, 10,HEIGHT -60)

		# Sauvegarder et charger les données
		if save_button.draw(screen):
			# Sauvegarder les données du niveau en changebt le format
	
			template = add_nb_template(template_replace_name(change_format(world_data),creator_list_tile_clear()))
	
			with open(f'data/rooms_load/room_load{room}_data.csv', 'w', newline='') as csvfile:
				writer = csv.writer(csvfile, delimiter = ',')
				for row in world_data:
					writer.writerow(row)
		
			with open(f'data/templates/rooms{room}_data.csv', 'w', newline='') as csvfile:
				writer = csv.writer(csvfile, delimiter = ',')
				for row in template:
					writer.writerow(row)    
		
		if load_button.draw(screen):
			# Charger les données du niveau
			# Réinitialiser le défilement au début du niveau
			scroll = 0
			try :
				with open(f'data/rooms_load/room_load{room}_data.csv', newline='') as csvfile:
					reader = csv.reader(csvfile, delimiter = ',')
					for x, row in enumerate(reader):
						for y, tile in enumerate(row):
							world_data[x][y] = int(tile)
			# Si le template n'existe pas dans les fichiers alors on ne fait rien
			except:
				pass
		if exit_button.draw(screen):# sa marche car c'est une fonction que l'on appel en boucle dans le main
			mode = "main_menu"
			return run,mode
		
	
		# Choisir une tuile

		button_count = None
		for button_count, i in enumerate(button_list):
			if i.draw(screen):
				current_tile = button_count




		# Faire défiler la carte
		if scroll_left == True and scroll > 0:
			scroll -= 5 * scroll_speed
		if scroll_right == True and scroll < (MAX_COLS * TILE_SIZE) - WIDTH:
			scroll += 5 * scroll_speed

		# Ajouter de nouvelles tuiles à l'écran
		# Obtenir la position de la souris
		pos = pg.mouse.get_pos()
		pos_x = (pos[0] + scroll) // TILE_SIZE
		pos_y = pos[1] // TILE_SIZE

		# Vérifier que les coordonnées sont dans la zone des tuiles
		if pos[0] < WIDTH-SIDE_MARGIN-TILE_SIZE and pos[1] < HEIGHT-LOWER_MARGIN:
			# Mettre à jour la valeur de la tuile
			if pg.mouse.get_pressed()[0] == 1:
				if world_data[pos_y][pos_x] != current_tile:
					world_data[pos_y][pos_x] = current_tile
			if pg.mouse.get_pressed()[2] == 1:
				world_data[pos_y][pos_x] = -1


		for event in pg.event.get():
			if event.type == pg.QUIT:
				run = False

			# Appuis clavier
			if event.type == pg.KEYDOWN:
				if event.key == pg.K_UP:
					room += 1
				if event.key == pg.K_DOWN and room > 0:
					room -= 1
				if event.key == pg.K_LEFT:
					scroll_left = True
				if event.key == pg.K_RIGHT:
					scroll_right = True
				if event.key == pg.K_RSHIFT:
					scroll_speed = 5


			if event.type == pg.KEYUP:
				if event.key == pg.K_LEFT:
					scroll_left = False
				if event.key == pg.K_RIGHT:
					scroll_right = False
				if event.key == pg.K_RSHIFT:
					scroll_speed = 1


		pg.display.update()
	return run, mode

	pg.quit()