from pathlib import Path
import math
import sys

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
PAPER = '#f6f1e5'
INK = '#141414'
RED = '#a41f24'
NAVY = '#1e3a5c'
SCALE = 3
image = Image.new('RGB', (1024 * SCALE, 1024 * SCALE), PAPER)
draw = ImageDraw.Draw(image)


def font(size, kind='body'):
    names = {
        'body': 'NotoSans-Condensed.ttf',
        'label': 'NotoSans-CondensedBold.ttf',
        'head': 'NotoSerifDisplay-Bold.ttf',
        'mast': 'NotoSerifDisplay-Black.ttf',
    }
    path = Path('/usr/share/fonts/truetype/noto') / names[kind]
    if not path.exists():
        path = Path('/usr/share/fonts/truetype/dejavu') / (
            'DejaVuSans.ttf' if kind == 'body' else 'DejaVuSerif-Bold.ttf')
    return ImageFont.truetype(str(path), round(size * SCALE))


def line(points, fill=INK, width=0.5):
    draw.line([(round(x * SCALE), round(y * SCALE)) for x, y in points],
              fill=fill, width=max(1, round(width * SCALE)))


def rect(box, fill, outline=None, width=1):
    draw.rectangle(tuple(round(value * SCALE) for value in box), fill=fill,
                   outline=outline, width=round(width * SCALE))


def poly(points, fill):
    draw.polygon([(round(x * SCALE), round(y * SCALE)) for x, y in points], fill=fill)


def ellipse(box, fill, outline=None, width=1):
    draw.ellipse(tuple(round(value * SCALE) for value in box), fill=fill,
                 outline=outline, width=round(width * SCALE))


def text(value, x, y, size=11, kind='body', fill=INK, width=None, align='left'):
    face = font(size, kind)
    extent = draw.textlength(value, font=face)
    if width is not None and extent > width * SCALE:
        layer = Image.new('RGBA', (math.ceil(extent) + 6, round((size + 8) * SCALE)))
        ImageDraw.Draw(layer).text((0, 0), value, font=face, fill=fill, anchor='lt')
        layer = layer.resize((round(width * SCALE), layer.height), Image.Resampling.LANCZOS)
        image.paste(layer, (round(x * SCALE), round(y * SCALE)), layer)
    else:
        if align == 'center':
            x -= extent / SCALE / 2
        draw.text((round(x * SCALE), round(y * SCALE)), value, font=face, fill=fill, anchor='lt')


def paragraph(value, x, y, width, size=11, kind='body', leading=14):
    words = value.split()
    current = ''
    rows = []
    for word in words:
        candidate = (current + ' ' + word).strip()
        if draw.textlength(candidate, font=font(size, kind)) > width * SCALE and current:
            rows.append(current)
            current = word
        else:
            current = candidate
    rows.append(current)
    for index, row in enumerate(rows):
        text(row, x, y + index * leading, size, kind)
    return y + len(rows) * leading


stories = [
    (1, 'MID EAST', 'War & security'),
    (2, 'ASIA', 'Politics & diplomacy'),
    (3, 'AMERICAS', 'Politics & diplomacy'),
    (4, 'AMERICAS', 'Society & culture'),
    (5, 'AMERICAS', 'Technology'),
    (6, 'AMERICAS', 'Economy & labour'),
    (7, 'ASIA', 'Disasters & weather'),
    (8, 'WORLD', 'Climate & space'),
    (9, 'EUROPE', 'Politics & diplomacy'),
    (10, 'WORLD', 'Society & culture'),
    (11, 'EUROPE', 'War & security'),
    (12, 'ASIA', 'Justice'),
    (13, 'MID EAST', 'War & security'),
    (14, 'MID EAST', 'Politics & diplomacy'),
    (15, 'WORLD', 'Disasters & weather'),
    (16, 'MID EAST', 'War & security'),
    (17, 'AMERICAS', 'Economy & labour'),
    (18, 'AFRICA', 'War & security'),
    (19, 'AMERICAS', 'Technology'),
    (20, 'AMERICAS', 'Politics & diplomacy'),
    (21, 'AMERICAS', 'Politics & diplomacy'),
    (22, 'AMERICAS', 'Technology'),
    (23, 'AMERICAS', 'Technology'),
    (24, 'AMERICAS', 'Justice'),
    (25, 'AMERICAS', 'Justice'),
    (26, 'EUROPE', 'Society & culture'),
    (27, 'EUROPE', 'Politics & diplomacy'),
    (28, 'EUROPE', 'Climate & space'),
    (29, 'WORLD', 'Climate & space'),
    (30, 'WORLD', 'Society & culture'),
    (31, 'EUROPE', 'War & security'),
    (32, 'OCEANIA', 'Politics & diplomacy'),
    (33, 'EUROPE', 'Politics & diplomacy'),
    (34, 'AMERICAS', 'Politics & diplomacy'),
    (35, 'WORLD', 'Economy & labour'),
]


