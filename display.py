import arcade
CAMERA_SPEED = 500

class Display(arcade.Window):
    def __init__(self,graph, drones):
        super().__init__(fullscreen=True)
        self.graph = graph
        self.drones = drones
        self.camera = arcade.Camera2D()
        self.current_turn = 0

    def _draw_zone(self):
        for zone in self.graph.hubs.values():
            screen_x = self.width / 2 + zone.x * 180
            screen_y = self.height / 2 + zone.y * 180

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

        # Zone name above the circle
            arcade.draw_text(
                zone.name,
                screen_x,
                screen_y + 40,
                arcade.color.WHITE,
                12,
                anchor_x="center",
            )

        # Letter inside restricted or priority zones
            label = ""

            if zone.zone_type == "restricted":
                label = "R"
            elif zone.zone_type == "priority":
                label = "P"

            arcade.draw_text(
                label,
                screen_x,
                screen_y,
                arcade.color.PURPLE,
                12,
                anchor_x="center",
                anchor_y="center",
        )

    def _get_drone_position(self, drone):
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

    def _draw_drones(self):
        for drone in self.drones:
            position = self._get_drone_position(drone)
            if position is None:
                continue
            x, y = position

            arcade.draw_circle_filled(
                self.width / 2 + x * 180,
                self.height / 2 + y * 180,
                10,
                arcade.color.PINK
            )

    def _draw_connections(self):
        for zone_a in self.graph.hubs.values():
            for zone_b, connection, _ in self.graph.get_neighbors(zone_a.name):

                arcade.draw_line(
                    self.width / 2 + zone_a.x * 180,
                    self.height / 2 + zone_a.y * 180,
                    self.width / 2 + zone_b.x * 180,
                    self.height / 2 + zone_b.y * 180,
                    arcade.color.GRAY,
                    3,
                )

    def on_key_press(self, key: int, modifiers: int):
        camera_x, camera_y = self.camera.position
        if key == arcade.key.UP:
            camera_y += CAMERA_SPEED
        elif key == arcade.key.DOWN:
            camera_y -= CAMERA_SPEED
        elif key == arcade.key.LEFT:
            camera_x -= CAMERA_SPEED
        elif key == arcade.key.RIGHT:
            camera_x += CAMERA_SPEED

        if key == arcade.key.SPACE:
            self.current_turn += 1
        self.camera.position = camera_x , camera_y

    def on_draw(self):
        self.clear()
        self.camera.use()
        arcade.draw_text(
            f"Turn: {self.current_turn}",
            20,
            self.height - 40,
            arcade.color.WHITE,
            20,
        )
        self._draw_connections()
        self._draw_zone()
        self._draw_drones()
