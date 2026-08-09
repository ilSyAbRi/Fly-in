import arcade

from graph import Graph
from models import Drone

CAMERA_SPEED = 850


class Display(arcade.Window):
    """Display the graph and drone movements in an Arcade window."""

    def __init__(
        self,
        graph: Graph,
        drones: list[Drone],
    ) -> None:
        """Initialize the simulation display.

        Args:
            graph: Graph containing the zones and connections.
            drones: Drones and their planned paths.

        Returns:
            None.
        """
        super().__init__(
            fullscreen=True,
            vsync=True,
            title="FLY-IN",
        )

        self.graph = graph
        self.drones = drones
        self.camera = arcade.Camera2D()

        self.current_turn = 0

        self.last_turn = max(
            drone.path[-1][1]
            for drone in self.drones
        )

        self.up_pressed = False
        self.down_pressed = False
        self.left_pressed = False
        self.right_pressed = False

        self.space_pressed = False
        self.space_timer: float = 0
        self.background_color = (35, 35, 40)

    def _draw_zone(self) -> None:
        """Draw all zones in the graph.

        Returns:
            None.
        """
        for zone in self.graph.hubs.values():
            screen_x = self.width / 2 + zone.x * 130
            screen_y = self.height / 2 + zone.y * 130

            color = getattr(
                arcade.color,
                zone.color.upper(),
                arcade.color.WHITE,
            )

            arcade.draw_circle_filled(
                screen_x,
                screen_y,
                30,
                color,
            )

            arcade.draw_text(
                zone.name,
                screen_x,
                screen_y + 40,
                arcade.color.WHITE,
                10,
                anchor_x="center",
            )

            label = "N"

            if zone.zone_type == "restricted":
                label = "R"
            elif zone.zone_type == "priority":
                label = "P"

            arcade.draw_text(
                label,
                screen_x,
                screen_y,
                arcade.color.AMAZON,
                12,
                anchor_x="center",
                anchor_y="center",
            )

    def _get_drone_position(
        self,
        drone: Drone,
    ) -> tuple[float, float] | None:
        """Get the position of a drone at the current turn.

        Args:
            drone: Drone whose position should be calculated.

        Returns:
            The drone coordinates, or None if no position is available.
        """
        for zone, turn in drone.path:
            if turn == self.current_turn:
                return zone.x, zone.y

        for i in range(len(drone.path) - 1):
            zone_a, turn_a = drone.path[i]
            zone_b, turn_b = drone.path[i + 1]

            if turn_a < self.current_turn < turn_b:
                x = (zone_a.x + zone_b.x) / 2
                y = (zone_a.y + zone_b.y) / 2

                return x, y

        return None

    def _draw_drones(self) -> None:
        """Draw all drones at their current positions.

        Returns:
            None.
        """
        for drone in self.drones:
            position = self._get_drone_position(drone)

            if position is None:
                continue

            x, y = position

            arcade.draw_circle_filled(
                self.width / 2 + x * 130,
                self.height / 2 + y * 130,
                10,
                arcade.color.PINK,
            )

    def _draw_connections(self) -> None:
        """Draw all connections between zones.

        Returns:
            None.
        """
        for zone_a in self.graph.hubs.values():
            for zone_b, _, _ in self.graph.get_neighbors(zone_a.name):
                arcade.draw_line(
                    self.width / 2 + zone_a.x * 130,
                    self.height / 2 + zone_a.y * 130,
                    self.width / 2 + zone_b.x * 130,
                    self.height / 2 + zone_b.y * 130,
                    arcade.color.GRAY,
                    3,
                )

    def on_key_press(
        self,
        key: int,
        modifiers: int,
    ) -> None:
        """Handle keyboard press events.

        Args:
            key: Key that was pressed.
            modifiers: Active keyboard modifiers.

        Returns:
            None.
        """
        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = True

        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = True

        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = True

        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = True

        elif key == arcade.key.SPACE:
            self.space_pressed = True

            if self.current_turn < self.last_turn:
                self.current_turn += 1

    def on_key_release(
        self,
        key: int,
        modifiers: int,
    ) -> None:
        """Handle keyboard release events.

        Args:
            key: Key that was released.
            modifiers: Active keyboard modifiers.

        Returns:
            None.
        """
        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = False

        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = False

        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = False

        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = False

        elif key == arcade.key.SPACE:
            self.space_pressed = False
            self.space_timer = 0

    def on_update(self, delta_time: float) -> None:
        """Update camera movement and simulation timing.

        Args:
            delta_time: Time elapsed since the previous update.

        Returns:
            None.
        """
        camera_x, camera_y = self.camera.position

        if self.up_pressed:
            camera_y += CAMERA_SPEED * delta_time

        if self.down_pressed:
            camera_y -= CAMERA_SPEED * delta_time

        if self.left_pressed:
            camera_x -= CAMERA_SPEED * delta_time

        if self.right_pressed:
            camera_x += CAMERA_SPEED * delta_time

        self.camera.position = camera_x, camera_y

        if self.space_pressed:
            self.space_timer += delta_time

            if self.space_timer >= 0.2:
                if self.current_turn < self.last_turn:
                    self.current_turn += 1

                self.space_timer = 0

    def on_draw(self) -> None:
        """Draw the current simulation frame.

        Returns:
            None.
        """
        self.clear()
        self.camera.use()

        self._draw_connections()
        self._draw_zone()
        self._draw_drones()

        camera_x, camera_y = self.camera.position

        arcade.draw_text(
            f"Turn: {self.current_turn}",
            camera_x - self.width / 2 + 20,
            camera_y + self.height / 2 - 40,
            arcade.color.PINK,
            20,
        )