def count_bar(keys, index, y, size):
    counts = [sum(story[index] == key for story in stories) for key in keys]
    assert sum(counts) == 35
    cell = 976 / len(keys)
    for offset, (key, count) in enumerate(zip(keys, counts)):
        start = 24 + offset * cell
        text(f'{key} {count}', start + 4, y, size, 'label', NAVY, cell - 8)
        if offset:
            line([(start, y), (start, y + 12)], '#bdb5a7')
    return counts


text('LATE EDITION · ALL THE NEWS OF ONE DAY ON ONE PAGE', 24, 24, 11, 'label')
text('No. 2026-323', 917, 24, 11, 'label', width=83)
line([(24, 40), (1000, 40)])
text('THE WORLD IN ONE DAY', 512, 47, 57, 'mast', align='center')
rect((24, 112, 1000, 134), RED)
text('THURSDAY, 19 NOVEMBER 2026 — 35 STORIES · 7 REGIONS · 8 FIELDS · ONE PAGE',
     512, 117, 13, 'label', 'white', align='center')
assert count_bar(['MID EAST', 'AMERICAS', 'ASIA', 'EUROPE', 'AFRICA', 'OCEANIA', 'WORLD'], 1, 141, 11) == [4, 13, 3, 7, 1, 1, 6]
assert count_bar(['War & security', 'Politics & diplomacy', 'Economy & labour', 'Technology',
                  'Society & culture', 'Disasters & weather', 'Climate & space', 'Justice'], 2, 159, 11) == [6, 10, 3, 4, 4, 2, 3, 3]
line([(24, 177), (1000, 177)])
numbers = [('$115.8bn', 'Nvidia revenue, +103%'), ('€45bn', 'EU loan for Ukraine'),
           ('$83.17', 'WTI oil, −3.3% in a day'), ('$3,724', 'Gold, −3.3%'),
           ('1 light-day', 'Voyager 1 from Earth'), ('$190.4m', 'Record Van Gogh sale')]
for index, (number, label) in enumerate(numbers):
    center = 24 + (index + 0.5) * 976 / 6
    text(number, center, 184, 23, 'head', NAVY, align='center')
    text(label, center, 212, 11, align='center')
line([(24, 230), (1000, 230)], width=1.4)

text('MIDDLE EAST · GULF WAR', 24, 238, 11, 'label', RED)
text('Iran hits US base in Kuwait', 24, 254, 28, 'head', width=536)
text('as Gulf war widens', 24, 286, 28, 'head')
paragraph("Tehran's drones struck Ali Al Salem air base and Bahrain again — its first attack on Kuwait since September — in retaliation for Tuesday's US strike on Qeshm Island. Kuwait says its defences intercepted them; no US personnel were hurt.",
          24, 321, 534, 11, leading=13)
bullets = ["Bahrain intercepted Iranian attacks for the third time in a week; it hosts the US Navy's Fifth Fleet.",
           'Three US carrier groups are now in the region; diplomacy to end the nine-month war is deadlocked.',
           'Today in Shenzhen, Trump meets Xi and Putin — with the Iran war on the agenda.']
for index, bullet in enumerate(bullets):
    ellipse((25, 375 + index * 15, 28, 378 + index * 15), RED)
    text(bullet, 34, 372 + index * 15, 11, width=523)


