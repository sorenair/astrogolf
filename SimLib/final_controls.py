import pygame as pg

def click(animate):
    self = animate

    mouse_pos = pg.mouse.get_pos()
    if self.menu and (self.menu_page == 0):
        if self.levels_btn_hbox.collidepoint(mouse_pos):
            self.menu_page = 1
            if not self.mute:
                sfx = pg.mixer.Sound("Assignments/final/sfx/sfx_interface/menu_pause_01.wav")
                sfx.set_volume(1)
                sfx.play(loops=0)
        elif self.extra_btn_hbox.collidepoint(mouse_pos):
            if self.beat_game:
                self.lvl = 10
                self.jetpack_en = True
                self.render.bg = pg.image.load("Assignments/final/sprites/bgs/bg_bh.png")
                self.level_select()
                if not self.mute:
                    sfx = pg.mixer.Sound("Assignments/final/sfx/sfx_interface/menu_confirm_01.wav")
                    sfx.set_volume(0.7)
                    sfx.play(loops=0)
            else:
                if not self.mute:
                    sfx = pg.mixer.Sound("Assignments/final/sfx/sfx_interface/menu_cancel_01.wav")
                    sfx.set_volume(0.7)
                    sfx.play(loops=0)
    elif self.menu and (self.menu_page != 3):
        if self.pg_right_btn_hbox.collidepoint(mouse_pos):
            self.menu_page += 1
            if not self.mute:
                sfx = pg.mixer.Sound("Assignments/final/sfx/sfx_interface/menu_pause_01.wav")
                sfx.set_volume(1)
                sfx.play(loops=0)
        elif self.pg_left_btn_hbox.collidepoint(mouse_pos):
            self.menu_page -= 1
            if not self.mute:
                sfx = pg.mixer.Sound("Assignments/final/sfx/sfx_interface/menu_pause_01.wav")
                sfx.set_volume(1)
                sfx.play(loops=0)
    else:
        # get a list of all sprites that are under the mouse cursor
        clicked_sprites = [s for s in self.render.menu_sprites if s.rect.collidepoint(mouse_pos)]
        # do something with the clicked sprites...
        if len(clicked_sprites) > 0:
            self.menu = True
            self.menu_page = 0
            self.lvl = 0
            self.started = False
            self.play = False
            self.velocity = 0
            self.angle = 0
            if not self.beat_game:
                self.jetpack_en = False

            # Play sound effect
            if not self.mute:
                sfx = pg.mixer.Sound("Assignments/final/sfx/sfx_interface/menu_pause_01.wav")
                sfx.set_volume(1)
                sfx.play(loops=0)

def jetpack_controls(animate, event):
    self = animate

    if (event.key == pg.K_a):
        self.model.gphobjects.state[0,3] -= 1
        if not (self.lvl == 10):
            self.jetfuel -= 10
        self.update_fuelbar()
    if (event.key == pg.K_d):
        self.model.gphobjects.state[0,3] += 1
        if not (self.lvl == 10):
            self.jetfuel -= 10
        self.update_fuelbar()
    if (event.key == pg.K_w):
        self.model.gphobjects.state[0,5] -= 1
        if not (self.lvl == 10):
            self.jetfuel -= 10
        self.update_fuelbar()
    if (event.key == pg.K_s):
        self.model.gphobjects.state[0,5] += 1
        if not (self.lvl == 10):
            self.jetfuel -= 10
        self.update_fuelbar()
    
    if self.lvl == 10:
        if (event.key == pg.K_LEFT):
            self.model.gphobjects.state[1,3] -= 1
            if not (self.lvl == 10):
                self.jetfuel -= 10
            self.update_fuelbar()
        if (event.key == pg.K_RIGHT):
            self.model.gphobjects.state[1,3] += 1
            if not (self.lvl == 10):
                self.jetfuel -= 10
            self.update_fuelbar()
        if (event.key == pg.K_UP):
            self.model.gphobjects.state[1,5] -= 1
            if not (self.lvl == 10):
                self.jetfuel -= 10
            self.update_fuelbar()
        if (event.key == pg.K_DOWN):
            self.model.gphobjects.state[1,5] += 1
            if not (self.lvl == 10):
                self.jetfuel -= 10
            self.update_fuelbar()