# Automatizaciones QA - Despensalo

Suite de pruebas automatizadas con Selenium y pytest para el sitio [despensalo.cl](https://despensalo.cl/).

---

## Requisitos previos

- Python 3.10 o superior
- Google Chrome instalado
- ChromeDriver compatible con la version de Chrome instalada (puede gestionarse automaticamente con Selenium 4.6+)

---

## Instalacion del entorno

1. Clonar el repositorio:

```bash
git clone https://github.com/KevinEscobr/automatizacion.git
cd automatizacion
```

2. Crear y activar el entorno virtual:

```bash
# Windows
python -m venv venv
venv\Scripts\activate
```

3. Instalar las dependencias:

```bash
pip install -r requeriments.txt
```

---

## Variables de entorno requeridas

Las pruebas leen las credenciales desde variables de entorno. Deben definirse antes de ejecutar cualquier test.

```powershell
# PowerShell
$env:QA_EMAIL    = "tucorreo@ejemplo.com"
$env:QA_PASSWORD = "tucontrasena"
```

> La variable `QA_EMAIL` se usa como base para generar correos unicos en cada ejecucion de registro.
> El ultimo correo registrado se guarda automaticamente en `qa_last_email.txt` y es reutilizado por los tests de login.

---

## Descripcion de los tests

| Archivo | Funcion de test | Descripcion |
|---|---|---|
| `test_register.py` | `test_registro_usuario` | Registra un nuevo usuario con un correo unico generado automaticamente. |
| `test_datosEnBruto.py` | `test_registro_usuario` | Igual que el anterior pero con DevTools abierto para inspeccionar trafico de red. |
| `test_agregarInventario.py` | `test_login_y_agregar_inventario` | Inicia sesion y agrega un producto al inventario (incluye caso con cantidad negativa para validar errores). |
| `test_agregarMedicina.py` | `test_login_y_agregar_medicina` | Inicia sesion y agrega un medicamento (incluye caso con cantidad negativa para validar errores). |

---

## Ejecucion de los tests

### Ejecutar todos los tests

```bash
pytest
```

### Ejecutar un archivo especifico

```bash
pytest test_register.py
pytest test_datosEnBruto.py
pytest test_agregarInventario.py
pytest test_agregarMedicina.py
```

### Ejecutar con salida detallada

```bash
pytest -v
```

### Ejecutar con print habilitado (ver logs en consola)

```bash
pytest -s
```

### Combinar verbose y prints

```bash
pytest -v -s
```

---

## Orden recomendado de ejecucion

Algunos tests dependen del correo guardado por el test de registro. Se recomienda seguir este orden:

1. `test_register.py` - crea la cuenta y guarda el correo en `qa_last_email.txt`
2. `test_agregarInventario.py` - usa el correo guardado para iniciar sesion
3. `test_agregarMedicina.py` - usa el correo guardado para iniciar sesion
4. `test_datosEnBruto.py` - variante del registro con inspeccion de red

---

## Estructura del proyecto

```
automatizacion/
├── venv/                      # Entorno virtual (no se sube al repositorio)
├── test_register.py           # Test de registro de usuario
├── test_datosEnBruto.py       # Test de registro con DevTools habilitado
├── test_agregarInventario.py  # Test de agregar producto al inventario
├── test_agregarMedicina.py    # Test de agregar medicamento
├── qa_last_email.txt          # Ultimo correo registrado (generado automaticamente)
├── requeriments.txt           # Dependencias del proyecto
└── .gitignore
```

---

## Dependencias

```
selenium>=4.20
pytest>=8.0
```

---

## Autores

- **Johan Urrutia**
- **Kevin Escobar**
