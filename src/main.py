"""
Main module for the Python project template.
"""

import tkinter as tk
import math
import time


class App:
    """Tkinter application that shows a ball bouncing inside a spinning hexagon."""

    def __init__(self, width: int = 400, height: int = 400) -> None:
        self.width = width
        self.height = height
        self.root = tk.Tk()
        self.root.title("Bouncing Ball in a Spinning Hexagon")
        self.canvas = tk.Canvas(
            self.root, width=self.width, height=self.height, bg="white"
        )
        self.canvas.pack(fill="both", expand=True)

        # Hexagon parameters
        self.hex_center = (self.width / 2, self.height / 2)
        self.hex_side = (
            min(self.width, self.height) * 0.4
        )  # side length as a fraction of canvas size
        self.hex_angle = 0.0  # current rotation angle in radians
        self.hex_speed = math.radians(30)  # rotation speed (30 degrees per second)

        # Ball parameters
        self.ball_radius = 10
        self.ball_x = self.width / 2
        self.ball_y = self.height / 2
        self.ball_vx = 150.0  # initial x velocity (px/s)
        self.ball_vy = 0.0  # initial y velocity (px/s)
        self.gravity = 200.0  # gravity acceleration (px/s^2)
        self.friction = 0.99  # friction coefficient per frame

        # Time keeping
        self.last_time = time.time()

        # Bind resize event
        self.root.bind("<Configure>", self._on_resize)

    def _on_resize(self, event: tk.Event) -> None:
        """Handle window resize events."""
        # Update canvas size
        self.width = event.width
        self.height = event.height
        # Update hexagon center and side length
        self.hex_center = (self.width / 2, self.height / 2)
        self.hex_side = min(self.width, self.height) * 0.4

    def _hex_vertices(self) -> list[tuple[float, float]]:
        """Calculate the vertices of the hexagon based on the current angle."""
        cx, cy = self.hex_center
        vertices = []
        for i in range(6):
            angle = self.hex_angle + i * math.radians(60)
            x = cx + self.hex_side * math.cos(angle)
            y = cy + self.hex_side * math.sin(angle)
            vertices.append((x, y))
        return vertices

    def _draw_hexagon(self) -> None:
        """Draw the hexagon on the canvas."""
        self.canvas.delete("hexagon")
        vertices = self._hex_vertices()
        # Create a flat list of coordinates for create_polygon
        points = [coord for vertex in vertices for coord in vertex]
        self.canvas.create_polygon(
            points,
            outline="black",
            fill="",
            width=2,
            tags="hexagon",
        )

    def _draw_ball(self) -> None:
        """Draw the ball on the canvas."""
        self.canvas.delete("ball")
        self.canvas.create_oval(
            self.ball_x - self.ball_radius,
            self.ball_y - self.ball_radius,
            self.ball_x + self.ball_radius,
            self.ball_y + self.ball_radius,
            fill="red",
            outline="black",
            width=1,
            tags="ball",
        )

    def _update(self) -> None:
        """Update the simulation state and redraw."""
        # Compute time delta
        now = time.time()
        dt = now - self.last_time
        self.last_time = now

        # Update hexagon rotation
        self.hex_angle += self.hex_speed * dt
        self.hex_angle %= 2 * math.pi

        # Update ball physics
        self.ball_vy += self.gravity * dt
        self.ball_x += self.ball_vx * dt
        self.ball_y += self.ball_vy * dt

        # Apply friction
        self.ball_vx *= self.friction
        self.ball_vy *= self.friction

        # Collision with hexagon walls
        vertices = self._hex_vertices()
        for i in range(6):
            p1 = vertices[i]
            p2 = vertices[(i + 1) % 6]
            # Edge vector
            ex = p2[0] - p1[0]
            ey = p2[1] - p1[1]
            # Normal (pointing inward)
            nx = -ey
            ny = ex
            # Normalize normal
            length = math.hypot(nx, ny)
            nx /= length
            ny /= length

            # Vector from p1 to ball center
            dx = self.ball_x - p1[0]
            dy = self.ball_y - p1[1]
            # Distance from ball center to edge
            dist = dx * nx + dy * ny
            if dist < self.ball_radius:
                # Ball is intersecting this edge; reflect velocity
                # Compute dot product of velocity with normal
                vdotn = self.ball_vx * nx + self.ball_vy * ny
                # Reflect: v' = v - 2 * (v·n) * n
                self.ball_vx -= 2 * vdotn * nx
                self.ball_vy -= 2 * vdotn * ny
                # Adjust position to be exactly at radius distance
                self.ball_x = p1[0] + dx - (dist - self.ball_radius) * nx
                self.ball_y = p1[1] + dy - (dist - self.ball_radius) * ny

        # Redraw
        self._draw_hexagon()
        self._draw_ball()
        # Schedule next update
        self.root.after(20, self._update)

    def run(self) -> None:
        """Start the Tkinter main loop."""
        self._draw_hexagon()
        self._draw_ball()
        self.root.after(20, self._update)
        self.root.mainloop()


def main() -> None:
    """Main entry point for the application."""
    App().run()


if __name__ == "__main__":
    main()
