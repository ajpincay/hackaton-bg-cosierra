//Interfaz para mostrar los tipos de financiamientos que ofrece el banco a la PYME
export interface availableFinancingI {
    typeFinancing: string;
    shortDescription: string;
    maxAmount: number;
    interestRate: string;
    termsInMonth: string;
    requeriments: string;
    available: boolean;
    recommended: boolean;
}
