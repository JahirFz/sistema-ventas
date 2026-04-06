import ttkbootstrap as tb


PALETTE = {
    "bg": "#EEF3F8",
    "surface": "#FFFFFF",
    "surface_alt": "#F7FAFC",
    "sidebar": "#102033",
    "sidebar_hover": "#1A314C",
    "sidebar_active": "#2F7AF8",
    "text": "#102A43",
    "muted": "#6B7C93",
    "border": "#D9E2EC",
    "accent": "#2F7AF8",
    "success": "#1F9D73",
    "warning": "#F0A202",
    "danger": "#D64550",
    "info": "#2680C2",
}

FONTS = {
    "body": ("Segoe UI", 10),
    "body_bold": ("Segoe UI Semibold", 10),
    "subtitle": ("Segoe UI", 11),
    "title": ("Segoe UI Semibold", 24),
    "section": ("Segoe UI Semibold", 18),
    "metric_title": ("Segoe UI Semibold", 11),
    "metric_value": ("Segoe UI Semibold", 22),
}


def apply_global_styles(window):
    style = tb.Style()

    style.configure(".", font=FONTS["body"])
    window.configure(bg=PALETTE["bg"])

    style.configure("App.TFrame", background=PALETTE["bg"])
    style.configure("Surface.TFrame", background=PALETTE["surface"])
    style.configure("Muted.TFrame", background=PALETTE["surface_alt"])
    style.configure(
        "Sidebar.TFrame",
        background=PALETTE["sidebar"],
    )

    style.configure(
        "SidebarTitle.TLabel",
        background=PALETTE["sidebar"],
        foreground=PALETTE["surface"],
        font=("Segoe UI Semibold", 18),
    )
    style.configure(
        "SidebarLabel.TLabel",
        background=PALETTE["sidebar"],
        foreground="#9FB3C8",
        font=FONTS["subtitle"],
    )
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

    style.configure(
        "Sidebar.TButton",
        background=PALETTE["sidebar"],
        foreground="#D9E2EC",
        font=FONTS["body_bold"],
        padding=(16, 12),
        anchor="w",
        borderwidth=0,
        relief="flat",
    )
    style.map(
        "Sidebar.TButton",
        background=[("active", PALETTE["sidebar_hover"])],
        foreground=[("active", PALETTE["surface"])],
    )
    style.configure(
        "SidebarActive.TButton",
        background=PALETTE["sidebar_active"],
        foreground=PALETTE["surface"],
        font=FONTS["body_bold"],
        padding=(16, 12),
        anchor="w",
        borderwidth=0,
        relief="flat",
    )
    style.map(
        "SidebarActive.TButton",
        background=[("active", "#2668D6")],
        foreground=[("active", PALETTE["surface"])],
    )

    style.configure(
        "Treeview",
        background=PALETTE["surface"],
        fieldbackground=PALETTE["surface"],
        foreground=PALETTE["text"],
        rowheight=34,
        relief="flat",
        borderwidth=0,
    )
    style.map(
        "Treeview",
        background=[("selected", PALETTE["accent"])],
        foreground=[("selected", PALETTE["surface"])],
    )
    style.configure(
        "Treeview.Heading",
        background="#E5ECF6",
        foreground=PALETTE["text"],
        font=FONTS["body_bold"],
        padding=(10, 10),
        relief="flat",
        borderwidth=0,
    )
    style.map("Treeview.Heading", background=[("active", "#D9E2EC")])

    style.configure("TEntry", padding=8)
    style.configure("TCombobox", padding=7)
    style.configure("TLabelframe", background=PALETTE["surface"], borderwidth=0)
    style.configure(
        "TLabelframe.Label",
        background=PALETTE["surface"],
        foreground=PALETTE["muted"],
        font=FONTS["body_bold"],
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
