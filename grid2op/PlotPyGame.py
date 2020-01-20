import numpy as np
import cmath
import math # for regular real sqrt
import time
import pdb

try:
    import pygame
    from .PlotGraph import BasePlot
    can_plot = True
except:
    can_plot = False
    pass

__all__ = ["Renderer"]


class Point:
    # https://codereview.stackexchange.com/questions/70143/drawing-a-dashed-line-with-pygame
    # constructed using a normal tupple
    def __init__(self, point_t = (0,0)):
        self.x = float(point_t[0])
        self.y = float(point_t[1])

    # define all useful operators
    def __add__(self, other):
        return Point((self.x + other.x, self.y + other.y))

    def __sub__(self, other):
        return Point((self.x - other.x, self.y - other.y))

    def __mul__(self, scalar):
        return Point((self.x*scalar, self.y*scalar))

    def __div__(self, scalar):
        return Point((self.x/scalar, self.y/scalar))

    def __floordiv__(self, scalar):
        return Point((self.x/scalar, self.y/scalar))

    def __truediv__(self, scalar):
        return Point((self.x/scalar, self.y/scalar))

    def __len__(self):
        return int(math.sqrt(self.x**2 + self.y**2))

    # get back values in original tuple format
    def get(self):
        return (self.x, self.y)

    def to_cplx(self):
        return self.x + 1j * self.y

    @staticmethod
    def from_cplx(cplx):
        return Point((cplx.real, cplx.imag))


def draw_dashed_line(surf, color, start_pos, end_pos, width=1, dash_length=10):
    # https://codereview.stackexchange.com/questions/70143/drawing-a-dashed-line-with-pygame
    origin = Point(start_pos)
    target = Point(end_pos)
    displacement = target - origin
    length = len(displacement)
    slope = displacement/length

    for index in range(0, int(length/dash_length), 2):
        start = origin + (slope *    index    * dash_length)
        end   = origin + (slope * (index + 1) * dash_length)
        pygame.draw.line(surf, color, start.get(), end.get(), width)


def draw_arrow(surf, color, start_pos, end_pos, positive_flow, width=1, num_arrows=10,
               length_arrow=10, angle_arrow=30):
    if positive_flow:
        origin = Point(start_pos)
        target = Point(end_pos)
    else:
        target = Point(start_pos)
        origin = Point(end_pos)

    displacement = target - origin
    length = len(displacement)
    slope = displacement/length

    # phi = cmath.phase(slope.to_cplx()) * 360 / 2*cmath.pi
    phi = cmath.phase(displacement.to_cplx()) * 360 / (2*cmath.pi)
    cste_ = 2*cmath.pi / 360 * 1j
    rotatedown = cmath.exp(cste_ * (180 + phi + angle_arrow) )
    rotateup = cmath.exp(cste_ * (180 + phi - angle_arrow) )

    first_arrow_part = length_arrow*rotateup
    second_arrow_part = length_arrow*rotatedown

    per_displ = displacement / (num_arrows+1)

    for index in range(0, int(num_arrows)):
        mid   = origin + (per_displ * (index + 1) )
        start_arrow = Point.from_cplx(mid.to_cplx() + first_arrow_part)
        end_arrow = Point.from_cplx(mid.to_cplx() + second_arrow_part)
        # , end_arrow.get()
        pygame.draw.lines(surf, color, False,
                            [start_arrow.get(), mid.get(), end_arrow.get()],
                            width)


