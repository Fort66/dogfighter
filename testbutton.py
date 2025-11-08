"""
Модуль реализует продвинутые UI-виджеты для Pygame:
- Кнопки
- Переключатели (Toggle)
- Чекбоксы
- Радио-кнопки
- Слайдеры
С поддержкой теней, границ, анимаций и звуков.
"""

import pygame as pg
from pygame.locals import *
from pygame import Surface, Color, Rect
from pygame.sprite import Sprite
from typing import Optional, Callable, Union, List, Dict
from math import ceil


class ButtonText(Sprite):
    """
    Универсальный UI-элемент: кнопка, чекбокс, переключатель, радио, слайдер.
    """

    group = pg.sprite.Group()  # Все виджеты
    radio_groups: Dict[str, List['ButtonText']] = {}  # Группы радиокнопок

    # Типы виджетов
    WIDGET_BUTTON = "button"
    WIDGET_TOGGLE = "toggle"
    WIDGET_CHECKBOX = "checkbox"
    WIDGET_RADIO = "radio"
    WIDGET_SLIDER = "slider"

    def __init__(
        self,
        surface: Surface,
        pos: tuple[int, int],
        size: tuple[int, int],
        text: str = "",
        image_path: Optional[str] = None,
        font: Optional[str] = None,
        font_size: int = 26,
        bg_color: Union[str, tuple] = "#0B61A4",
        hover_color: Union[str, tuple] = "#033E6B",
        click_color: Union[str, tuple] = "#66A3D2",
        text_color: Union[str, tuple] = "#FFFFFF",
        disabled_color: Union[str, tuple] = "#2F4F4F",
        rounding: int = 8,
        on_click: Optional[Callable] = None,
        sound_hover: Optional[str] = None,
        sound_click: Optional[str] = None,
        hotkey: Optional[int] = None,
        auto_resize_text: bool = True,
        multiline: bool = False,
        line_spacing: int = 5,
        # Новые параметры:
        shadow_offset: tuple[int, int] = (4, 4),
        shadow_color: Union[str, tuple] = "#111111",
        border_width: int = 0,
        border_color: Union[str, tuple] = "#FFFFFF",
        widget_type: str = WIDGET_BUTTON,
        toggle_state: bool = False,
        slider_value: float = 0.0,  # 0.0 to 1.0
        slider_show_value: bool = False,
        slider_value_format: str = "{:.0%}",
        radio_group: Optional[str] = None,
    ):
        super().__init__(self.__class__.group)
        self.surface = surface
        self.pos = pos
        self.size = size
        self.text = text
        self.multiline = multiline
        self.line_spacing = line_spacing
        self.widget_type = widget_type
        self.toggle_state = toggle_state
        self.radio_group_name = radio_group
        self.slider_value = max(0.0, min(1.0, slider_value))  # Ограничиваем 0–1
        self.slider_show_value = slider_show_value
        self.slider_value_format = slider_value_format

        # Тень
        self.shadow_offset = shadow_offset
        self.shadow_color = self._parse_color(shadow_color)

        # Граница
        self.border_width = border_width
        self.border_color = self._parse_color(border_color)

        # Загрузка изображения
        self.image_surf = None
        if image_path:
            self.image_surf = pg.image.load(image_path).convert_alpha()
            self.image_surf = pg.transform.smoothscale(self.image_surf, (size[0] // 2, size[1] // 2))

        # Шрифт
        self.font_size = font_size
        self.font_name = font
        self.auto_resize_text = auto_resize_text
        self._init_font()

        # Цвета
        self.bg_color = self._parse_color(bg_color)
        self.hover_color = self._parse_color(hover_color)
        self.click_color = self._parse_color(click_color)
        self.text_color = self._parse_color(text_color)
        self.disabled_color = self._parse_color(disabled_color)

        self.rounding = rounding
        self.on_click = on_click or (lambda: None)

        # Звуки
        self.sound_hover = pg.mixer.Sound(sound_hover) if sound_hover else None
        self.sound_click = pg.mixer.Sound(sound_click) if sound_click else None
        self.played_hover = False

        # Состояния
        self.hotkey = hotkey
        self.on_enabled = True
        self.is_hovered = False
        self.is_clicked = False
        self.allow_clicking = True
        self.dragging = False  # Для слайдера

        # Цвет для анимации
        self.current_color = self.bg_color

        # Прямоугольник
        self.rect = Rect(0, 0, *size)
        self.rect.center = pos
        self.shadow_rect = self.rect.move(*self.shadow_offset)

        # Регистрация в группе радиокнопок
        if widget_type == self.WIDGET_RADIO and radio_group:
            if radio_group not in self.radio_groups:
                self.radio_groups[radio_group] = []
            self.radio_groups[radio_group].append(self)

    def _parse_color(self, color: Union[str, tuple]): #-> Color:
        return Color(color) if isinstance(color, str) else Color(*color)

    def _init_font(self):
        if self.font_name:
            self.font = pg.font.Font(self.font_name, self.font_size)
        else:
            self.font = pg.font.SysFont("Arial", self.font_size)

    def _render_text(self) -> List[Surface]:
        if not self.text:
            return []
        max_width = self.size[0] - 20
        lines = self.text.split('\n') if self.multiline else [self.text]
        surfaces = []

        for line in lines:
            if self.auto_resize_text and len(line) > 0:
                test_size = self.font_size
                temp_font = pg.font.Font(self.font_name, test_size)
                while temp_font.size(line)[0] > max_width and test_size > 8:
                    test_size -= 1
                    temp_font = pg.font.Font(self.font_name, test_size)
                self.font = temp_font
            text_surf = self.font.render(line, True, self.text_color)
            surfaces.append(text_surf)
        return surfaces

    def handle_event(self, event: pg.Event):
        mouse_pos = pg.mouse.get_pos()

        if event.type == MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(mouse_pos)
            if self.is_hovered and self.on_enabled and not self.played_hover and self.sound_hover:
                self.sound_hover.play()
                self.played_hover = True
            elif not self.is_hovered:
                self.played_hover = False

            # Перетаскивание слайдера
            if self.widget_type == self.WIDGET_SLIDER and self.dragging:
                rel_x = mouse_pos[0] - self.rect.left
                self.slider_value = max(0.0, min(1.0, rel_x / self.rect.width))
                self.on_click()  # Вызываем при изменении

        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            if self.widget_type == self.WIDGET_SLIDER and self.rect.collidepoint(mouse_pos):
                self.dragging = True
                rel_x = mouse_pos[0] - self.rect.left
                self.slider_value = max(0.0, min(1.0, rel_x / self.rect.width))
                self.on_click()
            elif self.is_hovered and self.on_enabled and self.allow_clicking:
                self.is_clicked = True

        if event.type == MOUSEBUTTONUP and event.button == 1:
            self.dragging = False
            if self.is_clicked and self.is_hovered:
                if self.widget_type == self.WIDGET_TOGGLE:
                    self.toggle_state = not self.toggle_state
                elif self.widget_type in (self.WIDGET_CHECKBOX, self.WIDGET_RADIO):
                    if self.widget_type == self.WIDGET_RADIO:
                        # Снимаем все радиокнопки в группе
                        for btn in self.radio_groups.get(self.radio_group_name, []):
                            btn.toggle_state = False
                        self.toggle_state = True
                    else:
                        self.toggle_state = not self.toggle_state
                    self.on_click()
                    if self.sound_click:
                        self.sound_click.play()
            self.is_clicked = False
            self.allow_clicking = True

        if event.type == KEYDOWN and self.hotkey and event.key == self.hotkey and self.on_enabled:
            if self.widget_type == self.WIDGET_TOGGLE:
                self.toggle_state = not self.toggle_state
            elif self.widget_type == self.WIDGET_CHECKBOX:
                self.toggle_state = not self.toggle_state
            elif self.widget_type == self.WIDGET_RADIO:
                for btn in self.radio_groups.get(self.radio_group_name, []):
                    btn.toggle_state = False
                self.toggle_state = True
            self.on_click()
            if self.sound_click:
                self.sound_click.play()

    def update(self):
        # Анимация цвета
        target_color = self.bg_color
        if not self.on_enabled:
            target_color = Color("#333333")
        elif self.is_clicked:
            target_color = self.click_color
        elif self.is_hovered:
            target_color = self.hover_color

        for i in range(3):
            delta = target_color[i] - self.current_color[i]
            if abs(delta) > 1:
                self.current_color[i] += delta

        # Обновление позиции тени
        self.shadow_rect = self.rect.move(*self.shadow_offset)

        # Отрисовка
        self._draw_shadow()
        self._draw_main()
        self._draw_border()
        self._draw_widget_specific()
        self._draw_text_or_image()

    def _draw_shadow(self):
        pg.draw.rect(self.surface, self.shadow_color, self.shadow_rect, border_radius=self.rounding)

    def _draw_main(self):
        pg.draw.rect(self.surface, self.current_color, self.rect, border_radius=self.rounding)

    def _draw_border(self):
        if self.border_width > 0:
            border_rect = self.rect.inflate(-2, -2)
            pg.draw.rect(
                self.surface,
                self.border_color,
                border_rect,
                width=self.border_width,
                border_radius=self.rounding
            )

    def _draw_widget_specific(self):
        if self.widget_type == self.WIDGET_SLIDER:
            self._draw_slider()
        elif self.widget_type == self.WIDGET_CHECKBOX and self.toggle_state:
            self._draw_checkmark()
        elif self.widget_type == self.WIDGET_RADIO:
            self._draw_radio_circle()

    def _draw_slider(self):
        # Трек
        track_rect = self.rect.inflate(-10, -20)
        pg.draw.rect(self.surface, "#AAAAAA", track_rect, border_radius=5)
        # Ползунок
        handle_x = track_rect.left + int(track_rect.width * self.slider_value)
        handle_rect = pg.Rect(0, 0, 12, track_rect.height + 6)
        handle_rect.centerx = handle_x
        handle_rect.centery = track_rect.centery
        pg.draw.circle(self.surface, "#FFFFFF", handle_rect.center, 8)
        pg.draw.circle(self.surface, "#0B61A4", handle_rect.center, 6)

        # Показ значения
        if self.slider_show_value:
            value_text = self.font.render(
                self.slider_value_format.format(self.slider_value),
                True,
                self.text_color
            )
            value_rect = value_text.get_rect(midright=(self.rect.left - 10, self.rect.centery))
            self.surface.blit(value_text, value_rect)

    def _draw_checkmark(self):
        check_size = min(self.size) // 3
        check_rect = pg.Rect(0, 0, check_size, check_size)
        check_rect.center = self.rect.center
        pg.draw.rect(self.surface, "#00FF00", check_rect, border_radius=4)

    def _draw_radio_circle(self):
        center = self.rect.center
        pg.draw.circle(self.surface, "#FFFFFF", center, 10)
        if self.toggle_state:
            pg.draw.circle(self.surface, "#0B61A4", center, 5)

    def _draw_text_or_image(self):
        if self.image_surf:
            img_rect = self.image_surf.get_rect(center=self.rect.center)
            self.surface.blit(self.image_surf, img_rect)

        text_surfs = self._render_text()
        total_height = sum(s.get_height() for s in text_surfs) + self.line_spacing * (len(text_surfs) - 1)
        y = self.rect.centery - total_height // 2

        for surf in text_surfs:
            text_rect = surf.get_rect(centerx=self.rect.centerx, y=y)
            self.surface.blit(surf, text_rect)
            y += surf.get_height() + self.line_spacing

    def enable(self):
        self.on_enabled = True

    def disable(self):
        self.on_enabled = False

    @classmethod
    def update_all(cls, events: List[pg.Event]):
        for event in events:
            for button in cls.group:
                button.handle_event(event)
        cls.group.update()

    def set_toggle_state(self, state: bool):
        self.toggle_state = state

    def is_toggled(self) -> bool:
        return self.toggle_state

    def set_slider_value(self, value: float):
        self.slider_value = max(0.0, min(1.0, value))

    def get_slider_value(self) -> float:
        return self.slider_value




pg.init()
screen = pg.display.set_mode((1000, 700))
clock = pg.time.Clock()
pg.display.set_caption("Радио и Слайдер")

def on_radio():
    selected = [b for b in ButtonText.radio_groups.get("theme", []) if b.is_toggled()]
    if selected:
        print(f"Выбрана тема: {selected[0].text}")

def on_slider():
    value = slider.get_slider_value()
    print(f"Громкость: {value:.0%}")

# Радио-кнопки
radio1 = ButtonText(
    surface=screen,
    pos=(200, 100),
    size=(120, 50),
    text="Тёмная",
    widget_type=ButtonText.WIDGET_RADIO,
    radio_group="theme",
    on_click=on_radio,
    bg_color="#333333",
    hover_color="#555555",
    click_color="#777777",
    rounding=25,
    shadow_offset=(3, 3),
    border_width=1,
    border_color="#AAAAAA"
)

radio2 = ButtonText(
    surface=screen,
    pos=(200, 180),
    size=(120, 50),
    text="Светлая",
    widget_type=ButtonText.WIDGET_RADIO,
    radio_group="theme",
    on_click=on_radio,
    bg_color="#CCCCCC",
    hover_color="#EEEEEE",
    click_color="#AAAAAA",
    text_color="#000000",
    rounding=25,
    shadow_offset=(3, 3),
    border_width=1,
    border_color="#888888"
)

# Слайдер
slider = ButtonText(
    surface=screen,
    pos=(500, 100),
    size=(300, 40),
    text="Громкость",
    widget_type=ButtonText.WIDGET_SLIDER,
    on_click=on_slider,
    bg_color="#333333",
    hover_color="#333333",
    click_color="#333333",
    text_color="#FFFFFF",
    rounding=5,
    slider_value=0.5,
    slider_show_value=True,
    slider_value_format="{:.0%}"
)

running = True
while running:
    events = pg.event.get()
    for event in events:
        if event.type == pg.QUIT:
            running = False

    screen.fill("#1E1E1E")
    ButtonText.update_all(events)
    pg.display.flip()
    clock.tick(60)

pg.quit()
