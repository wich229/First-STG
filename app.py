# space_shooting_game

# Import and initialize the pygame library
import pygame
import random
import os

pygame.init()
pygame.mixer.init() 

FPS = 60 # frames per second
WIDTH = 500
HEIGHT = 600

# insert images 
background_img = pygame.image.load(os.path.join("img", "background.png"))
player_img = pygame.image.load(os.path.join("img", "player.png"))
bullet_img = pygame.image.load(os.path.join("img", "bullet.png"))

def startGameinit():
    screen.blit(background_img, (0,0))
    drawText(screen, "Space Shooter", 55, WIDTH / 2, HEIGHT / 3)
    drawText(screen, "← → for move", 20, WIDTH / 2, (HEIGHT / 3) + 100)
    drawText(screen, "any button for START", 15, WIDTH / 2, (HEIGHT / 3) + 150)
    pygame.display.update()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                waiting = False

# life points images
playerLife_img = pygame.transform.scale(player_img, (25,18))
def lifePointImage(surf, times, img, x, y):
    for i in range(times):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)


# differnt stones images can be run
stonesImgsList = []
for i in range(7):
     stonesImgsList.append(pygame.image.load(os.path.join("img", f"rock{i}.png")))

# explorsion animation
# bullet hit the stone (large) - expl
# stone hit the player (small) - expl
explAnimDic ={
    "large" : [], "small" : [], "die" : []
}
for i in range(9):
    expl_img = pygame.image.load(os.path.join("img", f"expl{i}.png"))
    explPlayer_img = pygame.image.load(os.path.join("img", f"player_expl{i}.png"))
    explPlayerDie_img = pygame.image.load(os.path.join("img", f"player_expl{i}.png"))
    explAnimDic["large"].append(pygame.transform.scale(expl_img,(75,75)))
    explAnimDic["small"].append(pygame.transform.scale(explPlayer_img,(30,30)))
    explAnimDic["die"].append(explPlayerDie_img)

# bonus
bonus_imgs = {}
bonus_imgs["gun"] = pygame.image.load(os.path.join("img", "gun.png"))

# insert text
fontName = pygame.font.match_font("arial")
def drawText(surf, text, size, x, y):
    font = pygame.font.Font(fontName,size)
    textSurface = font.render(text,True,(255,255,255))
    textRect = textSurface.get_rect()
    textRect.centerx = x
    textRect.centery = y
    surf.blit(textSurface , textRect)

# add life bar
def lifeBar(surf, hp, x, y):
    if hp < 0:
        hp = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (hp/100) * BAR_LENGTH
    outlineRect = pygame.Rect(x , y , BAR_LENGTH , BAR_HEIGHT)
    fillRect = pygame.Rect(x , y , fill , BAR_HEIGHT)
    pygame.draw.rect(surf , (0,255,0), fillRect)
    pygame.draw.rect(surf , (255,255,255), outlineRect, 2)

# impore sounds
#background Music
pygame.mixer.music.load(os.path.join("sound", "background.ogg"))
pygame.mixer.music.set_volume(0.5)

shootingSound = pygame.mixer.Sound(os.path.join("sound", "shoot.wav"))
gunSound = pygame.mixer.Sound(os.path.join("sound", "pow1.wav"))
DieSound = pygame.mixer.Sound(os.path.join("sound", "rumble.ogg"))
stoneExplSoundList = [
    pygame.mixer.Sound(os.path.join("sound", "expl0.wav")),
    pygame.mixer.Sound(os.path.join("sound", "expl1.wav"))
]

