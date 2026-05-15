import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from image_processor import ImageProcessor
from game_logic import GameLogic

# Main game window class
class GameUI(tk.Tk):
    # BG color and bullet points to be used later
    BG = "#f6f6f6"
    bullet = "\u2022"
    def __init__(self):
        super().__init__()
        # Setting up the window
        self.title("Spot the Differences!")
        self.configure(bg=self.BG)
        self.geometry("1200x800")

        # Widget variables
        self.headerframe = None
        self.load_btn = None
        self.reveal_btn = None
        self.new_btn = None
        self.title_label = None

        # Separating different sections
        self.setup_root_grid()
        self.setup_header()
        self.setup_image_space()
        self.setup_footer()

        # Objects from classes
        self.ip = ImageProcessor(self.copy_img_label, self.ori_img_label)
        self.logic = GameLogic()


        self.set_reveal_btn(False)
        self.load_default_image()

    # Row and column configuration
    def setup_root_grid(self):
        self.columnconfigure(0, weight=1)
        # Header
        self.rowconfigure(0, weight=0)
        # Images
        self.rowconfigure(1, weight=1)
        # Footer
        self.rowconfigure(2, weight=0)

    # Creating the top header section
    def setup_header(self):
        self.headerframe = tk.Frame(self, bg=self.BG, pady=10)

        self.headerframe.columnconfigure(0, weight=1)
        self.headerframe.columnconfigure(1, weight=8)
        self.headerframe.columnconfigure(2, weight=1)

        self.headerframe.grid(row=0, column=0, sticky="ew")

        # Header Buttons
        self.load_btn = tk.Button(
            self.headerframe,
            text="Load Image",
            font=("Open Sans", 16),
            borderwidth=0,
            highlightthickness=0,
            command=self.load_image
        )
        self.load_btn.grid(row=0, column=0)

        self.reveal_btn = tk.Button(
            self.headerframe,
            text="Reveal Differences",
            font=("Open Sans", 16),
            borderwidth=0,
            highlightthickness=0, command=self.reveal_differences)
        self.reveal_btn.grid(row=0, column=2)

        # Title of the Game
        self.title_label = tk.Label(self.headerframe,
                               text="Spot the Difference!",
                               font=("Arial", 22, "bold",),
                               bg=self.BG, fg="black")
        self.title_label.grid(row=0, column=1)

    # The section for containing the images
    def setup_image_space(self):
        self.image_frame = tk.Frame(self, bg=self.BG, padx=10, pady=10)

        self.image_frame.columnconfigure(0, weight=1)
        self.image_frame.columnconfigure(1, weight=1)

        self.image_frame.grid(row=1, column=0, sticky="nsew")

        self.setup_original_image()
        self.setup_duplicate_image()

    def setup_original_image(self):
        self.ori_frame = tk.Frame(self.image_frame, bg=self.BG, padx=20, pady=10, bd=1, relief="solid")
        self.ori_frame.grid(row=0, column=0, sticky="n")

        self.ori_img_text = tk.Label(self.ori_frame,
                                text="Original Image",
                                font=("Arial", 14),
                                bg=self.BG,
                                fg="#656364",
                                pady=10)
        self.ori_img_text.grid(row=0, column=0)

        self.ori_img = Image.open("Images/placeholder_image.png").resize((500, 500))
        self.ori_img = ImageTk.PhotoImage(self.ori_img)

        self.ori_img_label = tk.Label(self.ori_frame, image=self.ori_img)
        self.ori_img_label.grid(row=1, column=0)


    def setup_duplicate_image(self):
        self.copy_frame = tk.Frame(self.image_frame, bg=self.BG, padx=15, pady=10, bd=1, relief="solid")
        self.copy_frame.grid(row=0, column=1, padx=10, sticky="n")

        self.copy_img_text = tk.Label(self.copy_frame,
                                 text="Altered Image (Click on the Differences!)",
                                 font=("Arial", 14),
                                 bg=self.BG,
                                 fg="#656364",
                                 pady=10)
        self.copy_img_text.grid(row=0, column=0)

        self.copy_img = Image.open("Images/placeholder_image.png").resize((500, 500))
        self.copy_img = ImageTk.PhotoImage(self.copy_img)

        self.copy_img_label = tk.Label(self.copy_frame, image=self.copy_img)
        self.copy_img_label.grid(row=1, column=0)
        self.copy_img_label.bind("<Button-1>", self.on_click)

    # Setting up the footer section
    def setup_footer(self):
        self.footer_frame = tk.Frame(self, bg=self.BG, padx=10, pady=10)

        self.footer_frame.columnconfigure(0, weight=1)
        self.footer_frame.columnconfigure(1, weight=1)
        self.footer_frame.columnconfigure(2, weight=1)

        self.footer_frame.grid(row=2, column=0, sticky="ew")

        self.counts()
        self.setup_instructions()
        self.setup_status()
    # To display remaining differences and mistakes
    def counts(self):
        self.count_frame = tk.Frame(self.footer_frame, bg=self.BG, padx=10, pady=10)
        self.count_frame.columnconfigure(0, weight=1)
        self.count_frame.columnconfigure(1, weight=1)
        self.count_frame.grid(row=0, column=0)

        # Remaining
        self.title_frame = tk.Frame(self.count_frame, bg=self.BG, padx=10, pady=10, bd=0.5, relief="solid")
        self.title_frame.grid(row=0, column=0, padx=10)

        self.rem_title = tk.Label(self.title_frame,
                             text="Remaining Differences",
                             font=("Arial", 16, "bold"),
                             bg=self.BG,
                             fg="black",
                             pady=10)
        self.rem_title.grid(row=0, column=0)

        self.rem_count_text = tk.Label(self.title_frame,
                             text="5",
                             font=("Arial", 35, "bold"),
                             bg=self.BG,
                             fg="green")
        self.rem_count_text.grid(row=1, column=0)

        self.rem_ins = tk.Label(self.title_frame,
                           text="(Find all 5)",
                           font=("Arial", 14),
                           bg=self.BG,
                           fg="black")
        self.rem_ins.grid(row=2, column=0)

        # Mistakes

        self.mistake_frame = tk.Frame(self.count_frame, bg=self.BG, padx=50, pady=10, bd=0.5, relief="solid")
        self.mistake_frame.grid(row=0, column=1, padx=10)

        self.mistake_title = tk.Label(self.mistake_frame,
                                 text="Mistakes",
                                 font=("Arial", 16, "bold"),
                                 bg=self.BG,
                                 fg="black",
                                 pady=10)
        self.mistake_title.grid(row=0, column=0)

        self.mistake_count_text = tk.Label(self.mistake_frame,
                                 text="0",
                                 font=("Arial", 35, "bold"),
                                 bg=self.BG,
                                 fg="green")
        self.mistake_count_text.grid(row=1, column=0)

        self.mistake_ins = tk.Label(self.mistake_frame,
                               text="Max 3",
                               font=("Arial", 14),
                               bg=self.BG,
                               fg="black")
        self.mistake_ins.grid(row=2, column=0)

    # Instructions sections
    def setup_instructions(self):
        self.ins_frame = tk.Frame(self.footer_frame, bg=self.BG, padx=10, pady=10, bd=0.5, relief="solid")
        self.ins_frame.grid(row=0, column=1, padx=10)

        self.ins_title = tk.Label(self.ins_frame,
                             text="How to Play",
                             font=("Arial", 16),
                             bg=self.BG,
                             fg="#656364")
        self.ins_title.grid(row=0, column=0)

        self.ins_text = tk.Label(self.ins_frame, text=f"{self.bullet} Click on the right image to find the differences.\n"
                                            f"{self.bullet} Correct clicks are market with a red circle.\n"
                                            f"{self.bullet} Wrong clicks increase your mistakes.\n"
                                            f"{self.bullet} You can make up to 3 mistakes.\n"
                                            f"{self.bullet} Click Reveal Differences to see remaining differences.",
                            justify="left",
                            font=("Arial", 14),
                            bg=self.BG,
                            fg="#656364")
        self.ins_text.grid(row=1, column=0)

    def setup_status(self):
        self.status_frame = tk.Frame(self.footer_frame, bg=self.BG, padx=10, pady=10, bd=0.5, relief="solid")
        self.status_frame.grid(row=0, column=2, padx=10)

        self.status_title = tk.Label(self.status_frame,
                                text="Status",
                                font=("Arial", 16, "bold"),
                                bg=self.BG,
                                fg="black")
        self.status_title.grid(row=0, column=0)

        self.status_text1 = tk.Label(self.status_frame,
                                text="Game Not Started",
                                font=("Arial", 16, "bold"),
                                bg=self.BG,
                                fg="orange")
        self.status_text1.grid(row=1, column=0)

        self.status_text2 = tk.Label(self.status_frame,
                                text="Load an Image",
                                font=("Arial", 14),
                                bg=self.BG,
                                fg="#656364")
        self.status_text2.grid(row=2, column=0)

        self.status_text3 = tk.Label(self.status_frame,
                                text="to Get Started!",
                                font=("Arial", 14),
                                bg=self.BG,
                                fg="#656364")
        self.status_text3.grid(row=3, column=0)

    # Function for opening the file explorer and loading up an image selection by user
    def load_image(self):
        self.file_path = filedialog.askopenfilename(
            title="Select an Image",
            filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp *.gif")]
        )
        # Function stops if user cancels
        if not self.file_path:
            return

        # Set up the size of the selected image
        self.img = Image.open(self.file_path).resize((500, 500))
        # Displaying the original image
        self.ori_img = ImageTk.PhotoImage(self.img)
        self.ori_img_label.configure(image=self.ori_img)

        # Loading the altered image from image processor class
        self.ip.create_copy(self.img)

        self.reset_game()
    # Function for loading default placeholder images
    def load_default_image(self):
        self.img = Image.open("Images/placeholder_image.png").resize((500, 500))
        self.ori_img_tk= ImageTk.PhotoImage(self.img)
        self.ori_img_label.configure(image=self.ori_img_tk)

        self.copy_img_tk = ImageTk.PhotoImage(self.img)
        self.copy_img_label.configure(image=self.copy_img_tk)

    # Mouse click handling
    def on_click(self, event):
        # Failsafe that stops click when the game is inactive
        if not self.logic.started or self.logic.is_lost() or self.logic.is_won():
            return

        # Check if click hit a difference
        hit_index = self.ip.find_hit(event.x, event.y, self.logic.found)

        # If player clicked a correct difference
        if hit_index is not None:
            # Hitbox's center position
            cx, cy = self.ip.get_center(hit_index)
            # Saving correct hit
            self.logic.register_hit(hit_index)
            # Drawing red circle
            self.ip.mark_difference(cx, cy, color=(0, 0, 255))
            self.ip.mark_original(cx, cy, color=(0, 0, 255))
            # Updating remaining difference counter
            self.rem_count_text.configure(text=str(self.logic.remaining()))
            # Condition to see winning
            if self.logic.is_won():
                self.status_text1.configure(text="You have found all the differences!", fg="green")
                self.status_text2.configure(text="You have won the game!", fg="green")
                self.status_text3.configure(text="LOAD A NEW IMAGE TO TRY AGAIN!", fg="green")
                self.set_reveal_btn(False)
        else:
            self.logic.register_miss()
            self.mistake_count_text.configure(text=str(self.logic.mistakes))
            if self.logic.is_lost():
                self.status_text1.configure(text="Game Over!", fg="red")
                self.status_text2.configure(text="Too Many Mistakes!", fg="red")
                self.status_text3.configure(text="LOAD A NEW IMAGE TO RETRY", fg="red")
                self.set_reveal_btn(False)

    def reset_game(self):
        self.logic.reset()
        self.rem_count_text.configure(text='5', fg='green')
        self.mistake_count_text.configure(text="0", fg='green')
        self.status_text1.configure(text="Game in Progress", fg='green')
        self.status_text2.configure(text="Click on the right image.")
        self.status_text3.configure(text="to find the differences.")
        self.set_reveal_btn(True)

    def reveal_differences(self):
        for i, diff in enumerate(self.ip.differences):
            if i not in self.logic.found:
                _, cx, cy, *_ = diff
                self.ip.mark_difference(cx, cy, color=(255, 0, 0))
                self.ip.mark_original(cx, cy, color=(255, 0, 0))
        self.logic.found = set(range(5))  # mark all as found so clicks stop
        self.rem_count_text.configure(text="0")
        self.status_text1.configure(text="Differences Revealed", fg="orange")
        self.status_text2.configure(text="Load a new image")
        self.status_text3.configure(text="to play again.")
        self.set_reveal_btn(False)

    def set_reveal_btn(self, enabled):
        state = tk.NORMAL if enabled else tk.DISABLED
        self.reveal_btn.configure(state=state)

