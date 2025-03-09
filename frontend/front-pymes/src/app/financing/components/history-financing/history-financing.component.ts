import { Component, Input } from '@angular/core';
import { historyFinancingI } from '../../interfaces/history-financing';

@Component({
  selector: 'app-history-financing',
  imports: [],
  templateUrl: './history-financing.component.html',
  styleUrl: './history-financing.component.css'
})
export class HistoryFinancingComponent {
    //Variables
    @Input() arrayHistoryFinancing: historyFinancingI[] = []
}