def gulf_map():
    rect((578, 238, 1000, 415), '#d9e9ed')
    poly([(578, 238), (1000, 238), (1000, 317), (957, 322), (928, 305),
          (892, 299), (858, 286), (827, 273), (788, 265), (749, 257), (699, 251), (649, 238)], '#e3d7bd')
    poly([(578, 238), (649, 238), (676, 257), (690, 284), (723, 306), (751, 327),
          (781, 344), (816, 373), (857, 390), (905, 401), (929, 415), (578, 415)], '#e9dec6')
    poly([(946, 317), (963, 322), (977, 321), (971, 327), (951, 324)], NAVY)
    text('IRAN', 850, 249, 18, 'label', NAVY)
    text('IRAQ', 598, 247, 12, 'label', NAVY)
    text('KUWAIT', 593, 276, 12, 'label', NAVY)
    text('SAUDI ARABIA', 601, 367, 13, 'label', NAVY)
    text('PERSIAN GULF', 799, 317, 15, 'label', NAVY)
    text('QESHM ISLAND', 894, 341, 11, 'label', NAVY)
    line([(962, 326), (953, 338)], NAVY)
    text('BAHRAIN', 732, 386, 11, 'label', NAVY)
    text('ALI AL SALEM', 591, 308, 11, 'label', RED)
    text('SHEIKH ISA', 784, 400, 11, 'label', RED)
    for target in [(674, 293), (780, 377)]:
        start = (885, 279)
        for step in range(0, 24, 2):
            first = step / 24
            second = (step + 1) / 24
            line([(start[0] + (target[0] - start[0]) * first, start[1] + (target[1] - start[1]) * first),
                  (start[0] + (target[0] - start[0]) * second, start[1] + (target[1] - start[1]) * second)], RED, 1.5)
        angle = math.atan2(target[1] - start[1], target[0] - start[0])
        poly([target, (target[0] - 9 * math.cos(angle - 0.4), target[1] - 9 * math.sin(angle - 0.4)),
              (target[0] - 9 * math.cos(angle + 0.4), target[1] - 9 * math.sin(angle + 0.4))], RED)
        ellipse((target[0] - 3, target[1] - 3, target[0] + 3, target[1] + 3), RED)


gulf_map()
line([(24, 423), (1000, 423)], width=1.2)


def star(center, radius, fill):
    points = []
    for index in range(10):
        angle = -math.pi / 2 + index * math.pi / 5
        length = radius if index % 2 == 0 else radius * 0.42
        points.append((center[0] + math.cos(angle) * length, center[1] + math.sin(angle) * length))
    poly(points, fill)


