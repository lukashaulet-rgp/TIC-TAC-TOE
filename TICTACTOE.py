import tkinter as tk
from tkinter import messagebox
import random
import math

class LightningTicTacToe: # boite du jeux 
    def __init__(self, root): # F cree le jeux 
        self.root = root
        self.root.title("⚡ Tic Tac Toe ⚡")
        self.root.geometry("800x900")
        self.root.configure(bg='#0a0f1e')
        
        # Variables du jeu
        self.board = [''] * 9
        self.current_player = 'X'
        self.game_over = False
        self.mode = None  # 1 = PvP, 2 = PvIA
        self.niveau_difficulte = 1  # 1 = Facile, 2 = Moyen, 3 = Expert
        self.weather_mode = 'sunny'  # 'sunny', 'rainy', 'stormy'
        
        # Canvas unique avec tout dessus
        self.canvas = tk.Canvas(root, width=800, height=900, bg='#0f1420', highlightthickness=0) # Zone de dessin 
        self.canvas.pack(fill=tk.BOTH, expand=True) # remplir contour
        
        # Effets d'animation - ORAGEUX
        self.lightnings = [] # 1
        self.clouds = [] # 2
        self.rain_drops = [] # 3 / 1, 2, 3 liste pour stocker animation
        self.flash_intensity = 0
        self.time = 0
        
        # Effets d'animation - ENSOLEILLÉ
        self.sun_rays = []
        self.birds = []
        self.white_clouds = []
        
        # Initialiser tous les effets
        self.init_stormy_weather() # Full element orageux 
        self.init_sunny_weather() # Full element ensoleiller
        
        self.current_screen = 'menu'  # 'menu', 'difficulty', 'game' ECRAN ACCEUIL
        
        # Démarrer l'animation
        self.animate() # Demarrer boucle animation 
    
    #  INITIALISATION DES MÉTÉOS #
    def init_stormy_weather(self):
        """Initialiser les effets orageux (Expert)"""
        for i in range(25):
            self.clouds.append({
                'x': random.randint(-100, 900),
                'y': random.randint(30, 180),
                'width': random.randint(120, 220),
                'height': random.randint(45, 80),
                'speed': random.uniform(0.1, 0.35),
                'darkness': random.uniform(0.6, 1.0),
                'puffiness': random.uniform(0.8, 1.3),
                'depth': random.random()
            })
        self.clouds.sort(key=lambda c: c['depth'])
        
        for i in range(350):
            self.rain_drops.append({
                'x': random.randint(-100, 900),          #
                'y': random.randint(0, 900),             #
                'speed': random.uniform(12, 18),         #
                'length': random.randint(25, 40),        # Parametre Pluie
                'opacity': random.uniform(0.4, 0.8),     #
                'thickness': random.uniform(1.5, 2.5)    #
            })
    
    def init_sunny_weather(self):
        """Initialiser les effets ensoleillés (Facile)"""
        
        for i in range(8):
            self.white_clouds.append({ # parametre nuage 
                'x': random.randint(-100, 900),
                'y': random.randint(50, 200),
                'width': random.randint(100, 180),
                'height': random.randint(40, 70),
                'speed': random.uniform(0.2, 0.4),
                'puffiness': random.uniform(0.9, 1.2),
                'depth': random.random()
            })
        self.white_clouds.sort(key=lambda c: c['depth'])
        
        # Oiseaux
        for i in range(5):
            self.birds.append({
                'x': random.randint(-100, 900),
                'y': random.randint(100, 300),
                'speed': random.uniform(1.5, 3.0),
                'wing_phase': random.uniform(0, math.pi * 2),
                'size': random.uniform(0.8, 1.2)
            })
        
        # Rayons de soleil
        for i in range(12):
            angle = (i / 12) * math.pi * 2 # Tiret soleil
            self.sun_rays.append({
                'angle': angle,
                'length': random.randint(80, 120),
                'width': random.randint(15, 25)
            })
    
    #  INTELLIGENCE ARTIFICIELLE #
    def est_gagnant(self, plateau, signe):
        """Vérifie si un joueur a gagné"""
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]
        for combo in winning_combinations:
            if plateau[combo[0]] == plateau[combo[1]] == plateau[combo[2]] == signe:
                return True
        return False
    
    def plateau_plein(self, plateau):
        """Renvoie True si le plateau est rempli"""
        return all(case != '' for case in plateau)
    
    def minimax(self, plateau, profondeur, tour_ia, signe_ia, signe_humain, prof_max): # Calcul les meilleur coups pour l'ia 
        """Algorithme Minimax pour l'IA"""
        if self.est_gagnant(plateau, signe_ia):
            return 10 - profondeur
        if self.est_gagnant(plateau, signe_humain):
            return profondeur - 10
        if self.plateau_plein(plateau) or profondeur >= prof_max:
            return 0
        
        if tour_ia:
            meilleur_score = -999
            for i in range(9):
                if plateau[i] == '':
                    plateau[i] = signe_ia # L'ia test tout les coups pour gagner 
                    score = self.minimax(plateau, profondeur + 1, False,
                                        signe_ia, signe_humain, prof_max)
                    plateau[i] = ''
                    meilleur_score = max(meilleur_score, score)
            return meilleur_score
        else:
            pire_score = 999
            for i in range(9):
                if plateau[i] == '':
                    plateau[i] = signe_humain
                    score = self.minimax(plateau, profondeur + 1, True,
                                        signe_ia, signe_humain, prof_max)
                    plateau[i] = ''
                    pire_score = min(pire_score, score)
            return pire_score
    
    def ia_jouer(self):
        """IA Tic Tac Toe avec niveaux + marge d'erreur réaliste"""
        signe = 'O'
        adversaire = 'X'
        plateau = self.board.copy()
        
        if self.niveau_difficulte == 1: # L'ia joue au hazard 
            cases_libres = [i for i, case in enumerate(plateau) if case == '']
            return random.choice(cases_libres) if cases_libres else None
        
        prof_max = 3 if self.niveau_difficulte == 2 else 999
        
        if self.niveau_difficulte == 2 and random.random() < 0.15: # calucluer pour avoir 15% de win sur l'ia 
            libres = [i for i, case in enumerate(plateau) if case == '']
            if libres:
                return random.choice(libres)
        
        if self.niveau_difficulte == 3 and random.random() < 0.05:# calucluer pour avoir 5% de win sur l'ia 
            libres = [i for i, case in enumerate(plateau) if case == '']
            if libres:
                return random.choice(libres)
        
        meilleur_coup = None
        meilleur_score = -999 # test chaque case pour avoir le meilleur resultat 
        for i in range(9):
            if plateau[i] == '':
                plateau[i] = signe
                score = self.minimax(plateau, 0, False, signe, adversaire, prof_max)
                plateau[i] = ''
                if score > meilleur_score:
                    meilleur_score = score
                    meilleur_coup = i
        return meilleur_coup
    
    #  INTERFACE UTILISATEUR #
    def draw_menu(self):
        """Dessiner le menu principal"""
        self.canvas.create_text(
            400, 150,
            text="⚡ Tic Tac Toe ⚡",
            font=('Arial', 32, 'bold'),
            fill='#66ccff', tags='ui'
        )
        
        self.canvas.create_text(
            400, 220,
            text="Choisissez un mode de jeu",
            font=('Arial', 20, 'bold'),
            fill='#000000', tags='ui'
        )
        
        # Bouton Joueur vs Joueur
        self.canvas.create_rectangle(
            250, 300, 550, 370,
            fill='#2266cc', outline='#5599ff', width=3, tags=('ui', 'btn_pvp')
        )
        self.canvas.create_text(
            400, 335,
            text="🧍 Joueur vs Joueur",
            font=('Arial', 18, 'bold'),
            fill='white', tags=('ui', 'btn_pvp')
        )
        self.canvas.tag_bind('btn_pvp', '<Button-1>', lambda e: self.choisir_mode(1))
        
        # Bouton Joueur vs IA
        self.canvas.create_rectangle(
            250, 400, 550, 470,
            fill='#2266cc', outline='#5599ff', width=3, tags=('ui', 'btn_ia')
        )
        self.canvas.create_text(
            400, 435,
            text="🤖 Joueur vs IA",
            font=('Arial', 18, 'bold'),
            fill='white', tags=('ui', 'btn_ia')
        )
        self.canvas.tag_bind('btn_ia', '<Button-1>', lambda e: self.choisir_mode(2))
    
    def draw_difficulty_menu(self):
        """Dessiner le menu de sélection de difficulté"""
        self.canvas.create_text(
            400, 120,
            text="⚡ NIVEAU DE DIFFICULTÉ ⚡",
            font=('Arial', 32, 'bold'),
            fill='#66ccff', tags='ui'
        )
        
        # Facile - Ensoleillé
        self.canvas.create_rectangle(
            200, 220, 600, 310,
            fill='#ffcc33', outline='#ffee66', width=3, tags=('ui', 'btn_facile')
        )
        self.canvas.create_text(
            400, 255,
            text="☀️ Facile - Ensoleillé",
            font=('Arial', 20, 'bold'),
            fill='#333333', tags=('ui', 'btn_facile')
        )
        self.canvas.create_text(
            400, 285,
            text="IA aléatoire - Météo agréable",
            font=('Arial', 12),
            fill='#555555', tags=('ui', 'btn_facile')
        )
        self.canvas.tag_bind('btn_facile', '<Button-1>', lambda e: self.choisir_difficulte(1))
        
        # Moyen - Pluvieux
        self.canvas.create_rectangle(
            200, 340, 600, 430,
            fill='#6699cc', outline='#99ccff', width=3, tags=('ui', 'btn_moyen')
        )
        self.canvas.create_text(
            400, 375,
            text="🌧️ Moyen - Pluvieux",
            font=('Arial', 20, 'bold'),
            fill='white', tags=('ui', 'btn_moyen')
        )
        self.canvas.create_text(
            400, 405,
            text="IA stratégique - Il pleut",
            font=('Arial', 12),
            fill='#e0e0e0', tags=('ui', 'btn_moyen')
        )
        self.canvas.tag_bind('btn_moyen', '<Button-1>', lambda e: self.choisir_difficulte(2))
        
        # Expert - Orageux
        self.canvas.create_rectangle(
            200, 460, 600, 550,
            fill='#cc2222', outline='#ff5555', width=3, tags=('ui', 'btn_expert')
        )
        self.canvas.create_text(
            400, 495,
            text="⚡ Expert - Orageux",
            font=('Arial', 20, 'bold'),
            fill='white', tags=('ui', 'btn_expert')
        )
        self.canvas.create_text(
            400, 525,
            text="IA quasi-parfaite - Tempête électrique",
            font=('Arial', 12),
            fill='#ffcccc', tags=('ui', 'btn_expert')
        )
        self.canvas.tag_bind('btn_expert', '<Button-1>', lambda e: self.choisir_difficulte(3))
        
        # Bouton Retour
        self.canvas.create_rectangle(
            250, 600, 550, 670,
            fill='#555555', outline='#888888', width=3, tags=('ui', 'btn_retour')
        )
        self.canvas.create_text(
            400, 635,
            text="⬅️ Retour",
            font=('Arial', 18, 'bold'),
            fill='white', tags=('ui', 'btn_retour')
        )
        self.canvas.tag_bind('btn_retour', '<Button-1>', lambda e: self.retour_menu())
    
    def draw_game_ui(self):
        """Dessiner l'interface de jeu par-dessus les animations"""
        # Couleurs adaptées à la météo
        if self.weather_mode == 'sunny':
            bg_color = '#fffaed'
            border_color = '#ffaa00'
            title_color = '#ff6600'
            status_color = '#ff8833'
        elif self.weather_mode == 'rainy':
            bg_color = '#d0d8e0'
            border_color = '#4477aa'
            title_color = '#3366aa'
            status_color = '#5588cc'
        else:  # stormy
            bg_color = '#0d1829'
            border_color = '#0088cc'
            title_color = '#66ccff'
            status_color = '#aaddff'
        
        # Fond semi-transparent
        self.canvas.create_rectangle(
            150, 200, 650, 800,
            fill=bg_color, outline='', stipple='gray50', tags='ui'
        )
        
        # Titre adapté
        if self.weather_mode == 'sunny':
            title = "☀️ MODE ENSOLEILLÉ ☀️"
        elif self.weather_mode == 'rainy':
            title = "🌧️ MODE PLUVIEUX 🌧️"
        else:
            title = "⚡ MODE ORAGEUX ⚡"
        
        self.canvas.create_text(
            400, 60,
            text=title,
            font=('Arial', 36, 'bold'),
            fill=title_color, tags='ui'
        )
        
        # Status
        status_text = "Joueur: " + self.current_player
        if self.game_over:
            winner = self.check_winner()
            if winner:
                status_text = f"🏆 {winner} a gagné!"
            else:
                status_text = "Match nul!"
        elif self.mode == 2 and self.current_player == 'O':
            status_text = "🤖 L'IA réfléchit..."
        
        self.canvas.create_text(
            400, 120,
            text=status_text,
            font=('Arial', 20, 'bold'),
            fill=status_color, tags='ui'
        )
        
        # Plateau de jeu
        board_x = 200
        board_y = 270
        board_size = 400
        cell_size = board_size // 3
        
        # Cadre du plateau
        self.canvas.create_rectangle(
            board_x - 25, board_y - 25,
            board_x + board_size + 25, board_y + board_size + 25,
            fill='', outline=border_color, width=5, tags='ui'
        )
        
        # Créer les cellules du morpion
        for i in range(9):
            row = i // 3
            col = i % 3
            x = board_x + col * cell_size
            y = board_y + row * cell_size
            
            # Couleur adaptée à la météo
            if self.weather_mode == 'sunny':
                cell_bg = '#fff8e1'
                cell_outline = '#ffbb33'
                text_color = '#ff6600'
            elif self.weather_mode == 'rainy':
                cell_bg = '#c8d4e0'
                cell_outline = '#5588bb'
                text_color = '#2255aa'
            else:
                cell_bg = '#050f1a'
                cell_outline = '#006699'
                text_color = '#88ddff'
            
            rect = self.canvas.create_rectangle(
                x + 8, y + 8,
                x + cell_size - 8, y + cell_size - 8,
                fill=cell_bg, outline=cell_outline, width=2, tags=('ui', f'cell_{i}')
            )
            
            text = self.canvas.create_text(
                x + cell_size // 2, y + cell_size // 2,
                text=self.board[i],
                font=('Arial', 56, 'bold'),
                fill=text_color, tags=('ui', f'cell_{i}')
            )
            
            self.canvas.tag_bind(f'cell_{i}', '<Button-1>', lambda e, idx=i: self.cell_clicked(idx))
        
        # Boutons
        btn_color = '#2266cc' if self.weather_mode == 'stormy' else ('#ffaa33' if self.weather_mode == 'sunny' else '#5588cc')
        btn_outline = '#5599ff' if self.weather_mode == 'stormy' else ('#ffcc66' if self.weather_mode == 'sunny' else '#88aadd')
        
        self.canvas.create_rectangle(
            200, 730, 400, 790,
            fill=btn_color, outline=btn_outline, width=3, tags=('ui', 'reset_btn')
        )
        self.canvas.create_text(
            300, 760,
            text="🔄 Nouvelle",
            font=('Arial', 18, 'bold'),
            fill='white', tags=('ui', 'reset_btn')
        )
        self.canvas.tag_bind('reset_btn', '<Button-1>', lambda e: self.reset_game())
        
        self.canvas.create_rectangle(
            420, 730, 600, 790,
            fill='#555555', outline='#888888', width=3, tags=('ui', 'menu_btn')
        )
        self.canvas.create_text(
            510, 760,
            text="⬅️ Menu",
            font=('Arial', 18, 'bold'),
            fill='white', tags=('ui', 'menu_btn')
        )
        self.canvas.tag_bind('menu_btn', '<Button-1>', lambda e: self.retour_menu())
    
    #  GESTION DES ÉVÉNEMENTS #
    def choisir_mode(self, mode):
        """Choisir le mode de jeu"""
        self.mode = mode
        if mode == 2:
            self.current_screen = 'difficulty'
        else:
            self.weather_mode = 'stormy'  # Par défaut pour PvP
            self.current_screen = 'game'
            self.reset_game()
    
    def choisir_difficulte(self, niveau):
        """Choisir la difficulté de l'IA"""
        self.niveau_difficulte = niveau
        # Définir la météo selon le niveau
        if niveau == 1:
            self.weather_mode = 'sunny'
        elif niveau == 2:
            self.weather_mode = 'rainy'
        else:
            self.weather_mode = 'stormy'
        self.current_screen = 'game'
        self.reset_game()
    
    def retour_menu(self):
        """Retourner au menu principal"""
        self.current_screen = 'menu'
        self.weather_mode = 'stormy'  # Retour à l'orageux par défaut
        self.reset_game()
    
    def cell_clicked(self, index):
        """Gérer le clic sur une cellule"""
        if self.game_over or self.board[index] != '':
            return
        
        if self.mode == 2 and self.current_player == 'O':
            return
        
        self.board[index] = self.current_player
        
        winner = self.check_winner()
        if winner:
            self.game_over = True
            self.root.after(100, lambda: messagebox.showinfo("Fin du jeu", f"Le joueur {winner} a gagné!"))
        elif '' not in self.board:
            self.game_over = True
            self.root.after(100, lambda: messagebox.showinfo("Fin du jeu", "Match nul!"))
        else:
            self.current_player = 'O' if self.current_player == 'X' else 'X'
            
            if self.mode == 2 and self.current_player == 'O':
                self.root.after(500, self.tour_ia)
    
    def tour_ia(self):
        """Tour de l'IA"""
        if self.game_over:
            return
        
        choix = self.ia_jouer()
        if choix is None:
            return
        
        self.board[choix] = 'O'
        
        winner = self.check_winner()
        if winner:
            self.game_over = True
            self.root.after(100, lambda: messagebox.showinfo("Fin du jeu", "L'IA a gagné! 🤖"))
        elif '' not in self.board:
            self.game_over = True
            self.root.after(100, lambda: messagebox.showinfo("Fin du jeu", "Match nul!"))
        else:
            self.current_player = 'X'
    
    def check_winner(self):
        """Vérifier s'il y a un gagnant"""
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]
        
        for combo in winning_combinations:
            if (self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]] 
                and self.board[combo[0]] != ''):
                return self.board[combo[0]]
        return None
    
    def reset_game(self):
        """Réinitialiser le jeu"""
        self.board = [''] * 9
        self.current_player = 'X'
        self.game_over = False
    
    #  EFFETS VISUELS - ENSOLEILLÉ #
    def draw_sunny_sky(self):
        """Dessiner un ciel ensoleillé"""
        # Dégradé bleu ciel
        for i in range(25):
            # Bleu clair en haut, plus pâle vers le bas
            r = 135 + i * 4
            g = 206 + i * 1
            b = 250
            color = f'#{min(255, r):02x}{min(255, g):02x}{b:02x}'
            
            self.canvas.create_rectangle(
                0, i*36, 800, (i+1)*36,
                fill=color, outline='', tags='bg'
            )
    
    def draw_sun(self):
        """Dessiner le soleil avec rayons"""
        sun_x, sun_y = 700, 120
        sun_radius = 50
        
        # Rayons rotatifs
        for ray in self.sun_rays:
            angle = ray['angle'] + self.time * 0.005
            end_x = sun_x + math.cos(angle) * ray['length']
            end_y = sun_y + math.sin(angle) * ray['length']
            
            # Dégradé du rayon
            self.canvas.create_line(
                sun_x, sun_y, end_x, end_y,
                fill='#ffee88', width=ray['width'], tags='sun'
            )
        
        # Glow du soleil
        for size in [70, 60, 50]:
            opacity = int((70 - size) * 5)
            color = f'#ffdd{opacity:02x}'
            self.canvas.create_oval(
                sun_x - size, sun_y - size,
                sun_x + size, sun_y + size,
                fill=color, outline='', tags='sun'
            )
        
        # Cœur du soleil
        self.canvas.create_oval(
            sun_x - sun_radius, sun_y - sun_radius,
            sun_x + sun_radius, sun_y + sun_radius,
            fill='#ffdd00', outline='#ffee44', width=3, tags='sun'
        )
    
    def draw_white_cloud(self, cloud):
        """Dessiner un nuage blanc"""
        num_puffs = 7
        
        for i in range(num_puffs):
            offset_x = (i - num_puffs/2) * cloud['width'] / (num_puffs + 1)
            height_factor = 1 - abs(i - num_puffs/2) / (num_puffs/2)
            offset_y = -height_factor * cloud['height'] / 3
            
            size_x = cloud['width'] / 3 * cloud['puffiness'] * (0.8 + height_factor * 0.4)
            size_y = cloud['height'] / 2 * cloud['puffiness'] * (0.7 + height_factor * 0.5)
            
            # Blanc avec légère ombre
            base = 240 + int(height_factor * 15)
            color = f'#{base:02x}{base:02x}{min(255, base+10):02x}'
            
            self.canvas.create_oval(
                cloud['x'] + offset_x - size_x,
                cloud['y'] + offset_y - size_y,
                cloud['x'] + offset_x + size_x,
                cloud['y'] + offset_y + size_y,
                fill=color, outline='#d0d0d0', width=1, tags='cloud'
            )
    
    def draw_bird(self, bird):
        """Dessiner un oiseau"""
        x, y = bird['x'], bird['y']
        size = bird['size']
        
        # Animation des ailes
        wing_angle = math.sin(bird['wing_phase']) * 0.3
        
        # Corps (simple V)
        wing_span = 15 * size
        self.canvas.create_line(
            x - wing_span, y + wing_span * wing_angle,
            x, y,
            x + wing_span, y + wing_span * wing_angle,
            fill='#333333', width=int(2 * size), tags='bird'
        )
    
    #  EFFETS VISUELS - PLUVIEUX #
    def draw_rainy_sky(self):
        """Dessiner un ciel pluvieux"""
        # Dégradé gris
        for i in range(25):
            intensity = 100 + i * 3
            color = f'#{intensity:02x}{intensity:02x}{intensity+15:02x}'
            
            self.canvas.create_rectangle(
                0, i*36, 800, (i+1)*36,
                fill=color, outline='', tags='bg'
            )
    
    def draw_rain_only(self):
        """Dessiner seulement la pluie (sans éclairs)"""
        for drop in self.rain_drops:
            drop['x'] += drop['speed'] * 0.7  # Pluie plus lente
            drop['y'] += drop['speed'] * 0.4
            
            if drop['x'] > 1000 or drop['y'] > 950:
                drop['x'] = random.randint(-150, -50)
                drop['y'] = random.randint(0, 900)
            
            # Pluie grise/bleue
            opacity = int(drop['opacity'] * 150)
            color = f'#{opacity:02x}{opacity:02x}{opacity+60:02x}'
            
            self.canvas.create_line(
                drop['x'], drop['y'],
                drop['x'] + drop['length'] * 0.6, drop['y'] + drop['length'] * 0.4,
                fill=color, width=drop['thickness'], capstyle=tk.ROUND, tags='rain'
            )
    
    #  EFFETS VISUELS - ORAGEUX #
    def create_lightning(self):
        """Créer un éclair ultra réaliste avec branches complexes"""
        lightning = {
            'start_x': random.randint(150, 650),
            'start_y': random.randint(60, 140),
            'segments': [],
            'branches': [],
            'life': 28,
            'max_life': 28,
            'color_type': random.choices(['blue', 'yellow', 'cyan'], weights=[60, 25, 15])[0],
            'thickness': random.uniform(1.2, 2.0),
            'intensity': random.uniform(0.8, 1.2)
        }
        
        x = lightning['start_x']
        y = lightning['start_y']
        lightning['segments'].append((x, y))
        
        max_segments = random.randint(45, 65)
        direction = random.choice([-1, 1]) * 0.4
        chaos = random.uniform(0.8, 1.2)
        
        for i in range(max_segments):
            x += random.randint(-60, 60) * chaos + direction * 8
            y += random.randint(10, 28)
            
            if random.random() < 0.15:
                direction *= -1
                chaos = random.uniform(0.7, 1.3)
            
            lightning['segments'].append((x, y))
            
            if random.random() < 0.4 and i > 3 and len(lightning['branches']) < 20:
                branch = self.create_branch(x, y, i, max_segments, depth=0)
                if branch:
                    lightning['branches'].append(branch)
            
            if y > 900:
                break
        
        return lightning
    
    def create_branch(self, start_x, start_y, parent_depth, max_depth, depth=0):
        """Créer une branche d'éclair avec sous-branches récursives"""
        if depth > 2 or parent_depth > max_depth * 0.85:
            return None
            
        branch = []
        x, y = start_x, start_y
        length = random.randint(5, 12) - depth * 2
        angle_bias = random.choice([-1.2, 1.2])
        
        for i in range(max(3, length)):
            x += random.randint(-45, 45) * angle_bias
            y += random.randint(8, 22)
            branch.append((x, y))
            
            if random.random() < 0.25 and i > 2 and depth < 2:
                sub_branch = self.create_branch(x, y, parent_depth, max_depth, depth + 1)
                if sub_branch:
                    return [branch, sub_branch]
        
        return branch
    
    def draw_lightning(self, lightning):
        """Dessiner un éclair avec effet glow multicouche ultra réaliste"""
        life_ratio = lightning['life'] / lightning['max_life']
        pulse = 1 + math.sin(lightning['life'] * 0.4) * 0.3
        alpha = min(1.0, life_ratio * pulse * lightning['intensity'])
        
        if lightning['color_type'] == 'blue':
            colors = [
                (f'#{int(30*alpha):02x}{int(100*alpha):02x}{int(255*alpha):02x}', 10),
                (f'#{int(80*alpha):02x}{int(160*alpha):02x}{int(255*alpha):02x}', 6),
                (f'#{int(150*alpha):02x}{int(200*alpha):02x}{int(255*alpha):02x}', 3.5),
                (f'#{int(220*alpha):02x}{int(240*alpha):02x}{int(255*alpha):02x}', 1.8),
                ('#f0f8ff', 0.8)
            ]
        elif lightning['color_type'] == 'yellow':
            colors = [
                (f'#{int(200*alpha):02x}{int(130*alpha):02x}{int(15*alpha):02x}', 10),
                (f'#{int(255*alpha):02x}{int(170*alpha):02x}{int(40*alpha):02x}', 6),
                (f'#{int(255*alpha):02x}{int(210*alpha):02x}{int(100*alpha):02x}', 3.5),
                (f'#{int(255*alpha):02x}{int(245*alpha):02x}{int(180*alpha):02x}', 1.8),
                ('#ffffd8', 0.8)
            ]
        else:
            colors = [
                (f'#{int(20*alpha):02x}{int(180*alpha):02x}{int(200*alpha):02x}', 10),
                (f'#{int(60*alpha):02x}{int(220*alpha):02x}{int(240*alpha):02x}', 6),
                (f'#{int(120*alpha):02x}{int(240*alpha):02x}{int(255*alpha):02x}', 3.5),
                (f'#{int(200*alpha):02x}{int(250*alpha):02x}{int(255*alpha):02x}', 1.8),
                ('#e0ffff', 0.8)
            ]
        
        def draw_branch_recursive(branch_data, is_main=False):
            if isinstance(branch_data, list) and len(branch_data) > 0:
                if isinstance(branch_data[0], tuple):
                    if len(branch_data) > 1:
                        width_mult = 1.0 if is_main else 0.6
                        for color, width in colors:
                            self.canvas.create_line(
                                branch_data, fill=color, 
                                width=width*lightning['thickness']*width_mult, 
                                smooth=True, capstyle=tk.ROUND, joinstyle=tk.ROUND,
                                tags='lightning'
                            )
                else:
                    for sub_branch in branch_data:
                        draw_branch_recursive(sub_branch, False)
        
        for branch in lightning['branches']:
            draw_branch_recursive(branch, False)
        
        if len(lightning['segments']) > 1:
            for color, width in colors:
                self.canvas.create_line(
                    lightning['segments'], fill=color, 
                    width=width*lightning['thickness'], 
                    smooth=True, capstyle=tk.ROUND, joinstyle=tk.ROUND,
                    tags='lightning'
                )
    
    def draw_dark_cloud(self, cloud):
        """Dessiner un nuage sombre"""
        darkness = cloud['darkness']
        depth_factor = 0.5 + cloud['depth'] * 0.5
        base_color = int(20 + darkness * 30)
        num_puffs = 9
        
        for i in range(num_puffs):
            offset_x = (i - num_puffs/2) * cloud['width'] / (num_puffs + 1)
            height_factor = 1 - abs(i - num_puffs/2) / (num_puffs/2)
            offset_y = -height_factor * cloud['height'] / 2.5 + math.sin(i + self.time*0.015) * 10
            
            size_x = cloud['width'] / 2.8 * cloud['puffiness'] * (0.8 + height_factor * 0.4)
            size_y = cloud['height'] / 1.8 * cloud['puffiness'] * (0.7 + height_factor * 0.5)
            
            color_var = int(base_color * depth_factor + (i - num_puffs/2) * 2)
            color_var = max(15, min(80, color_var))
            
            r = color_var
            g = color_var + 8
            b = color_var + 22
            color = f'#{r:02x}{g:02x}{b:02x}'
            
            self.canvas.create_oval(
                cloud['x'] + offset_x - size_x,
                cloud['y'] + offset_y - size_y,
                cloud['x'] + offset_x + size_x,
                cloud['y'] + offset_y + size_y,
                fill=color, outline=f'#{max(0,r-10):02x}{max(0,g-10):02x}{max(0,b-10):02x}',
                width=1, tags='cloud'
            )
    
    def draw_stormy_rain(self):
        """Dessiner la pluie orageuse"""
        for drop in self.rain_drops:
            drop['x'] += drop['speed']
            drop['y'] += drop['speed'] * 0.45
            
            if drop['x'] > 1000 or drop['y'] > 950:
                drop['x'] = random.randint(-150, -50)
                drop['y'] = random.randint(0, 900)
            
            wind = math.sin((drop['y'] + self.time * 2) * 0.015) * 6 + math.cos(drop['x'] * 0.01) * 3
            opacity = int(drop['opacity'] * 200)
            color = f'#{opacity:02x}{opacity+40:02x}{opacity+80:02x}'
            
            self.canvas.create_line(
                drop['x'] + wind, drop['y'],
                drop['x'] + wind + drop['length'], drop['y'] + drop['length'] * 0.45,
                fill=color, width=drop['thickness'], capstyle=tk.ROUND, tags='rain'
            )
            
            if random.random() < 0.05:
                splash_color = f'#{int(opacity*0.6):02x}{int((opacity+40)*0.6):02x}{int((opacity+80)*0.6):02x}'
                self.canvas.create_oval(
                    drop['x'] + wind - 1, drop['y'] - 1,
                    drop['x'] + wind + 1, drop['y'] + 1,
                    fill=splash_color, outline='', tags='rain'
                )
    
    #  BOUCLE D'ANIMATION PRINCIPALE #
    def animate(self):
        """Boucle d'animation principale optimisée"""
        self.time += 1
        self.canvas.delete('all')
        
        #  MODE ENSOLEILLÉ #
        if self.weather_mode == 'sunny':
            self.draw_sunny_sky()
            self.draw_sun()
            
            # Nuages blancs
            for cloud in self.white_clouds:
                cloud['x'] += cloud['speed']
                if cloud['x'] > 900:
                    cloud['x'] = -cloud['width'] - 50
                    cloud['y'] = random.randint(50, 200)
                self.draw_white_cloud(cloud)
            
            # Oiseaux
            for bird in self.birds:
                bird['x'] += bird['speed']
                bird['wing_phase'] += 0.15
                if bird['x'] > 900:
                    bird['x'] = -50
                    bird['y'] = random.randint(100, 300)
                self.draw_bird(bird)
        
        #  MODE PLUVIEUX #
        elif self.weather_mode == 'rainy':
            self.draw_rainy_sky()
            
            # Nuages gris
            for cloud in self.clouds:
                cloud['x'] += cloud['speed'] * 0.5
                if cloud['x'] > 900:
                    cloud['x'] = -cloud['width'] - 50
                    cloud['y'] = random.randint(30, 180)
                
                # Nuages gris (pas noirs)
                darkness = 0.4
                base_color = int(80 + darkness * 40)
                num_puffs = 7
                
                for i in range(num_puffs):
                    offset_x = (i - num_puffs/2) * cloud['width'] / (num_puffs + 1)
                    height_factor = 1 - abs(i - num_puffs/2) / (num_puffs/2)
                    offset_y = -height_factor * cloud['height'] / 3
                    
                    size_x = cloud['width'] / 3 * (0.8 + height_factor * 0.4)
                    size_y = cloud['height'] / 2 * (0.7 + height_factor * 0.5)
                    
                    color = f'#{base_color:02x}{base_color:02x}{base_color+20:02x}'
                    
                    self.canvas.create_oval(
                        cloud['x'] + offset_x - size_x,
                        cloud['y'] + offset_y - size_y,
                        cloud['x'] + offset_x + size_x,
                        cloud['y'] + offset_y + size_y,
                        fill=color, outline='#606070', width=1, tags='cloud'
                    )
            
            self.draw_rain_only()
        
        #  MODE ORAGEUX #
        else:
            # Fond orageux
            for i in range(25):
                intensity = 12 + i * 2.5
                
                if self.flash_intensity > 0:
                    flash_add = int(self.flash_intensity * 180)
                    r = min(255, int(intensity + flash_add * 0.8))
                    g = min(255, int(intensity + flash_add * 0.9))
                    b = min(255, int(intensity + 22 + flash_add))
                    color = f'#{r:02x}{g:02x}{b:02x}'
                else:
                    color = f'#{int(intensity):02x}{int(intensity):02x}{int(intensity+22):02x}'
                
                self.canvas.create_rectangle(
                    0, i*36, 800, (i+1)*36,
                    fill=color, outline='', tags='bg'
                )
            
            if self.flash_intensity > 0:
                self.flash_intensity -= 0.05
                if self.flash_intensity < 0:
                    self.flash_intensity = 0
            
            # Nuages sombres
            for cloud in self.clouds:
                cloud['x'] += cloud['speed'] * (0.5 + cloud['depth'] * 0.5)
                if cloud['x'] > 900:
                    cloud['x'] = -cloud['width'] - 50
                    cloud['y'] = random.randint(30, 180)
                self.draw_dark_cloud(cloud)
            
            self.draw_stormy_rain()
            
            # Éclairs
            if random.random() < 0.04:
                self.lightnings.append(self.create_lightning())
                self.flash_intensity = random.uniform(0.45, 0.75)
            
            remaining_lightnings = []
            for lightning in self.lightnings:
                if lightning['life'] > 0:
                    self.draw_lightning(lightning)
                    lightning['life'] -= 1
                    remaining_lightnings.append(lightning)
            self.lightnings = remaining_lightnings
        
        # Dessiner l'interface appropriée
        if self.current_screen == 'menu':
            self.draw_menu()
        elif self.current_screen == 'difficulty':
            self.draw_difficulty_menu()
        elif self.current_screen == 'game':
            self.draw_game_ui()
        
        self.root.after(35, self.animate)


if __name__ == "__main__":
    root = tk.Tk()
    game = LightningTicTacToe(root)
    root.mainloop()