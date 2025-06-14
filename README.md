
# Игровой набор на Python

Набор из 4 классических и современных игр, реализованных на Python с использованием Tkinter и Pygame.

## Содержание
1. [Установка](#установка)
2. [Описание игр](#описание-игр)
   - [Порядок vs Хаос](#порядок-vs-хаос)
   - [Вложенные крестики-нолики](#вложенные-крестики-нолики)
   - [Magic 15](#magic-15)
   - [Соединение точек 4x4](#соединение-точек-4x4)
3. [Управление](#управление)
4. [Автор](#автор)

## Установка

1. Убедитесь, что у вас установлен Python 3.6 или новее
2. Установите необходимые зависимости:
   ```bash
   pip install tkinter pygame
   ```
3. Запустите главное меню:
   ```bash
   python main.py
   ```

## Описание игр

### Порядок vs Хаос

**Описание:**  
Стратегическая игра для двух игроков на поле 6x6.  
- **Порядок** пытается создать линию из 5 одинаковых символов (X или O)
- **Хаос** пытается помешать Порядку, заполняя поле случайными символами

**Правила:**
- Порядок выбирает символ (X или O) в начале игры
- Игроки ходят по очереди
- Порядок побеждает, если создает линию из 5 своих символов
- Хаос побеждает, если заполняет все поле без создания линии

### Вложенные крестики-нолики

**Описание:**  
Усложненная версия классических крестиков-ноликов с двумя уровнями поля.

**Правила:**
- Игроки по очереди ставят X или O
- Каждое большое поле 3x3 содержит маленькие поля 3x3
- Победа в маленьком поле дает право поставить большой X или O
- Побеждает игрок, который первым выстроит линию на большом поле

### Magic 15

**Описание:**  
Математическая игра, где нужно собрать комбинацию из 3 чисел, дающих в сумме 15.

**Правила:**
- Игроки по очереди выбирают числа от 1 до 9
- Каждое число можно использовать только один раз
- Побеждает игрок, первым собравший комбинацию из 3 чисел с суммой 15

### Соединение точек 4x4

**Описание:**  
Геометрическая игра для двух игроков на поле 4x4 точек.

**Правила:**
- Игроки по очереди соединяют две точки прямыми линиями
- Нельзя пересекать уже существующие линии
- Нельзя соединять уже соединенные точки
- Проигрывает игрок, который не может сделать ход

## Управление

- **Главное меню:** Выбор игры с помощью кнопок
- **В играх:**
  - `Escape` - открыть меню
  - `R` - рестарт (в крестиках-ноликах)
  - ЛКМ - сделать ход
- Для выхода из игр используйте кнопку закрытия окна

## Автор

Проект разработан в образовательных целях. Весь код открыт для использования и модификации.