def illustration(number, x, y, width):
    backgrounds = {2: '#dce4e5', 3: '#d9e3ec', 4: '#d99278', 5: '#142f2c', 6: '#e6ddc5',
                   7: '#91c4cf', 8: '#152b49', 9: '#234c85', 10: '#e5bd4f'}
    rect((x, y, x + width, y + 28), backgrounds[number])
    center = x + width / 2
    if number == 2:
        for offset in range(3):
            start = center - 88 + offset * 71
            line([(start, y + 4), (start, y + 26)], NAVY, 1)
            if offset == 0:
                rect((start + 1, y + 3, start + 44, y + 20), '#fffaf0')
                for stripe in range(4):
                    rect((start + 1, y + 3 + stripe * 4, start + 44, y + 5 + stripe * 4), RED)
                rect((start + 1, y + 3, start + 19, y + 12), NAVY)
                star((start + 10, y + 7), 3, 'white')
            elif offset == 1:
                rect((start + 1, y + 3, start + 44, y + 20), RED)
                star((start + 11, y + 9), 4, '#f5d66d')
            else:
                for stripe, color in enumerate(['white', '#254d88', RED]):
                    rect((start + 1, y + 3 + stripe * 6, start + 44, y + 8 + stripe * 6), color)
    elif number == 3:
        ellipse((center - 27, y + 4, center + 27, y + 37), NAVY)
        rect((center - 29, y + 17, center + 29, y + 28), '#edf0e9')
        rect((center - 66, y + 23, center + 66, y + 28), NAVY)
        for offset in range(-4, 5):
            rect((center + offset * 12 - 2, y + 18, center + offset * 12 + 2, y + 27), NAVY)
        line([(center, y + 1), (center, y + 5)], NAVY, 2)
    elif number == 4:
        for stripe in range(28):
            fraction = stripe / 27
            color = tuple(round(first + (last - first) * fraction) for first, last in zip((102, 65, 130), (246, 167, 93)))
            rect((x, y + stripe, x + width, y + stripe + 1), color)
        for offset, height in enumerate([8, 13, 9, 17, 11, 14, 7, 19, 10]):
            rect((x + 20 + offset * 29, y + 28 - height, x + 39 + offset * 29, y + 28), '#343450')
        line([(x + 256, y + 27), (x + 253, y + 7)], '#202c38', 3)
        for tip in [(238, 8), (244, 2), (264, 3), (271, 11)]:
            line([(x + 253, y + 7), (x + tip[0], y + tip[1])], '#202c38', 2)
    elif number == 5:
        for offset in range(-3, 4):
            line([(center + offset * 10, y), (center + offset * 10, y + 28)], '#7ca658', 1)
            line([(center - 90, y + 14 + offset * 3), (center + 90, y + 14 + offset * 3)], '#7ca658', 1)
        rect((center - 34, y + 3, center + 34, y + 25), '#82b945', '#b6d687')
        text('NVIDIA', center, y + 9, 11, 'label', '#143123', align='center')
    elif number == 6:
        for offset in range(7):
            rect((x + 58 + offset * 25, y + 25 - offset * 3, x + 71 + offset * 25, y + 27), '#a5b6a0')
        text('$', x + 28, y + 2, 23, 'head', NAVY)
        line([(x + 65, y + 23), (x + 143, y + 18), (x + 196, y + 5), (x + 263, y + 4)], RED, 2)
        poly([(x + 263, y + 4), (x + 254, y + 1), (x + 256, y + 10)], RED)
    elif number == 7:
        poly([(x, y), (x + 120, y), (x + 139, y + 10), (x + 153, y + 17), (x + 157, y + 28), (x, y + 28)], '#c8d2aa')
        points = []
        for step in range(150):
            angle = step * 0.11
            radius = step * 0.085
            points.append((x + 190 + math.cos(angle) * radius * 2, y + 14 + math.sin(angle) * radius))
        line(points, 'white', 2)
        ellipse((x + 188, y + 12, x + 192, y + 16), NAVY)
    elif number == 8:
        for offset in range(22):
            ellipse((x + 7 + (offset * 47) % 300, y + 3 + (offset * 13) % 22,
                     x + 8 + (offset * 47) % 300, y + 4 + (offset * 13) % 22), '#e7e1ba')
        ellipse((center - 17, y + 5, center + 12, y + 18), '#ece5d3', '#a4b5c6')
        line([(center - 2, y + 12), (center + 25, y + 24)], '#d7c9a2', 2)
        line([(center + 9, y + 17), (center + 37, y + 7)], '#d7c9a2', 1)
        rect((center + 2, y + 16, center + 12, y + 22), '#c6ae76')
    elif number == 9:
        for offset in range(12):
            angle = offset * math.pi / 6
            star((center + 31 * math.cos(angle), y + 14 + 10 * math.sin(angle)), 2.3, '#f2d374')
        text('€', center, y + 3, 23, 'head', '#f2d374', align='center')
    else:
        for offset in range(17):
            center_x = x + 10 + offset * 18
            center_y = y + 9 + offset % 3 * 6
            line([(center_x, center_y), (center_x - 6, y + 28)], '#778549', 2)
            for petal in range(7):
                angle = petal * math.tau / 7
                ellipse((center_x + math.cos(angle) * 5 - 3, center_y + math.sin(angle) * 4 - 3,
                         center_x + math.cos(angle) * 5 + 3, center_y + math.sin(angle) * 4 + 3), '#f7d76a')
            ellipse((center_x - 3, center_y - 3, center_x + 3, center_y + 3), '#895b31')


