"""Laboratorio semana 14 - Tecnologías Inmersivas (PROG 409)
Convierte posiciones de píxel (px, py) de una foto 360° equirectangular
en ángulos (yaw, pitch) y en coordenadas 3D (x, y, z) para A-Frame.
Lee puntos.csv y escribe puntos.json (que carga index.html con fetch()).
"""
import csv
import json
import math

ANCHO = 4096      # ancho de la foto 360° en píxeles
ALTO = 2048       # alto de la foto 360° en píxeles (proporción 2:1)
R = 6.0           # distancia del visitante a los puntos (metros)
ALTURA_OJOS = 1.6


def pixel_a_angulos(px, py):
    # TODO 1: yaw y pitch a partir del píxel
    yaw = (px / ANCHO - 0.5) * 360      # 0° al frente, positivo a la derecha
    pitch = (0.5 - py / ALTO) * 180     # 0° en el horizonte, positivo hacia arriba
    return yaw, pitch


def angulos_a_posicion(yaw, pitch, r=R):
    # TODO 2: posición 3D (+X derecha, +Y arriba, -Z al frente)
    a = math.radians(yaw)
    b = math.radians(pitch)
    x = r * math.cos(b) * math.sin(a)
    y = ALTURA_OJOS + r * math.sin(b)
    z = -r * math.cos(b) * math.cos(a)
    return x, y, z


def main():
    puntos = []
    with open("puntos.csv", encoding="utf-8", newline="") as f:
        for fila in csv.DictReader(f):
            yaw, pitch = pixel_a_angulos(float(fila["px"]), float(fila["py"]))
            x, y, z = angulos_a_posicion(yaw, pitch)
            puntos.append({
                "id": fila["id"],
                "titulo": fila["titulo"],
                "descripcion": fila["descripcion"],
                "yaw": round(yaw, 1),
                "pitch": round(pitch, 1),
                "posicion": {"x": round(x, 3), "y": round(y, 3), "z": round(z, 3)},
            })

    with open("puntos.json", "w", encoding="utf-8") as f:
        json.dump(puntos, f, ensure_ascii=False, indent=2)

    print(f"{'id':<10}{'yaw':>8}{'pitch':>8}   posición (x, y, z)")
    for p in puntos:
        pos = p["posicion"]
        print(f"{p['id']:<10}{p['yaw']:>8}{p['pitch']:>8}   ({pos['x']}, {pos['y']}, {pos['z']})")
    print(f"\nSe generó puntos.json con {len(puntos)} puntos.")


if __name__ == "__main__":
    main()
