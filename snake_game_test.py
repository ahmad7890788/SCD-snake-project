import pytest
from snake_game import SnakeGame

@pytest.fixture
def game():
    return SnakeGame()

def test_initialization(game):
    assert game.score == 0
    assert game.delay == 0.1
    assert game.is_game_over is False

def test_snake_initial_position(game):
    assert game.snake.xcor() == 0
    assert game.snake.ycor() == 0

def test_snake_initial_direction(game):
    assert game.snake.direction == 'stop'

def test_fruit_initial_position(game):
    assert game.fruit.xcor() == 30
    assert game.fruit.ycor() == 30

def test_move_snake_up(game):
    game.snake.direction = 'up'
    y_before = game.snake.ycor()
    game.snake_move()
    y_after = game.snake.ycor()
    assert y_after > y_before  # Snake moved up

def test_move_snake_down(game):
    game.snake.direction = 'down'
    y_before = game.snake.ycor()
    game.snake_move()
    y_after = game.snake.ycor()
    assert y_after < y_before  # Snake moved down

def test_move_snake_left(game):
    game.snake.direction = 'left'
    x_before = game.snake.xcor()
    game.snake_move()
    x_after = game.snake.xcor()
    assert x_after < x_before  # Snake moved left

def test_move_snake_right(game):
    game.snake.direction = 'right'
    x_before = game.snake.xcor()
    game.snake_move()
    x_after = game.snake.xcor()
    assert x_after > x_before  # Snake moved right

def test_game_over_on_edge_hit(game):
    # Assuming the game over message is 'GAME OVER.'
    game.snake.goto(300, 0)  # Move snake to the right edge
    game.check_border_collision()
    assert game.is_game_over is True

def test_game_over_on_self_collision(game):
    # Assuming the game over message is 'GAME OVER.'
    game.snake.direction = 'right'
    game.move_snake_body()
    game.snake_move()  # Move the snake right to collide with itself
    game.check_self_collision()
    assert game.is_game_over is True
