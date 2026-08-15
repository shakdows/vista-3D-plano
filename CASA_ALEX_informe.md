# CASA ALEX — levantamiento, correcciones y hallazgos

## 1. Qué estaba mal

El JSON que tenías (`casa_alex_modelo_3d_claude.json`) era un **calco visual**: alguien miró el
croquis y estimó las coordenadas a ojo. Las áreas declaradas eran correctas porque estaban copiadas
del rótulo, pero los polígonos no.

El PDF no es una imagen: es un **CAD vectorial**. Las polilíneas están ahí, con coordenadas exactas.
Las extraje y calibré la escala contra los rótulos: **14.839 puntos por metro**.

| Elemento | Área calculada | Área rotulada | Error |
|---|---|---|---|
| CASA 2 PISOS | 61.11 m² | 61.04 m² | 0.11 % |
| AREA VERDE | 51.39 m² | 51.39 m² | 0.01 % |
| AREA DE LAVADO | 54.10 m² | 54.25 m² | 0.28 % |
| SALA DE ESPERA | 2.52 m² | 2.51 m² | 0.47 % |
| Camionetas (×5) | 10.24–10.27 m² | 10.26 m² | < 0.16 % |
| Autos (×2) | 8.10–8.11 m² | 8.10 m² | < 0.13 % |

Once de once por debajo del 0.5 %. La planta ya no es una aproximación.

**Conjunto:** 21.56 × 33.82 m de envolvente. 117.7 m² techados (casa + lavado + espera).

---

## 2. Dos cosas que el plano dice y que conviene mirar

### 2.1 Los rectángulos de estacionamiento son vehículos, no cajones

Medidos: **5.40 × 1.90 m** las camionetas y **4.50 × 1.80 m** los autos.

Eso no es un cajón de estacionamiento — es la huella de la carrocería. Una Hilux mide 5.33 × 1.86 m
y un Corolla 4.63 × 1.78 m. Los bloques del CAD son los autos dibujados, no el espacio asignado.

Importa porque las separaciones entre bloques vecinos son:

| Par | Separación |
|---|---|
| CAMIONETA 2 ↔ AUTO 2 | **0.53 m** |
| CAMIONETA 3 ↔ AUTO 2 | 0.75 m |
| AUTO ↔ CAMIONETA | 1.00 m |
| CAMIONETA ↔ CAMIONETA 2 | 1.01 m |
| CAMIONETA 5 ↔ CAMIONETA 4 | 1.25 m |

Una puerta delantera de camioneta necesita entre 0.75 y 0.90 m para abrirse lo suficiente como para
bajar sin contorsionarse. Con 0.53 m no se baja. Y si el negocio es lavado de autos, tus operarios
van a estar entrando y saliendo de esos vehículos todo el día, con mangueras y baldes.

Como referencia, el RNE peruano trabaja con cajones de alrededor de 2.40–2.50 m de ancho por 5.00 m
de largo. Si esos siete espacios se convierten en cajones normados, **no entran siete en esa
superficie** con esa disposición. Conviene decidirlo ahora y no después de vaciar el piso.

### 2.2 La "sala de espera" no es un ambiente

En el CAD es una franja en **L de 0.50 m de ancho**, de 3.50 m + 1.50 m de largo. Eso da los 2.51 m²
del rótulo. Es un **parapeto o una jardinera**, no un cuarto: el plano nunca dibuja el contorno del
recinto.

En el visor la modelé como muro bajo, no como el pabellón vidriado que aparece en tu render. Si la
sala de espera va a ser un ambiente techado, hay que dibujarla — hoy no existe en el plano.

---

## 3. El render de ChatGPT vs. el plano

El render es bueno como dirección estética. Como referencia dimensional **no sirve**, y conviene
tenerlo claro antes de enseñárselo a alguien:

- El área de lavado quedó en el lado opuesto respecto del croquis.
- Los siete espacios se volvieron una fila única de siete bajo toldos individuales.
- Aparecen elementos que el plano no tiene: muro perimétrico, módulos "SERVICIO 1", letrero,
  jardinería, escalinatas.
- La casa cambió de forma: en el plano es un polígono de 6 lados (6.23 · 5.04 · 3.40 · 7.22 · 4.03 ·
  11.25 m); en el render es una L limpia.

