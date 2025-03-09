//Interfaz de respuesta de la API para cuando se obtiene la información del Dashboard
export interface ApiResponseDashboardI{
    trust_score: number;
    tier: string;
    recent_activity: string[];
    certifications_completed: number;
    certifications_pending: number;
    financial_summary: {
        summary: string;
        recommendation: string;
    }
}