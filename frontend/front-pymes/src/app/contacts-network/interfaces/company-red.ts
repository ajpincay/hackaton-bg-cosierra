//Interfaz para mostrar la información de una PYME en la red de contactos P
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

//Interfaz para mostrar la información de una PYME en la red de contactos 
export interface companyInfoI{
    ruc: string;
    pyme_name: string;
    sector: string;
    location: string;
    peer_review: number;
    connected: boolean;
    pending: boolean;
}