Úsalo para decidir acabados y materiales. Para decidir dónde va cada cosa, usa el visor.

---

## 4. El visor

`casa_alex_visor_3d_v2.html` — **archivo único, sin internet**. Three.js va incrustado dentro, así
que abre con doble clic. El anterior dependía de un CDN: abierto como archivo local el navegador lo
bloqueaba y quedaba en negro.

- **4 cámaras**: perspectiva, aérea, planta y una a 1.70 m de altura como si estuvieras parado ahí.
- **Sol por hora** (6:00–19:00): sombras y color de luz reales. Sirve para ver qué zona del lavado
  recibe sol directo a media tarde.
- **Clic en cualquier volumen** → área calculada, área rotulada, desviación, perímetro, lados.
- **Cotas**: la medida de cada lado sobre la geometría.
- **Capas**: vehículos, vegetación, toldos, cerco, rejilla.

Todo lo horizontal viene del CAD. Todo lo vertical (6.20 m la casa, 4.20 m el techo del lavado,
2.95 m los toldos, 2.60 m el cerco) es **supuesto mío** y está marcado como tal en el panel, porque
el croquis no trae ni una sola cota de altura ni un corte.

---

## 5. Prompts para los siguientes renders

Anclados a la geometría real. Genéralos desde una **captura del visor** (image-to-image), no desde
texto puro — así la IA respeta la distribución en vez de inventarla, que es exactamente lo que pasó
con el render anterior.

**Flujo:** abre el visor → vista Aérea → apaga Etiquetas y Cotas → captura → esa imagen es el frame
inicial → pega el prompt.

### A · Aérea de conjunto (la de venta)
```
Aerial architectural visualization of a vehicle service compound, 3/4 overhead view.
Two-story modern house with flat roof and parapet, warm white stucco and dark bronze window
frames, at the far end of the lot. Open-sided steel wash canopy with matte black flat roof
supported on slim concrete columns, wet polished concrete floor with light reflections.
Row of vehicles under individual light grey metal canopies on brushed steel posts.
Perimeter wall in warm white plaster. Tropical landscaping: palms and rounded broadleaf trees
on manicured grass. Paved light concrete yard. Late afternoon sun, long soft shadows, clear sky.
Photorealistic architectural render, 35mm, high detail, no text, no logos.
```

### B · Ingreso desde la calle (vista de cliente)
```
Eye-level view from the street entrance of a vehicle wash and service compound.
Paved concrete driveway leading in, low white planter wall on the right delimiting a waiting
area with benches and greenery. Black-roofed open wash canopy visible ahead on the left,
two-story white house in the background. Warm morning light, soft shadows.
Photorealistic architectural render, 28mm, eye level 1.7m, no text.
```

### C · Área de lavado en operación
```
Interior of an open-sided vehicle wash bay under a matte black flat steel roof on concrete
columns. Two pickup trucks being washed, wet reflective concrete floor, foam and water spray,
drainage channel, coiled hoses on wall reels, workers in uniform. Bright daylight entering
from the open sides, strong contrast between the dark roof and the lit floor.
Photorealistic, 24mm, high detail, no text.
```

### D · Nocturna (la que mejor vende un negocio de servicio)
```
Night view of a vehicle service compound. Warm interior lights glowing through the two-story
house windows, cool white LED strips under the black wash canopy roof, ground-level uplights
along the perimeter wall washing the plaster, illuminated vehicles under canopies.
Deep blue dusk sky, wet reflective pavement. Cinematic architectural render, long exposure feel,
no text, no logos.
```

**Regla para todos:** ninguno menciona el letrero ni los módulos de servicio. Si los quieres,
primero dibújalos en el plano — si no, cada render te va a devolver una distribución distinta y
ninguna va a coincidir con lo que después construyas.

---

## 6. Lo que falta para pasar de conceptual a constructivo

1. **Cotas de altura o un corte.** Es lo único que hoy estoy suponiendo.
2. **El contorno de la sala de espera** si va a ser un ambiente.
3. **Decidir cajones vs. vehículos** en los siete espacios (punto 2.1).
4. **El DWG/DXF**, si existe. Con eso el modelo pasa de exacto en planta a exacto y editable.
