import pygame as pg
import speech_recognition as sr
import threading

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


# 音声認識で「下に移動」を処理

def voice_recognition_thread(marisa, move_queue):
  recognizer = sr.Recognizer()
  mic = sr.Microphone()

  while True:
    try:
      with mic as source:
        print("音声コマンドをお話しください...")
        audio = recognizer.listen(source)
      command = recognizer.recognize_google(audio, language="ja-JP")
      print(f"認識結果: {command}")

      # 音声コマンドによる移動処理
      if "右に移動" in command:
        move_queue.append((1, pg.Vector2(1, 0)))  # 右移動
      elif "左に移動" in command:
        move_queue.append((3, pg.Vector2(-1, 0)))  # 左移動
      elif "上に移動" in command:
        move_queue.append((0, pg.Vector2(0, -1)))  # 上移動
      elif "下に移動" in command:
        move_queue.append((2, pg.Vector2(0, 1)))  # 下移動

    except sr.UnknownValueError:
      print("音声を認識できませんでした。")
    except sr.RequestError as e:
      print(f"音声認識サービスに接続できません: {e}")


# ゲームループを含むメイン処理
def main():
  pg.init()
  pg.display.set_caption('Voice Control Test')
  disp_w = int(chip_s * map_s.x)
  disp_h = int(chip_s * map_s.y)
  screen = pg.display.set_mode((disp_w, disp_h))
  clock = pg.time.Clock()
  frame = 0
  exit_flag = False

  # キャラ生成
  marisa = PlayerCharacter('marisa', (3, 4), './data/img/marisa.png')

  # 移動ベクトル
  m_vec = [
      pg.Vector2(0, -1),  # 上移動
      pg.Vector2(1, 0),   # 右移動
      pg.Vector2(0, 1),   # 下移動
      pg.Vector2(-1, 0)   # 左移動
  ]

  # 音声コマンドによる移動キュー
  move_queue = []

  # 音声認識スレッドを開始
  voice_thread = threading.Thread(
      target=voice_recognition_thread, args=(marisa, move_queue), daemon=True)
  voice_thread.start()

  while not exit_flag:
    for event in pg.event.get():
      if event.type == pg.QUIT:
        exit_flag = True

    # 音声コマンドの処理
    if move_queue:
      direction, vec = move_queue.pop(0)
      if not marisa.is_moving:
        marisa.turn_to(direction)
        af_pos = marisa.pos + vec
        if (0 <= af_pos.x < map_s.x) and (0 <= af_pos.y < map_s.y):
          marisa.move_to(vec)

    if marisa.is_moving:
      marisa.update_move_process()

    # 描画処理
    screen.fill(pg.Color('WHITE'))
    screen.blit(marisa.get_img(frame), marisa.get_dp())
    pg.display.update()

    frame += 1
    clock.tick(30)

  pg.quit()


if __name__ == "__main__":
  main()
