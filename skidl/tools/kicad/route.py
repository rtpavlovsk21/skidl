# -*- coding: utf-8 -*-

# The MIT License (MIT) - Copyright (c) 2016-2021 Dave Vandenbout.

"""
Routing for schematics.
"""

from __future__ import (  # isort:skip
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from builtins import range, zip
from collections import defaultdict
from enum import Enum, auto
from itertools import zip_longest, chain
from random import randint
import pygame
import pygame.freetype

from future import standard_library

from ...logger import active_logger
from ...part import Part
from ...utilities import *
from .common import *
from .geometry import *

standard_library.install_aliases()

###################################################################
# Routing schematic nets:
#
# Create a list of horizontal and vertical endpoints of the part BBoxes.
# Use the endpoints to divide the routing area into an array of rectangles.
# Create the faces of each rectangle, each face shared between adjacent rects.
# Capacity of each face is its length / wiring grid, except for faces
#    inside part boundaries which have 0 capacity.
# Assign part pins to each face that lies on a part BBox and zero the
#    capacity of that face.
# For each face, store the indices of adjacent faces except for those that
#    have zero capacity AND no part pins (i.e., faces internal to part boundaries).
# For each net:
#    For each pin on net:
#        Create list of cell faces and route cost occupied by pin.
#    While # face lists > 1:
#        For each frontier cell face:
#            Compute the cost to reach each adjacent, unvisited cell face.
#        Select the lowest-cost, unvisited cell face.
#        If the cell face has already been visited by another net pin,
#          then connect the pins by combining their face lists.
###################################################################


def draw_start(bbox):
    """Initialize PyGame drawing area."""

    scr_bbox = BBox(Point(0, 0), Point(2000, 1500))

    border = max(bbox.w, bbox.h) / 20
    bbox = bbox.resize(Vector(border, border))
    bbox = round(bbox)

    scale = min(scr_bbox.w / bbox.w, scr_bbox.h / bbox.h)

    tx = Tx(a=scale, d=scale).dot(Tx(d=-1))
    new_bbox = bbox.dot(tx)
    move = scr_bbox.ctr - new_bbox.ctr
    tx = tx.dot(Tx(dx=move.x, dy=move.y))

    pygame.init()
    scr = pygame.display.set_mode((scr_bbox.w, scr_bbox.h))

    font = pygame.freetype.SysFont("consolas", 24)

    scr.fill((255, 255, 255))

    return scr, tx, font

def draw_end():
    """Display drawing and wait for user to close PyGame window."""
    pygame.display.flip()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    pygame.quit()


class Orientation(Enum):
    HORZ = auto()
    VERT = auto()
    LEFT = auto()
    RIGHT = auto()


# Put the orientation enums in global space to make using them easier.
_g = globals()
for orientation in Orientation:
    _g[orientation.name] = orientation.value


class NoSwitchBox(Exception):
    pass


class Boundary:
    pass


boundary = Boundary()


class Terminal:
    """Terminal on a Face from which a net is routed within a switchbox."""

    def __init__(self, net, face, coord):
        self.net = net
        self.face = face
        self.coord = coord

    def draw(self, scr, tx):
        if not self.net:
            return

        if self.face.track.orientation == HORZ:
            ctr = Point(self.coord, self.face.track.coord)
        else:
            ctr = Point(self.face.track.coord, self.coord)
        ctr = ctr.dot(tx)
        sz = 5
        corners = (
            (ctr.x, ctr.y + sz),
            (ctr.x + sz, ctr.y),
            (ctr.x, ctr.y - sz),
            (ctr.x - sz, ctr.y),
        )
        color = (0,0,0)
        pygame.draw.polygon(scr, color, corners, 0)


class Face:
    """A side of a rectangle bounding a routing switchbox."""

    def __init__(self, part, track, beg, end):
        self.part = set()
        if isinstance(part, set):
            self.part.update(part)
        elif part is not None:
            self.part.add(part)
        self.pins = []
        if beg > end:
            beg, end = end, beg
        self.beg = beg
        self.end = end
        self.adjacent = set()
        self.track = track
        track.add_face(self) # Add new face to track so it isn't lost.

    @property
    def bbox(self):
        bbox = BBox()
        bbox.add(Point(self.track.coord, self.beg.coord))
        bbox.add(Point(self.track.coord, self.end.coord))
        if self.track.orientation == HORZ:
            bbox = bbox.dot(Tx(a=0, b=1, c=1, d=0))
        return bbox

    def create_nonpin_terminals(self):
        self.terminals = []
        if not self.part:
            # Add non-pin terminals to non-part switchbox routing faces.
            from .gen_schematic import GRID

            beg = (self.beg.coord + GRID // 2 + GRID) // GRID * GRID
            end = self.end.coord - GRID // 2
            self.terminals = [
                Terminal(None, self, coord) for coord in range(beg, end, GRID)
            ]

    @property
    def connection_pts(self):
        return [terminal.coord for terminal in self.terminals]

    def set_capacity(self):
        if self.part:
            self.capacity = 0
        else:
            self.capacity = len(self.connection_pts)

    def has_nets(self):
        return any((terminal.net for terminal in self.terminals))

    def add_adjacency(self, adj_face):
        """Make two faces adjacent to one another."""

        # Faces on the boundary can never accept wires so they are never
        # adjacent to any face.
        if boundary in list(self.part) + list(adj_face.part):
            return

        # If a face is an edge of a part, then it can never be adjacent to
        # another face on the same part or else wires might get routed through
        # the part bounding box.
        if not self.part.intersection(adj_face.part):
            self.adjacent.add(adj_face)
            adj_face.adjacent.add(self)

    def split(self, mid):
        """If a point is in the middle of a face, split it and add remainder to track."""
        if self.beg < mid < self.end:
            new_face = Face(self.part, self.track, self.beg, mid)
            self.beg = mid

    def coincides_with(self, other_face):
        """Returns True if both faces have the same beginning and ending point on the same track."""
        return (self.beg, self.end) == (other_face.beg, other_face.end)

    def draw(self, scr, tx):
        p1 = Point(self.track.coord, self.beg.coord)
        p2 = Point(self.track.coord, self.end.coord)
        seg = Segment(p1, p2)
        if self.track.orientation == HORZ:
            seg = seg.dot(Tx(a=0, b=1, c=1, d=0))
        seg = seg.dot(tx)
        color = (128, 128, 128)
        line_thickness = 2
        pygame.draw.line(
            scr, color, (seg.p1.x, seg.p1.y), (seg.p2.x, seg.p2.y), width=line_thickness
        )
        for terminal in self.terminals:
            terminal.draw(scr, tx)


class Interval:
    def __init__(self, beg, end):
        if beg > end:
            beg, end = end, beg
        self.beg = beg
        self.end = end

    @property
    def len(self):
        return self.end - self.beg

    def __len__(self):
        return self.len

    def intersects(self, other):
        return not (self.beg > other.end or self.end < other.beg)

    def merge(self, other):
        if self.intersects(other):
            return Interval(min(self.beg, other.beg), max(self.end, other.end))
        return None


class NetInterval(Interval):
    def __init__(self, net, beg, end):
        super().__init__(beg, end)
        self.net = net

    def intersects(self, other):
        return super().intersects(other) and (self.net is not other.net)

    def merge(self, other):
        if self.net is other.net:
            merged_intvl = super().merge(other)
            if merged_intvl:
                merged_intvl.net = self.net
            return merged_intvl
        return None


class Target:
    def __init__(self, row, col, net):
        self.row = row
        self.col = col
        self.net = net

    def __lt__(self, other):
        return (self.col, self.row, id(self.net)) < (other.col, other.row, id(other.net))


class SwitchBox:
    def __init__(self, top_face):

        left_face = None
        left_track = top_face.beg
        for face in left_track:
            if face.end.coord == top_face.track.coord:
                left_face = face
                break

        if not left_face:
            raise NoSwitchBox("Unroutable switchbox!")

        right_face = None
        right_track = top_face.end
        for face in right_track:
            if face.end.coord == top_face.track.coord:
                right_face = face
                break

        if not right_face:
            raise NoSwitchBox("Unroutable switchbox!")

        if left_face.beg != right_face.beg:
            # This only happens when two parts are butted up against each other
            # to form a non-routable switchbox inside a part bounding box.
            raise NoSwitchBox("Unroutable switchbox!")

        bottom_face = None
        bottom_track = left_face.beg
        for face in bottom_track:
            if face.beg.coord == top_face.beg.coord:
                bottom_face = face
                break

        if not bottom_face:
            raise NoSwitchBox("Unroutable switchbox!")

        # If all four sides have a common part, then its a part bbox with no routing.
        if top_face.part & bottom_face.part & left_face.part & right_face.part:
            raise NoSwitchBox("Unroutable switchbox") 

        self.top_face = top_face
        self.bottom_face = bottom_face
        self.left_face = left_face
        self.right_face = right_face

        def find_terminal_net(terminals, terminal_coords, coord):
            try:
                return terminals[terminal_coords.index(coord)].net
            except ValueError:
                return None

        top_coords = [terminal.coord for terminal in self.top_face.terminals]
        bottom_coords = [terminal.coord for terminal in self.bottom_face.terminals]
        lr_coords = [self.left_face.track.coord, self.right_face.track.coord]
        self.column_coords = sorted(set(top_coords + bottom_coords + lr_coords))
        self.top_nets = [
            find_terminal_net(self.top_face.terminals, top_coords, coord)
            for coord in self.column_coords
        ]
        self.bottom_nets = [
            find_terminal_net(self.bottom_face.terminals, bottom_coords, coord)
            for coord in self.column_coords
        ]

        left_coords = [terminal.coord for terminal in self.left_face.terminals]
        right_coords = [terminal.coord for terminal in self.right_face.terminals]
        tb_coords = [self.top_face.track.coord, self.bottom_face.track.coord]
        self.track_coords = sorted(set(left_coords + right_coords + tb_coords))
        self.left_nets = [
            find_terminal_net(self.left_face.terminals, left_coords, coord)
            for coord in self.track_coords
        ]
        self.right_nets = [
            find_terminal_net(self.right_face.terminals, right_coords, coord)
            for coord in self.track_coords
        ]
        assert len(self.top_nets) == len(self.bottom_nets)
        assert len(self.left_nets) == len(self.right_nets)

    @property
    def bbox(self):
        bbox = BBox()
        bbox.add(self.top_face.bbox)
        bbox.add(self.bottom_face.bbox)
        bbox.add(self.left_face.bbox)
        bbox.add(self.right_face.bbox)
        return bbox

    def has_nets(self):
        for face in (self.top_face, self.bottom_face, self.left_face, self.right_face):
            if face.has_nets():
                return True
        return False

    def route(self):

        if not self.has_nets():
            return []

        def connect_top_btm(t_net, b_net, track_nets):
            """Connect top/bottom net to nets in horizontal tracks."""

            def find_connection(net, tracks, direction):
                """
                Searches for the closest track with the same net followed by the
                closest empty track. The indices of these tracks are returned.
                If the net cannot be connected to any track, return [].
                If the net given to connect is None, then return a list of [None].

                Args:
                    net (Net): Net to be connected.
                    tracks (list): Nets on tracks
                    direction (int): Search direction for connection.

                Returns:
                    list: Indices of tracks where the net can connect.
                """
                if net:
                    connections = []
                    if direction < 0:
                        tracks = tracks[::-1]
                    try:
                        connections.append(tracks[1:-1].index(net)+1)
                    except ValueError:
                        pass
                    try:
                        connections.append(tracks[1:-1].index(None)+1)
                    except ValueError:
                        pass
                    if direction < 0:
                        l = len(tracks)
                        connections = [l - 1 - cnct for cnct in connections]
                else:
                    connections = [None]
                return connections

            column = []
            t_cncts = find_connection(t_net, track_nets, -1)
            b_cncts = find_connection(b_net, track_nets, 1)

            # Test each possible pair of connections to find one that is free of interference.
            tb_cncts = [(t,b) for t in t_cncts for b in b_cncts]

            if not tb_cncts:
                # Top and/or bottom could not be connected.
                raise Exception
            for t_cnct, b_cnct in tb_cncts:
                if t_cnct is None or b_cnct is None:
                    # No possible interference if at least one connection is None.
                    break
                if t_cnct > b_cnct:
                    # Top & bottom connections don't interfere.
                    break
            else:
                raise Exception

            if t_cnct is not None:
                # Connection from track to terminal on top of switchbox.
                column.append(NetInterval(t_net, t_cnct, len(track_nets)-1))
            if b_cnct is not None:
                # Connection from terminal on bottom of switchbox to track.
                column.append(NetInterval(b_net, 0, b_cnct))

            # Return connection segments.
            return column

        def connect_splits(track_nets, column):

            # Make a copy so the original isn't disturbed.
            track_nets = track_nets[:]

            # Merge column nets into track nets so top-bottom terminal nets are accounted for.
            for intvl in column:
                track_nets[intvl.beg] = intvl.net
                track_nets[intvl.end] = intvl.net

            # Keep top/bottom tracks clear.
            track_nets[0] = None
            track_nets[-1] = None

            # Find nets that are running on multiple tracks.
            multi_nets = set(net for net in set(track_nets) if track_nets.count(net)>1)
            multi_nets.remove(None)  # Ignore empty tracks.

            # Find intervals for multi-track nets.
            net_intervals = []
            for net in multi_nets:
                net_trk_idxs = [idx for idx, nt in enumerate(track_nets[1:-1], 1) if nt is net]
                for index, trk1 in enumerate(net_trk_idxs[:-1], 1):
                    for trk2 in net_trk_idxs[index:]:
                        net_intervals.append(NetInterval(net, trk1, trk2))

            # Sort interval lengths from smallest to largest.
            net_intervals.sort(key=lambda ni: len(ni))

            # Connect tracks for each interval if it doesn't intersect an
            # already existing connection.
            for net_interval in net_intervals:
                for col_interval in column:
                    if net_interval.intersects(col_interval):
                        break
                else:
                    # No conflicts found with existing connections.
                    column.append(net_interval)

            column_nets = set(intvl.net for intvl in column)
            for net in column_nets:

                # Extract intervals if the current net has more than one interval.
                intervals = [intvl for intvl in column if intvl.net is net]
                if len(intervals) < 2:
                    continue
                for intvl in intervals:
                    column.remove(intvl)

                # Merge the extracted intervals as much as possible.
                merged = True
                while merged:
                    merged = False
                    merged_intervals = []

                    # Sort intervals by their beginning coordinates.
                    intervals.sort(key=lambda intvl: intvl.beg)

                    # Try merging consecutive pairs of intervals.
                    for intvl1, intvl2 in zip(intervals[:-1], intervals[1:]):
                        merged_intvl = intvl1.merge(intvl2)
                        if merged_intvl:
                            # Replace separate intervals with merged interval.
                            merged_intervals.append(merged_intvl)
                            # Merging happened, so iterate through intervals again
                            # to find more merges.
                            merged = True
                        else:
                            # Intervals couldn't be merged, so keep both.
                            merged_intervals.extend((intvl1, intvl2))
                    
                    # Update list of intervals to include merges and remove duplicates.
                    intervals = list(set(merged_intervals))

                # Place merged intervals back into column.
                column.extend(set(merged_intervals))

            return column

        # Collect target nets along top, bottom, right faces of switchbox.
        min_row = 1
        max_row = len(self.left_nets)-2
        max_col = len(self.top_nets)
        targets = []
        for col, (t_net, b_net) in enumerate(zip(self.top_nets, self.bottom_nets)):
            if t_net is not None:
                targets.append(Target(max_row, col, t_net))
            if b_net is not None:
                targets.append(Target(min_row, col, b_net))
        for row, r_net in enumerate(self.right_nets):
            if r_net is not None:
                targets.append(Target(row, max_col, r_net))
        targets.sort()

        def prune_targets(targets, col):
            return [target for target in targets if target.col > col]

        def insert_target_tracks(targets, track_nets):
            target_tracks = [None] * len(track_nets)
            for target in targets:

                # Skip target nets that aren't currently active.
                net = target.net
                if net not in track_nets:
                    continue

                row = target.row
                try:
                    row1 = track_nets[row:].index(net)
                except ValueError:
                    row1 = len(track_nets) # Greater than any possible value.
                try:
                    row2 = track_nets[row:].index(None)
                except ValueError:
                    row2 = len(track_nets)
                up = min(row1, row2)

                try:
                    row1 = track_nets[row::-1].index(net)
                except ValueError:
                    row1 = len(track_nets)
                try:
                    row2 = track_nets[row::-1].index(None)
                except ValueError:
                    row2 = len(track_nets)
                down = min(row1, row2)

                try:
                    if up <= down:
                        target_tracks[row+up] = net
                    else:
                        target_tracks[row-down] = net
                except IndexError:
                    # There was no place for this target net.
                    pass 

            return [net or target for (net, target) in zip(track_nets, target_tracks)]

        def extend_tracks(track_nets, column, targets):
            rightward_nets = set(target.net for target in targets)

            # Keep extending nets in current tracks if they do not intersect intervals in the 
            # current column with the same net.
            next_track_nets = track_nets[:]
            for intvl in column:
                for trk_idx in range(intvl.beg, intvl.end+1):
                    if next_track_nets[trk_idx] is intvl.net:
                        # Remove net from track since it intersects an interval with the 
                        # same net. The net may be extended from the interval in the next phase,
                        # or it may terminate here.
                        next_track_nets[trk_idx] = None

            # Extend track net if net has multiple column intervals that need further interconnection
            # or if there are terminals in rightward columns that need connections to this net.
            column_nets = [intvl.net for intvl in column]
            for intvl in column:
                net = intvl.net

                num_net_intvls = column_nets.count(net)
                if num_net_intvls == 1 and net not in rightward_nets:
                    continue

                target_row = None
                for target in targets:
                    if target.net is net:
                        target_row = target.row
                        break

                beg = max(intvl.beg, 1)
                end = min(intvl.end, len(track_nets)-2)
                if target_row is None:
                    row = track_nets[beg:end+1].index(None) + beg
                else:
                    try:
                        down = track_nets[target_row:beg-1:-1].index(None)
                    except ValueError:
                        down = len(track_nets)
                    try:
                        up = track_nets[target_row:end+1].index(None)
                    except ValueError:
                        up = len(track_nets)
                    if up < down:
                        row = target_row + up
                    else:
                        row = target_row - down

                next_track_nets[row] = net

            return next_track_nets

        # Main switchbox routing loop.
        tracks = [self.left_nets[:]]
        track_nets = tracks[0]
        columns = [[], ]
        for col, (t_net, b_net) in enumerate(zip(self.top_nets[1:-1], self.bottom_nets[1:-1]), start=1):
            column = connect_top_btm(t_net, b_net, track_nets)
            targets = prune_targets(targets, col)
            augmented_track_nets = track_nets[:]
            augmented_track_nets[0] = b_net
            augmented_track_nets[-1] = t_net
            augmented_track_nets = insert_target_tracks(targets, augmented_track_nets)
            column = connect_splits(augmented_track_nets, column)
            track_nets = extend_tracks(track_nets, column, targets)
            tracks.append(track_nets)
            columns.append(column)

        segments = []

        # Create horizontal wiring segments.
        for col_idx, trks in enumerate(tracks[:-1]):
            beg_col_coord = self.column_coords[col_idx]
            end_col_coord = self.column_coords[col_idx+1]
            for trk_idx, net in enumerate(trks[1:-1], start=1):
                if net:
                    trk_coord = self.track_coords[trk_idx]
                    p1 = Point(beg_col_coord, trk_coord)
                    p2 = Point(end_col_coord, trk_coord)
                    seg = Segment(p1,p2)
                    seg.net = net
                    segments.append(seg)

        # Create vertical wiring segments.
        for idx, column in enumerate(columns[1:], start=1):
            col_coord = self.column_coords[idx]
            for intvl in column:
                beg_trk_coord = self.track_coords[intvl.beg]
                end_trk_coord = self.track_coords[intvl.end]
                p1 = Point(col_coord, beg_trk_coord)
                p2 = Point(col_coord, end_trk_coord)
                seg = Segment(p1, p2)
                seg.net = intvl.net
                segments.append(seg)

        self.segments = segments

        return segments

    def draw(self, scr=None, tx=None):
        do_start_end = not bool(scr)

        if do_start_end:
            scr, tx, font = draw_start(self.bbox.resize(Vector(100,100)))

        self.top_face.draw(scr, tx)
        self.bottom_face.draw(scr, tx)
        self.left_face.draw(scr, tx)
        self.right_face.draw(scr, tx)

        net_colors = defaultdict(lambda: (randint(0,200),randint(0,200), randint(0,200)))
        def draw_seg(seg, scr, tx, color=(100, 100, 100), line_thickness=5):
            color = net_colors[seg.net]
            seg = seg.dot(tx)
            pygame.draw.line(
                scr, color, (seg.p1.x, seg.p1.y), (seg.p2.x, seg.p2.y), width=line_thickness
            )
        for segment in self.segments:
            draw_seg(segment, scr, tx)

        if do_start_end:
            draw_end()


class GlobalWire(list):
    """Global-routing wire connecting switchbox faces and terminals."""

    def __init__(self, *args, **kwargs):
        self.net = kwargs.pop("net")
        super().__init__(*args, **kwargs)


class GlobalTrack(list):
    """A horizontal/vertical track holding one or more faces all having the same Y/X coordinate."""

    def __init__(self, *args, **kwargs):
        self.orientation = kwargs.pop("orientation", HORZ)
        self.coord = kwargs.pop("coord", 0)
        self.idx = kwargs.pop("idx")
        super().__init__(*args, **kwargs)
        self.splits = set()

    def __hash__(self):
        return self.idx

    def __lt__(self, track):
        return self.coord < track.coord

    def __gt__(self, track):
        return self.coord > track.coord

    def add_face(self, face):
        self.append(face)
        self.add_split(face.beg)
        self.add_split(face.end)

    def extend_faces(self, orthogonal_tracks):
        for h_face in self[:]:
            if not h_face.part:
                continue
            for dir in (LEFT, RIGHT):
                if dir == LEFT:
                    start = h_face.beg
                    search = orthogonal_tracks[start.idx :: -1]
                else:
                    start = h_face.end
                    search = orthogonal_tracks[start.idx :]

                blocked = False
                for ortho_track in search:
                    for ortho_face in ortho_track:
                        if ortho_face.beg < self < ortho_face.end:
                            ortho_track.add_split(self)
                            self.add_split(ortho_track)
                            if ortho_face.part:
                                Face(None, self, start, ortho_track)
                                blocked = True
                            break
                    if blocked:
                        break

    def add_split(self, track_idx):
        self.splits.add(track_idx)

    def split_faces(self):
        for split in self.splits:
            for face in self[:]:
                face.split(split)

    def combine_faces(self):
        for i, face in enumerate(self):
            for other_face in self[i + 1 :]:
                if face.coincides_with(other_face):
                    other_face.part.update(face.part)
                    face.beg = face.end
                    break
        for face in self[:]:
            if face.beg == face.end:
                self.remove(face)

    def add_adjacencies(self):
        for top_face in self:

            try:
                swbx = SwitchBox(top_face)
            except NoSwitchBox:
                continue

            swbx.top_face.add_adjacency(swbx.bottom_face)
            swbx.left_face.add_adjacency(swbx.right_face)
            swbx.left_face.add_adjacency(swbx.top_face)
            swbx.left_face.add_adjacency(swbx.bottom_face)
            swbx.right_face.add_adjacency(swbx.top_face)
            swbx.right_face.add_adjacency(swbx.bottom_face)


def create_pin_terminals(internal_nets):
    from .gen_schematic import calc_pin_dir

    for net in internal_nets:
        for pin in net.pins:
            part = pin.part
            pt = pin.pt.dot(part.tx)
            dir = calc_pin_dir(pin)
            pin_track = {
                "U": part.bottom_track,
                "D": part.top_track,
                "L": part.right_track,
                "R": part.left_track,
            }[dir]
            coord = {
                "U": pt.x,
                "D": pt.x,
                "L": pt.y,
                "R": pt.y,
            }[dir]
            for face in pin_track:
                if part in face.part and face.beg.coord <= coord <= face.end.coord:
                    if not getattr(pin, "face", None):
                        # Only assign pin to face if it isn't already assigned to
                        # another face. This handles the case where a pin is exactly
                        # at the end coordinate and beginning coordinate of two
                        # successive faces in the same track.
                        pin.face = face
                        face.pins.append(pin)
                        terminal = Terminal(pin.net, face, coord)
                        face.terminals.append(terminal)
                    break


def route_globally(net):
    """Route a net from face to face.

    Args:
        net (Net): The net to be routed.

    Returns:
        List: Sequence of faces the net travels through.
    """

    routed_wires = []

    net_route_cnt = 0
    for pin in net.pins:
        if hasattr(pin.face, "seed_pin"):
            pin.do_route = False  # Only route one pin per face.
        else:
            pin.face.seed_pin = pin
            pin.face.dist = 0
            pin.face.prev = pin.face  # Indicates terminal pin.
            pin.frontier = set([pin.face])
            pin.visited = set()
            pin.do_route = True
            net_route_cnt += 1

    while net_route_cnt > 1:
        for pin in net.pins:
            if pin.do_route:

                try:
                    visit_face = min(pin.frontier, key=lambda face: face.dist)
                except ValueError:
                    print("No route found!")
                    pin.do_route = False
                    net_route_cnt -= 1
                    continue

                pin.frontier.remove(visit_face)
                pin.visited.add(visit_face)

                for next_face in visit_face.adjacent - pin.visited - pin.frontier:

                    if hasattr(next_face, "prev"):
                        # Found a connection with another pin on the net!
                        # Combine faces that have been visited and on the frontier.
                        # Turn off routing for one of the pins.
                        # Store sequence of faces connecting the two pins.
                        other_pin = next_face.seed_pin
                        pin.frontier.update(other_pin.frontier)
                        pin.visited.update(other_pin.visited)
                        other_pin.visited = set()
                        other_pin.frontier = set()
                        other_pin.do_route = False
                        net_route_cnt -= 1

                        def get_face_path(f):
                            path = [f]
                            while f.prev is not f:
                                path.append(f.prev)
                                f = f.prev
                            return path

                        wire = GlobalWire(
                            get_face_path(visit_face)[::-1]
                            + get_face_path(next_face)[:],
                            net=net,
                        )
                        for face in wire:
                            if face.capacity > 0:
                                face.capacity -= 1
                        routed_wires.append(wire)

                    elif next_face.capacity > 0:
                        pin.frontier.add(next_face)
                        next_face.seed_pin = pin
                        next_face.prev = visit_face
                        next_face.dist = visit_face.dist + 1

    for pin in net.pins:
        delattr(pin, "do_route")
        if hasattr(pin, "frontier"):
            for face in pin.visited | pin.frontier:
                delattr(face, "dist")
                delattr(face, "prev")
                delattr(face, "seed_pin")
            delattr(pin, "frontier")
            delattr(pin, "visited")

    return routed_wires


def assign_switchbox_terminals(global_routes):
    """Assign global routes to terminals in switchbox faces."""

    for route in global_routes:
        for wire in route:
            for i, face in enumerate(wire[:]):
                if face.part:
                    for terminal in face.terminals:
                        if terminal.net == wire.net:
                            wire[i] = terminal
                            break
                    else:
                        raise Exception

    def find_to_terminal_idx(from_terminal, to_face):
        from_face = from_terminal.face
        if to_face.track in (from_face.beg, from_face.end):
            # Right-angle faces.
            # to_face is positioned left/below w.r.t. from_face.
            if to_face.beg == from_face.track:
                # to_face is oriented upward/rightward w.r.t. from_face.
                search_range = range(len(to_face.terminals))
            elif to_face.end == from_face.track:
                # to_face is oriented downward/leftward w.r.t. from_face.
                search_range = range(len(to_face.terminals) - 1, -1, -1)
            else:
                raise Exception
        else:
            # Parallel faces.
            from_len = len(from_face.terminals)
            from_idx = from_face.terminals.index(from_terminal)
            search_range = chain(
                *zip_longest(range(from_idx, -1, -1), range(from_idx + 1, from_len))
            )

        for idx in search_range:
            if idx is not None:
                if to_face.terminals[idx].net in (None, from_terminal.net):
                    return idx
        raise Exception

    for route in global_routes:
        done = False
        while not done:
            done = True
            for wire in route:
                for i in range(0, len(wire) - 1):
                    face1, face2 = wire[i], wire[i + 1]
                    if isinstance(face1, Terminal) and isinstance(face2, Terminal):
                        continue
                    if isinstance(face1, Face) and isinstance(face2, Terminal):
                        terminal_idx = find_to_terminal_idx(face2, face1)
                        terminal = face1.terminals[terminal_idx]
                        terminal.net = wire.net
                        wire[i] = terminal
                        done = False
                        continue
                    if isinstance(face1, Terminal) and isinstance(face2, Face):
                        terminal_idx = find_to_terminal_idx(face1, face2)
                        terminal = face2.terminals[terminal_idx]
                        terminal.net = wire.net
                        wire[i + 1] = terminal
                        done = False
                        continue
                    if isinstance(face1, Face) and isinstance(face2, Face):
                        continue

                    raise Exception


def rank_net(net):
    """Rank net based on W/H of bounding box of pins and the # of pins."""
    bbox = BBox()
    for pin in net.pins:
        bbox.add(pin.pt)
    return (bbox.w + bbox.h, len(net.pins))


def route(node):
    """Route the wires between part pins in the node.

    Args:
        node (Node): Hierarchical node containing the parts to be connected.

    Returns:
        None

    Note:
        1. Divide the bounding box surrounding the parts into switchboxes.
        2. Do global routing of nets through sequences of switchboxes.
        3. Do detailed routing within each switchbox.
    """

    # Exit if no parts to route.
    if not node.parts:
        return

    # Extract list of nets internal to the node for routing.
    processed_nets = []
    internal_nets = []
    for part in node.parts:
        for part_pin in part:

            # A label means net is stubbed so there won't be any explicit wires.
            if len(part_pin.label) > 0:
                continue

            # No explicit wires if the pin is not connected to anything.
            if not part_pin.is_connected():
                continue

            net = part_pin.net

            if net in processed_nets:
                continue

            processed_nets.append(net)

            # No explicit wires for power nets.
            if net.netclass == "Power":
                continue

            def is_internal(net):

                # Determine if all the pins on this net reside in the node.
                for net_pin in net.pins:

                    # Don't consider stubs.
                    if len(net_pin.label) > 0:
                        continue

                    # If a pin is outside this node, then the net is not internal.
                    if net_pin.part.hierarchy != part_pin.part.hierarchy:
                        return False

                # All pins are within the node, so the net is internal.
                return True

            if is_internal(net):
                internal_nets.append(net)

    # Exit if no nets to route.
    if not internal_nets:
        return

    # Find the coords of the horiz/vert tracks that will hold the H/V faces of the routing switchboxes.
    v_track_coord = []
    h_track_coord = []

    # The top/bottom/left/right of each part's bounding box define the H/V tracks.
    for part in node.parts:
        bbox = round(part.bbox.dot(part.tx))
        v_track_coord.append(bbox.min.x)
        v_track_coord.append(bbox.max.x)
        h_track_coord.append(bbox.min.y)
        h_track_coord.append(bbox.max.y)

    # Create delimiting tracks for the routing area from the slightly-expanded total bounding box of the parts.
    expansion = Vector(node.bbox.w, node.bbox.h) / 20
    routing_bbox = round(node.bbox.resize(expansion))
    v_track_coord.append(routing_bbox.min.x)
    v_track_coord.append(routing_bbox.max.x)
    h_track_coord.append(routing_bbox.min.y)
    h_track_coord.append(routing_bbox.max.y)

    # Remove any duplicate track coords and then sort them.
    v_track_coord = list(set(v_track_coord))
    h_track_coord = list(set(h_track_coord))
    v_track_coord.sort()
    h_track_coord.sort()

    # Create an H/V track for each H/V coord containing a list for holding the faces in that track.
    v_tracks = [
        GlobalTrack(orientation=VERT, idx=idx, coord=coord)
        for idx, coord in enumerate(v_track_coord)
    ]
    h_tracks = [
        GlobalTrack(orientation=HORZ, idx=idx, coord=coord)
        for idx, coord in enumerate(h_track_coord)
    ]

    def bbox_to_faces(part, bbox):
        left_track = v_tracks[v_track_coord.index(bbox.min.x)]
        right_track = v_tracks[v_track_coord.index(bbox.max.x)]
        bottom_track = h_tracks[h_track_coord.index(bbox.min.y)]
        top_track = h_tracks[h_track_coord.index(bbox.max.y)]
        Face(part, left_track, bottom_track, top_track)
        Face(part, right_track, bottom_track, top_track)
        Face(part, bottom_track, left_track, right_track)
        Face(part, top_track, left_track, right_track)
        if isinstance(part, Part):
            part.left_track = left_track
            part.right_track = right_track
            part.top_track = top_track
            part.bottom_track = bottom_track

    # Add routing box faces for each side of a part's bounding box.
    for part in node.parts:
        part_bbox = round(part.bbox.dot(part.tx))
        bbox_to_faces(part, part_bbox)

    # Add routing box faces for each side of the expanded bounding box surrounding all parts.
    bbox_to_faces(boundary, routing_bbox)

    # Extend the part faces in each horizontal track and then each vertical track.
    for track in h_tracks:
        track.extend_faces(v_tracks)
    for track in v_tracks:
        track.extend_faces(h_tracks)

    # Apply splits to all faces and combine coincident faces.
    for track in h_tracks + v_tracks:
        track.split_faces()
        track.combine_faces()

    # Add terminals to all non-part faces.
    for track in h_tracks + v_tracks:
        for face in track:
            face.create_nonpin_terminals()

    # Add terminals to switchbox faces for all pins on internal nets.
    create_pin_terminals(internal_nets)

    # Add adjacencies between faces that define routing paths within switchboxes.
    for h_track in h_tracks[1:]:
        h_track.add_adjacencies()

    # Set routing capacity of faces.
    for track in h_tracks + v_tracks:
        for face in track:
            face.set_capacity()

    # Do global routing of nets internal to the node.
    internal_nets.sort(key=rank_net)
    global_routes = [route_globally(net) for net in internal_nets]
    assign_switchbox_terminals(global_routes)

    # Do detailed routing inside switchboxes.
    detailed_routes = []
    for h_track in h_tracks[1:]:
        for face in h_track:
            try:
                swbx = SwitchBox(face)
            except NoSwitchBox:
                continue
            else:
                detailed_routes.extend(swbx.route())


    def draw_init(bbox):
        scr_bbox = BBox(Point(0, 0), Point(2000, 1500))

        border = max(bbox.w, bbox.h) / 20
        bbox = bbox.resize(Vector(border, border))
        bbox = round(bbox)

        scale = min(scr_bbox.w / bbox.w, scr_bbox.h / bbox.h)

        tx = Tx(a=scale, d=scale).dot(Tx(d=-1))
        new_bbox = bbox.dot(tx)
        move = scr_bbox.ctr - new_bbox.ctr
        tx = tx.dot(Tx(dx=move.x, dy=move.y))

        pygame.init()
        scr = pygame.display.set_mode((scr_bbox.w, scr_bbox.h))

        font = pygame.freetype.SysFont("consolas", 24)

        scr.fill((255, 255, 255))

        return scr, tx, font

    def draw_seg(
        seg, scr, tx, color=(100, 100, 100), line_thickness=1, dot_thickness=3
    ):
        seg = seg.dot(tx)
        pygame.draw.line(
            scr, color, (seg.p1.x, seg.p1.y), (seg.p2.x, seg.p2.y), width=line_thickness
        )
        pygame.draw.circle(scr, color, (seg.p1.x, seg.p1.y), dot_thickness)
        pygame.draw.circle(scr, color, (seg.p2.x, seg.p2.y), dot_thickness)

    def face_seg(face):
        track = face.track
        orientation = track.orientation
        if orientation == HORZ:
            p1 = Point(face.beg.coord, track.coord)
            p2 = Point(face.end.coord, track.coord)
        else:
            p1 = Point(track.coord, face.beg.coord)
            p2 = Point(track.coord, face.end.coord)
        return Segment(p1, p2)

    def draw_text(txt, pt, scr, tx, font, color=(100, 100, 100)):
        pt = pt.dot(tx)
        font.render_to(scr, (pt.x, pt.y), txt, color)

    def draw_face(face, color, line_width, dot_width, scr, tx, font):
        if len(face.part) < 0:
            return
        seg = face_seg(face)
        draw_seg(face_seg(face), scr, tx, color, line_width, dot_width)
        mid_pt = (seg.p1 + seg.p2) / 2
        draw_text(str(face.capacity), mid_pt, scr, tx, font, color)

    def draw_track(track, scr, tx, font):
        face_colors = [(255, 0, 0), (0, 64, 0), (0, 0, 255), (0, 0, 0)]
        for face in track:
            if len(face.part) < 0:
                continue
            face_color = face_colors[len(face.part)]
            draw_face(face, face_color, 3, 4, scr, tx, font)

    def draw_channels(track, scr, tx):
        for face in track:
            seg = face_seg(face)
            p1 = (seg.p1 + seg.p2) / 2
            for adj_face in face.adjacent:
                seg = face_seg(adj_face)
                p2 = (seg.p1 + seg.p2) / 2
                draw_seg(Segment(p1, p2), scr, tx, (128, 0, 128), 1, 3)

    def draw_box(bbox, scr, tx):
        bbox = bbox.dot(tx)
        corners = (
            bbox.min,
            Point(bbox.min.x, bbox.max.y),
            bbox.max,
            Point(bbox.max.x, bbox.min.y),
        )
        corners = (
            (bbox.min.x, bbox.min.y),
            (bbox.min.x, bbox.max.y),
            (bbox.max.x, bbox.max.y),
            (bbox.max.x, bbox.min.y),
        )
        pygame.draw.polygon(scr, (192, 255, 192), corners, 0)

    def draw_parts(parts, scr, tx):
        for part in parts:
            draw_box(part.bbox.dot(part.tx), scr, tx)

    def draw_pin(pin, scr, tx):
        pt = pin.pt.dot(pin.part.tx)
        track = pin.face.track
        pt = {
            HORZ: Point(pt.x, track.coord),
            VERT: Point(track.coord, pt.y),
        }[track.orientation]
        pt = pt.dot(tx)
        sz = 5
        corners = (
            (pt.x, pt.y + sz),
            (pt.x + sz, pt.y),
            (pt.x, pt.y - sz),
            (pt.x - sz, pt.y),
        )
        pygame.draw.polygon(scr, (0, 0, 0), corners, 0)
        # draw_face(pin.face, (0,0,0), 4, 4, scr, tx)

    def draw_wire(wire, scr, tx):
        for pin in wire.net.pins:
            draw_pin(pin, scr, tx)

        def terminal_pt(terminal):
            track = terminal.face.track
            if track.orientation == HORZ:
                return Point(terminal.coord, track.coord)
            else:
                return Point(track.coord, terminal.coord)

        face_to_face = zip(wire[:-1], wire[1:])
        for terminal1, terminal2 in face_to_face:
            p1 = terminal_pt(terminal1)
            p2 = terminal_pt(terminal2)
            draw_seg(Segment(p1, p2), scr, tx, (0, 0, 0), 2, 0)

    def draw_end():
        pygame.display.flip()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
        pygame.quit()

    draw_scr, draw_tx, font = draw_init(routing_bbox)
    draw_parts(node.parts, draw_scr, draw_tx)
    for track in h_tracks + v_tracks:
        draw_track(track, draw_scr, draw_tx, font)
    # for track in h_tracks + v_tracks:
    #     draw_channels(track, draw_scr, draw_tx)
    for route in global_routes:
        for wire in route:
            draw_wire(wire, draw_scr, draw_tx)
    draw_end()

    return
