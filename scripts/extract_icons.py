"""Makes icons/<id>.png from each mod's title logo.

    python scripts/extract_icons.py                 # every entry without an icon
    python scripts/extract_icons.py <id> [<id>...]  # just these (made again)
    python scripts/extract_icons.py --local <id>=<zip or folder> ...
                                                    # from a file you have (MEGA,
                                                    # Google Drive: no program
                                                    # downloads from those)
    python scripts/extract_icons.py --image <id>=<picture> ...
                                                    # a logo found elsewhere: cropped
                                                    # and scaled like the others

Nearly every mod replaces the title screen's logo: `wiiMario_Title_logo_*.tpl`
in `openingTitle.arc` (a U8 archive in the mod's Opening/Layout folder). This
reads that one file out of the release zip with HTTP range requests - a few
hundred KB, not the whole mod - decodes the texture, crops its empty border and
scales it into 128 x 64, the shape of a logo (Reginald shows icons in a 2:1
box). Needs Pillow.

A logo that several mods share is the one they all started from (the game's
own, or Newer's): it says nothing about the mod, so it is reported, not used.
"""

import io
import json
import os
import re
import struct
import sys
import urllib.request
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENTRIES = os.path.join(ROOT, 'entries')
ICONS = os.path.join(ROOT, 'icons')
BOX = (128, 64)
#: Entries a shared logo belongs to: the mods others started from
OWN_LOGO = ('newer-smbw',)
AGENT = 'Patches-Catalog icon extractor'


class HttpFile(io.RawIOBase):
    """A remote file read with Range requests, for zipfile."""

    BLOCK = 256 * 1024

    def __init__(self, url):
        request = urllib.request.Request(url, headers={'Range': 'bytes=0-0', 'User-Agent': AGENT})
        with urllib.request.urlopen(request, timeout=60) as response:
            if response.status != 206:
                raise OSError('the server does not send parts of the file')
            self.url = response.geturl()
            self.size = int(response.headers['Content-Range'].split('/')[-1])
        self.pos = 0
        self.blocks = {}

    def readable(self):
        return True

    def seekable(self):
        return True

    def tell(self):
        return self.pos

    def seek(self, offset, whence=0):
        self.pos = {0: offset, 1: self.pos + offset, 2: self.size + offset}[whence]
        return self.pos

    def _block(self, index):
        if index not in self.blocks:
            first = index * self.BLOCK
            last = min(first + self.BLOCK, self.size) - 1
            request = urllib.request.Request(self.url, headers={'Range': 'bytes=%d-%d' % (first, last),
                                                                'User-Agent': AGENT})
            with urllib.request.urlopen(request, timeout=120) as response:
                self.blocks[index] = response.read()
        return self.blocks[index]

    def readinto(self, buffer):
        want = min(len(buffer), self.size - self.pos)
        done = 0
        while done < want:
            index, at = divmod(self.pos + done, self.BLOCK)
            chunk = self._block(index)[at:at + want - done]
            buffer[done:done + len(chunk)] = chunk
            done += len(chunk)
        self.pos += done
        return done


# --- U8 ---------------------------------------------------------------------

def u8_files(data):
    """{path: bytes} of a U8 archive."""
    magic, root, _header, _data = struct.unpack('>IIII', data[:16])
    if magic != 0x55AA382D:
        raise ValueError('not a U8 archive')
    count = struct.unpack('>I', data[root + 8:root + 12])[0]
    strings = root + count * 12
    files, stack = {}, [('', count)]
    for i in range(1, count):
        while stack and i >= stack[-1][1]:
            stack.pop()
        kind_name, offset, size = struct.unpack('>III', data[root + i * 12:root + i * 12 + 12])
        kind, name_at = kind_name >> 24, kind_name & 0xFFFFFF
        end = data.index(b'\0', strings + name_at)
        name = data[strings + name_at:end].decode('ascii', 'replace')
        path = '/'.join(p for p in (stack[-1][0] if stack else '', name) if p)
        if kind == 1:
            stack.append((path, size))
        else:
            files[path] = data[offset:offset + size]
    return files