class Renderer(BasePlot):
    """
    TODO
    """
    def __init__(self, substation_layout,
                 observation_space,
                 radius_sub=20.,
                 load_prod_dist=70.,
                 bus_radius=5.,
                 timestep_duration_seconds=1.,
                 fontsize=20):
        """

        Parameters
        ----------
        substation_layout: ``list``
            List of tupe given the position of each of the substation of the powergrid.

        observation_space: :class:`grid2op.Observation.ObservationHelper`
            Observation space

        """
        if not can_plot:
            raise RuntimeError("Impossible to plot as pygame cannot be imported.")

        self.window_grid = (1000, 700)
        self.lag_x = 150
        self.lag_y = 100

        BasePlot.__init__(self,
                          substation_layout=substation_layout,
                          observation_space=observation_space,
                          radius_sub=radius_sub,
                          load_prod_dist=load_prod_dist,
                          bus_radius=bus_radius)

        # pygame
        pygame.init()
        self.video_width, self.video_height = 1300, 700
        self.timestep_duration_seconds = timestep_duration_seconds
        self.display_called = False
        self.screen = pygame.display.set_mode((self.video_width, self.video_height), pygame.RESIZABLE)
        self.background_color = [70, 70, 73]
        self.font = pygame.font.Font(None, fontsize)

        # pause button
        self.font_pause = pygame.font.Font(None, 30)
        self.color_text = pygame.Color(255, 255, 255)
        self.text_paused = self.font_pause.render("Game Paused", True, self.color_text)

        # # graph layout
        # # convert the layout that is given in standard mathematical orientation, to pygame representation (y axis
        # # inverted)
        # self._layout = {}
        # tmp = self._get_sub_layout(substation_layout)
        # self._layout["substations"] = tmp

    def _get_sub_layout(self, init_layout):
        tmp = [(el1, -el2) for el1, el2 in init_layout]

        # then scale the grid to be on the window, with the proper margin (careful, margin are applied both left and r
        # and right, so count twice
        tmp_arr = np.array(tmp)
        min_ = tmp_arr.min(axis=0)
        max_ = tmp_arr.max(axis=0)
        b = min_
        a = max_ - min_
        res = [(int((el1- b[0]) / a[0] * (self.window_grid[0]  - 2*self.lag_x)) + self.lag_x,
                int((el2 - b[1]) / a[1] * (self.window_grid[1] - 2*self.lag_y)) + self.lag_y)
               for el1, el2 in tmp]
        return res

    def event_looper(self, force=False):
        has_quit = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                has_quit = True
                return force, has_quit
                # pygame.quit()
                # exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    has_quit = True
                    return force, has_quit
                    # pygame.quit()
                    # exit()
                if event.key == pygame.K_SPACE:
                    self.get_plot_pause()
                    # pause_surface = self.draw_plot_pause()
                    # self.screen.blit(pause_surface, (320 + self.left_menu_shape[0], 320))
                    return not force, has_quit
        return force, has_quit

    def close(self):
        self.display_called = False
        pygame.quit()

    def get_plot_pause(self):
        position = 300
        start_pause = position + self.text_paused.get_height()
        end_pause = start_pause + 50
        y_text_left = self.window_grid[0] + 100
        self.screen.blit(self.text_paused, (y_text_left, 300))

        pygame.draw.line(self.screen,
                         self.color_text,
                         (y_text_left+self.text_paused.get_width()//2-10, start_pause),
                         (y_text_left+self.text_paused.get_width()//2-10, end_pause),
                         10)
        pygame.draw.line(self.screen,
                         self.color_text,
                         (y_text_left+self.text_paused.get_width()//2+10, start_pause),
                         (y_text_left + self.text_paused.get_width()//2+10, end_pause),
                         10)
        pygame.display.flip()

    def _make_screen(self, obs, reward=None, done=None, timestamp=None):
        # print("Finally")
        if not "line" in self._layout:
            # update the layout of the objects only once to ensure the same positionning is used
            # if more than 1 observation are displayed one after the other.
            self._compute_layout(obs)

        # The game is not paused anymore (or never has been), I can render the next surface
        self.screen.fill(self.background_color)

        if not done:
            # draw the state now
            self._draw_generic_info(reward, done, timestamp)
            self._draw_subs(observation=obs)
            self._draw_powerlines(observation=obs)
            self._draw_loads(observation=obs)
            self._draw_gens(observation=obs)
            self._draw_topos(observation=obs)

    def get_rgb(self, obs, reward=None, done=None, timestamp=None):
        self._make_screen(obs, reward, done, timestamp)
        return pygame.surfarray.array3d(self.screen)

    def render(self, obs, reward=None, done=None, timestamp=None):
        if not self.display_called:
            self.display_called = True
            self.screen.fill(self.background_color)
            pygame.display.set_caption('Grid2Op Renderer')  # Window title

        force, has_quit = self.event_looper(force=False)
        while force:
            force, has_quit = self.event_looper(force=force)
            pygame.time.wait(250)  # it's in ms

        if has_quit:
            return has_quit

        self._make_screen(obs, reward, done, timestamp)

        pygame.display.flip()

    def _draw_generic_info(self, reward=None, done=None, timestamp=None):
        if reward is not None:
            text_label = "Instantaneous reward: {:.1f}".format(reward)
            text_graphic = self.font.render(text_label, True, self.color_text)
            self.screen.blit(text_graphic, (self.window_grid[0]+100, 100))
        if done is not None:
            pass

        if timestamp is not None:
            text_label = "Date : {:%Y-%m-%d %H:%M}".format(timestamp)
            text_graphic = self.font.render(text_label, True, self.color_text)
            self.screen.blit(text_graphic, (self.window_grid[0]+100, 200))

    def _draw_sub(self, center):
        pygame.draw.circle(self.screen,
                           self.color_text,
                           [int(el) for el in center],
                           int(self.radius_sub),
                           2)

    def _draw_powerlines(self, observation):

        for line_id, (rho, status, p_or) in enumerate(zip(observation.rho, observation.line_status, observation.p_or)):
            # the next 5 lines are always the same, for each observation, it makes sense to compute it once
            # and then reuse it

            pos_or, pos_ex, *_ = self._get_line_coord(line_id)

            if not status:
                # line is disconnected
                draw_dashed_line(self.screen, pygame.Color(0, 0, 0), pos_or, pos_ex)
            else:
                # line is connected

                # step 0: compute thickness and color
                rho_max = 1.5  # TODO here get it back from parameters, or environment or whatever

                if rho < (rho_max / 1.5):
                    amount_green = 255 - int(255. * 1.5 * rho / rho_max)
                else:
                    amount_green = 0

                amount_red = int(255 - (50 + int(205. * rho / rho_max)))

                color = pygame.Color(amount_red, amount_green, 20)

                width = 1
                if rho > rho_max:
                    width = 4
                elif rho > 1.:
                    width = 3
                elif rho > 0.9:
                    width = 2
                width += 3

                # step 1: draw the powerline with right color and thickness
                pygame.draw.line(self.screen, color, pos_or, pos_ex, width)

                # step 2: draw arrows indicating current flows
                draw_arrow(self.screen, color, pos_or, pos_ex,
                           p_or >= 0.,
                           num_arrows=width,
                           width=width)

    def _aligned_text(self, pos, text_graphic, pos_text):
        pos_x = pos_text.real
        pos_y = pos_text.imag
        width = text_graphic.get_width()
        height = text_graphic.get_height()

        if pos == "center|left":
            pos_y -= height // 2
        elif pos == "up|center":
            pos_x -= width // 2
            pos_y -= height
        elif pos == "center|right":
            pos_x -= width
            pos_y -= height // 2
        elif pos == "down|center":
            pos_x -= width // 2
        self.screen.blit(text_graphic, (pos_x, pos_y))

    def _draw_loads(self, observation):
        for c_id, por in enumerate(observation.load_p):
            pos_end_line, pos_load_sub, pos_load, how_center = self._get_load_coord(c_id)

            color = pygame.Color(0, 0, 0)
            width = 2
            pygame.draw.line(self.screen, color, pos_load_sub, (pos_end_line.real, pos_end_line.imag), width)
            text_label = "- {:.1f} MW".format(por)
            text_graphic = self.font.render(text_label, True, color)
            self._aligned_text(how_center, text_graphic, pos_load)

    def _draw_gens(self, observation):
        for g_id, por in enumerate(observation.prod_p):
            pos_end_line, pos_gen_sub, pos_gen, how_center = self._get_gen_coord(g_id)

            color = pygame.Color(0, 0, 0)
            width = 2
            pygame.draw.line(self.screen, color, pos_gen_sub, (pos_end_line.real, pos_end_line.imag), width)
            text_label = "+ {:.1f} MW".format(por)
            text_graphic = self.font.render(text_label, True, color)
            self._aligned_text(how_center, text_graphic, pos_gen)

    def _draw_topos(self, observation):
        for sub_id, elements in enumerate(self.subs_elements):
            buses_z, bus_vect = self.get_topo_coord(sub_id, observation, elements)

            if not buses_z:
                # I don't plot details of substations with 1 bus for better quality
                continue

            colors = [pygame.Color(255, 127, 14), pygame.Color(31, 119, 180)]

            # I plot the buses
            for bus_id, z_bus in enumerate(buses_z):
                pygame.draw.circle(self.screen,
                                   colors[bus_id],
                                   [int(z_bus.real), int(z_bus.imag)],
                                   int(self.bus_radius),
                                   0)

            # i connect every element to the proper bus with the proper color
            for el_nm, dict_el in elements.items():
                this_el_bus = bus_vect[dict_el["sub_pos"]] -1
                if this_el_bus >= 0:
                    pygame.draw.line(self.screen,
                                     colors[this_el_bus],
                                     [int(dict_el["z"].real), int(dict_el["z"].imag)],
                                     [int(buses_z[this_el_bus].real), int(buses_z[this_el_bus].imag)],
                                     2)