# window setting
pygame.display.set_caption("My first STG ")
pygame.display.set_icon(explPlayerDie_img)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# game object (player)
class Player(pygame.sprite.Sprite):
    # Constructor. Pass in the color of the block,
    def __init__(self):
       pygame.sprite.Sprite.__init__(self)
       # Create an image of the block, and fill it with a color.
       #self.image = pygame.Surface((50, 50))    # test
       self.image = pygame.transform.scale(player_img, (50,38))
       # self.image.fill((0,0,255))     # test
       # Update the position of this object by setting the values of rect.x and rect.y
       self.rect = self.image.get_rect()
       self.radius = 21
       # pygame.draw.circle(self.image,(255,0,0), self.rect.center, self.radius)      # test
       self.rect.centerx = WIDTH / 2
       self.rect.bottom = HEIGHT - 20
       self.life = 100
       self.life_point = 3
       self.hidden = False
       self.hideTime  = 0
       self.gunType = 1
       self.catchTime_gun = 0
              

    # moving action
    def update(self):
        nowTime = pygame.time.get_ticks()
        if self.gunType > 1 and nowTime - self.catchTime_gun > 5000:
            self.gunType = 1
            self.catchTime_gun = nowTime

        if self.life_point > 0 and self.hidden and pygame.time.get_ticks() -self.hideTime > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 20

        keyPressed = pygame.key.get_pressed()
        if keyPressed[pygame.K_RIGHT]:
            self.rect.x += 10
        if keyPressed[pygame.K_LEFT]:
            self.rect.x -= 10
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
    
    # shooting function
    def shoot(self):
        if not(self.hidden):
            if self.gunType == 1:
                bullet = Bullet(self.rect.centerx,self.rect.top)
                allGameItems.add(bullet)
                allBullets.add(bullet)
            else:
                bullet1 = Bullet(self.rect.left,self.rect.centery)
                bullet2 = Bullet(self.rect.right,self.rect.centery)
                allGameItems.add(bullet1)
                allGameItems.add(bullet2)
                allBullets.add(bullet1)
                allBullets.add(bullet2)
                
    
    # die and hiding
    def hide(self):
        self.hidden = True
        self.hideTime = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2 , HEIGHT + 500)
    
    def gunUpgrad(self):
        self.gunType += 1
        self.catchTime_gun = pygame.time.get_ticks()

# game object (bullets)
class Bullet(pygame.sprite.Sprite):
    
    def __init__(self, x, y):
       pygame.sprite.Sprite.__init__(self)
       self.image = bullet_img
    #    self.image = pygame.Surface((6,12))
    #    self.image.fill((255,0,0))
       self.rect = self.image.get_rect()
       self.rect.centerx = x
       self.rect.centery = y
       self.speedy = -10

    # moving action
    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

# game object (stones)
class Stone(pygame.sprite.Sprite):
 
    def __init__(self):
       pygame.sprite.Sprite.__init__(self)
       self.OriImage = random.choice(stonesImgsList)
       self.image = self.OriImage.copy()
    #    self.image = pygame.Surface((30,30))
    #    self.image.fill((118,118,118))
       self.rect = self.image.get_rect()
       self.radius = int(self.rect.width * 0.8 / 2)
    #    pygame.draw.circle(self.image,(255,0,0), self.rect.center, self.radius)    # test 
       self.rect.x = random.randrange(0,WIDTH)
       self.rect.y = random.randrange(-180, 100   )
       self.speedy = random.randrange(2, 6)
       self.speedx = random.randrange(-3, 3)
       self.totalDegree = 0
       self.rotDegree = random.randrange(-3, 3)
    
    # stones rotating
    def rotate(self):
        self.totalDegree += self.rotDegree
        self.totalDegree  = self.totalDegree  % 360
        self.image = pygame.transform.rotate(self.OriImage, self.totalDegree )
        # reset the center position to resolve shaking
        stoneOriCenter = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = stoneOriCenter

    # moving action
    def update(self):
        self.rotate()
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT:
            self.rect.x = random.randrange(0,WIDTH)
            self.rect.y = random.randrange(-50, 0)
            self.speedy = random.randrange(2, 10)
            self.speedx = random.randrange(-3, 3)
        elif self.rect.right < 0 or self.rect.left > WIDTH:
            self.rect.x = random.randrange(0,WIDTH)
            self.rect.y = random.randrange(-50, 0)
            self.speedy = random.randrange(2, 10)
            self.speedx = random.randrange(-3, 3)

