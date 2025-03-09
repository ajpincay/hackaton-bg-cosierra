//Interfaz para mostrar los tipos de financiamientos que ya han sido pagados (HISTORIAL)
export interface historyFinancingI {
    typeFinancing: string;
    shortDescription: string;
    originalAamount: number; //Monto original
    termInMonths: number; //Plazo en meses
    closingDate: string;
    status: string;
}
