"""
Modulo de Cifrado Caotico de Imagenes en 1D (Amin et al., 2010).

Implementa un criptosistema simetrico para imagenes digitales en escala de grises
basado en la dinamica caotica del Mapa de Tienda (Tent Map):
1. Carga, validacion y guardado de imagenes en formatos estandar (PNG, JPG, BMP).
2. Generacion de keystream caotico flotante y entero (8 bits).
3. Permutacion espacial de pixeles (Confusion) mediante ordenamiento indirecto (argsort).
4. Difusion XOR encadenada (Amin et al., 2010):
       C_i = P'_i ^ S_i ^ C_(i-1), con C_(-1) = IV
5. Descifrado exacto invertible sin perdidas (Fidelidad de Descifrado: MSE = 0.0).
6. Evaluacion de Sensibilidad a la Clave (NPCR y UACI) segun Wu, Noonan y Agaian (2011).
7. Pipeline completo para procesar imagenes arbitrarias y exportar a disco.
"""

import os
from typing import Tuple, Dict, Union, Optional
import numpy as np
from PIL import Image

from .maps import TentMap, LogisticMap


def load_image(image_path: str, max_size: Optional[int] = None) -> np.ndarray:
    """
    Carga cualquier archivo de imagen compatible (PNG, JPG, JPEG, BMP, etc.),
    lo valida y lo convierte a una matriz 2D de pixeles en escala de grises (uint8).

    Parametros:
    -----------
    image_path : str
        Ruta del archivo de imagen a procesar.
    max_size : int, opcional
        Dimension maxima permitida (ancho o alto). Si la imagen supera este limite,
        se redimensiona proporcionalmente manteniendo la relacion de aspecto.

    Retorna:
    --------
    np.ndarray (dtype=np.uint8)
        Matriz bidimensional de intensidades en el rango [0, 255].
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"No se encontro el archivo de imagen: {image_path}")

    pil_img = Image.open(image_path)

    # Convertir a escala de grises si es RGB o RGBA
    if pil_img.mode != 'L':
        pil_img = pil_img.convert('L')

    # Redimensionar si se especifica max_size para controlar el tiempo computacional
    if max_size is not None:
        width, height = pil_img.size
        if width > max_size or height > max_size:
            scale = max_size / max(width, height)
            new_w = max(1, int(width * scale))
            new_h = max(1, int(height * scale))
            pil_img = pil_img.resize((new_w, new_h), Image.Resampling.LANCZOS)

    img_array = np.array(pil_img, dtype=np.uint8)
    return img_array


def save_image(image_data: np.ndarray, output_path: str) -> str:
    """
    Guarda una matriz 2D de intensidades (uint8) como un archivo de imagen en disco.

    Parametros:
    -----------
    image_data : np.ndarray
        Matriz 2D de pixeles en escala de grises.
    output_path : str
        Ruta de destino donde se guardara la imagen.

    Retorna:
    --------
    str
        Ruta absoluta del archivo guardado.
    """
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    clean_arr = np.clip(image_data, 0, 255).astype(np.uint8)
    pil_img = Image.fromarray(clean_arr, mode='L')
    pil_img.save(output_path)
    return os.path.abspath(output_path)


def generate_keystream(
    map_instance: Union[TentMap, LogisticMap],
    x0: float,
    length: int,
    n_transient: int = 500,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Genera la secuencia caotica flotante X y la secuencia de claves discreta S de 8 bits.

    Parametros:
    -----------
    map_instance : TentMap o LogisticMap
        Instancia del mapa caotico configurado en regimen caotico.
    x0 : float
        Condicion inicial / semilla secreta (0 < x0 < 1).
    length : int
        Longitud de la secuencia requerida (L = M * N).
    n_transient : int
        Iteraciones iniciales descartadas para asentarse en el atractor caotico.

    Retorna:
    --------
    X : np.ndarray
        Secuencia flotante caotica de longitud length (usada para permutacion).
    S : np.ndarray (dtype=np.uint8)
        Secuencia de bytes pseudoaleatorios S_i = floor(|x_i| * 10^(14)) mod 256.
    """
    def iterate(val: float) -> float:
        val = float(map_instance.evaluate(val))
        if val in (0.0, 0.5, 1.0) or abs(val - round(val)) < 1e-14:
            val += 1e-7
        return val

    x = float(x0)

    # 1. Fase de transitorio para eliminar el sesgo de la condicion inicial
    for _ in range(n_transient):
        x = iterate(x)

    # 2. Generacion de la secuencia caotica
    X = np.empty(length, dtype=np.float64)
    for i in range(length):
        x = iterate(x)
        X[i] = x

    # 3. Discretizacion a 8 bits: S_i = floor(|x_i| * 10^(14)) mod 256
    S = (np.floor(np.abs(X) * 1e14).astype(np.int64) % 256).astype(np.uint8)

    return X, S


