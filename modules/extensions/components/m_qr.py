import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles import moduledrawers, colormasks

from modules.core import c_core


class QR:
    def __init__(
            self, value, box_size: int, border_size: int, fill: str = "black",
            background: str = "white", style: str = "square",
            color_mask: str = "solid"):
        self.error_correction = qrcode.constants.ERROR_CORRECT_M
        self.value = value
        self.box_size = box_size
        self.margin = border_size
        self.fill = fill
        self.background = background
        self.image = None
        
        if style in ("square",):
            self.module_drawer = moduledrawers.RoundedModuleDrawer()
        elif style in ("gaped", "gapped", "gap"):
            self.module_drawer = moduledrawers.GappedSquareModuleDrawer()
        elif style in ("circle",):
            self.module_drawer = moduledrawers.CircleModuleDrawer()
        elif style in ("rounded",):
            self.module_drawer = moduledrawers.RoundedModuleDrawer()
        elif style in ("vertical", "vertical"):
            self.module_drawer = moduledrawers.VerticalBarsDrawer()
        elif style in ("horizontal", "horizontal"):
            self.module_drawer = moduledrawers.HorizontalBarsDrawer()
        else:
            raise RuntimeError(f"Unknown style: {style}")
        
        if color_mask in ("solid",):
            self.color_mask = colormasks.SolidFillColorMask()
        elif color_mask in ("radial",):
            self.color_mask = colormasks.RadialGradiantColorMask()
        elif color_mask in ("vertical",):
            self.color_mask = colormasks.VerticalGradiantColorMask()
        elif color_mask in ("horizontal",):
            self.color_mask = colormasks.HorizontalGradiantColorMask()
        elif color_mask in ("image", "img", "picture", "pic"):
            self.color_mask = colormasks.ImageColorMask()
        else:
            raise RuntimeError(f"Unknown color mask: {color_mask}")
    
    def __str__(self):
        return self.value
    
    def add_value(self, value):
        self.value += "\n" + value

    def make_qr(self):
        qr = qrcode.QRCode(
            error_correction=self.error_correction,
            box_size=self.box_size,
            border=self.margin)
        qr.add_data(self.value)
        qr.make()
        self.image = qr.make_image(
            fill_color=self.fill,
            back_color=self.background,
            image_factory=StyledPilImage,
            module_drawer=self.module_drawer,
            color_mask=self.color_mask)

    def get_qr(self):
        return self.image
    
    def save_qr(self, location=c_core.my_work_dir):
        self.image.save(location)
