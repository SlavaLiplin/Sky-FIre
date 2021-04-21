from pygame import *
from random import randint
from time import time as timer 
font.init()
font1 = font.Font(None, 80)
win = font1.render('Mission Completed!', True, (255, 255, 255))
lose = font1.render('Mission Failed!', True, (180, 0, 0))

font2 = font.Font(None, 36)

 
#фоновая музыка
mixer.init()
mixer.music.load('BgSound.ogg')
mixer.music.play()
fire_sound = mixer.Sound('Untitled.ogg')
 
img_back = "Bg.jpeg" # фон игры
img_bullet = "bullet.png" # пуля
img_bullet_r = "bullet_r.png" # пуля вправо
img_bullet_l = "bullet_l.png" # пуля влево
img_hero = "Player.png" # герой
img_enemy = "vrag.png" # враг
img_ast = "m_raketa-removebg-preview.png" # ракета

score = 0 # сбито кораблей
goal = 20 # столько кораблей нужно сбить для победы
lost = 0 # пропущено кораблей
max_lost = 15 # проиграли, если пропустили столько
life = 3  # очки жизни

class GameSprite(sprite.Sprite):
   def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
       sprite.Sprite.__init__(self)

       self.image = transform.scale(image.load(player_image), (size_x, size_y))
       self.speed = player_speed

       self.rect = self.image.get_rect()
       self.rect.x = player_x
       self.rect.y = player_y

   def reset(self):
       window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):

    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

    # метод "выстрел" (используем место игрока, чтобы создать там пулю)
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

    def fire_r(self):
        bullet_r = Bullet(img_bullet_r, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets_r.add(bullet_r)

    def fire_l(self):
        bullet_l = Bullet(img_bullet_l, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets_l.add(bullet_l)
        
        
 
# класс спрайта-врага  
class Enemy(GameSprite):
   # движение врага
   def update(self):
       self.rect.y += self.speed
       global lost
       # исчезает, если дойдет до края экрана
       if self.rect.y > win_height:
           self.rect.x = randint(80, win_width - 80)
           self.rect.y = 0
           lost = lost + 1

# класс спрайта-пули  
class Bullet(GameSprite):

   def update(self):
       self.rect.y += self.speed
       # исчезает, если дойдет до края экрана
       if self.rect.y < 0:
           self.kill()

   def update_r(self):
       self.rect.y += self.speed
       self.rect.x += 15
       # исчезает, если дойдет до края экрана
       if self.rect.y < 0:
           self.kill()

   def update_l(self):
       self.rect.y += self.speed
       self.rect.x -= 15
       # исчезает, если дойдет до края экрана
       if self.rect.y < 0:
           self.kill()
      
# Создаем окошко
win_width = 700
win_height = 500
display.set_caption("Sky Fire")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))
# создаем спрайты
ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)

# создание группы спрайтов-врагов
monsters = sprite.Group()
for i in range(1, 6):
   monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
   monsters.add(monster)

# создание группы спрайтов-ракет 
asteroids = sprite.Group()
for i in range(1, 3):
    asteroid = Enemy(img_ast, randint(30, win_width - 30), -40, 80, 50, randint(1, 7))
    asteroids.add(asteroid)

  
bullets = sprite.Group()
bullets_r = sprite.Group()
bullets_l = sprite.Group()

# переменная "игра закончилась": как только там True, в основном цикле перестают работать спрайты
finish = False
# Основной цикл игры:
run = True # флаг сбрасывается кнопкой закрытия окна

rel_time = False # флаг отвечающий за перезарядку

num_fire = 0  # переменная для подсчта выстрела          

