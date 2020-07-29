import pandemic as pd
from typing import Optional
import tkinter as tk
import os
import sys


def main():
    if len(sys.argv) != 2 or os.path.isdir(sys.argv[1]):
        print("Usage: {} parameters.json".format(sys.argv[0]))
        sys.exit(1)

    params: str = sys.argv[1]

    try:
        simulator: Optional[pd.Simulator] = pd.Simulator.from_params(params)
    except KeyboardInterrupt:
        print("Interrupted")
        sys.exit(1)

    if simulator is None:
        print("Invalid parameters file {}".format(params))
        return

    GUI(simulator)()


def create_circle(canvas: tk.Canvas, x: int, y: int, r: int, **kwargs):
    return canvas.create_oval(x-r, y-r, x+r, y+r, **kwargs)


class GUI:
    color_susceptible: str = "#0000aa"
    color_infected: str = "#aa0000"
    color_patched: str = "#00aa00"

    def __init__(
        self,
        simulator: pd.Simulator,
    ):
        self.simulator: pd.Simulator = simulator
        self.ms = simulator.params.ms

        width = simulator.params.width
        height: int = int(width * simulator.params.map_size.y / simulator.params.map_size.x)
        self.scale = width / simulator.params.map_size.x

        self.root = tk.Tk()

        self.frame = tk.Frame(self.root, relief=tk.RAISED, borderwidth=1)

        label_frame_epoch = tk.LabelFrame(self.frame, text="Epoch")
        self.label_epoch = tk.Label(label_frame_epoch, text="0")
        self.label_epoch.pack(side=tk.RIGHT)
        label_frame_epoch.pack(side=tk.LEFT, expand="yes", fill=tk.BOTH)

        label_frame_patched = tk.LabelFrame(
            self.frame, text="Patched", foreground=self.color_patched)
        self.label_patched = tk.Label(label_frame_patched, text=self.label_patched_text())
        self.label_patched.pack(side=tk.RIGHT)
        label_frame_patched.pack(side=tk.LEFT, expand="yes", fill=tk.BOTH)

        label_frame_susceptible = tk.LabelFrame(
            self.frame, text="Susceptible", foreground=self.color_susceptible)
        self.label_susceptible = tk.Label(label_frame_susceptible, text="0")
        self.label_susceptible.pack(side=tk.RIGHT)
        label_frame_susceptible.pack(side=tk.LEFT, expand="yes", fill=tk.BOTH)

        label_frame_infected = tk.LabelFrame(
            self.frame, text="Infected", foreground=self.color_infected)
        self.label_infected = tk.Label(label_frame_infected, text="0")
        self.label_infected.pack(side=tk.RIGHT)
        label_frame_infected.pack(side=tk.LEFT, expand="yes", fill=tk.BOTH)

        self.stop_button_pressed: bool = False
        self.button_stop = tk.Button(
            self.frame, text="Stop", width=10, command=self.stop_button_command)
        self.button_stop.pack(side=tk.BOTTOM, padx=5, pady=1)

        self.frame.pack(fill=tk.BOTH, expand=True)

        canvas_frame = tk.Frame(self.root, relief=tk.RAISED, borderwidth=1)
        self.canvas = tk.Canvas(canvas_frame, height=height, width=width)
        self.canvas.pack()
        canvas_frame.pack()

    def __call__(self):
        def render_loop():
            try:
                self.step()
                self.all()

                if self.loop_stop_condition():
                    raise StopIteration()

                self.root.after(self.ms, render_loop)

            except StopIteration:
                self.stop()

        self.all()
        self.root.after(self.ms, render_loop)
        self.root.mainloop()

    def step(self):
        self.simulator.step()
        self.label_epoch["text"] = self.simulator.epoch
        self.label_susceptible["text"] = len(self.simulator.susceptible_peers)
        self.label_infected["text"] = len(self.simulator.infected_peers)
        self.label_patched["text"] = self.label_patched_text()

    def all(self):
        self.canvas.delete("all")

        for hotspot in self.simulator.map.hotspots:
            self.hotspot_fill(hotspot)

        for peer in self.simulator.map.peers:
            self.peer_fill(peer)

        for hotspot in self.simulator.map.hotspots:
            self.hotspot_outline(hotspot)

        for peer in self.simulator.patched_peers.values():
            self.peer_outline(peer)

        for peer in self.simulator.susceptible_peers.values():
            self.peer_outline(peer)

        for peer in self.simulator.infected_peers.values():
            self.peer_outline(peer)

    def hotspot_outline(self, hotspot: pd.Hotspot):
        create_circle(
            self.canvas,
            int(self.scale * hotspot.position.x),
            int(self.scale * hotspot.position.y),
            int(self.scale * hotspot.radius),
            outline="#0000ff")

    def hotspot_fill(self, hotspot: pd.Hotspot):
        create_circle(
            self.canvas,
            int(self.scale * hotspot.position.x),
            int(self.scale * hotspot.position.y),
            int(self.scale * hotspot.radius),
            outline="#fffff0",
            fill="#fffff0")

    def peer_outline(self, peer: pd.Peer):
        color = self.peer_color_outline(peer)
        create_circle(
            self.canvas,
            int(self.scale * peer.position.x),
            int(self.scale * peer.position.y),
            int(self.scale * peer.radius),
            outline=color)

    def peer_fill(self, peer: pd.Peer):
        color = self.peer_color_fill(peer)
        create_circle(
            self.canvas,
            int(self.scale * peer.position.x),
            int(self.scale * peer.position.y),
            int(self.scale * peer.radius),
            outline=color,
            fill=color)

    def peer_color_outline(self, peer: pd.Peer) -> str:
        if peer.infection_state == pd.IState.SUSCEPTIBLE:
            return self.color_susceptible
        elif peer.infection_state == pd.IState.INFECTIOUS:
            return self.color_infected
        else:
            return self.color_patched

    def peer_color_fill(self, peer: pd.Peer) -> str:
        if peer.infection_state == pd.IState.SUSCEPTIBLE:
            return "#f0f0ff"
        elif peer.infection_state == pd.IState.INFECTIOUS:
            return "#fff0f0"
        else:
            return "#f0fff0"

    def label_patched_text(self) -> str:
        if self.simulator.params.patching_begin_epoch is None:
            return "No Patch"
        if self.simulator.epoch < self.simulator.params.patching_begin_epoch:
            return "Begins at Epoch {}".format(self.simulator.params.patching_begin_epoch)
        return str(len(self.simulator.patched_peers))

    def loop_stop_condition(self) -> bool:
        return self.stop_button_pressed or self.simulator.stop_condition()

    def stop_button_command(self):
        self.stop_button_pressed = True

    def stop(self):
        self.button_stop["state"] = "disabled"

        if self.simulator.params.output_directory is not None and self.simulator.output():
            self.button_stop["text"] = "Savatage Error"
            return

        self.button_stop["text"] = "Stopped"


if __name__ == "__main__":
    main()
