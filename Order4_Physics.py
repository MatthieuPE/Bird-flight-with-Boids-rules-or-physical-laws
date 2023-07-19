import pygame
from random import randint, uniform
from math import sqrt
import numpy as np
import matplotlib.pyplot as plt

# === Interface ===

FPS=100 # vitesse d'affichage
h=0.9 # pas de temps
SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 700, 700
# doit être carré si la vision des oiseaux porte loin
BORDER = 50 # épaisseur bordure de l'écran
COLOR1 = (255, 255, 255) #RGB extérieur
COLOR2 = (0,0,0) # Intérieur

# === Variables ===

MAX_VELOCITY = 5 # vitesse initiale maximale
NUM_BOIDS = 100

VISION = 100 #distance à laquelle les oiseaux se voient
DISTCRIT = 50 #distance à partir de laquelle les oiseaux se repoussent

FORCE = 0.1 # coefficient force
FROTT=0.01 # coeff frottement

# === construction oiseaux ===
        
class Oiseau(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__() # appelle init de la classe mère, donc de pygame.sprite.Sprite
        # et l'applique à oiseau, donc self
        
        #self.image = pygame.image.load("oiseaux.png").convert() # image remplissant le bloc
        self.image = pygame.Surface([6, 6]) # crée une surface
        self.image.fill("red")  # couleur oiseau
     
        # Crée un rectangle avec les dimensions de l'image:
        self.rect = self.image.get_rect(center=(x,y))
        # rect nécessairement ce nom car utilisé par draw

        self.velocityX = uniform(-MAX_VELOCITY, MAX_VELOCITY) #genere vitesse alétoire, non entière
        self.velocityY = uniform(-MAX_VELOCITY, MAX_VELOCITY) 
        # nom velocityX/Y n'importe pas
        
        # On définit une position non entière:
        self.positionX=x
        self.positionY=y
        
        # On définit l'accélération :
        self.acc=[]
        
        # Positions initiales pour calcul du travail
        self.positinitX=0
        self.positinitY=0
        
    def distanceX(self, oiseau):
        distX = oiseau.positionX - self.positionX
        if abs(distX)>=SCREEN_WIDTH-2*BORDER-abs(distX):
            return distX - (SCREEN_WIDTH-2*BORDER)*np.sign(distX)
        else: return distX
    
    def distanceY(self, oiseau):
        distY = oiseau.positionY - self.positionY
        if abs(distY)>=SCREEN_HEIGHT-2*BORDER-abs(distY):
            return distY - (SCREEN_HEIGHT-2*BORDER)*np.sign(distY)
        else: return distY
    
    def distance(self, oiseau):
        return sqrt(self.distanceX(oiseau)**2+self.distanceY(oiseau)**2)


    def acceleration(self, oiseau_list):
        
        ForceX = 0
        ForceY = 0

        for oiseau in oiseau_list:

            xdiff = self.distanceX(oiseau)
            ydiff = self.distanceY(oiseau)
            distance = sqrt(xdiff**2+ydiff**2)

            ForceX -= -xdiff*(1-DISTCRIT/distance) # force harmonique
            ForceY -= -ydiff*(1-DISTCRIT/distance)
    
        #frottements incorporés:
        return (ForceX*FORCE-FROTT*self.velocityX,ForceY*FORCE-FROTT*self.velocityY)  
            
    
    def update(self,i):
        
        # RK4:
        if i==0:
            self.positinitX = self.positionX
            self.positinitY = self.positionY
            
            self.positionX += h*self.velocityX/2
            self.positionY += h*self.velocityY/2
            self.velocityX += h*self.acc[0][0]/2
            self.velocityY += h*self.acc[0][1]/2
        elif i==1:
            self.positionX += h**2 * self.acc[0][0]/4
            self.positionY += h**2 * self.acc[0][1]/4
            self.velocityX += h*(self.acc[1][0]-self.acc[0][0])/2
            self.velocityY += h*(self.acc[1][1]-self.acc[0][1])/2
        elif i==2:
            self.positionX += h*self.velocityX/2 + h**2 *(self.acc[1][0]-self.acc[0][0])/4
            self.positionY += h*self.velocityY/2 + h**2 *(self.acc[1][1]-self.acc[0][1])/4
            self.velocityX += h*(self.acc[2][0]-self.acc[1][0]/2)
            self.velocityY += h*(self.acc[2][1]-self.acc[1][1]/2)
        else:
            self.positionX += h**2 * (self.acc[0][0]-2*self.acc[1][0]+self.acc[2][0])/6
            self.positionY += h**2 * (self.acc[0][1]-2*self.acc[1][1]+self.acc[2][1])/6
            self.velocityX += h*(self.acc[0][0]+2*self.acc[1][0]-4*self.acc[2][0]+self.acc[3][0])/6
            self.velocityY += h*(self.acc[0][1]+2*self.acc[1][1]-4*self.acc[2][1]+self.acc[3][1])/6
        
        #Bords:
        if self.positionX < BORDER: 
            self.positionX += SCREEN_WIDTH - 2*BORDER
            self.positinitX += SCREEN_WIDTH - 2*BORDER 
        if self.positionX > SCREEN_WIDTH - BORDER:
            self.positionX -= SCREEN_WIDTH - 2*BORDER
            self.positinitX -= SCREEN_WIDTH - 2*BORDER
        if self.positionY < BORDER:
            self.positionY += SCREEN_HEIGHT -2* BORDER
            self.positinitY += SCREEN_HEIGHT -2* BORDER
        if self.positionY > SCREEN_HEIGHT - BORDER:
            self.positionY -= SCREEN_HEIGHT - 2*BORDER
            self.positinitY -= SCREEN_HEIGHT - 2*BORDER

        # Affichage:
        if i==3:
            self.rect.x = round(self.positionX)
            self.rect.y = round(self.positionY)

# === main ===

# --- init ---

pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)

