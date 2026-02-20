"""
UI.py - Clue (SDEV265) GUI
Role: Ziad (UI/Board Design)

Run:
    python UI.py
"""

from __future__ import annotations
import tkinter as tk
from tkinter import ttk, messagebox

# --- Helpers --------------------------------------------------------------

def pos_to_rc(pos: int, grid_size: int) -> tuple[int, int]:
    """Convert 1-based position to (row, col)."""
    idx = max(1, pos) - 1
    return idx // grid_size, idx % grid_size


def rc_to_pos(r: int, c: int, grid_size: int) -> int:
    """Convert (row, col) to 1-based position."""
    return r * grid_size + c + 1


# --- UI -------------------------------------------------------------------

class ClueUI(tk.Tk):
    TILE = 42  # px

    def __init__(self, game):
        super().__init__()
        self.title("Clue - Digital (SDEV265)")

        # --- Game references ---
        self.game = game
        self.board = self.game.board_manager
        self.cards = self.game.card_manager
        self.turns = self.game.turn_manager
        self.players = self.game.players

        self.moves_remaining = 0
        self.in_room_name: str | None = None

        # Token colors
        self.token_colors = {
            "Red": "#e74c3c",
            "Blue": "#3498db",
            "Yellow": "#f1c40f",
            "Green": "#2ecc71",
        }

        self._build_layout()
        self._bind_keys()
        self._refresh_all()

        # Start first player's turn
        self._start_turn(self.game.current_player())

    # ----- Layout ---------------------------------------------------------

    def _build_layout(self):
        self.geometry("1120x760")
        self.minsize(980, 680)

        # Top bar
        top = ttk.Frame(self, padding=(10, 10, 10, 6))
        top.pack(side=tk.TOP, fill=tk.X)
        self.lbl_turn = ttk.Label(top, text="Turn: ", font=("Segoe UI", 12, "bold"))
        self.lbl_turn.pack(side=tk.LEFT)
        self.lbl_status = ttk.Label(top, text="", font=("Segoe UI", 10))
        self.lbl_status.pack(side=tk.LEFT, padx=(14, 0))
        self.lbl_moves = ttk.Label(top, text="Moves: 0", font=("Segoe UI", 10, "bold"))
        self.lbl_moves.pack(side=tk.RIGHT)

        # Main split
        main = ttk.Frame(self, padding=(10, 0, 10, 10))
        main.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Board canvas
        board_frame = ttk.Frame(main)
        board_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.canvas = tk.Canvas(
            board_frame,
            width=self.board.grid_size * self.TILE,
            height=self.board.grid_size * self.TILE,
            highlightthickness=1,
            highlightbackground="#999",
            bg="#1f1f1f",
        )
        self.canvas.pack(side=tk.TOP, anchor="nw")

        hint = ttk.Label(
            board_frame,
            text="Tip: Roll dice, then use arrow keys or the Move buttons.",
            font=("Segoe UI", 9),
        )
        hint.pack(side=tk.TOP, anchor="w", pady=(6, 0))

        # Side panel
        side = ttk.Frame(main, width=320)
        side.pack(side=tk.RIGHT, fill=tk.Y, padx=(12, 0))

        # Controls
        dice_box = ttk.Labelframe(side, text="Controls", padding=10)
        dice_box.pack(side=tk.TOP, fill=tk.X)
        self.btn_roll = ttk.Button(dice_box, text="Roll Dice", command=self._roll_dice, state=tk.DISABLED)
        self.btn_roll.pack(side=tk.TOP, fill=tk.X)

        mv = ttk.Frame(dice_box)
        mv.pack(side=tk.TOP, fill=tk.X, pady=(10, 0))
        self.btn_up = ttk.Button(mv, text="↑", command=lambda: self._move("up"), width=5)
        self.btn_left = ttk.Button(mv, text="←", command=lambda: self._move("left"), width=5)
        self.btn_down = ttk.Button(mv, text="↓", command=lambda: self._move("down"), width=5)
        self.btn_right = ttk.Button(mv, text="→", command=lambda: self._move("right"), width=5)
        self.btn_up.grid(row=0, column=1, padx=2, pady=2)
        self.btn_left.grid(row=1, column=0, padx=2, pady=2)
        self.btn_down.grid(row=1, column=1, padx=2, pady=2)
        self.btn_right.grid(row=1, column=2, padx=2, pady=2)
        for i in range(3):
            mv.grid_columnconfigure(i, weight=1)

        # Suggest/Accuse/End
        self.btn_suggest = ttk.Button(dice_box, text="Make Suggestion", command=self._suggest, state=tk.DISABLED)
        self.btn_accuse = ttk.Button(dice_box, text="Make Accusation", command=self._accuse, state=tk.DISABLED)
        self.btn_end = ttk.Button(dice_box, text="End Turn", command=self._end_turn)
        self.btn_suggest.pack(side=tk.TOP, fill=tk.X, pady=(10, 0))
        self.btn_accuse.pack(side=tk.TOP, fill=tk.X, pady=(6, 0))
        self.btn_end.pack(side=tk.TOP, fill=tk.X, pady=(10, 0))

        # Cards
        cards_box = ttk.Labelframe(side, text="Your Cards", padding=10)
        cards_box.pack(side=tk.TOP, fill=tk.X, pady=(10, 0))
        self.cards_list = tk.Listbox(cards_box, height=6)
        self.cards_list.pack(side=tk.TOP, fill=tk.X)

        # Detective Notepad
        notes_box = ttk.Labelframe(side, text="Detective Notepad", padding=10)
        notes_box.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=(10, 0))
        self.notebook = ttk.Notebook(notes_box)
        self.notebook.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self._note_vars = {"Suspects": {}, "Weapons": {}, "Rooms": {}}
        self._build_notepad_tab("Suspects", self.cards.suspects)
        self._build_notepad_tab("Weapons", self.cards.weapons)
        self._build_notepad_tab("Rooms", self.cards.rooms)

    def _build_notepad_tab(self, title: str, items: list[str]):
        frame = ttk.Frame(self.notebook, padding=8)
        self.notebook.add(frame, text=title)
        frame.grid_columnconfigure(0, weight=1)
        for i, name in enumerate(items):
            var = tk.BooleanVar(value=False)
            self._note_vars[title][name] = var
            cb = ttk.Checkbutton(frame, text=name, variable=var)
            cb.grid(row=i, column=0, sticky="w", pady=2)

    def _bind_keys(self):
        self.bind("<Up>", lambda e: self._move("up"))
        self.bind("<Down>", lambda e: self._move("down"))
        self.bind("<Left>", lambda e: self._move("left"))
        self.bind("<Right>", lambda e: self._move("right"))

    # ----- State & Refresh ------------------------------------------------

    def _set_status(self, msg: str):
        self.lbl_status.config(text=msg)

    def _refresh_all(self):
        self._refresh_topbar()
        self._refresh_controls()
        self._refresh_cards()
        self._draw_board()

    def _refresh_topbar(self):
        p = self._current_player()
        elim = " (ELIMINATED)" if p.is_eliminated else ""
        self.lbl_turn.config(text=f"Turn: {p.name}{elim}")
        self.lbl_moves.config(text=f"Moves: {self.moves_remaining}")

    def _refresh_controls(self):
        # Disable movement buttons if no moves
        state = tk.NORMAL if self.moves_remaining > 0 else tk.DISABLED
        self.btn_up.config(state=state)
        self.btn_down.config(state=state)
        self.btn_left.config(state=state)
        self.btn_right.config(state=state)

    def _refresh_cards(self):
        self.cards_list.delete(0, tk.END)
        for c in self._current_player().hand:
            self.cards_list.insert(tk.END, c)

    def _save_current_player_notes(self):
        player = self.game.current_player()

        for category, items in self._note_vars.items():
            for name, var in items.items():
                player.notes[category][name] = var.get()

    def _load_current_player_notes(self):
        player = self.game.current_player()

        for category, items in self._note_vars.items():
            for name, var in items.items():
                value = player.notes[category].get(name, False)
                var.set(value)

    # ----- Board Drawing --------------------------------------------------

    def _draw_board(self):
        self.canvas.delete("all")
        gs = self.board.grid_size
        walls = set(self.board.room_walls)
        entrances = dict(self.board.room_entrances)

        for r in range(gs):
            for c in range(gs):
                pos = rc_to_pos(r, c, gs)
                x1 = c * self.TILE
                y1 = r * self.TILE
                x2 = x1 + self.TILE
                y2 = y1 + self.TILE

                if pos in walls:
                    fill = "#2c2c2c"
                    outline = "#3a3a3a"
                elif pos in entrances:
                    fill = "#b58900"
                    outline = "#c9a227"
                else:
                    fill = "#d0d0d0"
                    outline = "#b9b9b9"

                self.canvas.create_rectangle(x1, y1, x2, y2, fill=fill, outline=outline)

                if pos in entrances:
                    room = entrances[pos]
                    self.canvas.create_text(
                        x1 + self.TILE / 2,
                        y1 + self.TILE / 2,
                        text=room[0],
                        font=("Segoe UI", 10, "bold"),
                        fill="#111",
                    )

        # Player tokens
        for p in self.players:
            r, c = pos_to_rc(p.position, gs)
            x1 = c * self.TILE + 6
            y1 = r * self.TILE + 6
            x2 = x1 + self.TILE - 12
            y2 = y1 + self.TILE - 12
            color = self.token_colors.get(p.name, "#ffffff")
            self.canvas.create_oval(x1, y1, x2, y2, fill=color, outline="#111", width=2)
            self.canvas.create_text(
                (x1 + x2) / 2,
                (y1 + y2) / 2,
                text=p.name[0],
                font=("Segoe UI", 10, "bold"),
                fill="#111",
            )

        # Highlight current player
        cp = self._current_player()
        r, c = pos_to_rc(cp.position, gs)
        x1 = c * self.TILE
        y1 = r * self.TILE
        x2 = x1 + self.TILE
        y2 = y1 + self.TILE
        self.canvas.create_rectangle(x1, y1, x2, y2, outline="#ff4d4d", width=3)

    # ----- Actions --------------------------------------------------------

    def _current_player(self):
        return self.game.current_player()

    def _start_turn(self, player):
        self.moves_remaining = 0
        self.btn_roll.config(state=tk.NORMAL)
        self._refresh_all()
        self._set_status(f"{player.name}'s turn. Roll dice to move!")

    def _roll_dice(self):
        self.btn_roll.config(state=tk.DISABLED)
        self.moves_remaining = self.game.dice_roll()
        self._refresh_all()
        self._set_status(f"{self._current_player().name} rolled {self.moves_remaining} moves!")

    def _move(self, direction: str):
        if self.moves_remaining <= 0:
            return
        success = self.game.get_movement(direction)
        if success:
            self.moves_remaining -= 1
            self._refresh_all()
            # Check if entered a room
            room_name = self.board.get_room_at_player(self._current_player())
            if room_name:
                self.btn_suggest.config(state=tk.NORMAL)
                self.btn_accuse.config(state=tk.NORMAL)
                self.moves_remaining = 0
                self._set_status(f"{self._current_player().name} entered {room_name}.")
        else:
            self._set_status("Cannot move there!")

    def _suggest(self):
        room = self.board.get_room_at_player(self._current_player())
        if not room:
            self._set_status("You must be in a room to make a suggestion.")
            return
        from tkinter.simpledialog import askstring
        # Collect suspect, weapon, room
        dialog = SuggestAccuseDialog(
            self,
            "Make Suggestion",
            self.cards.suspects,
            self.cards.weapons,
            [room],
            room_fixed=True
        )
        result = dialog.result
        if result:
            s, w, r = result
            res = self.game.handle_room_action("suggestion", s, w, r)
            if res["card_shown"]:
                self._set_status(f"Card shown: {res['card_shown']}")
            else:
                self._set_status("No card shown")
            #self._set_status(f"Card shown: {res['card_shown']}" if res["card_shown"] else "No card shown.")
        self._refresh_all()
        self.btn_suggest.config(state=tk.DISABLED)
        self.btn_accuse.config(state=tk.DISABLED)
        self.moves_remaining = 0

    def _accuse(self):
        room = self.board.get_room_at_player(self._current_player())
        dialog = SuggestAccuseDialog(
            self,
            "Make Accusation",
            self.cards.suspects,
            self.cards.weapons,
            self.cards.rooms,
            room_fixed=False
        )
        result = dialog.result
        if result:
            s, w, r = result
            res = self.game.handle_room_action("accusation", s, w, r)
            if res["correct_accusation"]:
                self._set_status(f"{self._current_player().name} won! Correct accusation.")
            else:
                print(f"{self._current_player().name}")
                #self._current_player().is_eliminated = True
                self._set_status(f"{self._current_player().name} is eliminated! Wrong accusation.")
                #self.game.advance_turn()
                #self._start_turn(self._current_player())
        self._refresh_all()
        self.btn_accuse.config(state=tk.DISABLED)
        self.btn_suggest.config(state=tk.DISABLED)

    def _end_turn(self):
        self._save_current_player_notes()
        self.game.advance_turn()
        self._load_current_player_notes()
        self._start_turn(self._current_player())