while run:

    # событие нажатия на кнопку Закрыть
    for e in event.get():
        if e.type == QUIT:
            run = False
        # событие нажатия на пробел - спрайт стреляет
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                    # проверяем сколько выстеров сделано и не происходит ли перезарядка
                    if num_fire < 15 and rel_time == False:
                        num_fire = num_fire + 1
                        fire_sound.play()
                        ship.fire()

                    if num_fire  >= 15 and rel_time == False : # если игрок сделал 15 выстрелов
                        last_time = timer() # засекаем время, когда это произошло
                        rel_time = True # ставим флаг перезарядки

        # выстрел пули влево
            if e.key == K_v:
                    # проверяем сколько выстеров сделано и не происходит ли перезарядка
                    if num_fire < 15 and rel_time == False:
                        num_fire = num_fire + 1
                        fire_sound.play()
                        ship.fire_l()
                       
                    if num_fire  >= 15 and rel_time == False : # если игрок сделал 15 выстрелов
                        last_time = timer() # засекаем время, когда это произошло
                        rel_time = True # ставим флаг перезарядки

        # выстрел пули вправо
            if e.key == K_b:
                    # проверяем сколько выстеров сделано и не происходит ли перезарядка
                    if num_fire < 15 and rel_time == False:
                        num_fire = num_fire + 1
                        fire_sound.play()
                        ship.fire_l()
                       
                    if num_fire  >= 15 and rel_time == False : # если игрок сделал 15 выстрелов
                        last_time = timer() # засекаем время, когда это произошло
                        rel_time = True # ставим флаг перезарядки


    # сама игра: действия спрайтов, проверка правил игры, перерисовка
    if not finish:

        # обновляем фон
        window.blit(background,(0,0))

        # производим движения спрайтов
        ship.update()
        monsters.update()
        asteroids.update()
        bullets.update()
        bullets_r.update()
        bullets_l.update()

        # обновляем их в новом местоположении при каждой итерации цикла
        ship.reset()
        monsters.draw(window)
        asteroids.draw(window)
        bullets.draw(window)
        bullets_r.draw(window)
        bullets_l.draw(window)



        # перезарядка
        if rel_time == True:
            now_time = timer() # считываем время
         
            if now_time - last_time < 3: # пока не прошло 3 секунды выводим информацию о перезарядке
                reload = font2.render('Перезарядка', 1, (150, 0, 0))
                window.blit(reload, (260, 460))
            else:
                num_fire = 0   # обнуляем счетчик пуль
                rel_time = False # сбрасываем флаг перезарядки

        # проверка столкновения пули и врага (и врага, и пуля при касании исчезают)
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            # этот цикл повторится столько раз, сколько врагов подбито
            score = score + 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)


        # если спрайт коснулся врага уменьшает жизнь
        if sprite.spritecollide(ship, monsters, False) or sprite.spritecollide(ship, asteroids, False):
            sprite.spritecollide(ship, monsters, True) 
            sprite.spritecollide(ship, asteroids, True)
            life = life -1

        #проигрыш
        if life == 0 or lost >= max_lost:
            finish = True # проиграли, ставим фон и больше не управляем спрайтами.
            window.blit(lose, (200, 200))


        # проверка выигрыша: сколько очков набрали?
        if score >= goal:
            finish = True
            window.blit(win, (200, 200))

        # пишем текст на экране
        text = font2.render("Счет: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))

        text_lose = font2.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        # задаем разный цвет в зависимости от кол-ва жизней
        if life == 3:
            life_color = (0, 150, 0)
        if life == 2:
            life_color = (150, 150, 0)
        if life == 1:
            life_color = (150, 0, 0)

        
        text_life = font1.render(str(life), 1, life_color)
        window.blit(text_life, (650, 10))

        display.update()

    # автоматический перезапуск игры
    else:
        finish = False
        score = 0
        lost = 0
        num_fire = 0
        life = 3
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()
        for a in asteroids:
            a.kill()    
      

        time.delay(45)
        for i in range(1, 6):
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)
        for i in range(1, 3):
            asteroid = Enemy(img_ast, randint(30, win_width - 30), -40, 80, 50, randint(1, 7))
            asteroids.add(asteroid)    

        

    time.delay(45)
