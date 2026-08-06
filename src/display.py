import arcade
CAMERA_SPEED = 100

class Display(arcade.Window):
    def __init__(self,graph, drones):
        super().__init__(fullscreen=True)
        self.graph = graph
        self.drones = drones
        self.camera = arcade.Camera2D()
        self.current_turn = 0

    def _draw_zone(self):
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
    def _draw_connections(self):
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
        self._draw_connections()
        self._draw_zone()