# --- Suggest/Accuse Dialog -----------------------------------------------

class SuggestAccuseDialog(tk.Toplevel):
    def __init__(
        self,
        parent: tk.Tk,
        title: str,
        suspects: list[str],
        weapons: list[str],
        rooms: list[str],
        room_fixed: bool,
    ):
        super().__init__(parent)
        self.title(title)
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        self.result = None

        pad = 12
        outer = ttk.Frame(self, padding=pad)
        outer.pack(fill=tk.BOTH, expand=True)

        ttk.Label(outer, text=title, font=("Segoe UI", 12, "bold")).grid(row=0, column=0, columnspan=2, sticky="w")
        ttk.Label(outer, text="Suspect:").grid(row=1, column=0, sticky="w", pady=(10, 2))
        ttk.Label(outer, text="Weapon:").grid(row=2, column=0, sticky="w", pady=2)
        ttk.Label(outer, text="Room:").grid(row=3, column=0, sticky="w", pady=2)

        self.s_var = tk.StringVar(value=suspects[0] if suspects else "")
        self.w_var = tk.StringVar(value=weapons[0] if weapons else "")
        self.r_var = tk.StringVar(value=rooms[0] if rooms else "")

        self.s_box = ttk.Combobox(outer, textvariable=self.s_var, values=suspects, state="readonly", width=24)
        self.w_box = ttk.Combobox(outer, textvariable=self.w_var, values=weapons, state="readonly", width=24)
        self.r_box = ttk.Combobox(
            outer,
            textvariable=self.r_var,
            values=rooms,
            state=("disabled" if room_fixed else "readonly"),
            width=24,
        )

        self.s_box.grid(row=1, column=1, sticky="ew", pady=(10, 2))
        self.w_box.grid(row=2, column=1, sticky="ew", pady=2)
        self.r_box.grid(row=3, column=1, sticky="ew", pady=2)

        btns = ttk.Frame(outer)
        btns.grid(row=4, column=0, columnspan=2, sticky="e", pady=(12, 0))
        ttk.Button(btns, text="Cancel", command=self._cancel).pack(side=tk.RIGHT, padx=(6, 0))
        ttk.Button(btns, text="Confirm", command=self._confirm).pack(side=tk.RIGHT)

        outer.grid_columnconfigure(1, weight=1)
        # Center on parent
        self.update_idletasks()
        px = parent.winfo_rootx() + 80
        py = parent.winfo_rooty() + 80
        self.geometry(f"+{px}+{py}")

        self.protocol("WM_DELETE_WINDOW", self._cancel)
        self.wait_window(self)

    def _confirm(self):
        s = self.s_var.get().strip()
        w = self.w_var.get().strip()
        r = self.r_var.get().strip()
        if not (s and w and r):
            messagebox.showerror("Missing info", "Please select suspect, weapon, and room.")
            return
        self.result = (s, w, r)
        self.destroy()

    def _cancel(self):
        self.result = None
        self.destroy()

