import ttkbootstrap as tb
from tkinter import font as tkfont


PALETTE = {
    "bg": "#F5F7FA",
    "surface": "#FFFFFF",
    "surface_alt": "#F8FAFC",
    "sidebar": "#0F172A",
    "sidebar_hover": "#1E293B",
    "sidebar_active": "#3B82F6",
    "text": "#1E293B",
    "muted": "#64748B",
    "border": "#E2E8F0",
    "accent": "#3B82F6",
    "success": "#10B981",
    "warning": "#F59E0B",
    "danger": "#EF4444",
    "info": "#0EA5E9",
    "card_gradient_start": "#667EEA",
    "card_gradient_end": "#764BA2",
}

FONTS = {
    "body": ("Segoe UI", 10),
    "body_bold": ("Segoe UI Semibold", 10),
    "subtitle": ("Segoe UI", 11),
    "title": ("Segoe UI Semibold", 26),
    "section": ("Segoe UI Semibold", 16),
    "metric_title": ("Segoe UI", 11),
    "metric_value": ("Segoe UI Semibold", 28),
    "sidebar": ("Segoe UI Semibold", 11),
}


def apply_global_styles(window):
    style = tb.Style()

    # Configurar fuentes
    style.configure(".", font=FONTS["body"])
    window.configure(bg=PALETTE["bg"])

    # Frames principales con esquinas redondeadas (simuladas)
    style.configure("App.TFrame", background=PALETTE["bg"])
    style.configure("Surface.TFrame", background=PALETTE["surface"])
    style.configure("Muted.TFrame", background=PALETTE["surface_alt"])
    style.configure(
        "Sidebar.TFrame",
        background=PALETTE["sidebar"],
    )

    # Labels del sidebar
    style.configure(
        "SidebarTitle.TLabel",
        background=PALETTE["sidebar"],
        foreground="#F1F5F9",
        font=("Segoe UI Semibold", 20),
    )
    style.configure(
        "SidebarLabel.TLabel",
        background=PALETTE["sidebar"],
        foreground="#94A3B8",
        font=FONTS["sidebar"],
    )
    
    # Labels de página
    style.configure(
        "PageTitle.TLabel",
        background=PALETTE["surface"],
        foreground=PALETTE["text"],
        font=FONTS["title"],
    )
    style.configure(
        "PageSubtitle.TLabel",
        background=PALETTE["surface"],
        foreground=PALETTE["muted"],
        font=FONTS["subtitle"],
    )
    style.configure(
        "SectionTitle.TLabel",
        background=PALETTE["surface"],
        foreground=PALETTE["text"],
        font=FONTS["section"],
    )
    style.configure(
        "SectionSubtitle.TLabel",
        background=PALETTE["surface"],
        foreground=PALETTE["muted"],
        font=FONTS["subtitle"],
    )
    style.configure(
        "MutedTitle.TLabel",
        background=PALETTE["surface_alt"],
        foreground=PALETTE["text"],
        font=FONTS["section"],
    )
    style.configure(
        "MutedSubtitle.TLabel",
        background=PALETTE["surface_alt"],
        foreground=PALETTE["muted"],
        font=FONTS["subtitle"],
    )

    # Botones del sidebar con diseño moderno
    style.configure(
        "Sidebar.TButton",
        background=PALETTE["sidebar"],
        foreground="#CBD5E1",
        font=FONTS["sidebar"],
        padding=(20, 14),
        anchor="w",
        borderwidth=0,
        relief="flat",
    )
    style.map(
        "Sidebar.TButton",
        background=[("active", PALETTE["sidebar_hover"])],
        foreground=[("active", "#FFFFFF")],
    )
    style.configure(
        "SidebarActive.TButton",
        background=PALETTE["sidebar_active"],
        foreground="#FFFFFF",
        font=("Segoe UI Semibold", 11),
        padding=(20, 14),
        anchor="w",
        borderwidth=0,
        relief="flat",
    )
    style.map(
        "SidebarActive.TButton",
        background=[("active", "#2563EB")],
        foreground=[("active", "#FFFFFF")],
    )

    # Treeview moderno
    style.configure(
        "Treeview",
        background=PALETTE["surface"],
        fieldbackground=PALETTE["surface"],
        foreground=PALETTE["text"],
        rowheight=38,
        relief="flat",
        borderwidth=0,
    )
    style.map(
        "Treeview",
        background=[("selected", PALETTE["accent"])],
        foreground=[("selected", "#FFFFFF")],
    )
    style.configure(
        "Treeview.Heading",
        background="#F1F5F9",
        foreground=PALETTE["text"],
        font=("Segoe UI Semibold", 10),
        padding=(12, 12),
        relief="flat",
        borderwidth=0,
    )
    style.map("Treeview.Heading", background=[("active", "#E2E8F0")])

    # Entradas y combobox modernos
    style.configure("TEntry", padding=10, borderwidth=0, relief="flat")
    style.configure("TCombobox", padding=10, borderwidth=0, relief="flat")
    style.configure("TLabelframe", background=PALETTE["surface"], borderwidth=0)
    style.configure(
        "TLabelframe.Label",
        background=PALETTE["surface"],
        foreground=PALETTE["muted"],
        font=FONTS["body_bold"],
    )
    
    # Botones personalizados con bordes redondeados
    style.configure(
        "Modern.TButton",
        padding=(16, 10),
        borderwidth=0,
        relief="flat",
    )

    return style


def register_metric_card_style(style, name, background, foreground="#FFFFFF", muted="#D9E2EC"):
    style.configure(f"{name}.TFrame", background=background)
    style.configure(
        f"{name}.Title.TLabel",
        background=background,
        foreground=muted,
        font=FONTS["metric_title"],
    )
    style.configure(
        f"{name}.Value.TLabel",
        background=background,
        foreground=foreground,
        font=FONTS["metric_value"],
    )
    style.configure(
        f"{name}.Note.TLabel",
        background=background,
        foreground=muted,
        font=FONTS["body"],
    )


def create_rounded_frame(parent, bg_color=None, padding=10, **kwargs):
    """
    Crea un frame con apariencia de tarjeta moderna.
    Nota: tkinter no soporta bordes redondeados nativamente,
    pero podemos simularlo con padding y colores.
    """
    if bg_color is None:
        bg_color = PALETTE["surface"]
    
    frame = tb.Frame(parent, padding=padding, **kwargs)
    return frame