def encrypt_image(
    image_2d: np.ndarray,
    x0: float = 0.38472910542381,
    p: float = 2.0,
    iv: int = 105,
) -> np.ndarray:
    """
    Cifra una imagen 2D en escala de grises mediante el algoritmo 1D de Amin et al. (2010).

    Fases:
    1. Permutacion (Confusion): Reordena los pixeles segun los indices de argsort(X).
    2. Difusion XOR encadenada: C_i = P'_i ^ S_i ^ C_(i-1), con C_(-1) = iv.
    """
    if image_2d.ndim != 2:
        raise ValueError("La imagen de entrada debe ser una matriz 2D en escala de grises.")

    M, N = image_2d.shape
    P = np.ascontiguousarray(image_2d, dtype=np.uint8).ravel()
    L = len(P)

    # 1. Generacion de keystream caotico con el Mapa de Tienda
    tent = TentMap(p=p)
    X, S = generate_keystream(tent, x0=x0, length=L, n_transient=500)

    # 2. Permutacion (Confusion espacial)
    P_perm = P[np.argsort(X)]

    # 3. Difusion XOR Encadenada (Amin et al., 2010)
    C = np.empty(L, dtype=np.uint8)
    prev = np.uint8(iv)
    for i in range(L):
        prev = np.uint8(int(P_perm[i]) ^ int(S[i]) ^ int(prev))
        C[i] = prev

    return C.reshape((M, N))


def decrypt_image(
    cipher_2d: np.ndarray,
    x0: float = 0.38472910542381,
    p: float = 2.0,
    iv: int = 105,
) -> np.ndarray:
    """
    Descifra una imagen 2D generada por encrypt_image.
    Invierte exactamente las etapas de difusion y permutacion,
    asegurando una recuperacion exacta sin perdidas (Fidelidad: MSE = 0.0).
    """
    if cipher_2d.ndim != 2:
        raise ValueError("La imagen cifrada debe ser una matriz 2D en escala de grises.")

    M, N = cipher_2d.shape
    C = np.ascontiguousarray(cipher_2d, dtype=np.uint8).ravel()
    L = len(C)

    # 1. Regenerar keystream con la misma clave secreta
    tent = TentMap(p=p)
    X, S = generate_keystream(tent, x0=x0, length=L, n_transient=500)
    perm_indices = np.argsort(X)

    # 2. Inversion vectorizada de difusion XOR encadenada
    prev_C = np.empty(L, dtype=np.uint8)
    prev_C[0] = np.uint8(iv)
    prev_C[1:] = C[:-1]
    P_perm = C ^ S ^ prev_C

    # 3. Inversion de permutacion
    P_orig = np.empty(L, dtype=np.uint8)
    P_orig[perm_indices] = P_perm

    return P_orig.reshape((M, N))


def calculate_metrics(
    cipher1: np.ndarray,
    cipher2: np.ndarray,
) -> Dict[str, float]:
    """
    Calcula las metricas de Sensibilidad a la Clave entre dos imagenes cifradas
    segun el marco teorico de Wu, Noonan y Agaian (2011) y Zhang y Liu (2023):
    - NPCR: porcentaje de pixeles distintos entre cipher1 y cipher2.
    - UACI: diferencia media normalizada de intensidad entre cipher1 y cipher2.
    """
    c1 = cipher1.astype(np.float64)
    c2 = cipher2.astype(np.float64)
    total_pixels = float(c1.size)

    npcr = (np.sum(c1 != c2) / total_pixels) * 100.0
    uaci = (np.sum(np.abs(c1 - c2)) / (255.0 * total_pixels)) * 100.0

    return {
        "npcr": float(npcr),
        "uaci": float(uaci),
    }