# --- objets ---

oiseau_list = pygame.sprite.Group() # groupe de sprite: réunit tous les oiseaux

# crée les oiseaux à des positions aléatoires:
for i in range(NUM_BOIDS):
    oiseau = Oiseau(randint(BORDER, SCREEN_WIDTH-BORDER), randint(BORDER, SCREEN_HEIGHT-BORDER))
    oiseau_list.add(oiseau)

# --- mainloop ---

clock = pygame.time.Clock()

running = True

# Servent à l'affichage des graphes:
DIST_MOY=[]
VITX_MOY=[]; VITY_MOY=[]
NRJ=[]
E_POT=[]
TRAV=[]
trav=0.

while running:

    # --- events ---

    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:  # permet de fermer la fenetre 
            running = False
        if event.type == pygame.KEYDOWN: # racourcis clavier
            if event.key == pygame.K_ESCAPE: #echap
                running = False
    
# ======= RK4 ======= :    
    
    for oiseau in oiseau_list: oiseau.acc=[] #initialisation accélérations
    
    for i in range(4):
        for oiseau in oiseau_list:

            # crée la liste des oiseaux proches:
            closeBoids=[]
            for otherBoid in oiseau_list:
                
                if otherBoid == oiseau: continue
                
                if oiseau.distance(otherBoid) < VISION:
                    closeBoids.append(otherBoid)
            
            if len(closeBoids)>0:
                oiseau.acc.append(oiseau.acceleration(closeBoids)) # retourne la valeur de l'accélération
            else: oiseau.acc.append((0,0))
    
        oiseau_list.update(i) # on update tous les paramètres des oiseaux
    
# ======= Graphes ======= :
    
    moy=0.
    vitx=0.; vity=0.
    nrj=0.
    e_pot=0.
    
    for oiseau in oiseau_list:
        closeBoids=[]
        for otherBoid in oiseau_list:
            if otherBoid == oiseau: continue
            distance = oiseau.distance(otherBoid)
            moy+= distance
            if distance < VISION:
                closeBoids.append(otherBoid)
                e_pot+= FORCE*(distance-DISTCRIT)**2/2
            else: e_pot+= FORCE*(VISION-DISTCRIT)**2/2
        
        vx=oiseau.velocityX; vy=oiseau.velocityY
        vitx+= vx; vity+= vy
        nrj+= vx**2 + vy**2
        trav+=2*FROTT*(vx*(oiseau.positionX-oiseau.positinitX)+vy*(oiseau.positionY-oiseau.positinitY))
    
    DIST_MOY.append(moy)
    VITX_MOY.append(vitx); VITY_MOY.append(vity)
    NRJ.append(nrj)
    E_POT.append(e_pot)
    TRAV.append(trav)

    # --- draws ---

    screen.fill(COLOR1) # fond
    Bord=pygame.draw.rect(screen,COLOR2,pygame.Rect(BORDER,BORDER,SCREEN_WIDTH-2*BORDER,SCREEN_HEIGHT-2*BORDER))
    
    oiseau_list.draw(screen) # on dessine tout les oiseaux à leur nouvel emplacement sur le screen
    pygame.display.update() # met à jour tout l'écran

    clock.tick(FPS) # vitesse d'affichage
    # clock.tick_busy_loop(FPS)

DIST_MOY=np.array(DIST_MOY)
VITX_MOY=np.array(VITX_MOY); VITY_MOY=np.array(VITY_MOY)
NRJ=np.array(NRJ); E_POT=np.array(E_POT); TRAV=np.array(TRAV)

DIST_MOY/=(NUM_BOIDS-1)*NUM_BOIDS
VITX_MOY/=NUM_BOIDS; VITY_MOY/=NUM_BOIDS

plt.figure(1)
plt.plot(DIST_MOY); plt.title('Distance')

plt.figure(2)
plt.plot(VITX_MOY,label='x'); plt.plot(VITY_MOY,label='y')
plt.legend(); plt.title('Impulsion')

plt.figure(3)
plt.plot(NRJ,'r',label='Cinétique'); plt.plot(E_POT,'b',label='Potentielle')
plt.plot(NRJ+E_POT,'y',label='Mécanique')
plt.plot(NRJ+E_POT+TRAV,'k',label='E + W')
plt.legend(); plt.title('Energie')

# --- the end ---
pygame.quit() #permet de fermer pygame, si je veux par exemple faire un autre programme
