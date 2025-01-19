import pygame as pg
import threading
from keyboard import PlayerCharacter as KeyboardCharacter
from voice import PlayerCharacter as VoiceCharacter, voice_recognition_thread

# 初期化処理
scale_factor = 2
chip_s = int(24 * scale_factor)  # マップチップ基本サイズ
map_s = pg.Vector2(20, 20)        # マップの横・縦の配置数

def load_maze():
  """迷路データのロード"""
  maze = [
      [5, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0],
      [0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0],
      [0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0],
      [0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1],
      [0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0],
      [0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0],
      [0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
      [1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0],
      [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0],
      [1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0],
      [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 0, 0],
      [0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1],
      [0, 1, 2, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0],
      [0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0]
  ]
  return maze

def draw_maze(screen, maze, assets):
  """迷路を描画"""
  for y, row in enumerate(maze):
    for x, cell in enumerate(row):
      if cell in assets:
        screen.blit(assets[cell], (x * chip_s, y * chip_s))

def show_explanation(screen, clock, screen_width, screen_height):
  """操作説明を表示"""
  font = pg.font.Font('./msgothic.ttc', 20)
  explanation_lines = [
      "このゲームは、2人のキャラクターを操作して",
      "ギミックをクリアしていくゲームです。",
      "1人目のキャラクター（霊夢）はキーボードで操作。",
      "右移動「d」、左移動「a」、上移動「w」、下移動「s」。",
      "2人目のキャラクター（魔理沙）は音声で操作。",
      "右移動「右に移動」、左移動「左に移動」",
      "上移動「上に移動」、下移動「下に移動」。",
      "クリアは赤色のキャラクターが扉に触れること。"
  ]
  y_offset = screen_height // 2 + 20  # 操作説明の開始位置
  for line in explanation_lines:
    explanation_text = font.render(line, True, 'BLACK')
    screen.blit(explanation_text,
                (screen_width // 2 - explanation_text.get_width() // 2, y_offset))
    y_offset += 30
  pg.display.update()
  clock.tick(30)

def show_start_screen(screen, clock, screen_width, screen_height):
  """スタート画面と操作説明を表示"""
  font_title = pg.font.Font('./msgothic.ttc', 30)
  font_button = pg.font.Font('./msgothic.ttc', 20)
  screen.fill(pg.Color('WHITE'))
  title_lines = [
      "一人で二人のキャラクターを動かす！？",
      "～協力型ギミック迷路～"
  ]
  title_texts = [font_title.render(line, True, '#FFB241')
                 for line in title_lines]
  total_height = sum(text.get_height() for text in title_texts)
  y_offset = (screen_height - total_height) // 2 - 170  # 170px上に調整
  for text in title_texts:
    x_offset = (screen_width - text.get_width()) // 2  # 中央揃え
    screen.blit(text, (x_offset, y_offset))
    y_offset += text.get_height()  # 次の行の位置を調整
  explanation_text = font_button.render("操作説明", True, '#FF6969')
  explanation_text_rect = explanation_text.get_rect(
      center=(screen_width // 2, screen_height // 2 - 10))  # 10px下に調整
  screen.blit(explanation_text, explanation_text_rect)
  start_button_rect = pg.Rect(
      (screen_width - 150) // 2, screen_height // 2 - 90, 150, 60)
  pg.draw.rect(screen, pg.Color('BLUE'), start_button_rect)
  start_button_text = font_button.render("START", True, 'WHITE')
  screen.blit(start_button_text, (start_button_rect.x +
              25, start_button_rect.y + 15))
  pg.display.update()
  show_explanation(screen, clock, screen_width, screen_height)
  while True:
    for event in pg.event.get():
      if event.type == pg.QUIT:
        return False
      if event.type == pg.MOUSEBUTTONDOWN:
        if start_button_rect.collidepoint(event.pos):
          return True
    clock.tick(30)

def can_move_to(pos, maze, map_size):
  """指定位置へ移動できるか判定する関数"""
  if not (0 <= pos.x < map_size.x and 0 <= pos.y < map_size.y):
    return False  # 範囲外なら移動不可
  if maze[int(pos.y)][int(pos.x)] == 1:
    return False  # 壁があるなら移動不可
  return True  # それ以外は移動可能

def move_character(character, direction, maze, map_size, movement_vector):
  """キャラクターを移動させる処理"""
  if not character.is_moving:
    character.turn_to(direction)
    next_pos = character.pos + movement_vector
    if can_move_to(next_pos, maze, map_size):
      character.move_to(movement_vector)

def check_button_activated(character, maze):
  """キャラクターがボタンに乗っているか判定する関数"""
  x, y = int(character.pos.x), int(character.pos.y)
  return maze[y][x] == 2

def check_clear_condition(reimu, maze):
  """霊夢がクリアボタン（'5'）に到達したか判定"""
  x, y = int(reimu.pos.x), int(reimu.pos.y)
  return maze[y][x] == 5

def update_door_state(maze, reimu, marisa):
  """ボタンの上にキャラクターがいる場合に壁（3）を消す処理"""
  if check_button_activated(reimu, maze) or check_button_activated(marisa, maze):
      # キャラクターがボタン（2）の上に乗っている場合、特定の位置の壁（3）を消す
    if maze[9][4] == 1:  # (4, 9) の位置にある壁が消える
      maze[9][4] = 0  # 壁を消す
  else:
    # キャラクターがボタンの上にいない場合、壁（3）を元に戻す
    if maze[9][4] == 0:  # もしその位置が消えている場合
      maze[9][4] = 1  # 壁を元に戻す


def show_clear_screen(screen, clock, screen_width, screen_height):
  """クリア画面を表示"""
  font = pg.font.Font('./msgothic.ttc', 40)
  clear_text = font.render("クリア！", True, 'RED')
  screen.fill(pg.Color('WHITE'))
  screen.blit(clear_text, (screen_width // 2 - clear_text.get_width() // 2,
                           screen_height // 2 - clear_text.get_height() // 2))
  pg.display.update()
  pg.time.delay(10000)
  clock.tick(30)

def main():
  pg.init()
  pg.display.set_caption("一人で二人のキャラクターを動かす！？～協力型ギミック迷路～")
  screen_width, screen_height = 800, 600
  screen = pg.display.set_mode((screen_width, screen_height), pg.RESIZABLE)
  clock = pg.time.Clock()
  assets = {
      0: pg.transform.scale(pg.image.load('./data/img/yuka.png'), (chip_s, chip_s)),
      1: pg.transform.scale(pg.image.load('./data/img/kabe.png'), (chip_s, chip_s)),
      2: pg.transform.scale(pg.image.load('./data/img/button.png'), (chip_s, chip_s)),
      3: pg.transform.scale(pg.image.load('./data/img/kaiheitobira.png'), (chip_s, chip_s)),
      4: pg.transform.scale(pg.image.load('./data/img/door.png'), (chip_s, chip_s)),
      5: pg.transform.scale(pg.image.load('./data/img/gole.png'), (chip_s, chip_s))
  }
  if not show_start_screen(screen, clock, screen_width, screen_height):
    pg.quit()
    return
  maze = load_maze()

  # 初期位置設定（3つ下に変更）
  marisa_initial_pos = (0, map_s.y // 2 + 3)  # 左下から3つ下に設定
  reimu_initial_pos = (map_s.x - 1, map_s.y // 2 + 3)  # 右下から3つ下に設定
  reimu = KeyboardCharacter(
      'reimu', reimu_initial_pos, './data/img/reimu.png')
  marisa = VoiceCharacter('marisa', marisa_initial_pos,
                          './data/img/marisa.png')

  move_queue = []
  voice_thread = threading.Thread(
      target=voice_recognition_thread, args=(marisa, move_queue), daemon=True)
  voice_thread.start()
  frame = 0
  exit_flag = False

  while not exit_flag:
    for event in pg.event.get():
      if event.type == pg.QUIT:
        exit_flag = True
      if event.type == pg.VIDEORESIZE:
        screen_width, screen_height = event.w, event.h
        screen = pg.display.set_mode(
            (screen_width, screen_height), pg.RESIZABLE)

    # キー入力処理
    key = pg.key.get_pressed()
    cmd_move_km = [pg.K_w, pg.K_d, pg.K_s, pg.K_a]
    m_vec = [
        pg.Vector2(0, -1),  # 上移動
        pg.Vector2(1, 0),   # 右移動
        pg.Vector2(0, 1),   # 下移動
        pg.Vector2(-1, 0)   # 左移動
    ]
    cmd_move = -1
    for i, k in enumerate(cmd_move_km):
      if key[k]:
        cmd_move = i

    # 霊夢の移動
    if cmd_move != -1:
      move_character(reimu, cmd_move, maze, map_s, m_vec[cmd_move])

    if reimu.is_moving:
      reimu.update_move_process()

    # 魔理沙の移動
    if move_queue:
      direction, vec = move_queue.pop(0)
      move_character(marisa, direction, maze, map_s, vec)

    if marisa.is_moving:
      marisa.update_move_process()

    # 扉の状態を更新
    update_door_state(maze, reimu, marisa)

    # クリア条件の確認
    if check_clear_condition(reimu, maze):
      show_clear_screen(screen, clock, screen_width, screen_height)
      if not show_start_screen(screen, clock, screen_width, screen_height):
        pg.quit()
        return

    # その他の描画処理
    screen.fill(pg.Color('WHITE'))
    draw_maze(screen, maze, assets)
    reimu_rect = reimu.get_dp()
    screen.blit(reimu.get_img(frame), (reimu_rect[0], reimu_rect[1]))
    marisa_rect = marisa.get_dp()
    screen.blit(marisa.get_img(frame), (marisa_rect[0], marisa_rect[1]))
    pg.display.update()

    frame += 1
    clock.tick(40)

if __name__ == "__main__":
  main()
