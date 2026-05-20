# main.py
import flet as ft
import flet.canvas as cv
from core.ultimate_ttt import UltimateTTTEngine


def main(page: ft.Page):
    page.title = "Classic Tic-Tac-Toe"
    page.window.width = 420
    page.window.height = 620
    page.window.resizable = False
    page.theme_mode = ft.ThemeMode.DARK
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    ttt_engine = UltimateTTTEngine()
    ttt_buttons = {}
    ttt_text_controls = {}

    status_label = ft.Text(value="Player X's Turn", size=18, weight=ft.FontWeight.BOLD, color="#48bb78")

    # Interactive item selection selector radios
    piece_selector = ft.RadioGroup(
        content=ft.Row(
            controls=[
                ft.Radio(value="X", label="Place X", fill_color="#63b3ed"),
                ft.Radio(value="O", label="Place O", fill_color="#fc8181"),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=30
        ),
        value="X",
    )

    # Isolated canvas tool layer (Stored globally but appended dynamically on win)
    line_canvas = cv.Canvas(
        width=286,
        height=286,
        shapes=[],
    )

    # Pixel coordinate tracks for drawing paths
    LINE_COORDINATES = {
        0: (15, 45, 271, 45),  # Row 0
        1: (15, 143, 271, 143),  # Row 1
        2: (15, 241, 271, 241),  # Row 2
        3: (45, 15, 45, 271),  # Column 0
        4: (143, 15, 143, 271),  # Column 1
        5: (241, 15, 241, 271),  # Column 2
        6: (25, 25, 261, 261),  # Diagonal 0
        7: (261, 25, 25, 261),  # Diagonal 1
    }

    def handle_ttt_click(idx):
        # Read active radio selection state parameter right before calling engine logic
        ttt_engine.current_player = piece_selector.value
        if ttt_engine.make_move(idx):
            piece_selector.value = ttt_engine.current_player
            update_ttt_ui()

    def update_ttt_ui():
        for i in range(9):
            cell = ttt_buttons[i]
            txt_ctrl = ttt_text_controls[i]
            val = ttt_engine.board[i]

            txt_ctrl.value = val if val else ""
            txt_ctrl.color = "#63b3ed" if val == 'X' else "#fc8181" if val == 'O' else "white"

            if ttt_engine.winner:
                cell.bgcolor = "#1a202c"
                cell.opacity = 0.5
            else:
                cell.bgcolor = "#2d3748" if val is None else "#1a202c"
                cell.opacity = 1.0

        # FIX 1: Corrected y2 index map step and render canvas dynamically ONLY on match win
        if ttt_engine.winner and ttt_engine.winning_combo_idx is not None and len(line_canvas.shapes) == 0:
            coords = LINE_COORDINATES[ttt_engine.winning_combo_idx]
            line_color = "#63b3ed" if ttt_engine.winner == 'X' else "#fc8181"

            line_canvas.shapes.append(
                cv.Line(
                    x1=coords[0], y1=coords[1],
                    x2=coords[2], y2=coords[3],  # Fixed index coordinate assignment bug
                    paint=ft.Paint(
                        stroke_width=6,
                        color=line_color,
                        stroke_cap=ft.StrokeCap.ROUND
                    )
                )
            )
            # Securely overlay drawing layer only when interactions are disabled
            if line_canvas not in stacked_game_board.controls:
                stacked_game_board.controls.append(line_canvas)

        if ttt_engine.winner:
            if ttt_engine.winner == "Draw":
                status_label.value = "Game Over! It's a Draw!"
                status_label.color = "#ecc94b"
            else:
                status_label.value = f"Victory! Player {ttt_engine.winner} Wins!"
                status_label.color = "#63b3ed" if ttt_engine.winner == 'X' else "#fc8181"
        else:
            status_label.value = f"Player {ttt_engine.current_player}'s Turn"
            status_label.color = "#48bb78" if ttt_engine.current_player == 'X' else "#ed8936"

        page.update()

    def reset_ttt_match(e=None):
        ttt_engine.reset_game()
        piece_selector.value = "X"
        line_canvas.shapes.clear()
        # Cleanly lift overlay sheet away from active interaction grid container bounds
        if line_canvas in stacked_game_board.controls:
            stacked_game_board.controls.remove(line_canvas)
        update_ttt_ui()

    # FIX 2: Added Global Keyboard Integration Hook Matrix System
    def on_keyboard(e: ft.KeyboardEvent):
        key_input = e.key.upper() if e.key else ""

        # Part A: Hotkey mapping for structural piece selection swaps
        if key_input == "X":
            piece_selector.value = "X"
            page.update()
            return
        elif key_input == "O":
            piece_selector.value = "O"
            page.update()
            return

        # Part B: Grid tile allocations matching numerical inputs 1-9
        key_coordinate_map = {
            "1": 0, "2": 1, "3": 2,
            "4": 3, "5": 4, "6": 5,
            "7": 6, "8": 7, "9": 8
        }

        if e.key in key_coordinate_map:
            handle_ttt_click(key_coordinate_map[e.key])
        elif "NUMPAD" in key_input:
            numpad_digit = e.key.split()[-1]
            if numpad_digit in key_coordinate_map:
                handle_ttt_click(key_coordinate_map[numpad_digit])

        # Part C: Quick match layout clearing
        if key_input == "R" or e.key == "Escape":
            reset_ttt_match()

    def build_classic_board():
        ttt_buttons.clear()
        ttt_text_controls.clear()

        grid_rows = []
        for r_idx in range(3):
            row_cells = []
            for c_idx in range(3):
                idx = r_idx * 3 + c_idx
                text_ctrl = ft.Text(value="", size=32, weight=ft.FontWeight.BOLD)

                cell_box = ft.Container(
                    content=text_ctrl,
                    alignment=ft.Alignment(0, 0),
                    width=90,
                    height=90,
                    bgcolor="#2d3748",
                    border=ft.Border.all(2, "#1a202c"),
                    border_radius=12,
                    on_click=lambda e, cell_idx=idx: handle_ttt_click(cell_idx)
                )

                ttt_buttons[idx] = cell_box
                ttt_text_controls[idx] = text_ctrl
                row_cells.append(cell_box)

            grid_rows.append(ft.Row(controls=row_cells, alignment=ft.MainAxisAlignment.CENTER, spacing=8))

        return ft.Column(controls=grid_rows, alignment=ft.MainAxisAlignment.CENTER, spacing=8)

    board_element = build_classic_board()

    # Assembly frame stack layout container wrapper holding interactive elements safely
    stacked_game_board = ft.Stack(
        controls=[
            ft.Container(content=board_element, alignment=ft.Alignment(0, 0))
            # Notice line_canvas is NOT placed here on startup so clicks pass through flawlessly
        ],
        width=286,
        height=286
    )

    page.add(
        ft.Container(
            content=ft.Column(
                controls=[
                    status_label,
                    ft.Divider(height=10, color="transparent"),
                    piece_selector,
                    ft.Divider(height=15, color="transparent"),
                    stacked_game_board,
                    ft.Divider(height=25, color="transparent"),
                    ft.ElevatedButton(
                        content=ft.Text("Reset Match State", color="white", weight=ft.FontWeight.BOLD),
                        icon=ft.Icons.REFRESH,
                        bgcolor="#2b6cb0",
                        on_click=reset_ttt_match,
                        height=48,
                        width=290
                    )
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            padding=20
        )
    )

    # Mount keyboard capture event listeners right before tracking instantiation loop completes
    page.on_keyboard_event = on_keyboard
    update_ttt_ui()


if __name__ == "__main__":
    ft.run(main)