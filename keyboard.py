<<<<<<< HEAD
import pygame as pg

# 初期化処理・グローバル変数
scale_factor = 2
chip_s = int(24 * scale_factor)  # マップチップ基本サイズ
map_s = pg.Vector2(16, 9)        # マップの横・縦の配置数

# PlayerCharacterクラスの定義
class PlayerCharacter:

  def __init__(self, name, init_pos, img_path):
    self.pos = pg.Vector2(init_pos)
    self.size = pg.Vector2(24, 32) * scale_factor
    self.dir = 2
    self.name = name
    img_raw = pg.image.load(img_path)
    self.__img_arr = []
    for i in range(4):
      self.__img_arr.append([])
      for j in range(3):
        p = pg.Vector2(24 * j, 32 * i)
        tmp = img_raw.subsurface(pg.Rect(p, (24, 32)))
        tmp = pg.transform.scale(tmp, self.size)
        self.__img_arr[i].append(tmp)
      self.__img_arr[i].append(self.__img_arr[i][1])

    self.is_moving = False
    self.__moving_vec = pg.Vector2(0, 0)
    self.__moving_acc = pg.Vector2(0, 0)

  def turn_to(self, dir):
    self.dir = dir

  def move_to(self, vec):
    self.is_moving = True
    self.__moving_vec = vec.copy()
    self.__moving_acc = pg.Vector2(0, 0)
    self.update_move_process()

  def update_move_process(self):
    assert self.is_moving
    self.__moving_acc += self.__moving_vec * 3
    if self.__moving_acc.length() >= chip_s:
      self.pos += self.__moving_vec
      self.is_moving = False

  def get_dp(self):
    dp = self.pos * chip_s - pg.Vector2(0, 12) * scale_factor
    if self.is_moving:
      dp += self.__moving_acc
    return dp

  def get_img(self, frame):
    return self.__img_arr[self.dir][frame // 6 % 4]


# ゲームループを含むメイン処理
def main():
  pg.init()
  pg.display.set_caption('Keyboard Control Test')
  disp_w = int(chip_s * map_s.x)
  disp_h = int(chip_s * map_s.y)
  screen = pg.display.set_mode((disp_w, disp_h))
  clock = pg.time.Clock()
  frame = 0
  exit_flag = False

  # キャラ生成
  reimu = PlayerCharacter('reimu', (3, 4), './data/img/reimu.png')

  # キー設定（W, A, D）
  cmd_move_km = [pg.K_w, pg.K_d, pg.K_s, pg.K_a]
  m_vec = [
      pg.Vector2(0, -1),  # 上移動
      pg.Vector2(1, 0),   # 右移動
      pg.Vector2(0, 1),  # 下移動
      pg.Vector2(-1, 0)    # 左移動
  ]

  while not exit_flag:
    for event in pg.event.get():
      if event.type == pg.QUIT:
        exit_flag = True

    # キー入力の検知
    key = pg.key.get_pressed()
    cmd_move = -1
    for i, k in enumerate(cmd_move_km):
      if key[k]:
        cmd_move = i

    # キャラの移動
    if not reimu.is_moving:
      if cmd_move != -1:
        reimu.turn_to(cmd_move)
        af_pos = reimu.pos + m_vec[cmd_move]
        if (0 <= af_pos.x < map_s.x) and (0 <= af_pos.y < map_s.y):
          reimu.move_to(m_vec[cmd_move])

    if reimu.is_moving:
      reimu.update_move_process()

    # 描画処理
    screen.fill(pg.Color('WHITE'))
    screen.blit(reimu.get_img(frame), reimu.get_dp())
    pg.display.update()

    frame += 1
    clock.tick(30)

  pg.quit()


if __name__ == "__main__":
  main()
=======
import pygame as pg

# 初期化処理・グローバル変数
scale_factor = 2
chip_s = int(24 * scale_factor)  # マップチップ基本サイズ
map_s = pg.Vector2(16, 9)        # マップの横・縦の配置数

# PlayerCharacterクラスの定義
class PlayerCharacter:

  def __init__(self, name, init_pos, img_path):
    self.pos = pg.Vector2(init_pos)
    self.size = pg.Vector2(24, 32) * scale_factor
    self.dir = 2
    self.name = name
    img_raw = pg.image.load(img_path)
    self.__img_arr = []
    for i in range(4):
      self.__img_arr.append([])
      for j in range(3):
        p = pg.Vector2(24 * j, 32 * i)
        tmp = img_raw.subsurface(pg.Rect(p, (24, 32)))
        tmp = pg.transform.scale(tmp, self.size)
        self.__img_arr[i].append(tmp)
      self.__img_arr[i].append(self.__img_arr[i][1])

    self.is_moving = False
    self.__moving_vec = pg.Vector2(0, 0)
    self.__moving_acc = pg.Vector2(0, 0)

  def turn_to(self, dir):
    self.dir = dir

  def move_to(self, vec):
    self.is_moving = True
    self.__moving_vec = vec.copy()
    self.__moving_acc = pg.Vector2(0, 0)
    self.update_move_process()

  def update_move_process(self):
    assert self.is_moving
    self.__moving_acc += self.__moving_vec * 3
    if self.__moving_acc.length() >= chip_s:
      self.pos += self.__moving_vec
      self.is_moving = False

  def get_dp(self):
    dp = self.pos * chip_s - pg.Vector2(0, 12) * scale_factor
    if self.is_moving:
      dp += self.__moving_acc
    return dp

  def get_img(self, frame):
    return self.__img_arr[self.dir][frame // 6 % 4]


# ゲームループを含むメイン処理
def main():
  pg.init()
  pg.display.set_caption('Keyboard Control Test')
  disp_w = int(chip_s * map_s.x)
  disp_h = int(chip_s * map_s.y)
  screen = pg.display.set_mode((disp_w, disp_h))
  clock = pg.time.Clock()
  frame = 0
  exit_flag = False

  # キャラ生成
  reimu = PlayerCharacter('reimu', (3, 4), './data/img/reimu.png')

  # キー設定（W, A, D）
  cmd_move_km = [pg.K_w, pg.K_d, pg.K_s, pg.K_a]
  m_vec = [
      pg.Vector2(0, -1),  # 上移動
      pg.Vector2(1, 0),   # 右移動
      pg.Vector2(0, 1),  # 下移動
      pg.Vector2(-1, 0)    # 左移動
  ]

  while not exit_flag:
    for event in pg.event.get():
      if event.type == pg.QUIT:
        exit_flag = True

    # キー入力の検知
    key = pg.key.get_pressed()
    cmd_move = -1
    for i, k in enumerate(cmd_move_km):
      if key[k]:
        cmd_move = i

    # キャラの移動
    if not reimu.is_moving:
      if cmd_move != -1:
        reimu.turn_to(cmd_move)
        af_pos = reimu.pos + m_vec[cmd_move]
        if (0 <= af_pos.x < map_s.x) and (0 <= af_pos.y < map_s.y):
          reimu.move_to(m_vec[cmd_move])

    if reimu.is_moving:
      reimu.update_move_process()

    # 描画処理
    screen.fill(pg.Color('WHITE'))
    screen.blit(reimu.get_img(frame), reimu.get_dp())
    pg.display.update()

    frame += 1
    clock.tick(30)

  pg.quit()


if __name__ == "__main__":
  main()
>>>>>>> 616ae80 (修正)
