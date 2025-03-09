from app.core.constants import AVAILABLE_CERTIFICATIONS
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.core.db import get_db
from app.models.pymes import PymeCertifications, PymeTrust, TierEnum
from app.schemas.pymes import CertificationData, CertificationsResponse, CertificationCreate


router = APIRouter()


# Register a certification
@router.post("/register/{ruc}")
def register_certification(ruc: str, cert_data: CertificationCreate, db: Session = Depends(get_db)):
    try:
        new_cert = PymeCertifications(
            ruc=ruc,
            certificate_name=cert_data.name,
            issuer=cert_data.issuer,
            issue_date=cert_data.issue_date,
            expiration_date=cert_data.expiration_date,
        )
        db.add(new_cert)
        db.commit()
        db.refresh(new_cert)
        return {"message": "Certification registered successfully", "id": new_cert.id}
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error registering certification")

# Get certifications for a given RUC
@router.get("/{ruc}", response_model=CertificationsResponse)
def get_certifications(ruc: str, db: Session = Depends(get_db)):
    certifications = db.query(PymeCertifications).filter(PymeCertifications.ruc == ruc).all()
    pyme_trust = db.query(PymeTrust).filter(PymeTrust.ruc == ruc).first()
    
    if not certifications:
        raise HTTPException(status_code=404, detail="No certifications found for this RUC")
    
    cert_data = [
        CertificationData(name=cert.certificate_name, status="Completed") for cert in certifications
    ]
    return {
        "certifications": cert_data,
        "tier": pyme_trust.tier.value if pyme_trust else TierEnum.NA.value
    }

# Compare obtained vs. pending certifications
@router.get("/{ruc}/status")
def get_certification_status(ruc: str, db: Session = Depends(get_db)):
    obtained_certs = db.query(PymeCertifications.certificate_name).filter(PymeCertifications.ruc == ruc).all()
    obtained_cert_names = {cert[0] for cert in obtained_certs}
    
    pyme_trust = db.query(PymeTrust).filter(PymeTrust.ruc == ruc).first()
    pyme_tier = pyme_trust.tier if pyme_trust else TierEnum.NA
    
    possible_certs = [cert[0] for cert in AVAILABLE_CERTIFICATIONS if pyme_tier in cert[2]]
    total_available = len(possible_certs)
    obtained_count = len(obtained_cert_names.intersection(possible_certs))
    pending_count = total_available - obtained_count
    
    completion_percentage = (obtained_count / total_available * 100) if total_available > 0 else 0
    
    return {
        "certificates_obtained": obtained_count,
        "certificates_pending": pending_count,
        "completion_percentage": round(completion_percentage, 2),
        "eligible_certifications": possible_certs,
        "current_tier": pyme_tier.value
    }
