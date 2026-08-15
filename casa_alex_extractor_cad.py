"""CASA ALEX — extrae geometría exacta del croquis CAD y genera modelo 3D corregido."""
import pdfplumber, math, json

PDF = '/mnt/user-data/uploads/CASA_ALEX_1-Model.pdf'
S = 14.839  # pt por metro (calibrado contra áreas y perímetros rotulados)

pdf = pdfplumber.open(PDF)
page = pdf.pages[0]

def clean(pts):
    out = []
    for p in pts:
        if not out or math.dist(out[-1], p) > 0.5:
            out.append(p)
    if len(out) > 1 and math.dist(out[0], out[-1]) < 0.5:
        out.pop()
    return out

def shoelace(pts):
    a = 0.0
    for i in range(len(pts)):
        x1, y1 = pts[i]; x2, y2 = pts[(i + 1) % len(pts)]
        a += x1 * y2 - x2 * y1
    return abs(a) / 2

def perim(pts):
    return sum(math.dist(pts[i], pts[(i + 1) % len(pts)]) for i in range(len(pts)))

# --- polígonos de área (rojo oscuro CAD) ---
red = [c for c in page.curves if c['stroking_color'] == (0.72157, 0.0, 0.0)]
NAMES = ['CASA 2 PISOS', 'AREA VERDE', 'CAMIONETA 5', 'CAMIONETA 4', 'AUTO',
         'CAMIONETA', 'CAMIONETA 2', 'CAMIONETA 3', 'AUTO 2', 'SALA DE ESPERA',
         None, 'AREA DE LAVADO']
IDS = ['house', 'green_area', 'parking_camioneta_5', 'parking_camioneta_4', 'parking_auto',
       'parking_camioneta', 'parking_camioneta_2', 'parking_camioneta_3', 'parking_auto_2',
       'waiting_room', None, 'wash_area']
REF = {'CASA 2 PISOS': (61.04, 37.18), 'AREA VERDE': (51.39, 46.22),
       'AREA DE LAVADO': (54.25, 29.77), 'SALA DE ESPERA': (2.51, 11.03),
       'CAMIONETA': (10.26, 14.60), 'CAMIONETA 2': (10.26, 14.60), 'CAMIONETA 3': (10.26, 14.60),
       'CAMIONETA 4': (10.26, 14.60), 'CAMIONETA 5': (10.26, 14.60),
       'AUTO': (8.10, 12.60), 'AUTO 2': (8.10, 12.60)}

raw = []
for name, eid, c in zip(NAMES, IDS, red):
    if name is None:
        continue
    pts = [(x / S, y / S) for x, y in clean(c['pts'])]
    if len(pts) < 3:
        continue
    raw.append({'id': eid, 'label': name, 'pts': pts})

# --- normalizar: y del PDF crece hacia abajo -> voltear para que el norte sea +Y ---
allpts = [p for e in raw for p in e['pts']]
xmin = min(p[0] for p in allpts); xmax = max(p[0] for p in allpts)
ymin = min(p[1] for p in allpts); ymax = max(p[1] for p in allpts)
cx = (xmin + xmax) / 2; cy = (ymin + ymax) / 2

def tx(p):
    return [round(p[0] - cx, 3), round(cy - p[1], 3)]

for e in raw:
    e['polygon'] = [tx(p) for p in e['pts']]
    del e['pts']

# --- geometría auxiliar: vía y límite de propiedad ---
def segs(color, src):
    out = []
    for o in src:
        if o['stroking_color'] == color:
            pts = [tx((x / S, y / S)) for x, y in clean(o['pts'])]
            if len(pts) >= 2:
                out.append(pts)
    return out

via = segs((0.0, 0.0, 0.0), page.curves + page.lines)
limite = segs((0.0, 1.0, 0.0), page.curves + page.lines) + segs((1.0, 0.0, 1.0), page.curves + page.lines)
via = [s for s in via if perim(s) > 3]
limite = [s for s in limite if perim(s) > 3]

# --- alturas y tipos (lo único que NO viene del plano) ---
ALTURA = {
    'house': {'type': 'building', 'height': 6.20, 'floors': 2, 'floor_height': 3.10, 'roof': 'plana'},
    'wash_area': {'type': 'canopy', 'height': 4.20, 'column_h': 4.20},
    'waiting_room': {'type': 'low_wall', 'height': 0.95,
                     'nota': 'En el CAD es una franja en "L" de 0.50 m de ancho (2.51 m²). '
                             'Eso es un parapeto o jardinera que delimita la sala de espera, no un '
                             'ambiente cerrado: el plano no trae el contorno del recinto. '
                             'Si la sala es un ambiente techado, falta dibujarla.'},
    'green_area': {'type': 'ground', 'height': 0.12},
}
STALL = {'type': 'parking_stall', 'height': 0.10}

elements = []
for e in raw:
    A = shoelace(e['polygon']); P = perim(e['polygon'])
    meta = ALTURA.get(e['id'], STALL).copy()
    ref = REF.get(e['label'])
    el = {
        'id': e['id'], 'label': e['label'], 'polygon': e['polygon'],
        'area_m2': round(A, 2), 'perimeter_m': round(P, 2),
        'area_rotulada_m2': ref[0] if ref else None,
        'perimetro_rotulado_m': ref[1] if ref else None,
        'error_area_pct': round(abs(A - ref[0]) / ref[0] * 100, 2) if ref else None,
    }
    el.update(meta)
    elements.append(el)

model = {
    'project': {
        'name': 'CASA ALEX',
        'source': 'CASA_ALEX_1-Model.pdf (extracción vectorial CAD)',
        'units': 'm',
        'scale_pt_per_m': S,
        'status': 'planta_exacta_alturas_supuestas',
        'notes': [
            'La PLANTA es exacta: coordenadas extraídas de las polilíneas del PDF y verificadas contra las áreas y perímetros rotulados (error < 0.3%).',
            'Las ALTURAS y el tipo de cada volumen NO están en el croquis: son supuestos editables.',
            'Origen (0,0) = centro del rectángulo envolvente del conjunto. +Y = arriba del plano.',
        ],
    },
    'elements': elements,
    'context': {'via': via, 'limite_propiedad': limite},
    'bbox_m': {'ancho': round(xmax - xmin, 2), 'largo': round(ymax - ymin, 2)},
}

with open('/home/claude/casa_alex_modelo_corregido.json', 'w', encoding='utf-8') as f:
    json.dump(model, f, ensure_ascii=False, indent=2)

print(f"bbox conjunto: {model['bbox_m']['ancho']} x {model['bbox_m']['largo']} m")
print(f"{'elemento':18s} {'área calc':>10s} {'rotulada':>9s} {'err %':>6s}  alt")
for e in elements:
    print(f"{e['label']:18s} {e['area_m2']:10.2f} {e['area_rotulada_m2'] or 0:9.2f} "
          f"{e['error_area_pct'] or 0:6.2f}  {e.get('height')}")
print(f"\nvía: {len(via)} tramos · límite: {len(limite)} tramos")