class Bonus(pygame.sprite.Sprite):
    
    def __init__(self, center):
       pygame.sprite.Sprite.__init__(self)
       self.type = "gun"  # can add more and change to random in the future
       self.image = bonus_imgs[self.type]
       self.rect = self.image.get_rect()
       self.rect.center = center
       self.speedy = 3

    # moving action
    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill()

# game object (explosion)
class Explosion(pygame.sprite.Sprite):
    
    def __init__(self, center, size):
       pygame.sprite.Sprite.__init__(self)
       self.size = size
       self.image = explAnimDic[self.size][0]
       self.rect = self.image.get_rect()
       self.rect.center = center
       self.frame = 0
       self.lastUadate = pygame.time.get_ticks()
       self.frameRate = 200

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.lastUadate > self.frameRate:
            self.frame += 1            
            if self.frame < len(explAnimDic[self.size]):
                self.image = explAnimDic[self.size][self.frame]
                center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = center
            else:
                self.kill()

#add back stones
def addBackStone():
    stone = Stone()
    allGameItems.add(stone)
    allStones.add(stone)

# group all the game objects
# allGameItems = pygame.sprite.Group()
# player = Player()
# allGameItems.add(player)

# # group all the stones and the bullets
# allStones = pygame.sprite.Group()
# allBullets = pygame.sprite.Group()
# allBonus = pygame.sprite.Group()


# # adding 10 stones at once
# for num in range(11):
#     addBackStone()

# score = 0

pygame.mixer.music.play(-1)

# game loop: 
# process input => update game => render => amount of time and back to the loop
# game initialize
startPg = True
running = True
while running:
    if startPg:
        startGameinit()
        startPg = False
        allGameItems = pygame.sprite.Group()
        player = Player()
        allGameItems.add(player)
        # group all the stones and the bullets
        allStones = pygame.sprite.Group()
        allBullets = pygame.sprite.Group()
        allBonus = pygame.sprite.Group()
        # adding 10 stones at once
        for num in range(11):
            addBackStone()
        score = 0

    clock.tick(FPS)
    # get the user input
    # https://riptutorial.com/pygame/example/18046/event-loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
                shootingSound.play()

    # update into the game
    allGameItems.update()
    # find collisions between all the Sprites in two groups.
    hitsDic = pygame.sprite.groupcollide(allStones, allBullets, True, True) # return dictionary
    # add back the stone that been shooting down
    for num in hitsDic:
        random.choice(stoneExplSoundList).play() 
        score += num.radius
        explAnimate_SB = Explosion(num.rect.center,"large")
        allGameItems.add(explAnimate_SB)
        if random.random() > 0.97:
            power = Bonus(num.rect.center)
            allGameItems.add(power)
            allBonus.add(power)

        addBackStone()
        if player.life > 0 and player.life < 100:
            player.life += 0.2 
            if player.life > 100:
               player.life = 100
            if player.life_point < 3:
                player.life_point += 1 
    
    get_bonus = pygame.sprite.spritecollide(player, allBonus, True)
    for catch in get_bonus:
        if catch.type == "gun":
            gunSound.play()
            player.gunUpgrad()

    hitEnd = pygame.sprite.spritecollide(player, allStones, True, pygame.sprite.collide_circle) # return list
    for amount in hitEnd:
        addBackStone()
        player.life -= amount.radius
        explAnimate_PS = Explosion(amount.rect.center,"small")
        random.choice(stoneExplSoundList).play() 
        allGameItems.add(explAnimate_PS)
        if player.life <= 0: 
            player.life_point -= 1
            player.life = 100
            die = Explosion(player.rect.center,"die")
            allGameItems.add(die)
            DieSound.play()
            player.hide()

    if player.life_point == 0 and not(die.alive()):
        # running = False
        startPg = True

    # update on the window
    # Fill the background with black
    screen.fill((0, 0, 0))
    # insert the background image
    screen.blit(background_img, (0,0))
    allGameItems.draw(screen)
    drawText(screen, str(score), 18, (WIDTH / 2), 10 )
    lifeBar(screen, player.life, 10, 10)
    lifePointImage(screen, player.life_point, playerLife_img, WIDTH - 100, 10)
    pygame.display.update()

pygame.quit()