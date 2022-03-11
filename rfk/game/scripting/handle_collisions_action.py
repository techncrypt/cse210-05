import constants
from game.casting.actor import Actor
from game.scripting.action import Action
from game.shared.point import Point
from game.casting.score import Score
from game.casting.score2 import Score2


class HandleCollisionsAction(Action):
    """
    An update action that handles interactions between the actors.
    
    The responsibility of HandleCollisionsAction is to handle the situation when the rider
        collides with its segments, or the game is over.

    Attributes:
        _is_game_over (boolean): Whether or not the game is over.
    """

    def __init__(self):
        """Constructs a new HandleCollisionsAction."""
        self._is_game_over = False
        self._dead_player = None

    def execute(self, cast, script):
        """Executes the handle collisions action.

        Args:
            cast (Cast): The cast of Actors in the game.
            script (Script): The script of Actions in the game.
        """
        if not self._is_game_over:
            self._handle_self_collision(cast)
            self._handle_other_collisions(cast)
            # self._handle_segment_collision(cast)
            self._handle_game_over(cast)


    def _handle_self_collision(self,cast):
        cycle_1 = cast.get_first_actor("cycle_1")
        cycle_1_head = cycle_1.get_segments()[0]
        cycle_1_segments = cycle_1.get_segments()[1:]


        
        cycle_2 = cast.get_first_actor("cycle_2")
        cycle_2_head = cycle_2.get_segments()[0]
        cycle_2_segments = cycle_2.get_segments()[1:]

        for segment in cycle_1_segments:
            if cycle_1_head.get_position().equals(segment.get_position()):
                self._is_game_over = True
                self._dead_player = "cycle_1"
        
        for segment in cycle_2_segments:
            if cycle_2_head.get_position().equals(segment.get_position()):
                self._is_game_over = True
                self._dead_player = "cycle_2"

    def _handle_other_collisions(self,cast):
        cycle_1 = cast.get_first_actor("cycle_1")
        cycle_1_head = cycle_1.get_segments()[0]
        cycle_1_segments = cycle_1.get_segments()[1:]

        cycle_2 = cast.get_first_actor("cycle_2")
        cycle_2_head = cycle_2.get_segments()[0]
        cycle_2_segments = cycle_2.get_segments()[1:]
        score = cast.get_first_actor("scores")
        score2 = cast.get_first_actor("score2")
        # check if cycle_2 hit cycle_1
        for segment in cycle_1_segments:
            segment.set_color(constants.WHITE) 
            if cycle_2_head.get_position().equals(segment.get_position()):
                self._is_game_over = True
                self._dead_player = "cycle_2"
                score.add_points(1)
        # check if cycle_1 hit cycle_2
        for segment in cycle_2_segments:
            segment.set_color(constants.WHITE) 
            if cycle_1_head.get_position().equals(segment.get_position()):
                self._is_game_over = True
                self._dead_player = "cycle_1"
                score2.add_points(1)
                
    def _handle_game_over(self, cast):
        """Shows the 'game over' message if the game is over.
        
        Args:
            cast (Cast): The cast of Actors in the game.
        """
        if self._is_game_over:

            x = int(constants.MAX_X / 2)
            y = int(constants.MAX_Y / 2)
            position = Point(x, y)

            message = Actor()
            if self._dead_player == "cycle_1":#first snake
                color_winner = "Red"
            elif self._dead_player == "cycle_2": #second snake
                color_winner = "Yellow"
            message.set_text(f"Game Over! {color_winner} Wins!")
            message.set_position(position)
            cast.add_actor("messages", message)
