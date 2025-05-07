<h1 align="center">🎮 Arcade Survival</h1>

<p align="center">
  <img src="assets/images/background.jpg" alt="Arcade Survival Screenshot" width="600"/>
</p>

---

## 📖 About the Game

**Arcade Survival** is a top-down 2D survival shooter built with Python and Pygame. The player must survive waves of enemies by moving, dodging, and shooting in a dynamically scaling environment. The game features an elegant retro-style interface, adjustable resolution, sound options, and a responsive UI system.

---

## 📂 Project Structure

```

arcade\_survival/
├── main.py
├── config/
│   ├── **init**.py
│   ├── settings.py
│   └── paths.py
├── core/
│   ├── **init**.py
│   ├── game.py
│   ├── menus.py
│   └── utils.py
├── entities/
│   ├── **init**.py
│   ├── player.py
│   ├── bullet.py
│   └── enemy.py
├── assets/
│   ├── images/
│   │   ├── player.png
│   │   ├── enemy.png
│   │   └── background.jpg
│   ├── sounds/
│   │   ├── shoot.mp3
│   │   ├── kill.mp3
│   │   ├── gameover.mp3
│   │   └── music.mp3
│   └── fonts/
│       └── arial.ttf
├── data/
│   ├── highscores.json
│   └── settings.json
├── requirements.txt
├── README.md
└── .gitignore

````

---

## ✅ Features Implemented

- ✅ Modular project structure
- ✅ Functional main menu, pause menu, and options menu
- ✅ Player movement (WASD) and shooting
- ✅ Bullet collision with enemies
- ✅ Enemy wave spawning and scaling
- ✅ Health bar and player damage system
- ✅ Sound effects: shoot, kill, game over
- ✅ Background music
- ✅ Volume controls (global master volume)
- ✅ Resolution switching and fullscreen toggle
- ✅ JSON structure for persistent settings and scores
- ✅ Graceful error handling for missing assets

---

## 🛠️ To Do / Work in Progress

- ☐ Allow individual adjustment of `music_volume` and `effects_volume`
- ☐ Implement player score saving/loading from `highscores.json`
- ☐ Add animated sprites for player/enemies
- ☐ Add multiple enemy types
- ☐ Power-ups and upgrades (double shot, speed, etc.)
- ☐ Game over screen with retry/quit options
- ☐ Difficulty settings (easy, normal, hard)
- ☐ Controller support (optional)
- ☐ In-game settings menu with UI sliders
- ☐ Local leaderboard

---

## 🧩 Requirements

- Python 3.12+
- Pygame 2.6+

Install dependencies:

```bash
pip install -r requirements.txt
````

---

## 🚀 Running the Game

```bash
python main.py
```

---

## 🧠 Credits

* Developed using **Pygame** and Python.
* Art & sound assets are placeholders. Replace with your own or license-free content for production.

---

## 📃 License

This is a personal project under development. Not yet licensed for redistribution.

```

---