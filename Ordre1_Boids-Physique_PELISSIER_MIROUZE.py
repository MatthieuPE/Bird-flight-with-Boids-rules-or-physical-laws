import pygame
from random import randint, uniform
from math import sqrt
import numpy as np
import matplotlib.pyplot as plt

# === Paramètre affichage ===

FPS=100
SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 650, 650 #Taille écran
BORDER = 50 #taille bord
COLOR1 = (255, 255, 255) #couleur bord
COLOR2 = (0,0,0) # Couleur intérieur

# === Paramètres système ===

MAX_VELOCITY = 5 #Vitesse maximale
NUM_BOIDS = 100 #Nombres d'oiseaux simulés

VISION = 100 #distance à laquelle les oiseaux se voient
DISTCRIT = 50 #distance à partir de laquelle les oiseaux se repoussent

FORCE = 0.01 #coefficient force

# === Caractéristiques oiseaux ===
        
class Oiseau(pygame.sprite.Sprite): 

    def __init__(self, x, y):
        
        super().__init__() #Appel init de la classe mère pygame.sprite.Sprite
        # et l'applique à Oiseau, donc self
        self.image = pygame.Surface([6, 6]) #crée surface de dimension [a,b]
        self.image.fill("red")  # Remplit la surface de couleur
     
        #positionne l'image aux coord (x,y)
        self.rect = self.image.get_rect(center=(x,y)) 
        
        #genere vitesse alétoire bornée par Max_velocity selon chaque axe 
        self.velocityX = uniform(-MAX_VELOCITY, MAX_VELOCITY) 
        self.velocityY = uniform(-MAX_VELOCITY, MAX_VELOCITY) 
        
        # On définit une position pouvant prendre des valeurs décimales:
        self.positionX=x
        self.positionY=y
        
    
    #Calcule distance sur l'axe des X, orientée de self vers oiseau
    def distanceX(self, oiseau): 
        #distance vers oiseau
        distX = oiseau.positionX - self.positionX
        #verifie si oiseau pas plus proche via le bord
        if abs(distX)>=SCREEN_WIDTH-2*BORDER-abs(distX): 
            #si c'est le cas pointe vers à travers le bord
            return distX - (SCREEN_WIDTH-2*BORDER)*np.sign(distX)
        else: return distX
    
    
    #Calcule distance sur l'axe des X, orientée de self vers oiseau
    def distanceY(self, oiseau):
        distY = oiseau.positionY - self.positionY
        if abs(distY)>=SCREEN_HEIGHT-2*BORDER-abs(distY):
            return distY - (SCREEN_HEIGHT-2*BORDER)*np.sign(distY)
        else: return distY
        
        
    #Calcule distance algébrique entre self et oiseau
    def distance(self, oiseau):
        return sqrt(self.distanceX(oiseau)**2+self.distanceY(oiseau)**2)


    #Force subie par l'oiseau par influence des oiseaux de oiseau_list
    def acceleration(self, oiseau_list):  
        ForceX = 0
        ForceY = 0 
        for oiseau in oiseau_list: 
            xdiff = self.distanceX(oiseau)
            ydiff = self.distanceY(oiseau)
            distance = sqrt(xdiff**2+ydiff**2)
            if distance!=0:
                #stocke force exercée par chaque oiseau sur self
                ForceX -= -xdiff*(1-DISTCRIT/distance) 
                ForceY -= -ydiff*(1-DISTCRIT/distance)
    
        #modification de la vitesse par la force
        self.velocityX += ForceX * FORCE
        self.velocityY += ForceY * FORCE
        
        
    #Loi non physique, utile pour simuler plus esthétiquement des oiseaux
    #Permet de faire voler self aligné avec les oiseaux de oiseau_list
    def move_with(self, oiseau_list):
        avgX = 0
        avgY = 0
        for oiseau in oiseau_list:
            avgX += oiseau.velocityX 
            avgY += oiseau.velocityY

        # avgX est la moyenne des composantes des vitesses selon X des oiseaux
        # de oiseau_list. Idem selon Y pour avgY.
        avgX /= len(oiseau_list) 
        avgY /= len(oiseau_list)
        
        #On modifie la vitesse de self pour l'aligner avec le groupe.
        self.velocityX += (avgX/40)
        self.velocityY += (avgY/40)
   
        
    #Fonction pour update la position pour des oiseaux, lorsqu'on souhaite
    #utiliser move_with.
    def update(self): 
        #Necessaire pour eviter la divergence de la vitesse avec move_with.
        #On vérifie que la vitesse ne dépasse pas MAX_VELOCITY.
        if abs(self.velocityY) >= MAX_VELOCITY or abs(self.velocityX) >= MAX_VELOCITY:
             scaleFactor = MAX_VELOCITY / max(abs(self.velocityY), abs(self.velocityX))
             #on ajuste la composante trop grande à Max velocity, 
             #et l'autre garde la proportion (pour garder direction).  
             self.velocityY *= scaleFactor
             self.velocityX *= scaleFactor 
        
        #On déplace l'oiseau selon sa vitesse.
        self.positionX += self.velocityX 
        self.positionY += self.velocityY  

        #Si l'oiseau dépasse un bord on modifie sa position de l'autre côté.
        if self.positionX < BORDER: #bords
            self.positionX += SCREEN_WIDTH - 2*BORDER
        if self.positionX > SCREEN_WIDTH - BORDER:
            self.positionX -= SCREEN_WIDTH - 2*BORDER
        if self.positionY < BORDER:
            self.positionY += SCREEN_HEIGHT -2* BORDER
        if self.positionY > SCREEN_HEIGHT - BORDER:
            self.positionY -= SCREEN_HEIGHT - 2*BORDER
          
        # On modifie la position de l'image de l'oiseau sur l'écran.
        self.rect.x = round(self.positionX)
        self.rect.y = round(self.positionY)
        
        
    #Fonction pour update la position pour des oiseaux, lorsqu'on ne souhaite
    #pas utiliser move_with (système physique)
    # Pour l'utiliser changer nom en update et supprimer la première fct update
    def updateV2(self):
      #On déplace l'oiseau selon sa vitesse.
        self.positionX += self.velocityX 
        self.positionY += self.velocityY  
        
         #Si l'oiseau dépasse un bord on modifie sa position de l'autre côté.
        if self.positionX < BORDER:
            self.positionX += SCREEN_WIDTH - 2*BORDER
        if self.positionX > SCREEN_WIDTH - BORDER:
            self.positionX -= SCREEN_WIDTH - 2*BORDER
        if self.positionY < BORDER:
            self.positionY += SCREEN_HEIGHT -2* BORDER
        if self.positionY > SCREEN_HEIGHT - BORDER:
            self.positionY -= SCREEN_HEIGHT - 2*BORDER
            
        #On modifie la position de l'image de l'oiseau sur l'écran.   
        self.rect.x = round(self.positionX)
        self.rect.y = round(self.positionY)


