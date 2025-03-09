//Interfaz para mostrar los tipos de financiamientos que están en curso o ACTIVOS
export interface activeFinancingI {
    typeFinancing: string;
    shortDescription: string;
    originalAamount: number; //Monto original
    amountPaid: number; //Monto abonado
    nextPayment: string;
    status: string;
    progress: number;
}
