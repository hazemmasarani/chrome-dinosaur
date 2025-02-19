# __Chrome Dinosaur Game (Pygame)__
This is a simple implementation of the Chrome Dinosaur game using Pygame. The game mimics the iconic "T-Rex" dinosaur from Google Chrome that appears when the user loses internet connectivity. The player controls the dinosaur and must avoid obstacles like cacti and flying birds.

## Features
- __Playable Dinosaur:__ Control a dinosaur that runs across a desert-like terrain.
- __Obstacles:__ Avoid cacti and flying birds that appear as obstacles.
- __Game Over:__ The game ends when the dinosaur collides with an obstacle.
- __Score:__ A score counter increases as you successfully avoid obstacles.
- __Simple Graphics:__ The game uses basic Pygame graphics, giving it a retro feel.
## Prerequisites
Before running the game, ensure that you have the following installed:

- __Python 3.6+__
- __Pygame library__
To install Pygame, use the following command:
```bash copy
pip install pygame
```
#Installation
1. Clone the repository to your local machine:
```bash Copy
git clone https://github.com/yourusername/chrome-dinosaur-pygame.git
```
2. Navigate to the project directory:
```bash Copy
cd chrome-dinosaur-pygame
```
3. Install the required dependencies (e.g., Pygame):
```bash
pip install pygame
```
4. Run the game:
```python
python main.py
```
## Controls
- __Spacebar:__ Make the dinosaur jump.
- __Up Arrow:__ Make the dinosaur jump (alternative to spacebar).

You can control the dinosaur's jumping action to avoid obstacles.

## Game Mechanics
- The dinosaur runs automatically from left to right.
- Cacti and birds will appear randomly, and you need to jump over them to survive.
- Your score increases over time, based on how long you last without hitting obstacles.
## Contributing
If you'd like to contribute to this project, feel free to fork the repository and create a pull request with your improvements or bug fixes.

### How to Contribute:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit them (`git commit -am 'Add feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a pull request.
## License
This project is licensed under the MIT License - see the [LICENSE]('https://mit-license.org/') file for details.

## Acknowledgments
- Thanks to the Pygame library for enabling easy game development in Python.
- Inspiration for this project comes from the offline "T-Rex" dinosaur game in Google Chrome.