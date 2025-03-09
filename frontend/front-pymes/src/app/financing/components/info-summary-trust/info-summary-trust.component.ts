import { Component } from '@angular/core';
import { MatTabsModule } from '@angular/material/tabs';
import { ActiveFinancingComponent } from "../active-financing/active-financing.component";
import { activeFinancingI } from '../../interfaces/active-financing';
import { HistoryFinancingComponent } from "../history-financing/history-financing.component";
import { historyFinancingI } from '../../interfaces/history-financing';
import { AvailableFinancingComponent } from '../available-financing/available-financing.component';
import { availableFinancingI } from '../../interfaces/available-financing';

@Component({
  selector: 'app-info-summary-trust',
  imports: [
    AvailableFinancingComponent,
    MatTabsModule,
    ActiveFinancingComponent,
    HistoryFinancingComponent
],
  templateUrl: './info-summary-trust.component.html',
  styleUrl: './info-summary-trust.component.css'
})
export class InfoSummaryTrustComponent {
  //Variables
  arrayAvailableFinancing: availableFinancingI[] = [
    {
      typeFinancing: "Inyección de Capital",
      shortDescription: "Crédito para Capital de Trabajo",
      maxAmount: 10000,
      interestRate: "12% anual",
      termsInMonth: "12-36",
      requeriments: "Nivel Plata",
      available: true,
      recommended: true
    },
    {
      typeFinancing: "Crédito equipamiento",
      shortDescription: "Crédito para equipamiento de la empresa",
      maxAmount: 50000,
      interestRate: "8% anual",
      termsInMonth: "36-60",
      requeriments: "Nivel Platinium",
      available: true,
      recommended: false
    },
    {
      typeFinancing: "Banco empresarial",
      shortDescription: "Línea de Crédito Revolvente",
      maxAmount: 125000,
      interestRate: "5% anual",
      termsInMonth: "48-72",
      requeriments: "Nivel Golden",
      available: false,
      recommended: false
    },
  ];

  arrayActivesFinancing: activeFinancingI[] = [
    {
      typeFinancing: "Inyección de Capital",
      shortDescription: "Crédito para Capital de Trabajo",
      originalAamount: 10000,
      amountPaid: 2000,
      nextPayment: "09/03/2025",
      status: "Al corriente",
      progress: 15,
    },
    {
      typeFinancing: "Crédito equipamiento",
      shortDescription: "Crédito para equipamiento de la empresa",
      originalAamount: 45000,
      amountPaid: 38000,
      nextPayment: "09/03/2025",
      status: "Al corriente",
      progress: 83,
    }
  ];

  arrayHistoryFinancing: historyFinancingI[] = [
    {
      typeFinancing: "Inyección de Capital",
      shortDescription: "Crédito para Capital de Trabajo",
      originalAamount: 10000,
      termInMonths: 12,
      closingDate: "09/03/2025",
      status: "Pagado"
    },
    {
      typeFinancing: "Crédito equipamiento",
      shortDescription: "Crédito para equipamiento de la empresa",
      originalAamount: 45000,
      termInMonths: 48,
      closingDate: "09/03/2025",
      status: "Pagado"
    }
  ];
}