# --- TPL --------------------------------------------------------------------

def _rgb565(v):
    return ((v >> 11) & 31) * 255 // 31, ((v >> 5) & 63) * 255 // 63, (v & 31) * 255 // 31


def _rgb5a3(v):
    if v & 0x8000:
        return ((v >> 10) & 31) * 255 // 31, ((v >> 5) & 31) * 255 // 31, (v & 31) * 255 // 31, 255
    return ((v >> 8) & 15) * 17, ((v >> 4) & 15) * 17, (v & 15) * 17, ((v >> 12) & 7) * 255 // 7


def _blocks(width, height, bw, bh):
    for by in range(0, height, bh):
        for bx in range(0, width, bw):
            yield bx, by


def decode_tpl(data):
    """(width, height, RGBA bytes) of a TPL's first image."""
    magic, count, table = struct.unpack('>III', data[:12])
    if magic != 0x0020AF30 or not count:
        raise ValueError('not a TPL')
    header = struct.unpack('>I', data[table:table + 4])[0]
    height, width, fmt, at = struct.unpack('>HHII', data[header:header + 12])
    out = bytearray(width * height * 4)

    def put(x, y, rgba):
        if x < width and y < height:
            i = (y * width + x) * 4
            out[i:i + 4] = bytes(rgba)

    if fmt == 0:      # I4
        for bx, by in _blocks(width, height, 8, 8):
            for y in range(8):
                for x in range(0, 8, 2):
                    b = data[at]; at += 1
                    for dx, v in ((0, b >> 4), (1, b & 15)):
                        put(bx + x + dx, by + y, (v * 17,) * 3 + (255,))
    elif fmt in (1, 2):   # I8, IA4
        for bx, by in _blocks(width, height, 8, 4):
            for y in range(4):
                for x in range(8):
                    b = data[at]; at += 1
                    if fmt == 1:
                        put(bx + x, by + y, (b, b, b, 255))
                    else:
                        put(bx + x, by + y, ((b & 15) * 17,) * 3 + ((b >> 4) * 17,))
    elif fmt in (3, 4, 5):    # IA8, RGB565, RGB5A3
        for bx, by in _blocks(width, height, 4, 4):
            for y in range(4):
                for x in range(4):
                    v = struct.unpack('>H', data[at:at + 2])[0]; at += 2
                    if fmt == 3:
                        put(bx + x, by + y, (v & 255,) * 3 + (v >> 8,))
                    elif fmt == 4:
                        put(bx + x, by + y, _rgb565(v) + (255,))
                    else:
                        put(bx + x, by + y, _rgb5a3(v))
    elif fmt == 6:    # RGBA8: AR then GB, 64 bytes a block
        for bx, by in _blocks(width, height, 4, 4):
            ar, gb = data[at:at + 32], data[at + 32:at + 64]
            at += 64
            for i in range(16):
                put(bx + i % 4, by + i // 4, (ar[i * 2 + 1], gb[i * 2], gb[i * 2 + 1], ar[i * 2]))
    elif fmt == 14:   # CMPR: 8x8 blocks of four DXT1 sub-blocks
        for bx, by in _blocks(width, height, 8, 8):
            for sy in (0, 4):
                for sx in (0, 4):
                    c0, c1, bits = struct.unpack('>HHI', data[at:at + 8]); at += 8
                    p0, p1 = _rgb565(c0), _rgb565(c1)
                    if c0 > c1:
                        pal = [p0 + (255,), p1 + (255,),
                               tuple((2 * a + b) // 3 for a, b in zip(p0, p1)) + (255,),
                               tuple((a + 2 * b) // 3 for a, b in zip(p0, p1)) + (255,)]
                    else:
                        pal = [p0 + (255,), p1 + (255,),
                               tuple((a + b) // 2 for a, b in zip(p0, p1)) + (255,), (0, 0, 0, 0)]
                    for i in range(16):
                        put(bx + sx + i % 4, by + sy + i // 4, pal[(bits >> (30 - 2 * i)) & 3])
    else:
        raise ValueError('TPL format %d is not supported' % fmt)
    return width, height, bytes(out)


# --- the logo ---------------------------------------------------------------

def _arc_rank(name):
    """English first: the logo a player of this catalog reads."""
    lower = name.lower()
    for i, mark in enumerate(('openinge/', 'openingp/', '/eu/', '/us/', 'eng', 'openingtitle/')):
        if mark in lower:
            return i
    return 9


def layout_panes(brlyt):
    """The picture panes of a BRLYT: dicts with name, parent, visible,
    alpha, origin, translation, rotation, scale, size and texture name."""
    if brlyt[:4] != b'RLYT':
        return []
    at = struct.unpack('>H', brlyt[12:14])[0]
    count = struct.unpack('>H', brlyt[14:16])[0]
    textures, materials, panes, stack, last = [], [], [], [None], None
    for _ in range(count):
        magic, size = brlyt[at:at + 4], struct.unpack('>I', brlyt[at + 4:at + 8])[0]
        body = brlyt[at:at + size]
        if magic == b'txl1':
            for i in range(struct.unpack('>H', body[8:10])[0]):
                off = 12 + struct.unpack('>I', body[12 + i * 8:16 + i * 8])[0]
                textures.append(body[off:body.index(b'\0', off)].decode('ascii', 'replace'))
        elif magic == b'mat1':
            for i in range(struct.unpack('>H', body[8:10])[0]):
                m = body[struct.unpack('>I', body[12 + i * 4:16 + i * 4])[0]:]
                maps = struct.unpack('>I', m[0x3C:0x40])[0] & 15
                first = struct.unpack('>H', m[0x40:0x42])[0] if maps else None
                materials.append(textures[first] if first is not None and first < len(textures) else None)
        elif magic in (b'pan1', b'pic1', b'txt1', b'wnd1', b'bnd1'):
            tx, ty, _tz, _rx, _ry, rz, sx, sy, w, h = struct.unpack('>10f', body[36:76])
            last = {'name': body[12:28].split(b'\0')[0].decode('ascii', 'replace'), 'parent': stack[-1],
                    'visible': bool(body[8] & 1), 'origin': body[9], 'alpha': body[10],
                    'pos': (tx, ty), 'rot': rz, 'scale': (sx, sy), 'size': (w, h), 'texture': None}
            if magic == b'pic1':
                mat = struct.unpack('>H', body[92:94])[0]
                last['texture'] = materials[mat] if mat < len(materials) else None
                panes.append(last)
        elif magic == b'pas1':
            stack.append(last)
        elif magic == b'pae1':
            stack.pop()
        at += size
    return panes


def logo_from_layout(files):
    """The logo as the title screen shows it: every picture beside the logo's
    in the layout, placed where the layout puts them. Newer-based mods build
    theirs from parts - "New" with an "er" laid over it (Newer: title.tpl)."""
    from PIL import Image
    by_name = {path.rsplit('/', 1)[-1].lower(): data for path, data in files.items()}
    for path, brlyt in files.items():
        if not path.lower().endswith('.brlyt'):
            continue
        panes = layout_panes(brlyt)
        logo = next((p for p in panes if p['texture'] and 'logo' in p['texture'].lower()), None)
        if logo is None:
            continue
        group = [p for p in panes if p['parent'] is logo['parent'] and p['visible'] and p['alpha']
                 and p['texture'] and p['texture'].lower() in by_name]
        images = {}
        for pane in group:
            w, h, rgba = decode_tpl(by_name[pane['texture'].lower()])
            images[id(pane)] = Image.frombytes('RGBA', (w, h), rgba)
        # Layout units to pixels: the logo texture at its own resolution
        lw = logo['size'][0] * logo['scale'][0]
        k = max(images[id(logo)].width / lw if lw else 1, 1)
        rects = []
        for pane in group:
            w, h = pane['size'][0] * pane['scale'][0] * k, pane['size'][1] * pane['scale'][1] * k
            x, y = pane['pos'][0] * k, -pane['pos'][1] * k     # y down from here
            ox, oy = pane['origin'] % 3, pane['origin'] // 3
            left = x - (0, w / 2, w)[ox]
            top = y - (0, h / 2, h)[oy]
            rects.append((pane, left, top, w, h))
        x0 = min(r[1] for r in rects)
        y0 = min(r[2] for r in rects)
        x1 = max(r[1] + r[3] for r in rects)
        y1 = max(r[2] + r[4] for r in rects)
        canvas = Image.new('RGBA', (int(x1 - x0) + 2, int(y1 - y0) + 2), (0, 0, 0, 0))
        for pane, left, top, w, h in rects:        # file order is drawing order
            image = images[id(pane)].resize((max(int(w), 1), max(int(h), 1)), Image.LANCZOS)
            if pane['rot']:
                image = image.rotate(pane['rot'], expand=True, resample=Image.BICUBIC)
                left -= (image.width - w) / 2
                top -= (image.height - h) / 2
            if pane['alpha'] < 255:
                image.putalpha(image.getchannel('A').point(lambda a, f=pane['alpha']: a * f // 255))
            canvas.alpha_composite(image, (int(left - x0), int(top - y0)))
        return canvas.width, canvas.height, canvas.tobytes()
    return None


def logo_from_arc(arc):
    files = u8_files(arc)
    try:
        composed = logo_from_layout(files)
    except (ValueError, struct.error, IndexError, KeyError):
        composed = None
    if composed:
        return composed
    logos = [(path, data) for path, data in files.items()
             if path.lower().endswith('.tpl') and 'logo' in path.lower()]
    if not logos:
        return None
    best = None
    for path, data in logos:
        try:
            image = decode_tpl(data)
        except ValueError:
            continue
        if best is None or image[0] * image[1] > best[0] * best[1]:
            best = image
    return best


def logo_from_zip(source):
    """The logo image (w, h, rgba) of a zip (a path or a file object)."""
    with zipfile.ZipFile(source) as archive:
        arcs = sorted((n for n in archive.namelist() if n.lower().endswith('openingtitle.arc')
                       and '__macosx' not in n.lower()), key=_arc_rank)
        for name in arcs:
            data = archive.read(name)
            if data[:4] != b'\x55\xAA\x38\x2D':
                continue        # compressed; none seen so far
            logo = logo_from_arc(data)
            if logo:
                return logo
    return None


def logo_from_folder(folder):
    arcs = []
    for base, _dirs, names in os.walk(folder):
        arcs += [os.path.join(base, n) for n in names if n.lower() == 'openingtitle.arc']
    for path in sorted(arcs, key=lambda p: _arc_rank(p.replace(os.sep, '/'))):
        with open(path, 'rb') as f:
            logo = logo_from_arc(f.read())
        if logo:
            return logo
    return None


def github_raw(entry):
    """For a linked-source entry (no ranges from GitHub's archives): the
    logo through the repository's file list and its raw files."""
    source = entry['source']
    tree = 'https://api.github.com/repos/%s/git/trees/%s?recursive=1' % (source['repo'], source['commit'])
    request = urllib.request.Request(tree, headers={'User-Agent': AGENT})
    with urllib.request.urlopen(request, timeout=60) as response:
        paths = [t['path'] for t in json.load(response)['tree'] if t['path'].lower().endswith('openingtitle.arc')]
    for path in sorted(paths, key=_arc_rank):
        raw = 'https://raw.githubusercontent.com/%s/%s/%s' % (source['repo'], source['commit'],
                                                               urllib.request.quote(path))
        with urllib.request.urlopen(urllib.request.Request(raw, headers={'User-Agent': AGENT}),
                                    timeout=60) as response:
            logo = logo_from_arc(response.read())
        if logo:
            return logo
    return None


def to_icon(logo):
    from PIL import Image
    width, height, rgba = logo
    image = Image.frombytes('RGBA', (width, height), rgba)
    box = image.getchannel('A').point(lambda a: 255 if a > 16 else 0).getbbox()
    if box:
        image = image.crop(box)
    image.thumbnail(BOX, Image.LANCZOS)
    out = io.BytesIO()
    image.save(out, 'PNG', optimize=True)
    return out.getvalue(), image.tobytes()


def main():
    args = sys.argv[1:]
    local, pictures = {}, {}
    for flag, into in (('--local', local), ('--image', pictures)):
        while flag in args:
            i = args.index(flag)
            eid, _, path = args[i + 1].partition('=')
            into[eid] = path
            del args[i:i + 2]
    if pictures:
        from PIL import Image
        os.makedirs(ICONS, exist_ok=True)
        for eid, path in pictures.items():
            if not os.path.exists(os.path.join(ENTRIES, eid + '.json')):
                print('%-48s no entry of that id' % eid)
                continue
            image = Image.open(path).convert('RGBA')
            png, _pixels = to_icon((image.width, image.height, image.tobytes()))
            with open(os.path.join(ICONS, eid + '.png'), 'wb') as f:
                f.write(png)
            print('%-48s from %s, %d bytes' % (eid, os.path.basename(path), len(png)))
        if not args and not local:
            return
    wanted = set(args) | set(local)
    entries = []
    for name in sorted(os.listdir(ENTRIES)):
        with open(os.path.join(ENTRIES, name), encoding='utf-8') as f:
            entry = json.load(f)
        if wanted and entry['id'] not in wanted:
            continue
        if not wanted and os.path.exists(os.path.join(ICONS, entry['id'] + '.png')):
            continue
        entries.append(entry)
    os.makedirs(ICONS, exist_ok=True)
    made, seen = {}, {}

    def one(entry):
        eid, source = entry['id'], entry.get('source') or {}
        try:
            if eid in local:
                path = local[eid]
                logo = logo_from_folder(path) if os.path.isdir(path) else logo_from_zip(path)
            elif source.get('type') == 'linked-source':
                logo = github_raw(entry)
            elif (entry.get('download') or {}).get('url'):
                logo = logo_from_zip(io.BufferedReader(HttpFile(entry['download']['url']), 1024 * 1024))
            else:
                return eid, None, 'no download to read (an external or ongoing entry: --local)'
        except Exception as error:      # one mod never stops the others
            return eid, None, 'failed: %s' % error
        if not logo:
            return eid, None, 'no title logo in the mod'
        return eid, logo, None

    # A few at once: each is mostly waiting for range requests
    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(6) as pool:
        for eid, logo, problem in pool.map(one, entries):
            if problem:
                print('%-48s %s' % (eid, problem), flush=True)
                continue
            png, pixels = to_icon(logo)
            made[eid] = png
            seen.setdefault(pixels, []).append(eid)
            print('%-48s %dx%d logo, %d bytes' % (eid, logo[0], logo[1], len(png)), flush=True)
    shared = {eid for ids in seen.values() if len(ids) > 2 for eid in ids if eid not in OWN_LOGO}
    for ids in seen.values():
        if len(ids) > 2:
            print('shared by %d mods, used only by its own: %s' % (len(ids), ', '.join(ids)))
    for eid, png in made.items():
        if eid in shared:
            continue
        with open(os.path.join(ICONS, eid + '.png'), 'wb') as f:
            f.write(png)
    print('%d icons written' % (len(made) - len(shared & set(made))))


if __name__ == '__main__':
    main()