def encrypt_and_save_pipeline(
    input_image_path: str,
    output_dir: str = "outputs",
    base_name: Optional[str] = None,
    x0: float = 0.38472910542381,
    p: float = 2.0,
    iv: int = 105,
    delta_key: float = 1e-14,
) -> Dict[str, Union[float, str]]:
    """
    Pipeline completo de procesamiento criptografico:
    1. Carga y valida la imagen de entrada (cualquier resolucion y formato compatible).
    2. Ejecuta el cifrado caotico nominal con clave x0 (Amin et al., 2010).
    3. Descifra la imagen con clave x0 y valida MSE = 0.0 (Fidelidad de Descifrado).
    4. Cifra la misma imagen con clave perturbada (x0 + delta_key).
    5. Calcula metricas NPCR y UACI de sensibilidad a la clave (Wu et al., 2011).
    6. Genera la matriz de diferencia absoluta de cifrados |C1 - C2|.
    7. Guarda todas las imagenes resultantes en la carpeta especificada con nombres limpios.

    Retorna:
    --------
    dict
        Diccionario con metricas calculadas y rutas absolutas de los archivos guardados.
    """
    os.makedirs(output_dir, exist_ok=True)

    if base_name is None:
        file_name = os.path.basename(input_image_path)
        base_name = os.path.splitext(file_name)[0]

    # 1. Cargar imagen original
    img_orig = load_image(input_image_path)

    # 2. Cifrado nominal
    img_cipher = encrypt_image(img_orig, x0=x0, p=p, iv=iv)

    # 3. Descifrado con clave exacta
    img_decrypted = decrypt_image(img_cipher, x0=x0, p=p, iv=iv)
    mse_val = float(np.mean((img_orig.astype(float) - img_decrypted.astype(float)) ** 2))

    # 4. Cifrado con clave infinitesimalmente perturbada
    img_cipher_pert = encrypt_image(img_orig, x0=x0 + delta_key, p=p, iv=iv)

    # 5. Metricas de sensibilidad
    metrics = calculate_metrics(img_cipher, img_cipher_pert)

    # 6. Imagen de diferencia de sensibilidad
    img_diff = np.abs(img_cipher.astype(int) - img_cipher_pert.astype(int)).astype(np.uint8)

    # 7. Descifrado fallido con clave incorrecta
    img_dec_fail = decrypt_image(img_cipher, x0=x0 + delta_key, p=p, iv=iv)
    fail_rate = float(np.mean(img_orig != img_dec_fail) * 100.0)

    # Guardar en disco
    path_orig = os.path.join(output_dir, f"{base_name}_original.png")
    path_cipher = os.path.join(output_dir, f"{base_name}_cifrada.png")
    path_decrypted = os.path.join(output_dir, f"{base_name}_descifrada.png")
    path_cipher_pert = os.path.join(output_dir, f"{base_name}_cifrada_perturbada.png")
    path_diff = os.path.join(output_dir, f"{base_name}_diferencia_sensibilidad.png")
    path_dec_fail = os.path.join(output_dir, f"{base_name}_descifrada_fallida.png")

    save_image(img_orig, path_orig)
    save_image(img_cipher, path_cipher)
    save_image(img_decrypted, path_decrypted)
    save_image(img_cipher_pert, path_cipher_pert)
    save_image(img_diff, path_diff)
    save_image(img_dec_fail, path_dec_fail)

    return {
        "base_name": base_name,
        "image_shape": f"{img_orig.shape[0]}x{img_orig.shape[1]}",
        "mse": mse_val,
        "npcr": metrics["npcr"],
        "uaci": metrics["uaci"],
        "fail_rate": fail_rate,
        "path_original": os.path.abspath(path_orig),
        "path_cipher": os.path.abspath(path_cipher),
        "path_decrypted": os.path.abspath(path_decrypted),
        "path_cipher_pert": os.path.abspath(path_cipher_pert),
        "path_diff": os.path.abspath(path_diff),
        "path_dec_fail": os.path.abspath(path_dec_fail),
    }
