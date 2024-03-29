# Проект Game 2048
Игра сделана для забавы ради и удволетворения собственного любопытства.

## Описание
Игра сделана на Pygame – это библиотека модулей для языка Python, имеет смесь игровых механик тетриса и 2048.

Объединение одинаковых чисел с целью получения огромного удовольствия. Сложность игры постепенно увеличивается с большими пронумерованными блоками. Приятная анимация складывания кубиков, снимает стресс.

![Иллюстрация к проекту](https://github.com/PivnoyFei/game_2048/blob/main/game/madia/Game2048.png)

### Стек: 
```
Python 3.7, pygame.
```

### Запуск проекта:
#### Клонируем репозиторий и переходим в него:
```bash
git clone https://github.com/PivnoyFei/game_2048.git
cd game_2048
```

### Быстрый запуск MakeFile:
```bash
make start-linux  # Только для первого запуска
make start-windows  # Только для первого запуска
make start
```

### Обычный запуск:
#### Создаем и активируем виртуальное окружение:
```bash
python3 -m venv venv
source venv/bin/activate
```
#### для Windows
```bash
python -m venv venv
source venv/Scripts/activate
```
#### Обновляем пип:
```bash
python -m pip install --upgrade pip
```

#### Ставим зависимости из requirements.txt:
```bash
pip install -r requirements.txt
```

#### Запускаем проект:
```bash
cd game && python main.py
```

### Разработчик проекта
- [Смелов Илья](https://github.com/PivnoyFei)