# === Initialisation système ===

#On lance Pygame
pygame.init()
#On crée l'écran aux dimensions choisies
screen = pygame.display.set_mode(SCREEN_SIZE)

#Crée un groupe oiseau
oiseau_list = pygame.sprite.Group()  

# Crée chaque oiseaux
for i in range(NUM_BOIDS):
    #Les positionne aléatoirement sur l'écran
    oiseau = Oiseau(randint(BORDER, SCREEN_WIDTH-BORDER), randint(BORDER, SCREEN_HEIGHT-BORDER))
    #Ajoute l'oiseau au groupe 
    oiseau_list.add(oiseau)


# === Simulation ===

#Crée une horloge
clock = pygame.time.Clock()

#initialise la simulation
running = True

#Datas que l'on pourrait vouloir stocker
DIST_MOY=[]
VITX_MOY=[]; VITY_MOY=[]
NRJ=[]
E_POT=[]


while running and len(DIST_MOY)<5000:
    
    #Securité pour pouvoir arrêter le programme
    for event in pygame.event.get(): 
        #Si on stoppe pygame on stoppe la simulation
        if event.type == pygame.QUIT: 
            running = False
        #Si on appuie sur une touche vérifie si on veut quitter le programme
        if event.type == pygame.KEYDOWN: 
            #Si on appuie sur ECHAP on arrête le programme
            if event.key == pygame.K_ESCAPE:
                running = False
    