cards = [
    (2, 'ASIA · POLITICS', ['Trump, Xi and Putin', 'meet in Shenzhen'], 'First three-way meeting of its kind, at the APEC summit; Xi hugged Trump on the tarmac.'),
    (3, 'AMERICAS · POLITICS', ['Jeffries nominated, on course', 'to be first Black Speaker'], 'House Democrats back him 251–11; floor vote on 3 January. Clark to be first woman majority leader.'),
    (4, 'AMERICAS · CULTURE', ['GTA VI rolls out worldwide', 'after a 13-year wait'], 'Vice City opens at midnight, time zone by time zone.'),
    (5, 'AMERICAS · TECHNOLOGY', ['Nvidia revenue doubles', 'to $115.8bn'], 'Record quarter lifts shares; board rules out a return for ousted chief Huang. Kress is interim CEO.'),
    (6, 'AMERICAS · ECONOMY', ['Fed minutes point', 'to more rate hikes'], 'Nearly all officials expect further rises; Waller backs a half-point move in December.'),
    (7, 'ASIA · WEATHER', ["Cyclone Akvan nears", "India's east coast"], 'Landfall expected Friday between Machilipatnam and Puri.'),
    (8, 'WORLD · SPACE', ['Voyager 1 reaches one', 'light-day from Earth'], 'First human-made object that far, 49 years on.'),
    (9, 'EUROPE · POLITICS', ['EU proposes €45bn', 'loan for Ukraine'], 'Repaid after Russia pays reparations, Brussels says.'),
    (10, 'WORLD · CULTURE', ['Van Gogh sells for', 'a record $190.4m'], 'Châtaigniers en fleurs, painted in 1890, after a row over its Nazi history.'),
]
for index, (number, kicker, headlines, deck) in enumerate(cards):
    column = index % 3
    row = index // 3
    x = 24 + column * 331
    y = 431 + row * 101
    illustration(number, x, y, 314)
    text(f'{number} · {kicker}', x, y + 33, 11, 'label', RED)
    for offset, headline in enumerate(headlines):
        text(headline, x, y + 48 + offset * 18, 17, 'head', width=314)
    text(deck, x, y + 86, 11, width=314)
    if row < 2:
        line([(x, y + 98), (x + 314, y + 98)], '#bdb5a7')
for x in [346, 677]:
    line([(x, 431), (x, 728)], '#bdb5a7')
line([(24, 736), (1000, 736)], width=1.2)


def world_map():
    continents = [
        [(0.06, .18), (.18, .08), (.32, .16), (.28, .31), (.20, .39), (.24, .48), (.15, .42), (.09, .31)],
        [(.25, .46), (.34, .50), (.37, .61), (.32, .84), (.28, .93), (.25, .69)],
        [(.38, .09), (.45, .07), (.44, .24), (.39, .23)],
        [(.47, .31), (.55, .22), (.68, .16), (.84, .15), (.96, .27), (.87, .40), (.75, .39), (.70, .58), (.63, .48), (.56, .39)],
        [(.48, .39), (.61, .42), (.62, .57), (.55, .76), (.50, .65), (.46, .49)],
        [(.79, .68), (.88, .65), (.94, .77), (.86, .84), (.78, .79)],
        [(.73, .49), (.78, .53), (.81, .59), (.87, .60), (.84, .64), (.76, .59)],
    ]
    mask = Image.new('1', (220, 135))
    mask_draw = ImageDraw.Draw(mask)
    for continent in continents:
        mask_draw.polygon([(round(x * 219), round(y * 134)) for x, y in continent], fill=1)
    for row in range(0, 135, 4):
        for column in range(0, 220, 4):
            if mask.getpixel((column, row)):
                ellipse((24 + column, 775 + row, 25.4 + column, 776.4 + row), '#7f9595')
    pins = [(1, 153, 831), (2, 195, 820), (3, 82, 816), (4, 76, 841), (5, 54, 816),
            (6, 101, 797), (7, 177, 845), (8, 39, 779), (9, 130, 802), (10, 118, 781)]
    for number, x, y in pins:
        ellipse((x - 7, y - 7, x + 7, y + 7), RED)
        text(str(number), x, y - 4, 11, 'label', 'white', align='center')


