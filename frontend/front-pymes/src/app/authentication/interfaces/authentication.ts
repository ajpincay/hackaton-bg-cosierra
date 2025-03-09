//Interfaz de respuesta de la API para el login de usuario
export interface ApiResponseLoginUserI{
    ruc: string;
    pyme_name: string;
    trust_score: number,
    tier: string,
    token: string
}