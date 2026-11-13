"""Datos del alumno que el simulador espera recibir de la web de pagos virtuales.

En producción (web de pagos de TD2) estos datos vienen de la sesión del alumno ya autenticado:
la escala desde Panda y los cursos desde la matrícula. Aquí solo hay alumnos de ejemplo
para la demostración; no son datos reales.
"""
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Curso:
    codigo: str
    nombre: str
    creditos: float
    es_taller: bool = False   # True = taller / extra académico


@dataclass
class Alumno:
    nombre: str
    escala: str                              # viene del sistema; el alumno no la elige
    cursos: Optional[list] = field(default=None)  # None = aún no tiene matrícula en el periodo

    @property
    def tiene_matricula(self) -> bool:
        return bool(self.cursos)

    @property
    def creditos_cursos(self) -> float:
        return sum(c.creditos for c in self.cursos or [] if not c.es_taller)

    @property
    def creditos_talleres(self) -> float:
        return sum(c.creditos for c in self.cursos or [] if c.es_taller)


# --- Alumnos de ejemplo para la demo (ficticios) ---
ALUMNOS_DEMO = {
    "Alumno con matrícula registrada": Alumno(
        nombre="Alumno de prueba A",
        escala="2",
        cursos=[
            Curso("1AE01", "Microeconomía I", 4),
            Curso("1AE02", "Estadística I", 4),
            Curso("1AE03", "Contabilidad Financiera", 4),
            Curso("1AE04", "Matemáticas II", 4),
            Curso("1AE05", "Redacción Académica", 4),
            Curso("1TA01", "Taller de Oratoria (Grupo A)", 1, es_taller=True),
        ],
    ),
    "Alumno sin matrícula (periodo futuro)": Alumno(nombre="Alumno de prueba B", escala="3", cursos=None),
}