text('WHERE IT HAPPENED', 24, 746, 13, 'label', NAVY)
world_map()
text('Pins 1–10 · Space & sale shown schematically', 24, 916, 11, width=220)
text('ALSO ON THURSDAY 19 NOVEMBER', 261, 746, 13, 'label', RED)
briefs = [
    (11, 'EUROPE', "Crimean Bridge attacked again; traffic suspended, Crimea's head says."),
    (12, 'ASIA', "UN court to deliver historic genocide verdict on Myanmar's Rohingya case."),
    (13, 'MID EAST', "Israeli forces launch rare ground operation beyond Gaza's Yellow Line."),
    (14, 'MID EAST', "Israel's president taps Eisenkot to form a government, bypassing Netanyahu."),
    (15, 'WORLD', 'Australia, Canada, Italy and the UK urge Israel to let aid reach flooded Gaza.'),
    (16, 'MID EAST', 'Houthi rocket attack kills 53 soldiers at a Yemeni military camp.'),
    (17, 'AMERICAS', 'US details $12bn in Venezuelan oil and mineral revenue in a 53-page report.'),
    (18, 'AFRICA', 'Somalia accuses the UAE of secretly building military bases on its soil.'),
    (19, 'AMERICAS', 'Senators warn AI cyber threats are outpacing US defences.'),
    (20, 'AMERICAS', 'Democrat Peltola wins in Alaska, securing a 56–44 Senate majority.'),
    (21, 'AMERICAS', "Canada's Carney adjusts China ties, seeking the right deal with the US."),
    (22, 'AMERICAS', 'Anthropic poised for a $1.4tn-plus stock-market debut; founders set for billions.'),
    (23, 'AMERICAS', 'Waymo pulls all its driverless cars from US freeways.'),
    (24, 'AMERICAS', 'Russian arrested for spying on US defence firm Palantir over Ukraine support.'),
    (25, 'AMERICAS', "McDonald's sex-abuse case can go ahead, a judge rules."),
    (26, 'EUROPE', 'France sees a fourth weekend of protests over the cost of living.'),
    (27, 'EUROPE', 'Zelensky accuses the US of blocking paid missile deliveries.'),
    (28, 'EUROPE', "Finland approves the world's first nuclear-waste repository."),
    (29, 'WORLD', 'Nearly all coral reefs face extinction within 50 years, an IUCN study warns.'),
    (30, 'WORLD', 'Muslims to outnumber Christians worldwide by 2035, Pew projects.'),
    (31, 'EUROPE', 'Germany arrests a suspected Russian spy; 2027 tax forecast hits €1tn.'),
    (32, 'OCEANIA', 'Australia sanctions Israeli settlers over West Bank expansion.'),
    (33, 'EUROPE', 'LPG tanker that sank off Bulgaria was hit by projectiles, an official says.'),
    (34, 'AMERICAS', 'House Oversight chair orders Trump allies to preserve records ahead of probes.'),
    (35, 'WORLD', 'Markets slip on hawkish Fed minutes: oil and gold fall, S&P 500 down.'),
]
for index, (number, region, brief) in enumerate(briefs):
    column = 0 if index < 13 else 1
    row = index if index < 13 else index - 13
    text(f'{number} {region} — {brief}', 261 + column * 376, 770 + row * 12.5,
         11, width=363)
line([(625, 768), (625, 929)], '#bdb5a7')

rect((24, 939, 1000, 977), PAPER, RED, 1)
text('DATE CHECK — Left out on purpose because they broke before today:', 32, 941, 12, 'label', RED)
text("Jensen Huang resigned from Nvidia on 12 Nov; the first US strike on Qeshm Island was Tuesday 17 Nov — today's story is the widening;",
     32, 954, 11, width=959)
text("India's 2–1 SAFF final win over Pakistan was Tuesday 17 Nov in Dhaka; the NSA network outage was first reported Tuesday.",
     32, 966, 11, width=959)
line([(24, 984), (1000, 984)])
text('Drawn entirely by program · Set in Noto Serif Display & Noto Sans Condensed · Every story happened or was first reported Thursday 19 November 2026.',
     24, 989, 11, width=976)
text('Sources: AP, Reuters, AFP, Bloomberg, NYT, BBC, FT, The Hindu, MarketWatch, The Guardian. Original drawings.',
     24, 1002, 11, width=976)

image = image.resize((1024, 1024), Image.Resampling.LANCZOS)
destination = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / 'entry.png'
image.save(destination, format='PNG', optimize=True)
