//Interfaz para mostrar la información de una PYME en la red de contactos
export interface companyRedI{
    name: string;
    type: string;
    location: string;
    rate: number;
    conected: boolean;
    pending: boolean;
    details:{
        phone: string;
        email: string;
        web: string;
    }
}