import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageEnhance, ImageDraw
import os


class TkView:

    def __init__(self, controller):
        self.controller = controller

        self.root = tk.Tk()
        self.root.title("Mestizaje - Latin American Art Experience")
        self.root.geometry("660x860")
        self.root.minsize(620, 780)
        # Launch in fullscreen for maximum visibility
        self.root.attributes("-fullscreen", True)

        # Palette
        self.bg_gradient_start = "#0b1224"
        self.bg_gradient_end = "#1c2740"
        self.card_bg = "#f4f7fb"
        self.border_color = "#cbd5e1"
        self.accent = "#7bdcb5"
        self.text_color = "#0b1224"
        self.text_muted = "#4b5563"
        self.fade_start = "#555555"

        # Compatibility colors used in fade/animation backgrounds
        self.bg_color = self.card_bg

        self.root.configure(bg=self.bg_gradient_start)

        self.bg_label = None
        self.bg_photo = None

        self._configure_styles()

        self.show_info = False
        self.selected_artwork_count = 40
        self.current_base_image = None
        self.info_label = None

        self.show_settings_screen()

    def _configure_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("TLabel",
                        background=self.card_bg,
                        foreground=self.text_color,
                        font=("Segoe UI", 13))

        style.configure("Glass.TFrame",
                        background=self.card_bg,
                        borderwidth=1,
                        relief="solid")

        style.configure("Heading.TLabel",
                        background=self.card_bg,
                        foreground=self.text_color,
                        font=("Segoe UI", 38, "bold"))

        style.configure("Subheading.TLabel",
                        background=self.card_bg,
                        foreground=self.text_color,
                        font=("Segoe UI", 22, "bold"))

        style.configure("Body.TLabel",
                        background=self.card_bg,
                        foreground=self.text_muted,
                        font=("Segoe UI", 14))

        style.configure("TButton",
                        background="#e2e8f0",
                        foreground=self.text_color,
                        padding=10,
                        font=("Segoe UI", 13, "bold"),
                        borderwidth=0)
        style.map("TButton", background=[("active", "#cbd5e1")])

        style.configure("Red.TButton",
                        background="#ef4444",
                        foreground="white",
                        padding=12,
                        font=("Segoe UI", 14, "bold"),
                        borderwidth=0)
        style.map("Red.TButton", background=[("active", "#dc2626")])

        style.configure("Green.TButton",
                        background="#10b981",
                        foreground="white",
                        padding=12,
                        font=("Segoe UI", 14, "bold"),
                        borderwidth=0)
        style.map("Green.TButton", background=[("active", "#059669")])

        style.configure("Gold.TButton",
                        background=self.accent,
                        foreground=self.text_color,
                        padding=12,
                        font=("Segoe UI", 14, "bold"),
                        borderwidth=0)
        style.map("Gold.TButton", background=[("active", "#68c5a2")])

        style.configure("Blue.TButton",
                        background="#2563eb",
                        foreground="white",
                        padding=12,
                        font=("Segoe UI", 14, "bold"),
                        borderwidth=0)
        style.map("Blue.TButton", background=[("active", "#1d4ed8")])

    def _clear_root(self):
        for w in self.root.winfo_children():
            w.destroy()

    def _render_background(self):
        width = max(self.root.winfo_width(), 780)
        height = max(self.root.winfo_height(), 960)
        gradient = Image.new("RGB", (width, height), color=self.bg_gradient_start)
        draw = ImageDraw.Draw(gradient)
        start_rgb = tuple(int(self.bg_gradient_start.lstrip("#")[i:i+2], 16) for i in (0, 2, 4))
        end_rgb = tuple(int(self.bg_gradient_end.lstrip("#")[i:i+2], 16) for i in (0, 2, 4))

        for y in range(height):
            ratio = y / max(1, height - 1)
            r = int(start_rgb[0] + (end_rgb[0] - start_rgb[0]) * ratio)
            g = int(start_rgb[1] + (end_rgb[1] - start_rgb[1]) * ratio)
            b = int(start_rgb[2] + (end_rgb[2] - start_rgb[2]) * ratio)
            draw.line([(0, y), (width, y)], fill=(r, g, b))

        self.bg_photo = ImageTk.PhotoImage(gradient)
        self.bg_label = tk.Label(self.root, image=self.bg_photo, borderwidth=0)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    def _reset_screen(self):
        self._clear_root()
        self._render_background()
        card = ttk.Frame(self.root, style="Glass.TFrame", padding=22)
        card.pack(padx=22, pady=22, fill="both", expand=True)
        return card

  
    def load_art_image(self, artwork):
        folder = os.path.dirname(artwork.path)
        file_id = os.path.splitext(os.path.basename(artwork.path))[0]

        extensions = [".jpg", ".jpeg", ".png", ".JPG", ".JPEG", ".PNG"]
        tried = []

        # Try the declared filename and a digits-only fallback (e.g., AG01 -> 01)
        name_candidates = [file_id]
        digits_only = "".join(ch for ch in file_id if ch.isdigit())
        if digits_only and digits_only not in name_candidates:
            name_candidates.append(digits_only)

        for name in name_candidates:
            for ext in extensions:
                candidate = os.path.join(folder, name + ext)
                tried.append(candidate)
                if os.path.exists(candidate):
                    try:
                        return Image.open(candidate).resize((460, 460))
                    except Exception:
                        pass

        print(f"[IMAGE NOT FOUND] Tried: {tried}")
        return Image.new("RGB", (550, 550), "gray")


    def fade_in_text(self, label, steps=10, delay=25):
        """Fade text from dark gray to black"""
        def fade(step=0):
            if step > steps:
                return

            shade = 85 - int(85 * (step / steps))  # 85 -> 0
            color = f"#{shade:02x}{shade:02x}{shade:02x}"

            label.config(foreground=color)
            self.root.after(delay, fade, step + 1)

        fade()

    def fade_out_text(self, label, callback=None, steps=10, delay=25):
        """Fade text from black to background color"""
        def fade(step=0):
            if step > steps:
                label.config(text="")
                if callback:
                    callback()
                return

            bg = self.bg_color.lstrip("#")
            bg_r = int(bg[0:2], 16)
            bg_g = int(bg[2:4], 16)
            bg_b = int(bg[4:6], 16)

            factor = step / steps

            r = int((1 - factor) * 0 + factor * bg_r)
            g = int((1 - factor) * 0 + factor * bg_g)
            b = int((1 - factor) * 0 + factor * bg_b)

            color = f"#{r:02x}{g:02x}{b:02x}"

            label.config(foreground=color)
            self.root.after(delay, fade, step + 1)

        fade()

    def show_settings_screen(self):
        card = self._reset_screen()

        title = ttk.Label(card, text="Mestizaje Settings",
                           style="Heading.TLabel")
        title.pack(pady=(12, 6))

        lbl = ttk.Label(card,
                        text="How many artworks would you like to explore?",
                        style="Body.TLabel")
        lbl.pack(pady=6)

        self.artwork_count_var = tk.IntVar(value=40)
        box = ttk.Combobox(card, textvariable=self.artwork_count_var,
                           values=[10, 20, 30, 40, 50],
                           state="readonly", width=12)
        box.pack(pady=14)

        continue_btn = ttk.Button(card, text="Continue",
                                  style="Gold.TButton",
                                  command=self.go_to_start_screen)
        continue_btn.pack(pady=18)

    def go_to_start_screen(self):
        self.selected_artwork_count = int(self.artwork_count_var.get())
        self.controller.__init__(self.controller.countries,
                                 max_artworks=self.selected_artwork_count)
        self.show_start_screen()

    def show_start_screen(self):
        card = self._reset_screen()

        title = ttk.Label(card, text="Mestizaje",
                           style="Heading.TLabel")
        title.pack(pady=60)

        start_btn = ttk.Button(card, text="Start",
                               style="Gold.TButton",
                               command=self.start_swiping)
        start_btn.pack(pady=40)

    def start_swiping(self):
        self.controller.start_session()
        self.show_info = False
        self.show_swipe_screen()

    def fade_in_image(self, img, steps=10, duration=150):
        delay = max(1, duration // steps)
        enhancer = ImageEnhance.Brightness(img)

        frames = []
        for i in range(steps):
            factor = i / (steps - 1)
            frame = enhancer.enhance(factor)
            frames.append(ImageTk.PhotoImage(frame))
        return frames, delay

    def swipe_animation(self, direction):
        img = self.current_base_image
        frames = []
        w, h = img.size

        for offset in range(0, 450, 50):
            bg = Image.new("RGB", (w, h), self.bg_color)
            frame = bg.copy()
            x = offset if direction == "right" else -offset
            frame.paste(img, (x, 0))
            frames.append(ImageTk.PhotoImage(frame))

        return frames


    def show_swipe_screen(self):
        card = self._reset_screen()

        artwork = self.controller.get_current_artwork()
        if not artwork:
            self.show_results_screen()
            return

        base_img = self.load_art_image(artwork)
        self.current_base_image = base_img
        img = base_img

        info_text = f"{artwork.artist.name} - {artwork.country.name}" if self.show_info else ""

        self.info_label = ttk.Label(card,
                                    text=info_text,
                                    style="Subheading.TLabel")
        self.info_label.pack(pady=(10, 4))

        if self.show_info:
            self.fade_in_text(self.info_label)

        frames, delay = self.fade_in_image(img)
        self.image_label = ttk.Label(card, background=self.card_bg)
        self.image_label.pack(pady=(8, 16))
        self.animate_frames(frames, delay)

        # Counter
        current, total = self.controller.get_counter()
        counter_label = ttk.Label(card, text=f"{current} / {total}",
                                  style="Body.TLabel")
        counter_label.pack(pady=4)

        # Buttons
        frame = ttk.Frame(card, style="Glass.TFrame")
        frame.pack(pady=16)

        ttk.Button(frame, text="Skip", style="Red.TButton",
                   command=lambda: self._handle("skip")).grid(row=0, column=0, padx=32)

        ttk.Button(frame, text="Show Info", style="Blue.TButton",
                   command=self._toggle_info).grid(row=0, column=1, padx=32)

        ttk.Button(frame, text="Like", style="Green.TButton",
                   command=lambda: self._handle("like")).grid(row=0, column=2, padx=32)


    def animate_frames(self, frames, delay):
        def step(i=0):
            if i < len(frames):
                self.image_label.config(image=frames[i])
                self.image_label.image = frames[i]
                self.root.after(delay, step, i + 1)
        step()

    def _toggle_info(self):
        self.show_info = not self.show_info
        self.show_swipe_screen()


    def _handle(self, direction):

        if self.info_label and self.info_label.cget("text"):
            self.fade_out_text(self.info_label, callback=lambda: self._finish_swipe(direction))
        else:
            self._finish_swipe(direction)

    def _finish_swipe(self, direction):
        """Perform swipe after fade-out finishes"""
        frames = self.swipe_animation("right" if direction == "like" else "left")

        def animate(i=0):
            if i < len(frames):
                self.image_label.config(image=frames[i])
                self.image_label.image = frames[i]
                self.root.after(10, animate, i + 1)
            else:
                self.controller.handle_choice(direction)
                if self.controller.is_session_finished():
                    self.show_results_screen()
                else:
                    self.show_swipe_screen()

        animate()

    def show_results_screen(self):
        card = self._reset_screen()

        title = ttk.Label(card,
                          text="Your Favorite Countries",
                          style="Subheading.TLabel")
        title.pack(pady=30)

        results = self.controller.get_results()

        def fade_word(country, delay):
            lbl = ttk.Label(card, text=country,
                            font=("Segoe UI", 20, "bold"),
                            foreground=self.text_color,
                            background=self.card_bg)
            self.root.after(delay, lbl.pack, {"pady": 10})

        delay = 0
        for c in results:
            fade_word(c, delay)
            delay += 300

        again = ttk.Button(card, text="Play Again",
                           style="Gold.TButton",
                           command=self.show_settings_screen)
        self.root.after(delay + 500, again.pack, {"pady": 24})

    def run(self):
        self.root.mainloop()
