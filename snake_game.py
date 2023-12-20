import turtle
import random
import time

class SnakeGame:
    def __init__(self):
        self.screen = self.setup_screen()
        self.draw_border()
        self.score = 0
        self.delay = 0.1
        self.snake = self.create_snake()
        self.fruit = self.create_fruit()
        self.old_fruit = []
        self.scoring = turtle.Turtle()
        self.setup_scoring()
        self.setup_keyboard_controls()
        self.is_game_over = False

    def setup_screen(self):
        screen = turtle.Screen()
        screen.title('Snake Game')
        screen.setup(width=700, height=700)
        screen.tracer(0)
        turtle.bgcolor('lightgreen')
        return screen

    def draw_border(self):
        turtle.speed(5)
        turtle.pensize(4)
        turtle.penup()
        turtle.goto(-310, 250)
        turtle.pendown()
        turtle.color('black')
        for _ in range(2):
            turtle.forward(600)
            turtle.right(90)
            turtle.forward(500)
            turtle.right(90)
        turtle.penup()
        turtle.hideturtle()

    def create_snake(self):
        snake = turtle.Turtle()
        snake.speed(0)
        snake.shape('square')
        snake.color("blue")
        snake.penup()
        snake.goto(0, 0)
        snake.direction = 'stop'
        return snake

    def create_fruit(self):
        fruit = turtle.Turtle()
        fruit.speed(0)
        fruit.shape('circle')
        fruit.color('red')
        fruit.penup()
        fruit.goto(30, 30)
        return fruit

    def setup_scoring(self):
        self.scoring.speed(0)
        self.scoring.color("red")
        self.scoring.penup()
        self.scoring.hideturtle()
        self.scoring.goto(0, 300)
        self.display_score()

    def display_score(self):
        self.scoring.clear()
        self.scoring.write("Score:{}".format(self.score), align="center", font=("Courier", 24, "bold"))

    def setup_keyboard_controls(self):
        self.screen.listen()
        self.screen.onkeypress(self.snake_go_up, "Up")
        self.screen.onkeypress(self.snake_go_down, "Down")
        self.screen.onkeypress(self.snake_go_left, "Left")
        self.screen.onkeypress(self.snake_go_right, "Right")
        self.screen.onkeypress(self.start_new_game, "n")
        self.screen.onkeypress(self.remove_snake, "r")
        self.screen.onkeypress(self.add_new_snake, "a")
        self.screen.onkeypress(self.update_snake, "u")

    def update_snake(self):
        if not self.is_game_over:
            available_colors = ["purple", "green", "yellow", "blue", "black"]
            selected_color = random.choice(available_colors)
            self.snake.color(selected_color)

    def start_new_game(self):
        if self.is_game_over:
            restart = turtle.textinput("New Game", "Do you want to start a new game? (yes/no)").lower()
            if restart == "yes":
                # Reset game variables
                self.score = 0
                self.delay = 0.1
                self.snake.goto(0, 0)
                self.snake.direction = 'stop'
                for segment in self.old_fruit:
                    segment.hideturtle()
                self.old_fruit.clear()
                self.is_game_over = False
                self.display_score()

                # Create a new fruit
                self.fruit.goto(30, 30)
                self.create_new_fruit()

                # Start the game loop
                self.main_game_loop()

    def remove_snake(self):
        if not self.is_game_over:
            self.snake.hideturtle()
            self.is_game_over = True
            self.scoring.goto(0, 0)
            self.scoring.write("Snake removed. Your Score is {}".format(self.score), align="center",
                               font=("Courier", 30, "bold"))

    def add_new_snake(self):
        if not self.is_game_over:
            new_snake = turtle.Turtle()
            new_snake.speed(0)
            new_snake.shape('circle')
            new_snake.color("green")
            new_snake.penup()
            new_snake.goto(0, 0)
            new_snake.direction = 'stop'
            self.snake = new_snake

    def main_game_loop(self):
        while not self.is_game_over:
            self.screen.update()
            self.check_food_collision()
            self.move_snake_body()
            self.snake_move()
            self.check_border_collision()
            self.check_self_collision()
            time.sleep(self.delay)

    def move_snake_body(self):
        for index in range(len(self.old_fruit)-1, 0, -1):
            a, b = self.old_fruit[index-1].xcor(), self.old_fruit[index-1].ycor()
            self.old_fruit[index].goto(a, b)

        if self.old_fruit:
            a, b = self.snake.xcor(), self.snake.ycor()
            self.old_fruit[0].goto(a, b)

    def snake_move(self):
        if self.snake.direction == "up":
            self.snake.sety(self.snake.ycor() + 20)
        elif self.snake.direction == "down":
            self.snake.sety(self.snake.ycor() - 20)
        elif self.snake.direction == "left":
            self.snake.setx(self.snake.xcor() - 20)
        elif self.snake.direction == "right":
            self.snake.setx(self.snake.xcor() + 20)

    def snake_go_up(self):
        if self.snake.direction != "down":
            self.snake.direction = "up"

    def snake_go_down(self):
        if self.snake.direction != "up":
            self.snake.direction = "down"

    def snake_go_left(self):
        if self.snake.direction != "right":
            self.snake.direction = "left"

    def snake_go_right(self):
        if self.snake.direction != "left":
            self.snake.direction = "right"

    def check_food_collision(self):
        if self.snake.distance(self.fruit) < 20:
            x, y = random.randint(-290, 270), random.randint(-240, 240)
            self.fruit.goto(x, y)
            self.score += 1
            self.display_score()
            self.delay -= 0.001
            self.create_new_fruit()

    def create_new_fruit(self):
        new_fruit = turtle.Turtle()
        new_fruit.speed(0)
        new_fruit.shape('square')
        new_fruit.color('red')
        new_fruit.penup()
        self.old_fruit.append(new_fruit)

    def check_border_collision(self):
        if (
            self.snake.xcor() > 280 or
            self.snake.xcor() < -300 or
            self.snake.ycor() > 240 or
            self.snake.ycor() < -240
        ):
            self.game_over("GAME OVER. Your Score is {}".format(self.score))

    def check_self_collision(self):
        for food in self.old_fruit:
            if food.distance(self.snake) < 20:
                self.game_over("GAME OVER. Your Score is {}".format(self.score))

    def game_over(self, message):
        time.sleep(1)
        self.screen.clear()
        self.screen.bgcolor('lightgreen')
        self.scoring.goto(0, 0)
        self.scoring.write(message, align="center", font=("Courier", 30, "bold"))
        self.is_game_over = True

def main():
    snake_game = SnakeGame()
    snake_game.main_game_loop()
    turtle.mainloop()

if __name__ == "__main__":
    main()
