"""
Repository layer para la API de Monster Hunter Weapons.

Este módulo contiene la implementación del patrón Repository que separa
la lógica de acceso a datos de la lógica de negocio, proporcionando:

- Abstracción del acceso a la base de datos
- Facilidad para testing con mocks
- Reutilización de queries complejas
- Separación clara de responsabilidades

Repositories disponibles:
- WeaponCategoryRepository: Acceso a datos de categorías
- WeaponRepository: Acceso a datos de armas
"""