# ==== Degré1 ===== : 
    
    #On regarde tous les oiseaux
    for oiseau in oiseau_list:
        closeBoids=[]
        #Pour chaque oiseau on trouve ceux qu'il peut voir
        for otherBoid in oiseau_list:
            #il ne se voit pas lui même
            if otherBoid == oiseau: continue 
            #Si les autres oiseaux sont plus près que VISION alors il les voit
            if oiseau.distance(otherBoid) < VISION: 
                closeBoids.append(otherBoid)
        
        #Si l'oiseau ne voit personne alors il ne subie pas de force
        if len(closeBoids)>0:
            #Sinon on lui applique acceleration pour tous les oiseaux proches
            oiseau.acceleration(closeBoids)
            #On peut aussi lui appliquer move_with (système non physique)
            oiseau.move_with(closeBoids)
    
    #Une fois toutes les vitesses des oiseaux modifiées, on update 
    # leur positions simultanément.
    oiseau_list .update() 


# ==== Graphiques ==== :
    
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
    
    DIST_MOY.append(moy)
    VITX_MOY.append(vitx); VITY_MOY.append(vity)
    NRJ.append(nrj)
    E_POT.append(e_pot)

    # === Affichage ===:
    
    #On affiche les bords et le fond
    screen.fill(COLOR1) 
    Bord=pygame.draw.rect(screen,COLOR2,pygame.Rect(BORDER,BORDER,SCREEN_WIDTH-2*BORDER,SCREEN_HEIGHT-2*BORDER))
    
    # On affiche tous les oiseaux
    oiseau_list .draw(screen) 

    # On met à jour l'écran
    pygame.display.update() #met à jour tout l'écran

    # Règle la vitesse d'affichage
    clock.tick(FPS)

#=== Plots === : 

DIST_MOY=np.array(DIST_MOY)
VITX_MOY=np.array(VITX_MOY); VITY_MOY=np.array(VITY_MOY)
NRJ=np.array(NRJ); E_POT=np.array(E_POT)

DIST_MOY/=(NUM_BOIDS-1)*NUM_BOIDS
VITX_MOY/=NUM_BOIDS; VITY_MOY/=NUM_BOIDS

plt.figure(1)
plt.plot(DIST_MOY)
plt.ylabel('Distance moyenne'); plt.xlabel('Temps')
plt.savefig("Oiseau_o1_dist_moy2", format='pdf',dpi=1000)

plt.figure(2)
plt.plot(VITX_MOY,label='Impulsion totale selon x'); plt.plot(VITY_MOY,label='Impulsion totale selon y')
plt.legend()
plt.ylabel('Impulsion totale'); plt.xlabel('Temps')
plt.savefig("Oiseau_o1_impulsion", format='pdf',dpi=1000)

plt.figure(3)
plt.plot(NRJ,'r',label='Cinétique'); plt.plot(E_POT,'b',label='Potentielle')
plt.plot(NRJ+E_POT,'y',label='Mécanique')
plt.legend(); 
plt.ylabel('Energie'); plt.xlabel('Temps')
plt.savefig("Oiseau_o1_Energie", format='pdf',dpi=1000)


# === Fin ===
#permet de fermer pygame, si par exemple on veut  faire un autre programme
pygame.quit() 