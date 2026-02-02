

import pygame
from pygame import Vector2

from ..canvas import Transformation, world_globals, HandleBase, Element


class SurfHandle(HandleBase):
    def __init__(self, owner: 'SurfElement'):
        super().__init__(owner.transformation, owner)
        self.surf: pygame.Surface = owner.surf

    def set_surf(self, surf: pygame.Surface) -> None:
        self.surf = surf
    
    def hit_test(self, world_pos: Vector2) -> bool:
        # surface hit
        rect = pygame.Rect(self.transformation.pos.x, self.transformation.pos.y,
                           self.surf.get_width(), self.surf.get_height())
        return rect.collidepoint(world_pos.x, world_pos.y)
    
    def draw(self, win: pygame.Surface, transform: Transformation) -> None:
        # draw bounding box
        my_world_pos = transform.transform(self.transformation)
        rect = pygame.Rect(my_world_pos.pos.x, my_world_pos.pos.y,
                            self.surf.get_width() * transform.scale,
                            self.surf.get_height() * transform.scale)
        pygame.draw.rect(win, (0, 255, 0), rect, 1)
    
    def set_pos(self, new_pos: Vector2) -> None:
        super().set_pos(new_pos)
        self.owner.refresh_surf()



class SurfElement(Element):
    def __init__(self, surf: pygame.Surface):
        super().__init__()
        self.surf = surf
        # Cache
        self._cached_surf: pygame.Surface = None
        self._cached_draw_pos: Vector2 = None
        self._cached_world_transform: Transformation = None
        self.handles.append(SurfHandle(self))

    def _needs_recalculation(self, world_transform: Transformation) -> bool:
        """Check if the cached surface needs to be recalculated."""
        if self._cached_surf is None or self._cached_world_transform is None:
            return True
        return (self._cached_world_transform.pos != world_transform.pos or
                self._cached_world_transform.scale != world_transform.scale)

    def _calculate_visible_region(self, world_transform: Transformation) -> tuple:
        """
        Calculate the visible region of the surface.
        Returns (src_rect, dest_size, draw_pos) or None if nothing is visible.
        """
        elem_world_pos = self.transformation.pos
        surf_width, surf_height = self.surf.get_size()
        
        # Calculate the element's screen position (top-left corner)
        screen_pos = (elem_world_pos - world_transform.pos) * world_transform.scale
        
        # Calculate scaled dimensions
        scaled_width = surf_width * world_transform.scale
        scaled_height = surf_height * world_transform.scale
        
        # Calculate visible region in screen coordinates
        visible_left = max(0, -screen_pos.x)
        visible_top = max(0, -screen_pos.y)
        visible_right = min(scaled_width, world_globals.win_width - screen_pos.x)
        visible_bottom = min(scaled_height, world_globals.win_height - screen_pos.y)
        
        # Check if any part is visible
        if visible_left >= visible_right or visible_top >= visible_bottom:
            return None
        
        # Convert visible screen region back to source surface coordinates
        src_left = int(visible_left / world_transform.scale)
        src_top = int(visible_top / world_transform.scale)
        src_right = int(visible_right / world_transform.scale)
        src_bottom = int(visible_bottom / world_transform.scale)
        
        # Clamp to surface bounds
        src_left = max(0, min(src_left, surf_width))
        src_top = max(0, min(src_top, surf_height))
        src_right = max(0, min(src_right, surf_width))
        src_bottom = max(0, min(src_bottom, surf_height))
        
        src_width = src_right - src_left
        src_height = src_bottom - src_top
        
        if src_width <= 0 or src_height <= 0:
            return None
        
        # Calculate the destination size for the visible portion
        dest_width = int(src_width * world_transform.scale)
        dest_height = int(src_height * world_transform.scale)
        
        if dest_width <= 0 or dest_height <= 0:
            return None
        
        src_rect = (src_left, src_top, src_width, src_height)
        dest_size = (dest_width, dest_height)
        draw_pos = Vector2(screen_pos.x + visible_left, screen_pos.y + visible_top)
        
        return src_rect, dest_size, draw_pos

    def _update_cache(self, world_transform: Transformation) -> bool:
        """
        Update the cached surface if needed.
        Returns True if there's something to draw, False otherwise.
        """
        result = self._calculate_visible_region(world_transform)
        
        if result is None:
            self._cached_surf = None
            self._cached_world_transform = None
            return False
        
        src_rect, dest_size, draw_pos = result
        
        # Extract and scale the visible portion
        visible_subsurface = self.surf.subsurface(src_rect)
        self._cached_surf = pygame.transform.scale(visible_subsurface, dest_size)
        self._cached_draw_pos = draw_pos
        self._cached_world_transform = Transformation(Vector2(world_transform.pos), world_transform.scale)
        
        return True
    
    def refresh_surf(self) -> None:
        # Invalidate the cache
        self._cached_surf = None

    def draw(self, win: pygame.Surface, world_transform: Transformation) -> None:
        if self._needs_recalculation(world_transform):
            if not self._update_cache(world_transform):
                return  # Nothing visible
        
        win.blit(self._cached_surf, self._cached_draw_pos)

