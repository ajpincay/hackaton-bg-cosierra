from app.models.pymes import TierEnum


AVAILABLE_CERTIFICATIONS = [
    ("Certificación de procesos", "IEEE", [TierEnum.PLATA, TierEnum.ORO, TierEnum.PLATINO]),
    ("Certificación de idoneidad", "Empresa X", [TierEnum.PLATA, TierEnum.ORO]),
    ("Certificación SERCOP", "SERCOP", [TierEnum.ORO, TierEnum.PLATINO]),
    ("Certificación ambiental", "Entidad Y", [TierEnum.PLATA, TierEnum.ORO]),
    ("Auditoría", "Entidad Z", [TierEnum.ORO, TierEnum.PLATINO]),
    ("Certificación de tecnología", "Tech Org", [TierEnum.PLATINO]),
    ("Reconocimiento de calidad", "Calidad S.A.", [TierEnum.PLATA, TierEnum.ORO, TierEnum.PLATINO]),
    ("Certificación de seguridad", "Seguridad S.A.", [TierEnum.ORO, TierEnum.PLATINO]),
    ("Certificación de calidad", "Calidad S.A.", [TierEnum.PLATA, TierEnum.ORO]),
]
